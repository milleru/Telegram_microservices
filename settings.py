import os
import json

DATA_FILE = 'login_data.session'
DATA_DIR = '/Telegram_message_sender/'
logo = '''\033[2J\033[H\033[1;34m
              ┏┳┓  ┓  ┓    
               ┃ ┏┓┃┏┓┣┓┏┓╋
               ┻ ┗ ┗┗ ┗┛┗┛┗
            =================\033[m'''
path = ''
if os.name == 'nt':
    if not os.path.exists(os.path.join(os.environ['USERPROFILE'], 'Documents') + DATA_DIR):
        print(f'\033[1;91mDiretório {DATA_DIR} não encontrado\033[m')
        os.mkdir(os.path.join(os.environ['USERPROFILE'], 'Documents') + DATA_DIR)
        print(f'\033[1;92mDiretório {DATA_DIR} criado\033[m')
        path = os.path.join(os.environ['USERPROFILE'], 'Documents')
    else:
        path = os.path.join(os.environ['USERPROFILE'], 'Documents') + DATA_DIR
else:
    if not os.path.exists(os.path.join(os.environ['HOME'], 'Documents') + DATA_DIR):
        print(f'\033[1;91mDiretório {DATA_DIR} não encontrado\033[m')
        os.mkdir(os.path.join(os.environ['HOME'], 'Documents') + DATA_DIR)
        print(f'\033[1;92mDiretório {DATA_DIR} criado\033[m')
        path = os.path.join(os.environ['HOME'], 'Documents') + DATA_DIR
    else:
        path = os.path.join(os.environ['HOME'], 'Documents') + DATA_DIR


data_session = os.path.join(path,DATA_FILE)
login_save = os.path.join(path,'autenticator.json')

msgs_path = os.path.join(path,'msgs.csv')
users_path = os.path.join(path,'users.csv')
log_path = os.path.join(path, 'log.csv')

if not os.path.exists(msgs_path):
    with open(msgs_path,'x') as file:
        print(f'\033[1;92mArquivo \033[1;97m{msgs_path}\033[1;92m criado.\033[m')
if not os.path.exists(users_path):
    with open(users_path,'x') as file:
        print(f'\033[1;92mArquivo \033[1;97m{users_path}\033[1;92m criado.\033[m')
if not os.path.exists(log_path):
    with open(log_path,'x') as file:
        print(f'\033[1;92mArquivo \033[1;97m{log_path}\033[1;92m criado.\033[m')
