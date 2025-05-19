from telebot import TeleBot, types
import random

bot = TeleBot("8056628335:AAE5E_Z1pGr1gzLydyDiC1s-nIYH6c6jRck")
saldos = {}
giftcards = {
"GIFT123456": 10, "GIFT654321": 10, "GIFT987654": 10, "GIFT000001": 10, "GIFT000002": 10, "GIFT000003": 10, "GIFT000004": 10, "GIFT000005": 10, "GIFT000006": 10, "GIFT000007": 10, "GIFT000008": 10, "GIFT000009": 10, "GIFT000010": 10, "GIFT000011": 10, "GIFT000012": 10, "GIFT000013": 10, "GIFT000014": 10, "GIFT000015": 10, "GIFT000016": 10, "GIFT000017": 10,
"GIFT050001": 50, "GIFT050002": 50, "GIFT050003": 50, "GIFT050004": 50, "GIFT050005": 50, "GIFT050006": 50, "GIFT050007": 50, "GIFT050008": 50, "GIFT050009": 50, "GIFT050010": 50, "GIFT050011": 50, "GIFT050012": 50, "GIFT050013": 50, "GIFT050014": 50, "GIFT050015": 50, "GIFT050016": 50, "GIFT050017": 50, "GIFT050018": 50, "GIFT050019": 50, "GIFT050020": 50,
"GIFT100A": 100, "GIFT100B": 100, "GIFT100C": 100, "GIFT100D": 100, "GIFT100E": 100, "GIFT100F": 100, "GIFT100G": 100, "GIFT100H": 100, "GIFT100I": 100, "GIFT100J": 100,
"GIFT2K1": 2000, "GIFT2K2": 2000, "GIFT2K3": 2000, "GIFT2K4": 2000, "GIFT2K5": 2000
}
cards_bin_498440 = ["4984400135658155|07|2028|315", "4984400136154410|07|2028|299", "4984400176477010|07|2028|232"]
cards_bin_456331 = ["4563318508347348|07|2028|260", "4563311483248433|07|2028|742", "4563315122842738|07|2028|703"]
admin_id = 6194292650

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in saldos:
        saldos[user_id] = 0
    bot.reply_to(message, "👋 Bem-vindo! Use /menu para ver opções ou /resgata para usar um gift card.")

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💳 Comprar"), types.KeyboardButton("➕ Adicionar saldo"), types.KeyboardButton("💰 Ver saldo"))
    bot.send_message(message.chat.id, "Escolha uma opção:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💳 Comprar")
def comprar(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("BIN 498440", callback_data="bin_498440"), types.InlineKeyboardButton("BIN 456331", callback_data="bin_456331"))
    bot.send_message(message.chat.id, "Escolha a BIN que deseja comprar:\nValor: R$5\n💸 *Pix:* b8ff1dea-563f-4414-ba32-ddd7da5750c7\nEnvie o comprovante aqui após o pagamento.", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def escolha_bin(call):
    user_id = call.from_user.id
    bin_id = call.data.split("_")[1]
    if user_id not in saldos or saldos[user_id] < 5:
        bot.send_message(call.message.chat.id, "❌ Você não tem saldo suficiente. Adicione saldo ou envie o comprovante do Pix.")
        return
    saldos[user_id] -= 5
    if bin_id == "498440":
        card = random.choice(cards_bin_498440)
    elif bin_id == "456331":
        card = random.choice(cards_bin_456331)
    else:
        card = "Erro ao buscar card."
    bot.send_message(call.message.chat.id, f"✅ GG! Live e testado agora mesmo:\n{card}", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "➕ Adicionar saldo")
def adicionar_saldo(message):
    bot.send_message(message.chat.id, "Para adicionar saldo, envie o valor para o Pix:\n*Chave Pix:* b8ff1dea-563f-4414-ba32-ddd7da5750c7\n\nDepois envie o comprovante aqui.", parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def receber_comprovante(message):
    user_id = message.from_user.id
    saldos[user_id] = saldos.get(user_id, 0) + 5
    bot.send_message(message.chat.id, "✅ Comprovante recebido! R$5 de saldo adicionado.")

@bot.message_handler(commands=['resgata'])
def resgatar(message):
    bot.send_message(message.chat.id, "Digite o código do gift card para resgatar:")

@bot.message_handler(func=lambda m: m.text in giftcards)
def aplicar_gift(m):
    user_id = m.from_user.id
    valor = giftcards.pop(m.text)
    saldos[user_id] = saldos.get(user_id, 0) + valor
    bot.reply_to(m, f"🎁 Gift de R${valor} resgatado com sucesso!\n💰 Saldo atual: R${saldos[user_id]}")

@bot.message_handler(commands=['versaldo'])
@bot.message_handler(func=lambda m: m.text == "💰 Ver saldo")
def ver_saldo(message):
    user_id = message.from_user.id
    saldo = saldos.get(user_id, 0)
    bot.reply_to(message, f"💰 Seu saldo atual é: R${saldo}")

@bot.message_handler(commands=['usuarios'])
def ver_usuarios(message):
    if message.from_user.id == admin_id:
        total = len(saldos)
        bot.reply_to(message, f"👥 Total de usuários únicos: {total}")
    else:
        bot.reply_to(message, "❌ Você não tem permissão para usar esse comando.")

bot.polling()
