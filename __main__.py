#!/usr/bin/env python3
"""
Pointeur (utilisant tkinter)
- les fichiers (1/j) se trouvent dans data/
 format des fichiers : (nom : yyyy-mm-dd.txt)
    début : <hh:mm:ss>
    fin : <hh:mm:ss>
    
    début : ...

    TOTAL : <hh:mm:ss>
- TOTAL, créé avec le fichier, à mettre à jour dynamiquement ; blocs début/fin ajoutés dynamiquement
- GUI :
    - bouton "start"
    - bouton "stop"
    - temps travaillé aujourd'hui
"""

"""
sum_work :stocké sous la forme de datetime.timedelta(0,%S,0,0,%M,%H)
"""
import time
import datetime
import os 
import re
import tkinter
from tkinter.messagebox import showwarning as warning
import sys ; sys.stderr = open("data/crash.log","at")


#phase 1 : récupération et analyse du fichier
file_struct = "^(début : [0-2][0-9]:[0-5][0-9]:[0-5][0-9]\n\
fin : [0-2][0-9]:[0-5][0-9]:[0-5][0-9]\n\n)*\
\
(début : [0-2][0-9]:[0-5][0-9]:[0-5][0-9]\n\
(fin : [0-2][0-9]:[0-5][0-9]:[0-5][0-9]\n\n)?)?\
TOTAL : [0-2]?[0-9]:[0-5][0-9]:[0-5][0-9]$"

today = datetime.date.today().isoformat()+".txt"
if today in [x.name for x in os.scandir("data/") if x.is_file()]:
    data = open("data/"+today,"rt").readlines()
    if not re.match(file_struct,"".join(data)):
        if len(data) :
            warning("Fichier invalide",
            "Le fichier de pointage d'aujourd'hui est illisible ou a été modifié ; il va être réinitialisé.")
        data = list()
        sum_work = datetime.timedelta(0,0,0,0,0,0)
    else :
        sum_work = data.pop(-1)[8:]#TOTAL ln with numbers only
        sum_work = [int(x) for x in sum_work.split(":")]
        sum_work = datetime.timedelta(0,sum_work[2],0,0,sum_work[1],sum_work[0])
else :
    data = list()
    sum_work = datetime.timedelta(0,0,0,0,0,0)


#phase 2 : GUI
def write_start():
    now = time.strftime("%H:%M:%S")
    data.append("début : "+now+"\n")
    open("data/"+today,"wt").write("".join(data)+"TOTAL : "+str(sum_work))

def write_stop():
    global sum_work
    start = [int(x) for x in  data[-1][8:].split(":")]
    now = time.localtime()
    now = (now.tm_hour, now.tm_min, now.tm_sec)
    sum_work += datetime.timedelta(0,now[2]-start[2],0,0,now[1]-start[1],now[0]-start[0])
    data.extend(["fin : "+time.strftime("%H:%M:%S")+"\n","\n"])
    open("data/"+today,"wt").write("".join(data)+"TOTAL : "+str(sum_work))
    label.configure(text="Vous avez déjà travaillé "+str(sum_work))

def button_func(*args):
    if main_button["text"] == "Commencer" :
        write_start()
        main_button["text"] = "Finir"
    elif main_button["text"] == "Finir" :
        write_stop()
        main_button["text"] = "Commencer"
    else :
        raise ValueError("Bad value for main_button['text'] : "+main_button["text"])

main = tkinter.Tk()
main.title("Pointeur")

main_button = tkinter.Button(main,command=button_func)
if len(data)%3 == 0 :
    main_button["text"] = "Commencer"
elif len(data)%3 == 1 :
    main_button["text"] = "Finir"
else :
    raise ValueError("Bad len for data : "+str(len(data)))
main_button.pack(side="top",fill="x")

label = tkinter.Label(main,text="Vous avez déjà travaillé "+str(sum_work))
label.pack(side="bottom",fill="x")

main.mainloop()
