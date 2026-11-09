import telebot

# Token Bot Telegram Kamu
TOKEN = "9085870788:AAHbBkbbTKlJ_XeFkkEcoBvh3O8GQLR00J4"
bot = telebot.TeleBot(TOKEN)

# ⚠️ GANTI ANGKA DI BAWAH INI DENGAN USER ID TELEGRAM ASLI KAMU (CEK VIA @userinfobot)
ADMIN_CHAT_ID = 123456789  

# 1. PESAN SAAT MEMBER MENGETIK /START
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type != 'private':
        return
        
    nama_user = message.from_user.first_name
    welcome_text = (
        "📩 **LAYANAN PENGADUAN / HELP DESK** 📩\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Halo, **{nama_user}**! ✨\n"
        "Silakan kirimkan pesan, pertanyaan, kritik, atau laporan kendala kamu di sini.\n\n"
        "👉 Pesan kamu akan otomatis diteruskan ke Admin, dan balasan dari Admin akan langsung muncul di chat ini."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# 2. JIKA ADMIN MEMBALAS (REPLY) LAPORAN DI TELEGRAM
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID and message.reply_to_message is not None)
def reply_to_user(message):
    try:
        if message.reply_to_message.forward_from:
            target_user_id = message.reply_to_message.forward_from.id
            
            # Mengirim balasan Admin ke member
            if message.text:
                bot.send_message(target_user_id, f"💬 **BALASAN DARI ADMIN:**\n\n{message.text}", parse_mode="Markdown")
            elif message.photo:
                bot.send_photo(target_user_id, message.photo[-1].file_id, caption=f"💬 **BALASAN DARI ADMIN:**\n\n{message.caption or ''}")
            
            bot.reply_to(message, "✅ Balasan berhasil terkirim ke member!")
        else:
            bot.reply_to(message, "⚠️ Gagal membalas: Privasi akun member tersebut menyembunyikan informasi forward.")
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi kesalahan: {e}")

# 3. MENGIRIM PESAN/PENGADUAN DARI MEMBER KE ADMIN
@bot.message_handler(func=lambda message: message.chat.type == 'private' and message.chat.id != ADMIN_CHAT_ID)
def forward_pengaduan(message):
    if message.text and message.text.startswith('/'):
        return  # Abaikan perintah bot
        
    nama_user = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Tanpa Username"
    
    # Notifikasi untuk Admin
    bot.send_message(
        ADMIN_CHAT_ID,
        f"📩 **PENGADUAN BARU MASUK!**\n"
        f"👤 Pengirim: **{nama_user}** ({username})\n"
        f"🆔 ID: `{message.from_user.id}`\n"
        f"👇 *(Reply/Balas pesan di bawah ini untuk membalas member)*:",
        parse_mode="Markdown"
    )
    
    # Meneruskan pesan asli member ke Admin
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    
    # Konfirmasi ke member
    bot.reply_to(message, "✅ **Pesan kamu telah dikirim ke Admin.**\nMohon tunggu sebentar ya, Admin akan segera membalasnya di sini!")

# Membersihkan webhook agar tidak error 409 Conflict
try:
    bot.remove_webhook()
    print("Webhook lama berhasil dibersihkan...")
except Exception as e:
    print(f"Info webhook: {e}")

print("Bot Pengaduan murni siap & berjalan...")
bot.infinity_polling(none_stop=True, interval=0, timeout=20)
