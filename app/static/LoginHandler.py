__author__ = 'vimal'

from static.WikiHandler import WikiHandler
from static.User import User


def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))


class LoginHandler(WikiHandler):

    def get(self):
        self.render("login.html")

    def post(self):

        user_valid = self.request.get("username")
        pass_valid = self.request.get("password")
        valid_login = User.all().filter("username =", user_valid).get()
        error = ""
        if valid_login and user_valid == valid_login.username and pass_valid == valid_login.password:
            self.set_secure_cookie("user_name", str(user_valid))
            self.redirect("/")
        else:
            error = "That's not a valid Login"
        self.render("login.html", error=error, valid_login=valid_login)

