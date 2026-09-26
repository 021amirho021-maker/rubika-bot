import google.generativeai as genai
from robobot import Bot

genai.configure(api_key="API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot("BOT_TOKEN_HERE")

@bot.on_message()
async def chat_handler(bot, event):
    user_message = event.text 
    if not user_message:
        return
    try:
        response = model.generate_content(user_message)
        await event.reply(response.text)
    except Exception as e:
        await event.reply("الان نتونستم جواب بدم، بعداً پیام بده.")

bot.run()