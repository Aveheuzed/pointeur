#!/usr/bin/env python3

import pickle, time, datetime, tkinter
from threading import Thread

"""Les données sont stockées sous forme sérialisée dans ./data.pick ;
Le moment du dernier pointage est stocké sous forme sérialisée dans ./lasttick.pick

Contenu de data.pick :
[
        [jour <datetime.date(année, mois, jour)>,  temps_travaillé <secondes <=> int> ],
]

Contenu de lasttick.pick :
lasttick <int : time.time())>"""

PATH = dict(data="data.pick", lasttick="lasttick.pick")

def get_data(file):
        return pickle.load(open(file, "rb"))

def set_data(new_data, file):
        pickle.dump(new_data, open(file, "wb"))
#il serait utile de faire un cache de data, pour éviter d'utiliser le dique à tout bout de champ...

def update_lasttick():
        set_data(int(time.time()), PATH["lasttick"])


class TimeManager(Thread):
        """Cette classe modélise un Thred qui va,  à intervalles de 5 mn,
        actualiser la durée travaillée.
        Si le dernier pointage date de plus de 5 mn (ex veille du PC),
        le temps depuis le dernier pointage est retranché.
        """
        TIMESTAMP = 5#5 min = 300 s
        WORKING = False
        _singleton = None
        def __new__(cls) :
                if TimeManager._singleton is None :
                         TimeManager._singleton = object.__new__(cls)
                return TimeManager._singleton
        # def __init__(self):
        #         super().__init__()
        def run(self):
                while True :
                        if TimeManager.WORKING :
                                lasttick = get_data(PATH["lasttick"])
                                #processing,  checking,  incrementing...
                                now = int(time.time())
                                prev_now = now - TimeManager.TIMESTAMP
                                data = get_data(PATH["data"])
                                #on utilise un intervalle de +/-1 s pour plus de sécurité
                                if lasttick in range(prev_now-1, prev_now+1) :#si pas d'interruption depuis le dernier tick
                                        #incrémentation simple
                                        data[-1][1] += TimeManager.TIMESTAMP

                                        total_work = str(datetime.timedelta(seconds=data[-1][1]))
                                        label.configure(text="Vous avez déjà travaillé "+total_work)
                                else :
                                        #fin de la période de travail en cours ; début d'une nouvelle
                                        today = datetime.date.today()
                                        if data[-1][0] != today :#on change de jour
                                                data.append([today, 0])
                                        #si on reste dans la me journée, il n'y a rien à faire

                                set_data(data, PATH["data"])

                        update_lasttick()
                        time.sleep(TimeManager.TIMESTAMP)


time_manager = TimeManager()
time_manager.start()


def button_func(*args):
        if main_button["text"] == "Commencer" :
                main_button["text"] = "Finir"
        elif main_button["text"] == "Finir" :
                main_button["text"] = "Commencer"
        else :
                raise ValueError("Bad value for main_button['text'] : "+main_button["text"])
        TimeManager.WORKING = not TimeManager.WORKING

main = tkinter.Tk()
main.title("Pointeur")

main_button = tkinter.Button(main,command=button_func,text="Commencer")

main_button.pack(side="top",fill="x")

data = get_data(PATH["data"])[-1][1]
label = tkinter.Label(main,text="Vous avez déjà travaillé "+str(data))
label.pack(side="bottom",fill="x")

# main.bind("<Destroy",what_on_exit)

main.mainloop()
