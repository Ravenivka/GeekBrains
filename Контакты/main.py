from sqlite3 import *
from easygui import *
from tkinter import *



window = Tk()
#Декларация
myfiletypes = ["*.db", "*.db3", "*.sqlite", "*.sqlite3", "*.*"] 
path = ''
db = None

#Подключение базы данных
def Connect(dbpath):
    conn = Connection(dbpath)
    cur = conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS "Контакты" (
	            "title"	text NOT NULL,
	            "phones"	text,
	            "mail"	text,
	            "birthday"	text,
	            "addons"	text,
	            PRIMARY KEY("title")
                );
                ''')
    return conn

#Обработчики для меню
def OpenDB():
    global db
    global path
    path = fileopenbox(None, 'Выбор файла', '*.db', myfiletypes)
    db = Connect(path)
   
   
    
 
def NewDB():
    global path
    global db
    path = filesavebox(None, 'Сохранить как ...', 'Контакты.db', myfiletypes)
    db = Connect(path)

def NewRec():
    pass

def SearchRec():
    pass

window.title("Телефонный справочник")
window.geometry('800x600')  

#card viewer
lbl_path = Label(text = '')
lbl_path.pack_forget()


#меню
menu = Menu(window)  
new_item = Menu(menu)  
new_item.add_command(label='Новый', command=NewDB)  
new_item.add_command(label='Открыть', command=OpenDB)
menu.add_cascade(label='Файл', menu=new_item) 
sec_item =Menu(menu)
sec_item.add_command(label='Новая', command=NewRec)  
sec_item.add_command(label='Найти', command=SearchRec)
menu.add_cascade(label='Запись', menu=sec_item) 
window.config(menu=menu)
window.mainloop()



