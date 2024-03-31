from sqlite3 import *
from easygui import *
from pathlib import *
import shutil
import csv 

# Создание таблиц

path = 'Base.db'
flag = True
db = connect(path)
cur = db.cursor()
sql_str = '''
CREATE TABLE if not exists "replacer" (
    "ID" TEXT,
    "value" TEXT,
    PRIMARY KEY("ID")
);
'''
def Read_replacer():
    result = cur.execute("SELECT * FROM replacer").fetchall()
    res = dict()
    for item in result:
        res[item[0]] = item[1]
    return res

replacer = Read_replacer()


cur.execute(sql_str)
for key, value in replacer.items():
    sql_str = "insert into replacer values('" + key + "', '" + value + "');"
    try: 
        cur.execute(sql_str)
    except:
        pass

sql_str = '''
CREATE TABLE if not exists "mail" (
	"ID"	INTEGER NOT NULL,
	"user"	TEXT NOT NULL,
	"mail"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
'''
cur.execute(sql_str)
sql_str = '''
CREATE TABLE if not exists "phon" (
	"ID"	INTEGER NOT NULL,
	"user"	TEXT NOT NULL,
	"phon"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
'''
cur.execute(sql_str)
sql_str = '''
CREATE TABLE if not exists "users" (
	"user"	TEXT NOT NULL,
	"bday"	TEXT,
	PRIMARY KEY("user")
);
'''
cur.execute(sql_str)
db.commit()


#список таблиц
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
tables = [t[0].strip() for t in tables if t[0] != 'sqlite_sequence']


def Createfield_single(name):        
    sql_str = 'ALTER TABLE users ADD COLUMN ' + name + ' TEXT;'
    try:
        cur.execute(sql_str)
        db.commit()       
    except OperationalError as e:
        msgbox(e, 'Ошибка')
    return

def Createfield_multiple(name):        
    sql_str = 'CREATE TABLE ' + name + '(ID INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, ' + name + ' TEXT);'
    try:
        cur.execute(sql_str)
        db.commit()       
    except OperationalError as e:
        msgbox(e, 'Ошибка')
    return  

msg = '''
        Команды управления:
            welcome - показать стартовое сообщение            
            help - список команд
            save - сохранить справочник
            view - показать весь справочник
            search - найти контакт
            del - удалить контакт
            add - добавить категорию
            import - импортировать справочник
            edit - редактировать запись
            new - новая запись
            q - выход
        '''
def Invers(x):
    for key, value in replacer.items():
        if value == x:
            return key
        else:
            return None
        
def Wcm(): #welcome
    msgbox(msg, 'Телефонный справочник')

def ViewTable(Tablename, base: Connection, username):
    curs = base.cursor()
    s = "SELECT " + Tablename + " FROM " + Tablename + " WHERE user ='" + username + "';"
    result = curs.execute(s)
    vals = result.fetchall()
    if len(vals) !=0:
        print(replacer[Tablename])
        for v in vals:
            print('     ', v[Tablename])



def View(base: Connection):    
    base.row_factory = Row
    s = 'SELECT * FROM users;'
    curs = base.cursor()
    result = curs.execute(s) 
    names = [description[0] for description in result.description]  
    vals = result.fetchall() 
    if len(vals) == 0:
        print('Записи отсутствуют')
        return    
    for item in vals:        
        for v in names:
            print(f"{replacer[v]}: {item[v]}")            
        for t in tables:
            if (t in ['replacer', 'users']) == False:
                ViewTable(t, base, item['user'])

def ViewOne(conn: Connection, usr):
    if usr == None:
        msgbox('Подьзователь не выбран', 'Ошибка')
        return
    conn.row_factory = Row
    s = "SELECT * FROM users WHERE user = '" + usr + "';"
    curs = conn.cursor()
    result = curs.execute(s)
    names = [description[0] for description in result.description]
    vals = result.fetchone()
    if len(vals) == 0:
        print('Записи отсутствуют')
        return  
    for v in names:        
        print(f"{replacer[v]}: {vals[v]}")
    for t in tables:
        if (t in ['sqlite_sequence', 'users', 'replacer']) == False:
            ViewTable(t, conn, vals['user'])
    
def Save():
    new_path = filesavebox('Выберите папку назначения:', 'Сохранить как', 'Контакты.db', "*.db")
    if new_path != None:
        shutil.copyfile(path, new_path)
    
