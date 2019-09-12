from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
import werkzeug.exceptions
from bot_handler import *
import time
from database import *
import subprocess


def main_index(request):
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return Response("{'Response': 200}")


routes = Map([
    # Rule('/', endpoint='main/index'),
    # Rule('/{0}'.format(config.TELEGRAM_API), endpoint='main/index'),
    # Rule('/{0}/'.format(config.TELEGRAM_API), endpoint='main/index'),
    # Rule('/api', endpoint='main/index')
    #Rule('/api/schedule/<string:command_cd>', endpoint='api/schedule')
])
controllers = {
    '/': main_index,
    'main/index': main_index,
}


# Class веб-приложения бота для webhook
class FaBot:
    """

    """

    def __init__(self):
        # some magic setting class config
        return

    # needed in order with WSGI (PEP3333)
    def __call__(self, environ, start_response):
        return FaBot.dispatcher(environ, start_response)

    @staticmethod
    def dispatcher(environ, start_response):
        request = Request(environ)
        urls = routes.bind_to_environ(environ)
        try:
            try:
                response = urls.dispatch(lambda endpoint, v: controllers[endpoint](request, **v))
            except Exception as e:
                if isinstance(e, werkzeug.exceptions.NotFound):
                    response = Response(response='404 Error',
                                        status='404')
                else:
                    response = Response(response='500 Error',
                                        status='500')

        except Exception as e:
            response = Response(str(e))
        return response(environ, start_response)


def set_webhook():
        subprocess.call('{0}'.format(config.CURLWEBHOOK), shell=True)


if config.WEBHOOKSET:
    bot.remove_webhook()
    time.sleep(1)
    set_webhook()
    time.sleep(1)
else:
    bot.polling(none_stop=True, timeout=2)



# Блок для запуска встроенного веб-сервера. Для Apache не нужен
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = FaBot()
    run_simple(config.HOST_NAME, config.HOST_PORT, app, use_debugger=config.USE_DEBUG, use_reloader=config.USE_RELOAD,
               ssl_context=(config.HOST_SSL_CRT_PATH, config.HOST_SSL_KEY_PATH))
