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
    box_addons.delete(0, END)
    box_phone.delete(0, END)
    box_mails.delete(0, END)
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
    phones = [word.strip() for word in item[1].split(';') if word != '']        
    phones_var.set(phones)
    mails =[word.strip() for word in item[2].split(';') if word != '']
    box_mails.config(height=len(mails))
    mails_var.set(mails)
    ent_bday.delete(0, END)
    ent_bday.insert(0,item[3])
    addons = [word.strip() for word in item[4].split(';') if word != '']
    if len(addons) > len(phones):
        box_addons.config(height=len(addons))
        box_phone.config(height=len(addons))
    else:
        box_addons.config(height=len(phones))
        box_phone.config(height=len(phones))
    addons_var.set(addons)
    lbl_index.config(text=str(recindex))

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
    lbl_index.config(text='*')

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
    lbl_index.config(text=str(index))   

def New_addons():    
    newvalue = enterbox('Добавьте информацию', 'Добавить', '' )
    if newvalue == '':
        return
    if box_addons.size() == 0:
        addons_var.set([newvalue])
    else:        
        box_addons.insert(END, newvalue)
    if box_addons.size() > box_phone.size():
        box_addons.config(height=box_addons.size())
        box_phone.config(height=box_addons.size())
    else:
        box_addons.config(height=box_phone.size())
        box_phone.config(height=box_phone.size())
    
def New_phone():
    newvalue = enterbox('Добавьте номер телефона', 'Добавить', '' )
    if newvalue == '':
        return    
    if box_phone.size() == 0 :
        phones_var.set([newvalue])
    else:        
        box_phone.insert(END, newvalue)
    if box_phone.size() > box_addons.size():
        box_addons.config(height=box_phone.size())
        box_phone.config(height=box_phone.size())
    else:
        box_addons.config(height=box_addons.size())
        box_phone.config(height=box_addons.size())

def New_email():
    newvalue = enterbox('Добавьте e-mail', 'Добавить', '' )
    if newvalue == '':
        return     
    if box_mails.size() == 0:
        mails_var.set([newvalue])
    else:        
        box_mails.insert(END, newvalue)
    box_mails.config(height=box_mails.size())

def Del_rec():
    curs = db.cursor()
    card_name = ent_title.get()
    curs.execute('DELETE FROM Контакты WHERE title=?', (card_name, ))
    db.commit()  
    Read_db(db, 0)            

def Save_rec(): 
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
        index = 0
    else:
        if lbl_index.cget('text') == '*':
            index = 0
        else:
            index = int(lbl_index.cget('text'))
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
    Read_db(db, index)
   
        
def Movie_first():
    Read_db(db, 0)
    
def Movie_prev():
    i = int(lbl_index.cget('text'))
    if i != 0:
        i = i-1
        Read_db(db, i)

def Movie_next():
    i = int(lbl_index.cget('text'))
    if i != len(records) - 1 :
        i+=1
        Read_db(db, i)
    
def Movie_last():
    Read_db(db, len(records) - 1) 

def Edit(list : Listbox):
    value = ';'.join(list.get(0,END))
    result = enterbox('Внесите изменения', 'Внимание', value)
    if result != None:
        array=[word.strip() for word in result.split(';') if word != '']
        list.delete(0, END)
        list.config(listvariable = StringVar(value=array))


def Edit_phone():
    Edit(box_phone)

def Edit_email():
    Edit(box_mails)

def Edit_addons():
    Edit(box_addons)
    

