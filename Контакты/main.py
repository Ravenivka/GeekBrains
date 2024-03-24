from sqlite3 import *
from easygui import *
from tkinter import *

db = None

def NewDB():
    myfiletypes = ["*.db", "*.db3", "*.sqlite", "*.sqlite3", "*.*"]
    filename = filesavebox(msg=None, title='Сохранить как....', default='Контакты.db', filetypes=myfiletypes)
    if filename != None:
        conn = connect(filename)
        return conn
    else:
        return None

       


def clicked():
    lbl.configure(text="Я же просил...")


window = Tk()
window.title("Телефонный справочник")
window.geometry('800x600')  
#тестовая метка
lbl = Label(window, text="Привет")
lbl.grid(column=0, row=0)
#меню
menu = Menu(window)  
new_item = Menu(menu)  
new_item.add_command(label='Новый', command=NewDB)  
new_item.add_command(label='Открыть', command=clicked)
menu.add_cascade(label='Файл', menu=new_item) 
window.config(menu=menu)
window.mainloop()