def Import(conn: Connection):
    new_path = diropenbox("Выберите директортю:", "Выбор папки")
    if new_path == None:
        return
    print('output:')
    for t in tables:
        if (t in ['sqlite_sequence']) == False:
            p = Path(new_path)
            outpath = p / (t + '.csv')
            cursor = conn.cursor()
            s = 'SELECT * FROM '+ t +';'
            cursor.execute(s)
            with open(outpath, 'w',newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
            print(outpath)

def SELECT(conn: Connection):
    array = []    
    pattern = enterbox('Введите часть имени', 'Найти', '')
    cursor = conn.cursor()
    result = cursor.execute('SELECT user FROM users;')    
    vals = result.fetchall()
    for record in vals:
        if pattern == None:
            return
        if pattern in record[0]:
            array.append(record[0])
    if len(array) == 0:
        msgbox('Ничего не найдено')
        return
    return array


def Search(conn: Connection):
    array = SELECT(conn) 
    if array == None:
        msgbox("Ничего не найдено")
        return 
    if len(array) ==1:
        choice = enterbox('Результат:', 'Поиск', array[0])
    else:
        choice = choicebox('Сделайте выбор', 'Поиск', array)
    try:
        ViewOne(conn, choice)
    except OperationalError as e:
        msgbox(e, 'Ошибка')        
            
def Del(conn: Connection):
    array = SELECT(conn)  
    if len(array) ==1:
        choice = enterbox('Результат:', 'Поиск', array[0])
    else:
        choice = choicebox('Сделайте выбор', 'Поиск', array) 
    cursor  = conn.cursor()
    s = "DELETE FROM Users WHERE user ='" + choice + "';"
    try:
        cursor.execute(s)
    except OperationalError as e:
        msgbox(e, 'Ошибка') 
        return
    for t in tables:
        s = "DELETE FROM " + t + " WHERE user ='" + choice + "';"
        try:
            cursor.execute(s)
        except OperationalError as e:
            msgbox(e, 'Ошибка') 
            return
    conn.commit()

def Add(base: Connection):
    choise = choicebox("Какую категорию вы хотите создать?", "Выбор", ["Однострочную", "Многострочную"])    
    caption = enterbox("Введите название, желательно латиницей", "Внимание")
    if (choise != None) and (caption != None):
        print(choise)
    if caption.strip() == '':
        msgbox("Недопустимое название")
        return
    new_column = "ALTER TABLE users ADD COLUMN " + caption + " TEXT;"
    curs = base.cursor()
    if choise == 'Однострочную':
        curs.execute(new_column)
    else:
        sql_str = "CREATE TABLE if not exists " + caption + "(ID INTEGER NOT NULL, " + "user TEXT NOT NULL, " + caption + " TEXT, PRIMARY KEY(ID AUTOINCREMENT));"
        curs.execute(sql_str)
        sql_str = "Insert into replacer values('" + caption + "', '" + caption + "');"
        curs.execute(sql_str)
        base.commit()

def Edit(base: Connection): 
    base.row_factory = Row   
    array = SELECT(base)
    if len(array) ==1:
        choice = enterbox('Результат:', 'Поиск', array[0])
    else:
        choice = choicebox('Сделайте выбор', 'Поиск', array) 
    cursor  = base.cursor()
    sql_str = "SELECT * FROM users WHERE user = '" + choice + "';" 
    result = cursor.execute(sql_str)
    array = result.fetchone()
    names = [description[0] for description in result.description]
    record = []
    for nm in names:
        record.append(array[nm])
    form = multenterbox('Шаг 1', 'Редактор', names, record)
    sql_str = "DELETE FROM Users WHERE user ='" + choice + "';"
    result = cursor.execute(sql_str)
    sql_str = "('"
    for s in form:
        sql_str = sql_str + s + "', '"
    sql_str = "INSERT INTO users Values" + sql_str[:-3] + ");"
    reult = cursor.execute (sql_str)
    base.commit()   
    for t in tables:
        Fields = []
        Values = []
        if (t in ['replacer', 'users']) == False:
            sql_str = "SELECT ID, " + t + " FROM " + t +";"            
            result = cursor.execute(sql_str).fetchall()            
            for item in result:
                Fields.append(item['ID'])
                Values.append(item[t] )
            form2 = multenterbox(t, 'Редактор', Fields, Values)
            for i in range(len(Fields)):
                sql_str = "UPDATE " + t + " SET " + t + " = '" + form2[i] + "' WHERE ID = " + str(Fields[i]) + ";"
                result = cursor.execute(sql_str)
                base.commit()

def Add_new(base: Connection):       
    curs = base.cursor()
    result = curs.execute("PRAGMA table_info(users)").fetchall()
    names = [replacer[item[1]] for item in result]     
    user = multenterbox('Введите данные контакта', 'Новый контакт', names)  
    tables2 = list() 
    for item in tables:
        if (item != 'replacer') and (item != 'users'):
            tables2.append(item)    
    tbls2 = [replacer[item] for item in tables2]
    another = multenterbox('Дополнительная информация', 'Новый контакт', tbls2)
    sql_str = ''
    for item in user:
        sql_str = sql_str + "'" + item + "', "
    sql_str = "INSERT INTO users VALUES(" + sql_str[:-2] + ");"
    curs.execute(sql_str)
    sql_str = ''
    for i in range(len(tables2)):
        sql_str = "INSERT INTO " + tables2[i] + "(user, " + tables2[i] + ") VALUES ('" + user[0]+ "', '" + another[i] + "');"
        curs.execute(sql_str)
    base.commit()



    
       
            



Wcm()

# просмотр, сохранение, импорт, поиск, удаление, изменение данных
while flag:
    replacer = dict()
    sql_str = "SELECT * FROM replacer"    
    replacer_items = cur.execute(sql_str).fetchall()
    for item in replacer_items:
        replacer[item[0]] = item[1]    
    com = input('Введите команду: ')
    match com:
        case 'welcome': Wcm()
        case 'q': flag = False
        case 'help': print(msg)
        case 'view': View(db)
        case 'save': Save()
        case 'import' : Import(db)
        case 'search' : Search(db)
        case 'del' : Del(db)
        case 'add' : Add(db)
        case 'edit' : Edit(db)
        case 'new' : Add_new(db)


msgbox('До встречи!', 'Сообщение')
db.close()
quit()





