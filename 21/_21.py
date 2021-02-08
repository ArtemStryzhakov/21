from tkinter import *
from tkinter import ttk, messagebox, scrolledtext
from translate import Translator
import math
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import webbrowser
import time, random

def theme():
    tab1.configure(background="#2F4F4F")
    tab2.configure(background="#2F4F4F")
    tab3.configure(background="#2F4F4F")
    txt_box.configure(background="gray")
    txt_box1.configure(background="gray")
    display.configure(background="#2F4F4F")

def theme1():
    tab1.configure(background="#FAF0E6")
    tab2.configure(background="#FAF0E6")
    tab3.configure(background="#FAF0E6")
    txt_box.configure(background="white")
    txt_box1.configure(background="white")
    display.configure(background="#FAF0E6")

def translate():
    read = txt_box.get(0.0, END)
    translator= Translator(from_lang="English", to_lang="Russian")
    translation = translator.translate(read)
    txt_box1.insert(0.0, translation)

def translate_1():
    read = txt_box.get(0.0, END)
    translator= Translator(from_lang="Russian", to_lang="English")
    translation = translator.translate(read)
    txt_box1.insert(0.0, translation)

def weather():
    owm = OWM('fd3ea34bb5eb7ae4faae0c8095446b88')
    mgr = owm.weather_manager()

    check = True
    quetion = ent.get()
    try:
        observation = mgr.weather_at_place(quetion)
        w = observation.weather
    except:
        lbl.configure(text="Error during writing.", font="Arial 20", fg="red")
        check = False

    if check == False:
        pass
    else:
        status = w.detailed_status
        wind = w.wind()['speed']
        humid = w.humidity
        temp = w.temperature('celsius')['temp']

        lbl.configure(text=f"Status: {status}.\nSpeed of wind: {wind} m/s.\nHumidity: {humid}%.\nTemprerature: {int(temp)}℃.", justify=LEFT, font="Arial 20", fg="GREEN")

balls_for_bot = 0
balls_for_player = 0
carts = ["шестерка", "семерка", "восьмерка", "девятка", "десятка", "валет", "дама", "король", "туз"] * 4
balls = [6, 7, 8, 9, 10, 2, 3, 4, 11] * 4

