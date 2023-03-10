import os
import requests_api
from dotenv import load_dotenv, find_dotenv
from telegram.ext import *


# Carrega as variáveis de ambiente
load_dotenv(find_dotenv())

# Pega o token do bot
TOKEN = os.getenv("TOKEN")

print('Bot iniciado!')

# Comando /start
def start_command(update, context):
    update.message.reply_text('Olá, quer ver a loja atual do fortnite? Digite /loja \n Para ver os outros comandos disponíveis digite /ajuda')

# Comando /ajuda
def help_command(update, context):
    
    commands = """
    Comandos disponíveis:
    /loja - Mostra a loja atual do Fortnite
    /diaria - Mostra apenas os itens na seção Diária
    /destaque - Mostra apenas os itens na seção Destaque
    /lojatxt - Mostra a loja atual do Fortnite em formato de texto
    /diariatxt - Mostra apenas  os itens na seção Diária em texto
    /destaquetxt - Mostra apenas os itens na seção Destaque em texto
    /ajuda - Mostra os comandos disponíveis
    """
    
    update.message.reply_text(commands)

# Comando /lojatxt
def shop_txt_command(update, context):

    # Pega a loja atual do fortnite,
    # se o conteúdo da loja for maior que 4096 caracteres, ele divide a mensagem em partes de 4096 caracteres
    message = requests_api.get_shop_txt()

    msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for text in msgs:
        update.message.reply_text(text=text)

def shop_txt_daily_command(update, context):
    message = requests_api.get_shop_daily_text()

    msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for text in msgs:
        update.message.reply_text(text=text)

def shop_txt_featured_command(update, context):
    message = requests_api.get_shop_featured_text()

    msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for text in msgs:
        update.message.reply_text(text=text)

# Comando /loja
def shop_command(update, context):
    
    message = requests_api.get_shop()
    
    print('gerando imagem...')

    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(message, 'rb'), timeout = 1000)

def shop_daily_command(update, context):

    message = requests_api.get_shop_daily()
    
    print('gerando imagem...')

    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(message, 'rb'), timeout = 1000)

def shop_featured_command(update, context):

    message = requests_api.get_shop_featured()
    
    print('gerando imagem...')

    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(message, 'rb'), timeout = 1000)

# Função que trata a mensagem do usuário, caso não seja um comando.
def handle_response(text: str) -> str:
    return 'Não entendi o que você disse, digite /ajuda para ver os comandos disponíveis!'

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = ''

    response = handle_response(text)

    update.message.reply_text(response)

# Função que trata os erros
def error(update, context):
    print(f"Update {update} causou um o erro {context.error}")

# Função principal
def main():
    # Cria o updater e o dispatcher, recebe o TOKEN do bot.
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Adiciona os comandos e suas respectivas funções
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("loja", shop_command))
    dp.add_handler(CommandHandler("diaria", shop_daily_command))
    dp.add_handler(CommandHandler("destaque", shop_featured_command))
    dp.add_handler(CommandHandler("lojatxt", shop_txt_command))
    dp.add_handler(CommandHandler("diariatxt", shop_txt_daily_command))
    dp.add_handler(CommandHandler("destaquetxt", shop_txt_featured_command))
    dp.add_handler(CommandHandler("ajuda", help_command))

    # Adiciona a função que trata as mensagens do usuário, caso não seja um comando.
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Adiciona a função que trata os erros
    dp.add_error_handler(error)

    # Inicia o bot, o bot possui 10 segundos de delay entre os comandos
    updater.start_polling(10)

    # Mantém o bot rodando
    updater.idle()

# Inicia o bot
main()
