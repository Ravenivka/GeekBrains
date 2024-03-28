from sqlite3 import *
from tkinter import *
from tkinter import filedialog as fd
from easygui import *
import os

#Декларация
path = ''
db = None
my_filetypes =[("DB files", "*.db"),
                   ("db3 files", "*.db3;*.htm"),("sqlite files","*.sqlite"),
                   ("sqlite files","*.sqlite3"),("All files", "*.*")]
records = []

#Главное окно
window = Tk()

def Read_db(Data : Connection, recindex):  #Opening DB
    global records
    lbl_path.config(text = path)    
    cur = Data.cursor()
    cur.execute('Select * From Контакты;')
    records = cur.fetchall()
    records.sort()
    Data.commit()
    if len(records) == 0:
        msgbox(msg='Записи отсутствуют', title='Внимание')
        return       
    item = records[recindex]
    ent_title.delete(0, END)
    ent_title.insert(0,item[0])    
    phones =[word.strip() for word in item[1].split(';')]        
    phones_var.set(phones)
    mails =[word.strip() for word in item[2].split(';')]
    box_mails.config(height=len(mails))
    mails_var.set(mails)
    ent_bday.delete(0, END)
    ent_bday.insert(0,item[3])
    addons = [word.strip() for word in item[4].split(';')]
    if len(addons) > len(phones):
        box_addons.config(height=len(addons))
        box_phone.config(height=len(addons))
    else:
        box_addons.config(height=len(phones))
        box_phone.config(height=len(phones))
    addons_var.set(addons)

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
def Open_db():
    global db
    global path
    path = fd.askopenfilename(filetypes=my_filetypes, title='Выбор файла', initialfile='*.db') 
    db = Connect(path)
    Read_db(db, 0)  
    
 
def New_db():
    global path
    global db    
    path = fd.asksaveasfilename(filetypes = my_filetypes, title = "Сохранить как ....", defaultextension = my_filetypes) 
    db = Connect(path)
    Read_db(db, 0)

def New_rec():
    lbl_path.config(text = path) 
    ent_title.delete(0, END)       
    phones =[]        
    phones_var.set(phones)
    mails =[]
    box_mails.config(height=1)
    mails_var.set(mails)
    ent_bday.delete(0, END)    
    addons = []    
    box_addons.config(height=1)
    box_phone.config(height=1)    
    addons_var.set(addons)

def Search_rec():
    rslt = []
    for item in records:
        if ent_search.get() in item[0]:
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
    Read_db(db, index)    

def New_addons():    
    newvalue = enterbox('Добавьте информацию, для удобства используйте формат ТИП : Значение', 'Добавить', '' )
    if newvalue == '':
        return
    box_addons.insert(END, newvalue)
    if box_addons.size() > len(phones):
        box_addons.config(height=box_addons.size())
        box_phone.config(height=box_addons.size())
    else:
        box_addons.config(height=len(phones))
        box_phone.config(height=len(phones))
    
def New_phone():
    newvalue = enterbox('Добавьте номер телефона', 'Добавить', '' )
    if newvalue == '':
        return    
    box_phone.insert(END, newvalue)
    if box_phone.size() > len(addons):
        box_addons.config(height=box_phone.size())
        box_phone.config(height=box_phone.size())
    else:
        box_addons.config(height=len(addons))
        box_phone.config(height=len(addons))

def New_email():
    newvalue = enterbox('Добавьте e-mail', 'Добавить', '' )
    if newvalue == '':
        return     
    box_mails.insert(END, newvalue)
    box_mails.config(height=box_mails.size())



