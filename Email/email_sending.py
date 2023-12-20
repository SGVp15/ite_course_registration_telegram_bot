class EmailSending:
    def __init__(self, subject='', from_email='', to='', bcc='', text=''):
        self.subject = subject
        self.from_email = from_email
        self.to = to
        self.bcc = bcc
        self.text = text

    def send_email(self):
        pass
