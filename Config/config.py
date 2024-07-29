# -----------------------------------------------------------------------------------------------------------------------
QUEUE = './data/queue.txt'
LOG_FILE = './data/.log.txt'
LOG_BACKUP = './data/.history.txt'
COURSES_FILE = './data/.courses.txt'
COURSES_FILE_BACKUP = './data/.courses_backup.txt'
SELLERS = './data/.seller.txt'
LOG_PROGRAM = './logs.txt'
WEBINAR_LOG = './data/webinar_registration.txt'

IMPORT_FILE = './data/input.txt'
OLD_USERS = './data/users.txt'

# -----------------------------------------------------------------------------------------------------------------------
# https://events.webinar.ru/ITExpert/569285096/1bd05f2176c42f9208556acf5e594f32
# https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL

PATTERN_URL = r'https://\S+'
PATTERN_WEBINAR_EVENT_ID = r'https://(my.mts-link.ru|events.webinar.ru)/\w+/(\d+)'
PATTERN_ZOOM_URL = r"\s*(https://.*zoom.us/\S+)"

# -----------------------------------------------------------------------------------------------------------------------

FILE_XPATH_BTN_ZOOM_REGISTRATION = './Config/xpath_btn_registration_zoom.txt'
WEBINAR_HISTORY = './data/.webinar_history.txt'
