import re


class User:
    def __init__(self, last_name: str, first_name: str, email: str, url_registration: str = '', course: str = '',
                 webinar_events_id: str | None = '', curator_email: str | None = '', webinar_name: str | None = '',
                 link: str | None = '', date: str | None = '', teacher: str | None = '',
                 manager_email: str | None = '', abs_course=''):
        """

        :type webinar_events_id: String from https://events.Webinar.ru/event/999146969
        """
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.url_registration = url_registration
        self.course = course
        self.date = date
        self.abs_course = abs_course

        try:
            self.date_start = re.findall(r'\d{2}\.\d{2}\.\d{4}', date)[0]
            self.date_stop = re.findall(r'\d{2}\.\d{2}\.\d{4}', date)[-1]
        except IndexError:
            self.date_start = ''
            self.date_stop = ''

        self.role = 'GUEST'
        self.webinar_events_id = webinar_events_id
        self.curator_email = curator_email
        self.manager_email = manager_email
        self.link = link
        self.teacher = teacher
        self.webinar_name = webinar_name

    def __str__(self):
        return (
            f'Курс:{self.abs_course}'
            f'\nТренер:{self.teacher}'
            f'\nДаты проведения курса:{self.date}'
            f'\n{self.last_name} {self.first_name} {self.email}'
            f'\n{self.url_registration}')

    def __eq__(self, other):
        if self.last_name == other.last_name and self.first_name == other.first_name and self.email == other.email:
            if self.webinar_events_id != '':
                if self.webinar_events_id == other.webinar_events_id:
                    return True
            elif self.url_registration == other.url_registration:
                return True
        return False
