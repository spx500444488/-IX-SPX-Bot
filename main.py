
import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
app = Flask(__name__)

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 تحليل SPX500", callback_data="analyze"),
         InlineKeyboardButton("📈 الإشارات", callback_data="signals")],
        [InlineKeyboardButton("🎯 المستويات", callback_data="levels"),
         InlineKeyboardButton("🌐 اتجاه السوق", callback_data="market")],
        [InlineKeyboardButton("📜 سجل الإشارات", callback_data="history"),
         InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🟡 <b>IX SPX</b>\n"
        "<i>AI • SMART ANALYSIS</i>\n\n"
        "مرحبًا بك في بوت IX SPX لتحليل SPX500.\n\n"
        "اختر الخدمة من القائمة أدناه 👇\n\n"
        "⚠️ التحليل تعليمي وليس ضمانًا للربح."
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=main_menu())

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "📊 <b>تحليل SPX500</b>\n\n"
        "🟡 محرك التحليل قيد التجهيز.\n"
        "في النسخة القادمة سنربطه ببيانات السوق الحية ونضيف CALL / PUT / NO TRADE.",
        parse_mode="HTML", reply_markup=main_menu()
    )

async def simple_section(update: Update, title: str, body: str):
    await update.effective_message.reply_text(
        f"{title}\n\n{body}", parse_mode="HTML", reply_markup=main_menu()
    )

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(update, "📈 <b>الإشارات</b>",
                         "لا توجد إشارة حية حتى الآن. سيتم تفعيلها بعد ربط بيانات السوق.")

async def levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(update, "🎯 <b>المستويات</b>",
                         "سيتم عرض الدعم والمقاومة والدخول والأهداف ووقف الخسارة بعد تفعيل محرك السوق.")

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(update, "🌐 <b>اتجاه السوق</b>",
                         "سيتم تحديد الاتجاه من بيانات SPX500 الحية بعد الربط بمصدر بيانات موثوق.")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(update, "📜 <b>سجل الإشارات</b>",
                         "السجل فارغ حاليًا. ستظهر هنا نتائج الإشارات بعد تشغيل المحرك.")

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(update, "⚙️ <b>الإعدادات</b>",
                         "الإعدادات المتاحة لاحقًا: الفريم، مستوى المخاطرة، والتنبيهات.")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    handlers = {
        "analyze": analyze, "signals": signals, "levels": levels,
        "market": market, "history": history, "settings": settings
    }
    await handlers[query.data](update, context)

telegram_app = Application.builder().token(BOT_TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("analyze", analyze))
telegram_app.add_handler(CommandHandler("signals", signals))
telegram_app.add_handler(CommandHandler("levels", levels))
telegram_app.add_handler(CommandHandler("market", market))
telegram_app.add_handler(CommandHandler("history", history))
telegram_app.add_handler(CommandHandler("settings", settings))
telegram_app.add_handler(CallbackQueryHandler(button))

@app.get("/")
def health():
    return "IX SPX is online", 200

@app.post("/telegram")
def telegram_webhook():
    update = Update.de_json(
        request.get_json(force=True),
        telegram_app.bot
    )

    async def handle():
        await telegram_app.initialize()
        await telegram_app.process_update(update)
        await telegram_app.shutdown()

    asyncio.run(handle())

    return "ok", 200
