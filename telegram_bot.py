# telegram_bot.py

import telepot
import json
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from rss_parser import parse_planetpy_rss  # Ensure this function is defined in rss_parser.py

TOKEN = '<Your_Bot_Token>'
TelegramBot = telepot.Bot(TOKEN)

def _display_help():
    return render_to_string('help.md')

def _display_planetpy_feed():
    return render_to_string('feed.md', {'items': parse_planetpy_rss()})

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != TOKEN:
            return HttpResponseForbidden('Invalid token')
        commands = {
            '/start': _display_help,
            'help': _display_help,
            'feed': _display_planetpy_feed,
        }
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command
            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
