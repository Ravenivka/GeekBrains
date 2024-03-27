from sqlite3 import *
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter import simpledialog
from easygui import *

#Декларация
path = ''
db = None
myfiletypes =[("DB files", "*.db"),
                   ("db3 files", "*.db3;*.htm"),("sqlite files","*.sqlite"),
                   ("sqlite files","*.sqlite3"),("All files", "*.*")]
records = []

#Главное окно
window = Tk()

def ReadDB(Data : Connection, recindex):  #Opening DB
    global records
    lblpath.config(text = path)    
    cur = Data.cursor()
    cur.execute('Select * From Контакты;')
    records = cur.fetchall()
    records.sort()
    Data.commit()
    if len(records) == 0:
        showwarning(message='Записи отсутствуют', title='Внимание')
        return       
    item = records[recindex]
    enttitle.delete(0, END)
    enttitle.insert(0,item[0])    
    Phones =[word.strip() for word in item[1].split(';')]        
    Phones_var.set(Phones)
    Mails =[word.strip() for word in item[2].split(';')]
    boxmails.config(height=len(Mails))
    Mails_var.set(Mails)
    entday.delete(0, END)
    entday.insert(0,item[3])
    Addons = [word.strip() for word in item[4].split(';')]
    if len(Addons) > len(Phones):
        boxAddons.config(height=len(Addons))
        boxphone.config(height=len(Addons))
    else:
        boxAddons.config(height=len(Phones))
        boxphone.config(height=len(Phones))
    Addons_var.set(Addons)

def Connect(dbpath): #Подключение базы данных
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
    path = fd.askopenfilename(filetypes=myfiletypes, title='Выбор файла', initialfile='*.db') 
    db = Connect(path)
    ReadDB(db, 0)  
    
 
def NewDB():
    global path
    global db    
    path = fd.asksaveasfilename(filetypes = myfiletypes, title = "Сохранить как ....", defaultextension = myfiletypes) 
    db = Connect(path)
    ReadDB(db, 0)

def NewRec():
    lblpath.config(text = path) 
    enttitle.delete(0, END)       
    Phones =[]        
    Phones_var.set(Phones)
    Mails =[]
    boxmails.config(height=1)
    Mails_var.set(Mails)
    entday.delete(0, END)    
    Addons = []    
    boxAddons.config(height=1)
    boxphone.config(height=1)    
    Addons_var.set(Addons)

def SearchRec():
    rslt = []
    for item in records:
        if entsearch.get() in item[0]:
            rslt.append(item[0])
    if len(rslt) == 0:
        msgbox('Ничего не найдено')
        return
    elif len(rslt) == 1:
        choice = enterbox(msg='', title='Результаты выборв', default=rslt[0])
    else:
        choice = choicebox(msg='', title='Результаты выборв', choices=rslt)
    if choice == '':
        return
    for i in range(len(records)):
        item = records[i]
        if item[0] == choice:
            index = i
    ReadDB(db, index)
        

    

def NewAddon():
    newvalue = simpledialog.askstring('Добавить', 'Добавьте информацию, для удобства используйте формат ТИП : Значение')
    boxAddons.insert(END, newvalue)
    if boxAddons.size() > len(Phones):
        boxAddons.config(height=boxAddons.size())
        boxphone.config(height=boxAddons.size())
    else:
        boxAddons.config(height=len(Phones))
        boxphone.config(height=len(Phones))
    
def NewPhone():
    newvalue = simpledialog.askstring('Добавить', 'Добавьте номер телефона')
    boxphone.insert(END, newvalue)
    if boxphone.size() > len(Addons):
        boxAddons.config(height=boxphone.size())
        boxphone.config(height=boxphone.size())
    else:
        boxAddons.config(height=len(Addons))
        boxphone.config(height=len(Addons))

def NewMail():
    newvalue = simpledialog.askstring('Добавить', 'Добавьте e-mail')
    boxmails.insert(END, newvalue)
    boxmails.config(height=boxmails.size())
    

window.title("Телефонный справочник")
window.geometry('1024x600') 
lblpath = Label(text = '', font = ("Arial", 10))
lblpath.grid(row=0, column=0, pady=10, padx=10, columnspan=3)
lbltitle = Label(text = 'Имя', font = ("Script MT Bold", 14))
lbltitle.grid(row=1, column=0, pady=10, padx=10) 
enttitle = Entry()
enttitle.grid(row=1, column=1, pady=10, padx=10)
lblphon = Label(text = 'Телефоны:', font = ("Script MT Bold", 14))
lblphon.grid(row=2, column=0, pady=10, padx=10)
Phones = []
Phones_var = StringVar(value=Phones)
boxphone = Listbox(listvariable=Phones_var, height=1)
boxphone.grid(row=2, column=1, pady=10, padx=10)
btnphone = Button(text = 'Добавить', command=NewPhone)
btnphone.grid(row = 2, column=2, sticky='E')
lblmail = Label(text = 'e-mail', font = ("Script MT Bold", 14))
lblmail.grid(row=3, column=0, pady=10, padx=10) 
lblday = Label(text = 'День рождения', font = ("Script MT Bold", 14))
lblday.grid(row=4, column=0, pady=10, padx=10) 
Mails = []
Mails_var = StringVar(value=Mails)
boxmails = Listbox(listvariable=Mails_var, height=1)
boxmails.grid(row=3, column=1, pady=10, padx=10)
btnmail = Button(text = 'Добавить', command=NewMail)
btnmail.grid(row = 3, column=2, sticky='E')
entday = Entry()
entday.grid(row=4, column=1, pady=10, padx=10)
lbladdon = Label(text = "Дополнительная информация", font = ("Script MT Bold", 14))
lbladdon.grid(row=1, column=4, pady=10, padx=10, columnspan=2) 
Addons = []
Addons_var = StringVar(value = Addons)
boxAddons = Listbox(listvariable = Addons_var, height=1, width=60)
boxAddons.grid(row=2, column=4, columnspan=2, pady=10, padx=10)
btnAddon = Button(text = 'Добавить', command=NewAddon)
btnAddon.grid(row = 1, column=6, sticky='E')
entsearch = Entry(width=40)
entsearch.insert(string='Найти', index=0)
entsearch.grid(row=0, column=5, pady=10, padx=10)
btnsearch = Button(text = 'Поиск', command=SearchRec)
btnsearch.grid(row = 0, column=6, sticky='E')

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



