import os

DATA_DIR = os.path.join(os.getcwd(), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------------------------------------------------------------------------------------------------

QUEUE = os.path.join(DATA_DIR, 'queue.pk')
LOG_FILE = os.path.join(DATA_DIR, '.log.txt')
LOG_BACKUP = os.path.join(DATA_DIR, '.history.txt')
COURSES_FILE = os.path.join(DATA_DIR, '.courses.txt')
COURSES_FILE_BACKUP = os.path.join(DATA_DIR, '.courses_backup.txt')
SELLERS = os.path.join(DATA_DIR, '.seller.txt')
LOG_PROGRAM = os.path.join(DATA_DIR, 'logs.txt')
WEBINAR_LOG = os.path.join(DATA_DIR, 'webinar_registration.txt')

OLD_USERS = os.path.join(DATA_DIR, 'users.pk')

# -----------------------------------------------------------------------------------------------------------------------
# https://events.webinar.ru/ITExpert/569285096/1bd05f2176c42f9208556acf5e594f32
# https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL

PATTERN_URL = r'https://\S+'
PATTERN_WEBINAR_EVENT_ID = r'https://(my.mts-link.ru|events.webinar.ru)/\w+/(\d+)'
PATTERN_ZOOM_URL = r"\s*(https://.*zoom.us/\S+)"

# -----------------------------------------------------------------------------------------------------------------------

FILE_XPATH_BTN_ZOOM_REGISTRATION = './Config/xpath_btn_registration_zoom.txt'
WEBINAR_HISTORY = os.path.join(DATA_DIR, '.webinar_history.txt')

SYSTEM_LOG = os.path.join(DATA_DIR, 'system_log.txt')
