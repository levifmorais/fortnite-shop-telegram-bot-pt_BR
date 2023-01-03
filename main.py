import os
import requests
from dotenv import load_dotenv, find_dotenv
from telegram.ext import *

# Carrega as variáveis de ambiente
load_dotenv(find_dotenv())

# Pega o token do bot
TOKEN = os.getenv("TOKEN")

print('Bot iniciado!')

# Função que pega a loja atual do fortnite, é esperado retornar uma string
def get_shop() -> str:
    
    response = requests.get(url='https://fortnite-api.com/v2/shop/br/combined', params={'language': 'pt-BR'})

    received_data = response.json()
    
    text = ''

    for entry in received_data['data']['daily']['entries']:
        for item in entry['items']:
            
            name = item['name']
            price = entry['finalPrice']
            item_type = item['type']['value']

            match item_type:
                case 'outfit':
                    item_type = 'Skin'
                case 'backpack':
                    item_type = 'Mochila'
                case 'pickaxe':
                    item_type = 'Picareta'
                case 'emote':
                    item_type = 'Emote'
                case 'glider':
                    item_type = 'Asa-delta'
                case 'wrap':
                    item_type = 'Envelopamento'

            text += f"\n{name} - {price} Vbucks - {item_type}\n"
    
    return text


# Comando /start
def start_command(update, context):
    update.message.reply_text('Olá, quer ver a loja atual do fortnite? Digite /loja \n Para ver os outros comandos disponíveis digite /ajuda')

# Comando /ajuda
def help_command(update, context):
    
    commands = """
    Comandos disponíveis:\n 
    /loja - Mostra a loja atual do fortnite\n
    /ajuda - Mostra os comandos disponíveis\n
    """
    
    update.message.reply_text(commands)

# Comando /loja
def shop_command(update, context):

    update.message.reply_text(get_shop)


#def custom_command(update, context):
#    update.message.reply_text('placeholder')

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
    dp.add_handler(CommandHandler("ajuda", help_command))
    dp.add_handler(CommandHandler("loja", shop_command))

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
