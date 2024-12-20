import os

os.chdir('D:\\Новая папка')

del_text = 'deti-online.com_-_'

for f in os.listdir():
    new_name = f.replace(del_text, '')
    os.rename(f, new_name)
