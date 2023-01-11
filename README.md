# Instruções para configurar ambiente de desenvolvimento

### Requisitos básicos

#### Dependências

- Python 3.9 ou superior (As versões anteriores não foram testadas)

- dotenv

- python-telegram-bot 13.13 (Qualquer versão antes da 20.0 funciona)

#### Configuração

1. Abra o Telegram e procure por @BotFather.

2. Clique em Start.

3. Digite /newbot e escolha um nome para o bot, além de um nome de usuário.

4. Copie o token gerado pelo BotFather e coloque em um arquivo **.env**, atribua o token há uma variável de nome *TOKEN*. Coloque o .env no .gitignore para impedir o upload para o git.

5. Instale a biblioteca *python-telegram-bot* com o comando: \
```pip install python-telegram-bot==13.13```

6. Execute o arquivo *main.py* com o comando: \
```python main.py```

7. Entre na conversa com o bot que você criou no Telegram e digite /Start. Em seguida, use os comandos disponíveis em /ajuda para utilizar suas funcionalidades.


### Contribuição

Forks e pull requests são bem-vindos. Para mudanças importantes, abra uma issue para discutir o que você gostaria de mudar!

### Exemplo

<img src='imgs/loja.jpg' style='width:500px; display:block; margin-left:auto; margin-right: auto;'/>