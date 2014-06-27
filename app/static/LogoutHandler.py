__author__ = 'vimal'

from static.WikiHandler import WikiHandler


class LogoutHandler(WikiHandler):

    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_name=; Path=/')
        self.redirect('/')
