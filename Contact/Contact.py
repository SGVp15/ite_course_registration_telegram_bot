import re


class User:
    def __init__(self, last_name: str, first_name: str, email: str, url_registration: str = '', course: str = '',
                 webinar_eventsid: str = '', curator_email='', webinar_name='', link='', date='', teacher='',
                 manager_email=''):
        """

        :type webinar_eventsid: String from https://events.webinar.ru/event/999146969
        """
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.url_registration = url_registration
        self.course = course
        self.date = date
        self.role = 'GUEST'
        self.webinar_eventsid = webinar_eventsid
        self.curator_email = curator_email
        self.manager_email = manager_email
        self.link = link
        self.teacher = teacher
        self.webinar_name = webinar_name

    def __str__(self):
        return f'{self.last_name}\t{self.first_name}\t{self.email}\t{self.url_registration}\t{self.course}'

    def __eq__(self, other):
        if self.last_name == other.last_name and self.first_name == other.first_name and self.email == other.email:
            if self.webinar_eventsid != '':
                if self.webinar_eventsid == other.webinar_eventsid:
                    return True
            elif self.url_registration == other.url_registration:
                return True
        return False
