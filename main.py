import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write (self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template,**kw))

class BlogPosts(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Index(Handler):

    def get(self):
        recentPosts = db.GqlQuery("SELECT * from BlogPosts ORDER BY created DESC")

        self.render("recent.html", posts=recentPosts)

    # def render_front(self, title="", content="", error=""):
    #     posts = db.GqlQuery("SELECT * from BlogPosts ORDER BY created DESC")
    #
    #     self.render("front.html", title=title, content=content, error=error, posts=posts)
    #
    # def get(self):
    #     self.render_front()
    #
    # def post(self):
    #     title = self.request.get("title")
    #     content = self.request.get("content")
    #
    #     if title and content:
    #         a = BlogPosts(title=title, content=content)
    #         a.put()
    #
    #         self.redirect("/")
    #
    #     else:
    #         error = "try again"
    #         self.render_front(title,content,error)

class Blog(Handler):

    def get(self):
        recentPosts = db.GqlQuery("SELECT * from BlogPosts ORDER BY created DESC LIMIT 5")

        self.render("recent.html", posts=recentPosts)

class NewPost(Handler):
    def render_front(self, title="", content="", titleerror="",contenterror="", error=""):
        posts = db.GqlQuery("SELECT * from BlogPosts ORDER BY created DESC")

        self.render("front.html", title=title, content=content, titleerror=titleerror, contenterror=contenterror, posts=posts, error=error)

    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        titleerror = ""
        contenterror = ""

        if title and content:
            a = BlogPosts(title=title, content=content)
            a.put()

            akey = str(a.key().id())

            self.redirect("/blog/" + akey)

        if not title:
            titleerror = "Please enter a title."

        if not content:
            contenterror = "Please enter content."

        self.render("front.html",contenterror=contenterror,titleerror=titleerror)


class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        post = BlogPosts.get_by_id(int(id))

        if not post:
            self.response.write(id)

        t = jinja_env.get_template("post.html")
        post = t.render(post=post)

        self.response.write(post)

def get_posts(limit, offset):
    recentPosts = db.GqlQuery("SELECT * from BlogPosts ORDER BY created DESC LIMIT" + limit + "OFFSET" + offset)

    def post(limit,offset):
        self.render("recent.html", posts=recentPosts)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/blog', Blog),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),

], debug=True)
