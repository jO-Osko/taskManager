import os

import jinja2
import webapp2

from models import Task

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class IndexHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class DodajTaskHandler(BaseHandler):
    def get(self):
        return self.render_template("dodaj.html")

    def post(self):
        naslov = self.request.get("input-naslov")
        besedilo = self.request.get("input-besedilo")
        pomembnost = int(self.request.get("input-pomembnost"))

        task = Task(naslov=naslov, besedilo=besedilo, pomembnost=pomembnost)

        task.put()
        return self.redirect_to("index")


class SeznamTaskovHandler(BaseHandler):
    def get(self):
        params = {"tasks": Task.query().fetch()}
        return self.render_template("seznam.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route("/", IndexHandler, name="index"),
    webapp2.Route("/dodaj", DodajTaskHandler),
    webapp2.Route("/seznam", SeznamTaskovHandler),
], debug=True)
