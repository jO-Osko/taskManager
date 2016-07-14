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


class PosamezenTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("posamezen_task.html", params=params)


class UrediTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("uredi_task.html", params=params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))

        task.naslov = self.request.get("input-naslov")
        task.besedilo = self.request.get("input-besedilo")
        task.pomembnost = int(self.request.get("input-pomembnost"))
        task.dokoncano = int(self.request.get("input-dokoncano"))/100.0

        task.put()
        return self.redirect_to("seznam")


class IzbrisiTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("izbrisi_task.html", params=params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))
        task.key.delete()
        return self.redirect_to("seznam")

app = webapp2.WSGIApplication([
    webapp2.Route("/", IndexHandler, name="index"),
    webapp2.Route("/dodaj", DodajTaskHandler),
    webapp2.Route("/seznam", SeznamTaskovHandler, name="seznam"),
    webapp2.Route("/task/<task_id:\\d+>", PosamezenTaskHandler),
    webapp2.Route("/task/<task_id:\\d+>/uredi", UrediTaskHandler),
    webapp2.Route("/task/<task_id:\\d+>/izbrisi", IzbrisiTaskHandler),
], debug=True)
