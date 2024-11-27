import os.path
from datetime import datetime
from typing import TextIO

from telethon import *
from telethon.errors import SessionPasswordNeededError, CodeInvalidError,UserInvalidError,UsernameInvalidError
import random
from settings import *


client = None

async def connect_to_telegram(_api_id, _api_hash, _phone, _code=None, _passwd=None):
    client = TelegramClient(data_session, _api_id, _api_hash)
    await client.connect()

    # Validação da sessão
    if not await client.is_user_authorized():
        await client.send_code_request(_phone)

        if _code:
            try:
                await client.sign_in(_phone, _code)
                if await client.is_user_authorized():
                    print("\033[1;92mConectado com sucesso!\033[m")
            except SessionPasswordNeededError:
                if _passwd:
                    try:
                        await client.sign_in(phone=_phone, code=_code, password=_passwd)
                    except:
                        print('\033[1;91mErro ao conectar\033[m')
                raise ValueError("\033[1;91mSenha 2FA necessária, mas não fornecida.\033[m")
            except Exception as e:
                print(f"\033[1;91mErro ao autenticar: {e}\033[m")
                await client.disconnect()
                raise ValueError("\033[1;91mCódigo de verificação inválido.\033[m")
    else:
        print("\033[1;92mSessão válida reutilizada!\033[m")

        print("\033[1;92mConectado com sucesso!\033[m")
    return client

async def conectar(_api_id,_api_hash,_phone):
    global client
    if os.path.exists(login_save):
        with open(login_save) as log:
            file = json.load(log)
        _api_id, _api_hash, _phone = file['api_id'],file['api_hash'],file['phone']

    try:
        client = await connect_to_telegram(_api_id, _api_hash, _phone)
        await client.disconnect()
    except Exception as e:
        print(f"ERRO: {str(e)}")

async def send_message():
    pass

def save_login(_api_id: int,_api_hash: str,_phone_number: str):
    with open(login_save, "w") as file:
        json.dump({"api_id": _api_id,
                   "api_hash": _api_hash,
                   "phone": _phone_number}, file)

def clear_saved_login():
    if os.path.exists(data_session):
        os.remove(data_session)
    if os.path.exists(login_save):
        os.remove(login_save)

async def check_saved_login():
    if os.path.exists(data_session):
        if os.path.exists(login_save):
            with open(login_save,'r') as dados:
                file = json.load(dados)
                client = TelegramClient(data_session,file['api_id'],file['api_hash'])
            await client.connect()
            if await client.is_user_authorized():
                await client.disconnect()
                return True
            await client.disconnect()
        else:
            return False
    else:
        return False

def get_users():
    users = []
    with open(users_path, 'r', newline='') as file_user:
        for linha in file_user:
            if '\n' in linha:
                users.append(linha.replace('\n', ''))
            else:
                users.append(linha)
        return users

def get_messages():
    msgs = []
    with open(msgs_path, 'r', newline='') as file:
        for msg in file:
            if '\n' in msg:
                msgs.append(msg.replace('\n', ''))
            else:
                msgs.append(msg)
        return msgs

def save_messages(messages: str):
    message = messages.strip().capitalize()
    with open(msgs_path,'a',newline='') as file:
        file.write(message + '\n')
    while True:
        try:
            opc = str(input('Adicionar uma mensagem? [N/S]'))
        except Exception as e:
            print(f'\033[1;91mERRO! {str(e)}\033[m')
        else:
            if opc in 'Ss':
                return True
            if opc in 'Nn':
                return False

def check_duplicate(new_users: str):
    verificado = []
    users = get_users()
    news_users = ['@' + user.strip() for user in new_users.split('@') if user != '']
    for user in news_users:
        if user not in users:
            if user not in verificado:
                verificado.append(user)
    return verificado

def save_users_already_sent(users: list):
    with open(users_path,'a',newline='') as file:
        for user in users:
            file.write(user + '\n')

def save_log(log: str):
    with open(log_path, 'a', newline='') as file:
        file.write(log + '\n')

async def main():
    global client

    if await check_saved_login():
        print('\033[1;92mlogin salvo encontrado\033[m')
        with open(login_save) as log:
            file = json.load(log)
        api_id = file['api_id']
        api_hash = file['api_hash']
        phone = file['phone']
    else:
        api_id = int(input('\033[1;97mAPI_ID: \033[m'))
        api_hash = input('\033[1;97mAPI_HASH: \033[m')
        phone = input('\033[1;97mCelular(+5535999999999): \033[m')

    while True: # Cliente é conectado aqui
        try:
            client = await connect_to_telegram(api_id, api_hash, phone)
            if await client.is_user_authorized():
                break
            else:
                try:
                    codigo = int(input('\033[1;93mCodigo de verificação: \033[m'))
                except Exception as e:
                    print(f'ERRO ao logar: {str(e)}')
                    continue
                else:
                    try:
                        client = await connect_to_telegram(api_id, api_hash, phone, codigo)
                    except Exception as e:
                        print(f'\033[1;91mERRO: {str(e)}\033[m')
                        continue
                    else:
                        break
        except Exception as e:
            print(f'ERRO ao logar: {str(e)}')

    while True:
        print(logo)
        print('''\033[1;97m
            Message Sender
            1 - Enviar várias mensagens
            2 - Salvar lista de mensagens
            3 - Salvar login
            4 - Excluir login salvo
            0 - SAIR
            \033[m''')
        try:
            opc = int(input('\033[1;97m\
            Sua opção: \033[m'))
        except Exception as e:
            print(f'\033[1;91mERRO: {str(e)}\033[m')
        else:
            match opc:
                case 1:
                    users = str(input('Digite ou cole sua lista de usuários: '))
                    users = check_duplicate(users)

                    for user in users:
                        try:
                            # await client.send_message(user,random.choice(get_messages()))
                            entity = await client.get_entity(user)
                            log = f'Mensagem enviada para {user} em {datetime.now().date()} as {datetime.now().time()}'
                            save_log(log)
                            print(f'\033[1.92mMensagem enviada para {entity.username}.\033[m')
                        except UsernameInvalidError:
                            print(f'\033[1;91mUsuário {user} não é válido.\033[m')
                        except Exception as e:
                            print(f'\033[1;91mERRO: {str(e)}\033[m')
                    save_users_already_sent(users)
                case 2:
                    while True:
                        msg = str(input('\033[1mSua mensagem: \033[m'))
                        if not save_messages(msg):
                            break
                case 3:
                    save_login(api_id, api_hash, phone)
                case 4:
                    await client.disconnect()
                    clear_saved_login()
                    print('\033[1;93mLogin salvo apagado. Desconectando...\033[m')
                    break
                case 0:
                    await client.disconnect() # Cliente é desconectado, toda ação deve ser feita antes desse ponto
                    if not os.path.exists(login_save):
                        clear_saved_login()
                    break
                case _:
                    print('\033[1;91mOpção inválida\033[m')


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

