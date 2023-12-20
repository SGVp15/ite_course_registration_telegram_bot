from jinja2 import Environment, FileSystemLoader


class MyJinja:
    def __init__(self, template_file):
        self.environment = Environment(auto_reload=True, loader=FileSystemLoader('./Config/template_email'))
        self.template_file = self.environment.get_template('course_registration.html')

    def create_document(self, template_file, user):
        self.template_file = self.environment.get_template(template_file)
        return self.chillde_present.render(user)
