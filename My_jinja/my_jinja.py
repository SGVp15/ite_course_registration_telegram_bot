from jinja2 import Environment, FileSystemLoader


class MyJinja:
    def __init__(self, template_folder='./Email/template_email', template_file='course_registration.html'):
        self.environment = Environment(auto_reload=True, loader=FileSystemLoader(template_folder))
        self.template_file = self.environment.get_template(template_file)

    def create_document(self, user):
        return self.template_file.render(user=user)
