__author__ = 'vimal'

import webapp2


from google.appengine.ext import db
from static.WikiHandler import WikiHandler
from static.SignupHandler import SignupHandler
from static.LoginHandler import LoginHandler
from static.User import User
from static.LogoutHandler import LogoutHandler


def valid_user(content):
        user = User.all().filter('content=', content)
        return user


class WikiContent(db.Model):
    subject = db.StringProperty(required=False)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'title': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt)}
        return d


class EditHandler(WikiHandler):
    print "hello"

    def get(self, path):
        print path
        if path == '':
            path = None
        valid_login = self.read_secure_cookie("user_name")
        if not valid_login:
            self.redirect('/login')

        v = self.request.get('v')
        page = None
        if v:
            print v
            if v.isdigit():
                page = WikiContent.all().filter('subject =', path).order('-created').fetch(100)
                for i in page:
                    print i.content
                self.render("edit.html", page=page[int(v)-1])

        else:
            page = WikiContent.all().filter('subject =', path).order('-created').get()

            self.render("edit.html", path=path, page=page)

    def post(self, path):
        if not valid_user:
            self.error(404)
            return
        if path == "":
            path = None
        content = self.request.get('content')

        if content:
            p = WikiContent(subject=path, content=content)
            p.put()

        content_old = WikiContent.all().filter('subject=', path).get()
        print "i am here"
        print content_old
        if not path:
            path = ''

        self.redirect('/'+path)


class MainPage(WikiHandler):
    def get(self):
        post = WikiContent.all().filter('subject =', None).order('-created').get()
        print post

        valid_login = self.read_secure_cookie("user_name")
        print valid_login
        if self.format == 'html':
            self.render('Front.html', contents=post, valid_login=valid_login)
        else:
            return self.render_json([p.as_dict() for p in post])


class WikiPage(WikiHandler):
    def get(self, path):
        v = self.request.get('v')
        page = None
        if v:
            if v.isdigit():
                page = WikiContent.all().filter('subject =', path).order('-created').fetch(100)
                print page
                page = page[int(v)-1]

            if not page:
                return
        else:
            page = WikiContent.all().filter('subject =', path).order('-created').get()
            print "view"
            print page

        if page:
            valid_login = self.read_secure_cookie("user_name")
            self.render("pagere.html", contents=page, path=path, valid_login=valid_login)
        else:
            self.redirect("/_edit/" + path)


class HistoryPage(WikiHandler):
    def get(self, path):
        v = self.request.get('v')
        page = None
        if v:
            if v.isdigit():
                x = WikiContent.all().filter('subject =', path).order('-created').fetch(100)
                self.render("history.html", path=path, page=x[int(v)-1])
            if not page:
                return
        print path
        if path == '':
            path = None
        q = WikiContent.all().filter('subject =', path).order('-created').fetch(limit=100)
        posts = list(q)
        if posts:
            valid_login = self.read_secure_cookie("user_name")
            if not path:
                path = ''
            self.render("history.html", posts=posts, path=path, valid_login=valid_login)
        else:
            self.redirect('/_edit')

PAGE_RE = r'/?((?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/?', MainPage), ('/signup', SignupHandler),
                               ('/login', LoginHandler), ('/_edit' + PAGE_RE, EditHandler),
                               ('/logout', LogoutHandler), ('/_history' + PAGE_RE, HistoryPage),
                               ('/'+PAGE_RE, WikiPage)], debug=True)