def begin():
    global balls_for_bot, balls_for_player, lbl_for_game
    #Раздаём две карты боту
    random_for_bot1 = random.choice(carts)
    index_bot1 = carts.index(random_for_bot1)
    balls_for_bot += balls[index_bot1]
    #Раздаём две карты игроку
    random_for_game1 = random.choice(carts)
    index_ball1 = carts.index(random_for_game1)
    balls_for_player += balls[index_ball1]

    lbl_for_game.configure(text=f"""
    Боту выдали карту {random_for_bot1} с достоинством {balls[index_bot1]}.
    Вам выдали карту {random_for_game1} с достоинством {balls[index_ball1]}.
    У бота очков {balls_for_bot}.
    У вас очков {balls_for_player}.""")

    carts.remove(random_for_bot1)
    balls.pop(index_bot1)
    carts.remove(random_for_game1)
    balls.pop(index_ball1)
    btn2.grid_remove()

    def bot(carts, balls):
        global balls_for_bot, balls_for_player, lbl_for_game       
        random_for_One = random.choice(carts)
        index_bot = carts.index(random_for_One)
        balls_for_bot += balls[index_bot]
        if balls_for_bot > 21:
            lbl_for_game.configure(text=f"""
            Боту выпала карта {random_for_One} с достоинством {balls[index_bot]}.
            У бота очков {balls_for_bot}.
            У вас очков {balls_for_player}.
            Вы выйграли, бот проиграл.""")
            btn.grid_remove()
            btn1.grid_remove()
            btn2.grid(row=1, column=0)
            balls_for_bot = 0
            balls_for_player = 0
        else:
            lbl_for_game.configure(text=f"""
            Боту выпала карта {random_for_One} с достоинством {balls[index_bot]}.
            У бота очков {balls_for_bot}.
            У вас очков {balls_for_player}.""")
            carts.remove(random_for_One)
            balls.pop(index_bot)

    def game():
        global balls_for_bot, balls_for_player, lbl_for_game
        random_for_game = random.choice(carts)
        index_ball = carts.index(random_for_game)
        balls_for_player += balls[index_ball]
        if balls_for_player > 21:
            lbl_for_game.configure(text=f"""Вам выпала карта {random_for_game} с достоинством {balls[index_ball]}.
            У бота очков {balls_for_bot}.
            У вас очков {balls_for_player}.
            Вы проиграли, бот выйграл.""")
            btn.grid_remove()
            btn1.grid_remove()
            btn2.grid(row=1, column=0)
            balls_for_bot = 0
            balls_for_player = 0
        else:
            lbl_for_game.configure(text=f"""Вам выпала карта {random_for_game} с достоинством {balls[index_ball]}.
            У бота очков {balls_for_bot}.
            У вас очков {balls_for_player}.""")
            if balls_for_bot >= 18:
                random_BOT = random.randint(1,100)
                if random_BOT < 60:
                    bot(carts, balls)
                else:
                    lbl_for_game.configure(text=f"""Бот не берёт карту.
                    У бота очков {balls_for_bot}.
                    У вас очков {balls_for_player}.""")
            else:
                bot(carts, balls)
        carts.remove(random_for_game)
        balls.pop(index_ball)

        if balls_for_player > 21 and balls_for_bot > 21:
            lbl_for_game.configure(text="Ничья.")
            btn.grid_remove()
            btn1.grid_remove()
            btn2.grid(row=1, column=0)
            balls_for_bot = 0
            balls_for_player = 0
        if balls_for_player == 21:
            lbl_for_game.configure(text="У вас блэк джек, вы победили!")
            btn.grid_remove()
            btn1.grid_remove()
            btn2.grid(row=1, column=0)
            balls_for_bot = 0
            balls_for_player = 0

        elif balls_for_bot == 21:
            lbl_for_game.configure(text="У бота блэк джек, вы проиграли!")
            btn.grid_remove()
            btn1.grid_remove()
            btn2.grid(row=1, column=0)
            balls_for_bot = 0
            balls_for_player = 0

    def notTake():
        bot(carts, balls)
    
    btn = Button(tab3, width=13, height=3, bd=5, text="Take a card", command=game)
    btn1 = Button(tab3, width=13, height=3, bd=5, text="Don't take a card", command=notTake)
    btn1.grid(row=2, column=0)
    btn.grid(row=1, column=0)


display = Tk()
display.geometry("700x350")
display.title("Programm V-(beta).")

vid = ttk.Notebook(display)
list_for_actions = ["Translator","Weather","Game"]

tab1 = Frame(vid)
tab2 = Frame(vid)
tab3 = Frame(vid)
vid.add(tab1, text=list_for_actions[0])
vid.add(tab2, text=list_for_actions[1])
vid.add(tab3, text=list_for_actions[2])
vid.pack()
vid.pack(fill="both")

tab1.configure(background="#FAF0E6")
tab2.configure(background="#FAF0E6")
tab3.configure(background="#FAF0E6")
display.configure(background="#FAF0E6")

menu = Menu(display)
display.config(menu=menu)
m1 = Menu(menu, tearoff=0)
menu.add_cascade(label="Theme", menu=m1)
m1.add_command(label="Dark", command=theme)
m1.add_separator()
m1.add_command(label="Light", command=theme1)

button = Button(tab1, text="English/Russian", command=translate)
button.grid(row=0, column=0)
button_1 = Button(tab1, text="Russian/English", command=translate_1)
button_1.grid(row=0, column=1)

txt_box = scrolledtext.ScrolledText(tab1, width=40, height=5)
txt_box.grid(row=1, column=0, columnspan=3)
txt_box1 = scrolledtext.ScrolledText(tab1, width=40, height=5)
txt_box1.grid(row=1, column=3, columnspan=3)

ent = Entry(tab2, width=15, font="Arial 25", bd=5, justify=CENTER, bg="CYAN")
button = Button(tab2, width=7, bd=5, text="Press", command=weather, font="Arial 15")
lbl = Label(tab2, width=70, height=5, bg="LightBlue")

ent.pack()
button.pack()
lbl.pack()

btn2 = Button(tab3,  width=13, height=3, bd=5, text="Start the game", command=begin)

lbl_for_game = Label(tab3, width=80, height=15, bd=5, bg="LightBlue")
lbl_for_game.grid(row=0, column=4, rowspan=3)
btn2.grid(row=1, column=0)
display.mainloop()