import telepot
import urllib3
import telepot.api


class Bot:

    def __init__(self, config):
        token = config['Bot']['token']
        self.chanel = config['Bot']['chanel']
        self.disable_web_page_preview = config.getboolean('Bot', 'disable_web_page_preview')
        self.content_length = config.getint('Bot', 'max_content_length')

        if 'Proxy' in config:
            server = config['Proxy']['server']
            port = config['Proxy']['port']
            user = config['Proxy']['login']
            password = config['Proxy']['password']

            headers = urllib3.make_headers(proxy_basic_auth='{0}:{1}'.format(user, password))
            proxy_url = '{0}:{1}'.format(server, port)
            telepot.api._pools = {
                'default': urllib3.ProxyManager(proxy_url=proxy_url, proxy_headers=headers, num_pools=3, maxsize=10,
                                                retries=False, timeout=30),
            }
            telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1,
                                                                         retries=False, timeout=30))

        self.bot = telepot.Bot(token)

    @staticmethod
    def prettify_title(title):
        title = list(title)
        title[0] = title[0].upper()
        title = "".join(title)
        return '<b>{0}</b>'.format(title)

    def send_message(self, title, content, url):
        title = self.prettify_title(title)
        content = content[:self.content_length] + '...' if len(content) > self.content_length else content
        post = '{0}\n{1}\n{2}'.format(title, content, url)
        print(post)
        self.bot.sendMessage(self.chanel, text=post, parse_mode='HTML',
                             disable_web_page_preview=self.disable_web_page_preview)