#Окно
window.title("Телефонный справочник")
window.geometry('1024x600')
add_img = PhotoImage(file="add.png")
edit_img = PhotoImage(file="edit.png")
lbl_path = Label(text = '', font = ("Arial", 10)) #Путь к файлу
lbl_path.grid(row=0, column=0, pady=10, padx=10, columnspan=3)
lbl_title = Label(text = 'Имя', font = ("Script MT Bold", 14)) 
lbl_title.grid(row=1, column=0, pady=10, padx=10) 
ent_title = Entry() #Поле title
ent_title.grid(row=1, column=1, pady=10, padx=10)
lbl_phon = Label(text = 'Телефоны:', font = ("Script MT Bold", 14))
lbl_phon.grid(row=2, column=0, pady=10, padx=10)
phones = []
phones_var = StringVar(value=phones)
box_phone = Listbox(listvariable=phones_var, height=1) #Список телефонов
box_phone.grid(row=2, column=1, pady=10, padx=10)
btn_phone = Button(text = 'Добавить', command=New_phone, image=add_img)
btn_phone.grid(row = 2, column=2, sticky='W')
btn_e_phone = Button(text = 'Изменить', command=Edit_phone, image=edit_img)
btn_e_phone.grid(row = 2, column=3, sticky='E')
lbl_mail = Label(text = 'e-mail', font = ("Script MT Bold", 14))
lbl_mail.grid(row=3, column=0, pady=10, padx=10) 
lbl_day = Label(text = 'День рождения', font = ("Script MT Bold", 14))
lbl_day.grid(row=4, column=0, pady=10, padx=10) 
mails = []
mails_var = StringVar(value=mails)
box_mails = Listbox(listvariable=mails_var, height=1) #Список почтовых адресов
box_mails.grid(row=3, column=1, pady=10, padx=10)
btn_mail = Button(text = 'Добавить', command=New_email, image=add_img)
btn_mail.grid(row = 3, column=2, sticky='W')
btn_e_mail = Button(text = 'Изменить', command=Edit_email, image=edit_img)
btn_e_mail.grid(row = 3, column=3, sticky='E')
ent_bday = Entry() #День рождения
ent_bday.grid(row=4, column=1, pady=10, padx=10)
lbl_addon = Label(text = "Дополнительная информация", font = ("Script MT Bold", 14))
lbl_addon.grid(row=1, column=4, pady=10, padx=10, columnspan=2) 
addons = []
addons_var = StringVar(value = addons)
box_addons = Listbox(listvariable = addons_var, height=1, width=60) #Дополнения
box_addons.grid(row=2, column=4, columnspan=2, pady=10, padx=10)
btn_addons = Button(text = 'Добавить', command=New_addons, image=add_img)
btn_addons.grid(row = 1, column=6, sticky='W')
btn_e_addons = Button(text = 'Изменить', command=Edit_addons, image=edit_img)
btn_e_addons.grid(row = 1, column=7, sticky='E')
ent_search = Entry(width=40)
ent_search.insert(string='Найти', index=0)
ent_search.grid(row=0, column=5, pady=10, padx=10)
btn_search = Button(text = 'Поиск', command=Search_rec)
btn_search.grid(row = 0, column=6, sticky='E')
btn_Save_rec = Button(text='Сохранить изменения', command=Save_rec)
btn_Save_rec.grid(row=5, column=3, columnspan=2)
first_img = PhotoImage(file="Button-Rewind-icon.png")
last_img = PhotoImage(file="Button-Forward-icon.png")
prev_img = PhotoImage(file="Media-Controls-Rewind-icon.png")
next_img = PhotoImage(file="Media-Controls-Fast-Forward-icon.png")
btn_first = Button(command=Movie_first, image=first_img)
btn_first.grid(row=7, column=1, sticky='E', pady=10)
btn_prev = Button(command=Movie_prev, image=prev_img)
btn_prev.grid(row=7, column=2, sticky='W', pady=10)
lbl_index = Label(font = ("Script MT Bold", 16))
lbl_index.grid(row=7, column=3, pady=10)
btn_next = Button(command=Movie_next, image=next_img)
btn_next.grid(row=7, column=4, sticky='E', pady=10)
btn_last = Button(command=Movie_last, image=last_img)
btn_last.grid(row=7, column=5, sticky='W', pady=10)

#меню
menu = Menu(window)  
new_item = Menu(menu)  
new_item.add_command(label='Новый', command=New_db)  
new_item.add_command(label='Открыть', command=Open_db)
menu.add_cascade(label='Файл', menu=new_item) 
sec_item =Menu(menu)
sec_item.add_command(label='Новая', command=New_rec)
sec_item.add_command(label='Cохранить', command=Save_rec)
sec_item.add_command(label='Удалить', command=Del_rec)
menu.add_cascade(label='Запись', menu=sec_item) 
window.config(menu=menu)
window.mainloop()



