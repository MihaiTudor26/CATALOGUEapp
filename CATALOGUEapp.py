import tkinter as tk
from tkinter import ttk, messagebox#ttk este un submodul a lui tkinter
import mysql.connector
from tkinter import*

#BECK-END

#Exit button
def qExit():
    gui.destroy()
    
#Clear button
def Clear():
    Nume.set("")
    Prenume.set("")
    NotaLaborator.set("")
    NotaExamen.set("")

#Obtinerea valorilor
global e1
global e2
global e3
global e4
def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    e1.insert(0,select['Nume'])
    e2.insert(0,select['Prenume'])
    e3.insert(0,select['Nota Laborator'])
    e4.insert(0,select['Nota Examen'])

#Adaugarea inregistrarilor in baza de date(mysql)    

def Add():
    x = e1.get()
    y= e2.get()#datele introduse de user sunt retinute in variabilele x,y,z,w
    z = e3.get()
    w = e4.get()

    mysqldb=mysql.connector.connect(host="localhost",user="root",password="mihai",database="note_studenti")
    mycursor=mysqldb.cursor()
    #numele  tabelului din mysql este registation
    try:
       sql = "INSERT INTO  note (Nume,Prenume,NotaLaborator,NotaExamen) VALUES (%s, %s, %s, %s)"
       val = (x,y,z,w)
       mycursor.execute(sql, val)
       mysqldb.commit()
       #lastid = mycursor.lastrowid
       messagebox.showinfo("information", "Inserted")
       e1.delete(0, END)
       e2.delete(0, END)#entry-urile devin vide dupa adaugarea informatiilor in mysql
       e3.delete(0, END)
       e4.delete(0, END)
       e1.focus_set()#primul entry devine din nou activ dupa stergerea informatiilor in urma adaugarii lor in mysql
    except Exception as e:
       print(e)
       mysqldb.rollback()#in cazul unei erori se revine la ultima forma a bazei de date, datele putand fi recuperate folosind metoda commit
       mysqldb.close()#inchiderea bazei de date

       
#Stergerea inregistrarilor din baza de date(mysql)

def delete():
    x = e1.get()

    mysqldb=mysql.connector.connect(host="localhost",user="root",password="mihai",database="note_studenti")
    mycursor=mysqldb.cursor()

    try:
       sql = "delete from note where Nume = %s"
       val = (x,)#stergerea se face avand ca mijloc de identificare numele
       mycursor.execute(sql, val)
       mysqldb.commit()
       lastid = mycursor.lastrowid
       messagebox.showinfo("information", "Deleted")

       e1.delete(0, END)
       e2.delete(0, END) #toate entry-urile devin  vide in urma stergerii din baza de date
       e3.delete(0, END)
       e4.delete(0, END)
       e1.focus_set()

    except Exception as e:

       print(e)
       mysqldb.rollback()
       mysqldb.close()
       

#Afisarea inregistrarilor din mysql si in aplicatie

def show():
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="mihai", database="note_studenti")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT Nume,Prenume,NotaLaborator,NotaExamen FROM note")
        records = mycursor.fetchall()#selectie totala
        print(records)#afisarea si in consola a datelor

        for i, (Nume,Prenume,NotaLaborator,NotaExamen) in enumerate(records, start=1):
            listBox.insert("", "end", values=(Nume,Prenume, NotaLaborator,NotaExamen))#inserarea inregistrarilor in widget-ul aplicatiei
            mysqldb.close()
      
       
###############################################################################################

#FRONT-ENT
gui=Tk()
gui.geometry("1000x700")

#Label-uri
label1=Label(gui,text="Evidenta Studentilor",font=('Verdana',25,'bold'),fg='black',bd=2)
label1.place(x=300, y=5)
label2= Label(gui,text ="Nume",font=('arial', 15, 'bold'),fg = "Steel Blue",bd = 10, anchor = 'w')
label2.place(x=10,y=90)
label3= Label(gui,text ="Prenume",font=('arial', 15, 'bold'),fg = "Steel Blue",bd = 10, anchor = 'w')
label3.place(x=10,y=140)
label4= Label(gui,text ="Nota Laborator",font=('arial', 15, 'bold'),fg = "Steel Blue",bd = 10, anchor = 'w')
label4.place(x=10,y=200)
label5= Label(gui,text ="Nota Examen",font=('arial', 15, 'bold'),fg = "Steel Blue",bd = 10, anchor = 'w')
label5.place(x=10,y=250)

#Entry-uri
Nume=StringVar()
Prenume=StringVar()
NotaLaborator=StringVar()
NotaExamen=StringVar()
e1=Entry(gui,font = ('arial', 15),textvariable=Nume,bg = "powder blue")
e1.place(x=120,y=100)
e2=Entry(gui,font = ('arial', 15),textvariable=Prenume,bg = "powder blue")
e2.place(x=120,y=150)
e3=Entry(gui,font = ('arial', 15),textvariable=NotaLaborator,bg = "powder blue",width=5)
e3.place(x=170,y=210)
e4=Entry(gui,font = ('arial', 15),textvariable=NotaExamen,bg = "powder blue",width=5)
e4.place(x=170,y=260)

#Button-uri
button1=Button(gui, text="Add",height=3,width= 13,fg = "black",bg = "powder blue",command=Add)
button1.place(x=30,y=310)
button2=Button(gui, text="Delete",height=3,width= 13,fg = "black",bg = "powder blue",command=delete)
button2.place(x=140,y=310)
button4=Button(gui, text="Exit",height=3,width= 13,fg = "black",bg = "red",command=qExit)
button4.place(x=550,y=310)
button5=Button(gui, text="Clear",height=3,width= 13,fg = "black",bg = "green",command=Clear)
button5.place(x=660,y=310)

#Inregistrarile--crearea box-ului cu inregistrari din aplicatie

cols = ('Nume', 'Prenume', 'Nota Laborator','Nota Examen')#retine antetul tabelului
listBox = ttk.Treeview(gui, columns=cols, show='headings' )#cream un treeview widget

for col in cols:
    listBox.heading(col, text=col)#adaugam antetul fiecarei colane
    listBox.grid(row=1, column=0, columnspan=2)#amplasrea "capetelor" de tabel
    listBox.place(x=10, y=410)#amplasarea widget-ului

#Adaugarea unui scrollbar
scrollbar = ttk.Scrollbar(gui, orient=tk.VERTICAL, command=listBox.yview)
listBox.configure(yscroll=scrollbar.set)#amplasarea verticala a scrollbar-ului pe treeview
scrollbar.place(x=795,y=410)#pozitionarea sa

show()
listBox.bind('<Double-Button-1>',GetValue)#bind permite legarea a doua functii intre ele
#in cazul nostru la selectia unui rand din box, acesta apare in entry-uri prin intermediul functiei getvalue
#'<Double-Button-1>'-aparitia valorilor inregistrarii in entry-uri se face cu dublu click
gui.mainloop()