def Save_card(): 
    global path 
    global db   
    if db == None: #автосоздание базы данных
        counter = 1
        filename = "Контакты(1).db"
        while os.path.isfile(filename):
            counter += 1
            filename = "Контакты(" + str(counter) + ").db"
        path = os.path.abspath(filename)
        db = Connect(path)
    rows = []
    card_name = ent_title.get()
    rows.append(card_name)
    get_phones = ';'.join(box_phone.get(0, END))
    rows.append(get_phones)
    get_mails = ';'.join(box_mails.get(0, END))
    rows.append(get_mails)
    get_bd = ent_bday.get()
    rows.append(get_bd)
    get_addons = ';'.join(box_addons.get(0, END)) 
    rows.append(get_addons)
    curs = db.cursor() 
    info = curs.execute('SELECT * FROM Контакты WHERE title=?', (card_name, )).fetchone()
    if (info != None):
        info = curs.execute('DELETE FROM Контакты WHERE title=?', (card_name, ))
    curs.execute('INSERT into Контакты VALUES(?, ?, ?, ?, ?)', rows)
    db.commit()  
    Read_db(db, 0)
   
        

    


    

window.title("Телефонный справочник")
window.geometry('1024x600') 
lbl_path = Label(text = '', font = ("Arial", 10))
lbl_path.grid(row=0, column=0, pady=10, padx=10, columnspan=3)
lbl_title = Label(text = 'Имя', font = ("Script MT Bold", 14))
lbl_title.grid(row=1, column=0, pady=10, padx=10) 
ent_title = Entry()
ent_title.grid(row=1, column=1, pady=10, padx=10)
lbl_phon = Label(text = 'Телефоны:', font = ("Script MT Bold", 14))
lbl_phon.grid(row=2, column=0, pady=10, padx=10)
phones = []
phones_var = StringVar(value=phones)
box_phone = Listbox(listvariable=phones_var, height=1)
box_phone.grid(row=2, column=1, pady=10, padx=10)
btn_phone = Button(text = 'Добавить', command=New_phone)
btn_phone.grid(row = 2, column=2, sticky='E')
lbl_mail = Label(text = 'e-mail', font = ("Script MT Bold", 14))
lbl_mail.grid(row=3, column=0, pady=10, padx=10) 
lbl_day = Label(text = 'День рождения', font = ("Script MT Bold", 14))
lbl_day.grid(row=4, column=0, pady=10, padx=10) 
mails = []
mails_var = StringVar(value=mails)
box_mails = Listbox(listvariable=mails_var, height=1)
box_mails.grid(row=3, column=1, pady=10, padx=10)
btn_mail = Button(text = 'Добавить', command=New_email)
btn_mail.grid(row = 3, column=2, sticky='E')
ent_bday = Entry()
ent_bday.grid(row=4, column=1, pady=10, padx=10)
lbl_addon = Label(text = "Дополнительная информация", font = ("Script MT Bold", 14))
lbl_addon.grid(row=1, column=4, pady=10, padx=10, columnspan=2) 
addons = []
addons_var = StringVar(value = addons)
box_addons = Listbox(listvariable = addons_var, height=1, width=60)
box_addons.grid(row=2, column=4, columnspan=2, pady=10, padx=10)
btn_addons = Button(text = 'Добавить', command=New_addons)
btn_addons.grid(row = 1, column=6, sticky='E')
ent_search = Entry(width=40)
ent_search.insert(string='Найти', index=0)
ent_search.grid(row=0, column=5, pady=10, padx=10)
btn_search = Button(text = 'Поиск', command=Search_rec)
btn_search.grid(row = 0, column=6, sticky='E')
btn_save_card = Button(text='Сохранить изменения', command=Save_card)
btn_save_card.grid(row=5, column=3, columnspan=2)

#меню
menu = Menu(window)  
new_item = Menu(menu)  
new_item.add_command(label='Новый', command=New_db)  
new_item.add_command(label='Открыть', command=Open_db)
menu.add_cascade(label='Файл', menu=new_item) 
sec_item =Menu(menu)
sec_item.add_command(label='Новая', command=New_rec)
menu.add_cascade(label='Запись', menu=sec_item) 
window.config(menu=menu)
window.mainloop()



