from pathlib import Path

from Contact import parser
from Excel.converter import read_xls, read_xlsx
from Webinar.registration import start_registration


EXCEL_DIR = Path("path/to/excel")


def parser_and_registration():
    users = []

    for path in EXCEL_DIR.iterdir():
        if not path.is_file():
            continue

        try:
            if path.suffix.lower() == ".xls":
                s = read_xls(path)
            elif path.suffix.lower() == ".xlsx":
                s = read_xlsx(path)
            else:
                continue

            # Если файл успешно прочитан
            u = parser.get_list_users_from_string(s)

            if u:
                users.extend(u)

            # Удаляем только после успешного чтения
            path.unlink()
            print(f"Файл обработан и удалён: {path}")

        except Exception as e:
            print(f"Ошибка при обработке {path}: {e}")
            # Файл НЕ удаляем, чтобы можно было обработать его позже

    text = start_registration(users)
    return text
