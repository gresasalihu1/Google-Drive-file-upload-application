#importimi i librarive
import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from guizero import  error
import tkinter as tk
import json
import requests
from PIL import Image, ImageTk

#krijimi i nje dritareje permes tkinter
window = Tk()

#ndryshimi i specifikave te dritares
window.configure(bg='#1569C7')
window.title("Ngarkimi i fajllit ne Google Drive")
window.geometry('500x200')
#vendosja e ikones te aplikacionit
window.iconbitmap("img/up.ico")

#krijimi i  variablave te tipit string
token=token_var = tk.StringVar()
folder_var = tk.StringVar()

#krijimi i label l dhe vendosja e specifikave te saj
l = Label(window, text="  Ngarkimi i fajllave ne Google Drive permes Python ",font=('calibre', 12, 'normal'),fg='white',bg='#1569C7')

#percaktimi i pozicionit te label-it ne dritare
l.place(relx=0.1,rely=0.3,anchor=NW)

#vendosja e fotos me size te percaktuar
image = Image. open('img/fotoo.jpg')
image = image. resize((60, 50), Image. ANTIALIAS)
my_img = ImageTk. PhotoImage(image)
panel = Label(window, image = my_img)

#percaktimi i pozicionit te fotos ne dritare
panel.place(relx=0.4,rely=0.5,anchor=NW)


#krijimi i funksionit upload
def upload():
    #fshirja e labels te caktuar pas shtypjes se menus Upload
    panel.destroy()
    l.destroy()

    #krijimi i labels dhe percaktimi i specifikate te tyre
    tk.Label(window, text='Token', font=('calibre', 11, 'normal'), fg='white',bg='#1569C7').place(relx=0.1, rely=0.1, anchor=NE)
    tk.Label(window, text='Folder', font=('calibre', 11, 'normal'), fg='white',bg='#1569C7').place(relx=0.1, rely=0.25, anchor=NE)

    #krijimi i fushave per vendosjen e tokenit dhe folderit
    tk.Entry(window, textvariable=token_var, font=('calibre', 11, 'normal')).place(relx=0.15, rely=0.1,width=260)
    tk.Entry(window, textvariable=folder_var, font=('calibre', 11, 'normal')).place(relx=0.15, rely=0.25,width=260)

    #vendosja e butonit me shtypjen  e te cilit ekzekutohet funksioni openfile
    Button(window, text='Upload File', font=('calibre', 9, 'normal'),fg='white',bg="#003c5e",highlightcolor="blue" ,command=openfile).place(relx=0.27, rely=0.5, anchor=CENTER)

#krijimi i funksionit openfile
def openfile():
    token = token_var.get()
    folder = folder_var.get()
    #kontrollojm nese tokeni i vendosur eshte gabim
    if token.startswith("ya29.") and len(token)!=0 and len(folder)!=0:

        # krijimi i nje variable filepath e cila permban specifikat e file te zgjedhur nga perdoruesi
        filepath = filedialog.askopenfilename(
                                              title="Open file",
                                              filetypes= ((".docx",".docx"),
                                              (".doc","*.doc*"), (".xls","*.xls*"),(".xlsx","*.xlsx*")))

        #marrim emrin dhe extension nga file i zgjedhur
        name, extension = os.path.splitext(filepath)


        #vendosja e tokenit dhe folderit nga perdoruesi per te pas qasje ne google drive dhe ne folderin specifik
        headers = {
            "Authorization": "Bearer " + token_var.get()}
        para = {
            "name": os.path.basename(name),
            "parents" : [folder_var.get()]
        }

        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open(filepath, "rb")
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )
        print("Dokumenti " + os.path.basename(name) + " u be  upload ne Google Drive")
        print(r.text)
        messagebox.showinfo("Upload", "Dokumenti u ruajt me sukses")

    else:
        error("Gabim ", "Ju lutem shkruani Access Tokenin dhe Folderin e duhur")

#krijimi i funksionit help qe na jep nje informacion ndihmes rreth perdorimit te aplikacionit
def help():

    messagebox.showinfo("Help", "Zgjedh Upload dhe vendos file")

#krijimi i funksionit exitt qe mundeson mbylljen e aplikacionit
def exitt():
    messagebox.showinfo("Exit", "Aplikacioni u mbyll")
    window.destroy()

#krijimi i menubar
menubar = Menu(window)

#krijimi i filemenu dhe  i komandave te saj
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Upload", command=upload)
filemenu.add_command(label="Exit", command=exitt)
menubar.add_cascade(label="File", menu=filemenu)

#krijimi i helpmenu  dhe  i komandes te saj
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=help)
menubar.add_cascade(label="Help", menu=helpmenu)

#vendosja e menus ne dritare
window.config(menu=menubar)
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
menu = Menu(menubar, tearoff=0)

window.mainloop()


