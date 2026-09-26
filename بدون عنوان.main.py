import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import google.generativeai as genai
from robobot import Bot

# --- سرور ساده برای بیدار موندن Render ---
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

# --- بخش ربات ---
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

# --- اجرای همزمان سرور و ربات ---
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run()
