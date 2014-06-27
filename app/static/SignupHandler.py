__author__ = 'vimal'
import cgi
import re


from static.WikiHandler import WikiHandler
from static.User import User
from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def escape_html(s):
    return cgi.escape(s, quote=True)


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email) or not email


class SignupHandler(WikiHandler):
    def render_front(self, username="", password="", verify="", email="",
                     username_error="", password_error="", verify_error="", email_error=""):
        self.render("signup.html", username=username, password=password, verify=verify, email=email,
                    username_error=username_error, password_error=password_error,
                    verify_error=verify_error, email_error=email_error)

    def get(self):
        self.render("signup.html")

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        user_name = escape_html(user_username)
        user_pass = escape_html(user_password)
        pass_verify = escape_html(user_verify)
        email_id = escape_html(user_email)

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        error = False
        temp = User.all().filter('username =', user_username).get()

        if not valid_username(user_username) or temp is not None:
            print 'kjbjlj'
            username_error = "That's not a valid Username!"
            error = True

        if not valid_password(user_password):
            password_error = "That's not a valid password!"
            error = True

        if not user_verify or not user_password == user_verify:
            verify_error = "Passwords do not match"
            error = True

        if not valid_email(user_email):
            email_error = "That's not a valid email!"
            error = True

        if error:
            self.render("signup.html", username=user_name, email=email_id, username_error=username_error,
                        password_error=password_error, verify_error=verify_error, email_error=email_error)

        else:
            if not user_email or valid_email(user_email):
                b = User(username=user_username, password=user_password, email=user_email)
                b.put()
                self.set_secure_cookie("user_name", str(user_name))
                self.redirect("/")



