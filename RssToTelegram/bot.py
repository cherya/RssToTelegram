import telepot
import urllib3
import telepot.api
import time


class Bot:

    def __init__(self, config):
        token = config['Telegram']['token']
        self.channel = config['Telegram']['channel']
        self.disable_web_page_preview = config.getboolean('Telegram', 'disable_web_page_preview')
        self.content_length = config.getint('Telegram', 'max_content_length')
        self.bold_title = config.getboolean('Telegram', 'bold_title')


        self.bot = telepot.Bot(token)

    def prettify_title(self, title):
        title = list(title)
        title[0] = title[0].upper()
        title = "".join(title)
        if self.bold_title:
            return '<b>{0}</b>'.format(title)
        else:
            return title

    def send_message(self, title, content, url):
        title = self.prettify_title(title)
        if self.content_length:
            content = content[:self.content_length] + '...' if len(content) > self.content_length else content
        post = '{0}\n{1}\n{2}'.format(title, content, url)
        self.bot.sendMessage(self.channel, text=post, parse_mode='HTML',
                             disable_web_page_preview=self.disable_web_page_preview)
