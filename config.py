# *** НАСТРОЙКИ TELEGRAM ***
TELEGRAM_API = ''
ADMIN_USER_ID = ''

# *** НАСТРОЙКИ FA.RU ***
LOGIN = ''
PASS = ''

# *** КОНСТАНТЫ БОТА ***
# Дата с которой будет выгружено расписание
START_DT = '01/01/2019'
# Дата по которое будет выгружено расписание
END_DT = '31/01/2020'
EMODJI = {
    'pencil': u'\U0000270F',
    'greenbook': u'\U0001F4D7',
    'redbook': u'\U0001F4D5',
    'open_book': u'\U0001F4D6',
    'clock': u'\U000023F0',
    'pin': u'\U0001F4CC',
    'like': u'\U0001F44D',
    'alien': u'\U0001F47D'
}

# *** НАСТРОЙКИ ДОСТУПА К БАЗЕ ***
DB_HOST = ''
DB_USER = ''
DB_PASS = ''
DB_NAME = ''

# *** НАСТРОЙКИ ВЕБ-СЕРВЕРА ***
USE_DEBUG = False
USE_RELOAD = True

# *** НАСТРОЙКИ ВЕБ-СЕРВЕРА ***
HOST_NAME = '0.0.0.0'
HOST_ADDR = ''
HOST_PORT = 443

# *** СЕРТИФИКАТ ДЛЯ WEBHOOK ***
HOST_SSL_KEY_PATH = r'/tgbot.key'
HOST_SSL_CRT_PATH = r'/tgbot.pem'

# Использовать ли Webhook для общения с telegram API
WEBHOOKSET = False
# Workaround для самоподписанного сертификата
CURLWEBHOOK = 'curl -F "url=https://{0}:{1}/" -F "certificate=@{2}" "https://api.telegram.org/bot{3}/setwebhook"'.format(
    HOST_ADDR, HOST_PORT, HOST_SSL_CRT_PATH, TELEGRAM_API)