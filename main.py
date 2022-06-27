import time
import tkinter as tk
import os
import yaml
import customtkinter
from tkinter import *
from tkinter import Tk
from config import Config
import tkinter.font as font
from threading import Thread
from mcrcon import MCRcon as r
from tkinter.filedialog import askopenfilename

config = Config(os.path.join('.', 'config.yaml'))
settings = config.get_config('settings_server')

fileplace = settings['fileplace']
maxmemory = settings['maxmemory']
minmemory = settings['minmemory']
server_ip = settings['server_ip']
server_port = settings['server_port']
rcon_ip = settings['rcon_ip']
rcon_password = settings['rcon_password']

server_status_online = False
statustext = ""
statuscolor = ""
print_text = False

window = tk.Tk()
window.title("Minecraft Server Control Panel")
window.geometry('700x400')

window.image = PhotoImage(file='assets_py/background.png')
bg_logo = Label(window, image=window.image)
bg_logo.grid(row=0, column=0)

commandline = Listbox(window, width=62, fg='white', bd=0, height=16, bg='#222831')
commandline.place(x=125, y=70)

fileentey = customtkinter.CTkEntry(window, width=500, height=28, bg_color='#393E46', fg_color='#222831',
                                   text_color='white', placeholder_text="Please, select a server.jar file")
fileentey.place(x=125, y=12)
fileentey.insert(0, fileplace)

commandentey = customtkinter.CTkEntry(window, width=500, height=28, bg_color='#393E46', fg_color='#222831',
                                      text_color='white')
commandentey.place(x=125, y=360)

serverlable = customtkinter.CTkLabel(window, width=40, height=20, bg_color='#393E46', text='Server status:',
                                     text_color='white')
serverlable.place(x=210, y=43)

infolable = customtkinter.CTkLabel(window, width=40, height=20, bg_color='#393E46', text='',)
infolable.place(x=310, y=43)

playerlable = customtkinter.CTkLabel(window, width=40, height=20, bg_color='#393E46', text='Players online:',
                                     text_color='white')
playerlable.place(x=410, y=43)

infoplayerlable = customtkinter.CTkLabel(window, width=40, height=20, bg_color='#393E46', text='')
infoplayerlable.place(x=520, y=43)

menubar = Menu(window, bg="#393E46", foreground='white')
window.config(menu=menubar)

main_menu = Menu(menubar)


def status():
    output = os.popen('screen -ls').read()
    if '.minecraft' in output:
        return True
    else:
        return False


def statusserver():
    global print_text

    server_status = Config(os.path.join('.', 'server_status.yaml'))
    properties = server_status.get_config('server_status')
    server_status_online = properties['online']

    if not status() and server_status_online == False:
        infolable.config(text='Stopped', fg='red')
        infoplayerlable.config(text='0/0', fg='red')
        if print_text == True:
            commandline.insert(END, '  Server stopped')
            print_text = False
    if status() and server_status_online == False:
        infolable.config(text='Starting', fg='yellow')
        infoplayerlable.config(text='0/0', fg='red')
        commandline.insert(END, '  Server Starting, please wait')
        print_text = True
    if status() and server_status_online == True:
        infolable.config(text='Started', fg='green')
        players_online_now = properties['players_online_now']
        players_online_max = properties['players_online_max']
        infoplayerlable.config(text=f'{players_online_now}/{players_online_max}', fg='green')
        if print_text == True:
            commandline.insert(END, '  Server started')
            print_text = False
    if not status() and server_status_online == True:
        infolable.config(text='Stopping', fg='yellow')
        infoplayerlable.config(text='0/0', fg='red')
        commandline.insert(END, '  Server Stopping, please wait')
        print_text = True


def Thread_Status():
    while True == True:
        statusserver()
        time.sleep(10)


th = Thread(target=Thread_Status)
th.daemon = True
th.start()


def fileplacedef():
    global fileplace
    Tk().withdraw()
    filename = askopenfilename()
    fileplace = filename
    fileentey.delete(0, 'end')
    fileentey.insert(0, filename)
    with open(os.path.join('.', 'config.yaml'), 'w+') as file:
        documents = yaml.dump({"settings_server": {
            "fileplace": f"{filename}",
            "maxmemory": f"{maxmemory}",
            "minmemory": f"{minmemory}",
            "server_ip": f"{server_ip}",
            "server_port": f"{server_port}",
            "rcon_ip": f"{rcon_ip}",
            "rcon_password": f"{rcon_password}"}}, file)


def runcommand():
    with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
        command = mcr.command(f'{commandentey.get()}')
    commandline.insert(END, f'  {command}')
    commandentey.delete(0, 'end')


def runcommand_event(event):
    with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
        command = mcr.command(f'{commandentey.get()}')
    commandline.insert(END, f'  {command}')
    commandentey.delete(0, 'end')


window.bind('<Return>', runcommand_event)


def Status_Thread():
    exec(open("server_online.py").read())


th1 = Thread(target=Status_Thread)
th1.daemon = True
th1.start()


def start():
    if not status():
        os.system(f'screen -dmS "minecraft" java -Xmx{maxmemory}M -Xms{minmemory}M -jar {fileplace}')
    else:
        commandline.insert(END, "  Server already started")


def stop():
    if status():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('stop')
    else:
        commandline.insert(END, "  Server Stopped")


def openSettings():
    config = Config(os.path.join('.', 'config.yaml'))
    settings = config.get_config('settings_server')

    global fileplace
    global maxmemory
    global minmemory
    global server_ip
    global server_port
    global rcon_ip
    global rcon_password

    fileplace = settings['fileplace']
    maxmemory = settings['maxmemory']
    minmemory = settings['minmemory']
    server_ip = settings['server_ip']
    server_port = settings['server_port']
    rcon_ip = settings['rcon_ip']
    rcon_password = settings['rcon_password']

    settings = tk.Tk()
    settings.title("Settings")
    settings.geometry("380x400")
    settings.config(bg='#393E46')

    server_ip_lable = customtkinter.CTkLabel(settings, width=40, height=28, bg_color='#393E46', text='Server ip',
                                         text_color='white')
    server_ip_lable.place(x=10, y=8)

    server_port_lable = customtkinter.CTkLabel(settings, width=40, height=28, bg_color='#393E46', text='Server port',
                                         text_color='white')
    server_port_lable.place(x=10, y=48)

    maxmemlable = customtkinter.CTkLabel(settings, width=40, height=28, bg_color='#393E46', text='Max memory',
                                         text_color='white')
    maxmemlable.place(x=10, y=88)

    minmemlable = customtkinter.CTkLabel(settings, width=40, height=28, bg_color='#393E46', text='Min memory',
                                         text_color='white')
    minmemlable.place(x=10, y=128)

    rcon_ip_lable = customtkinter.CTkLabel(settings, width=40, height=28, bg_color='#393E46', text='Rcon ip',
                                         text_color='white')
    rcon_ip_lable.place(x=10, y=168)

    rcon_password_lable = customtkinter.CTkLabel(settings, width=40, height=28, bg_color='#393E46', text='Rcon password',
                                         text_color='white')
    rcon_password_lable.place(x=10, y=208)

    server_ip_entry = customtkinter.CTkEntry(settings, width=250, height=28, bg_color='#393E46', fg_color='#222831',
                                       text_color='white')
    server_ip_entry.place(x=120, y=8)
    server_ip_entry.insert(0, server_ip)

    server_port_entry = customtkinter.CTkEntry(settings, width=250, height=28, bg_color='#393E46', fg_color='#222831',
                                       text_color='white')
    server_port_entry.place(x=120, y=48)
    server_port_entry.insert(0, server_port)

    maxmementry = customtkinter.CTkEntry(settings, width=250, height=28, bg_color='#393E46', fg_color='#222831',
                                       text_color='white')
    maxmementry.place(x=120, y=88)
    maxmementry.insert(0, maxmemory)

    minmementry = customtkinter.CTkEntry(settings, width=250, height=28, bg_color='#393E46', fg_color='#222831',
                                         text_color='white')
    minmementry.place(x=120, y=128)
    minmementry.insert(0, minmemory)

    rcon_ip_entry = customtkinter.CTkEntry(settings, width=250, height=28, bg_color='#393E46', fg_color='#222831',
                                         text_color='white')
    rcon_ip_entry.place(x=120, y=168)
    rcon_ip_entry.insert(0, rcon_ip)

    rcon_password_entry = customtkinter.CTkEntry(settings, width=250, height=28, bg_color='#393E46', fg_color='#222831',
                                         text_color='white')
    rcon_password_entry.place(x=120, y=208)
    rcon_password_entry.insert(0, rcon_password)

    def save():
        global fileplace
        global maxmemory
        global minmemory
        global server_ip
        global server_port
        global rcon_ip
        global rcon_password

        max = maxmementry.get()
        min = minmementry.get()
        ip_server = server_ip_entry.get()
        port = server_port_entry.get()
        ip_rcon = rcon_ip_entry.get()
        password = rcon_password_entry.get()


        fileplace = fileplace
        maxmemory = max
        minmemory = min

        with open(os.path.join('.', 'config.yaml'), 'w+') as file:
            documents = yaml.dump({"settings_server": {
                "fileplace": f"{fileplace}",
                "maxmemory": f"{max}",
                "minmemory": f"{min}",
                "server_ip": f"{ip_server}",
                "server_port": f"{port}",
                "rcon_ip": f"{ip_rcon}",
                "rcon_password": f"{password}"}}, file)
        settings.destroy()

    def default():
        server_ip_entry.delete(0, 'end')
        server_port_entry.delete(0, 'end')
        maxmementry.delete(0, 'end')
        minmementry.delete(0, 'end')
        rcon_password_entry.delete(0, 'end')
        rcon_ip_entry.delete(0, 'end')
        server_ip_entry.insert(0, '')
        server_port_entry.insert(0, 25565)
        maxmementry.insert(0, 2048)
        minmementry.insert(0, 1024)
        rcon_password_entry.insert(0, '')
        rcon_ip_entry.insert(0, '0.0.0.0')

    ok = customtkinter.CTkButton(settings, text="Save", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                       width=80, height=26, command=save)
    ok.place(x=285, y=360)

    cancel = customtkinter.CTkButton(settings, text="Cancel", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                       width=80, height=26, command=settings.destroy)
    cancel.place(x=190, y=360)

    default = customtkinter.CTkButton(settings, text="Default", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                       width=80, height=26, command=default)
    default.place(x=14, y=360)

    settings.resizable(width=False, height=False)
    settings.mainloop()


def settime():
    time = tk.Tk()
    time.title("Time")
    time.geometry("140x182")
    time.config(bg='#393E46')

    def day():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set day')
        commandline.insert(END, f'  {command}')
        time.destroy()

    def midnight():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set midnight')
        commandline.insert(END, f'  {command}')
        time.destroy()

    def night():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set night')
        commandline.insert(END, f'  {command}')
        time.destroy()

    def noon():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set noon')
        commandline.insert(END, f'  {command}')
        time.destroy()

    setday = customtkinter.CTkButton(time, text="Day", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                     width=110, height=28, command=day)
    setday.place(x=14, y=14)

    setmidnight = customtkinter.CTkButton(time, text="Midnight", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                          width=110, height=28, command=midnight)
    setmidnight.place(x=14, y=140)

    setnight = customtkinter.CTkButton(time, text="Night", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                       width=110, height=28, command=night)
    setnight.place(x=14, y=98)

    setnoon = customtkinter.CTkButton(time, text="Noon", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                      width=110, height=28, command=noon)
    setnoon.place(x=14, y=56)

    time.mainloop()


def setweather():
    weather = tk.Tk()
    weather.title("Weather")
    weather.geometry("140x140")
    weather.config(bg='#393E46')

    def clear():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('weather clear')
        commandline.insert(END, f'  {command}')
        weather.destroy()

    def rain():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('weather rain')
        commandline.insert(END, f'  {command}')
        weather.destroy()

    def thunder():
        with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('weather thunder')
        commandline.insert(END, f'  {command}')
        weather.destroy()

    setclear = customtkinter.CTkButton(weather, text="Clear", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                       width=110, height=28, command=clear)
    setclear.place(x=14, y=14)

    setrain = customtkinter.CTkButton(weather, text="Rain", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                      width=110, height=28, command=rain)
    setrain.place(x=14, y=56)

    setthunder = customtkinter.CTkButton(weather, text="Thunder", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                                         width=110, height=28, command=thunder)
    setthunder.place(x=14, y=98)

    weather.mainloop()


def player_list_def():
    player_list_window = tk.Tk()
    player_list_window.title("Players")
    player_list_window.geometry("250x60")
    player_list_window.config(bg='#393E46')

    server_status = Config(os.path.join('.', 'server_status.yaml'))
    properties = server_status.get_config('server_status')
    player_list = properties['players_online_list']

    list = ['']
    list[0] = "Select a player:"
    player_name = ''

    for element in player_list:
        list.append(element)

    def player_select(choice):
        if choice == "Select a player:":
            player_list_window.geometry("250x60")
        else:
            global player_name
            player_name = choice
            player_selected()

    def player_selected():
        global player_name
        print("optionmenu dropdown clicked:", player_name)
        player_list_window.geometry("250x240")
        def gamemode():
            gamemode = tk.Tk()
            gamemode.title('Gamemode')
            gamemode.geometry("250x195")
            gamemode.config(bg='#393E46')

            def adventure():
                with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode adventure {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode.destroy()

            def creative():
                with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode creative {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode.destroy()

            def spectrator():
                with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode spectrator {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode.destroy()

            def survival():
                with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode survival {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode.destroy()

            creative = customtkinter.CTkButton(gamemode, text="Creative", text_color='black',
                                               bg_color='#393E46',
                                               fg_color='#EEEEEE',
                                               width=210, height=30, command=creative)
            creative.place(x=20, y=15)

            survival = customtkinter.CTkButton(gamemode, text="Survival", text_color='black',
                                               bg_color='#393E46',
                                               fg_color='#EEEEEE',
                                               width=210, height=30, command=survival)
            survival.place(x=20, y=60)

            adventure = customtkinter.CTkButton(gamemode, text="Adventure", text_color='black',
                                               bg_color='#393E46',
                                               fg_color='#EEEEEE',
                                               width=210, height=30, command=adventure)
            adventure.place(x=20, y=105)

            spectrator = customtkinter.CTkButton(gamemode, text="Spectrator", text_color='black',
                                               bg_color='#393E46',
                                               fg_color='#EEEEEE',
                                               width=210, height=30, command=spectrator)
            spectrator.place(x=20, y=150)

        def operator():
            with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                command = mcr.command(f'op {player_name}')
            if command == "Nothing changed. The player already is an operator":
                operator_info = tk.Tk()
                operator_info.title('Operetor')
                operator_info.geometry("250x168")
                operator_info.config(bg='#393E46')

                def answer_yes():
                    with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                        command = mcr.command(f'deop {player_name}')
                    commandline.insert(END, f'  {command}')
                    operator_info.destroy()

                def answer_no():
                    operator_info.destroy()

                lable1 = customtkinter.CTkLabel(operator_info, width=200, height=40, bg_color='#393E46',
                                                text=f'{player_name} already\nis an operator',
                                                text_color='white')
                lable1.place(x=25, y=10)

                lable2 = customtkinter.CTkLabel(operator_info, width=200, height=40, bg_color='#393E46',
                                                text=f'Revokes operator\nstatus from {player_name}?',
                                                text_color='white')
                lable2.place(x=25, y=60)

                yes = customtkinter.CTkButton(operator_info, text="Yes", text_color='black', bg_color='#393E46',
                                              fg_color='#EEEEEE',
                                              width=50, height=28, command=answer_yes)
                yes.place(x=180, y=120)

                no = customtkinter.CTkButton(operator_info, text="No", text_color='black', bg_color='#393E46',
                                              fg_color='#EEEEEE',
                                              width=50, height=28, command=answer_no)
                no.place(x=20, y=120)

            else:
                commandline.insert(END, f'  {command}')

        def ban():
            with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                command = mcr.command(f'ban {player_name}')
            commandline.insert(END, f'  {command}')

        def kill():
            with r(f'{rcon_ip}', f'{rcon_password}') as mcr:
                command = mcr.command(f'kill {player_name}')
            commandline.insert(END, f'  {command}')

        gamemode = customtkinter.CTkButton(player_list_window, text="Gamemode", text_color='black', bg_color='#393E46',
                                           fg_color='#EEEEEE',
                                           width=210, height=30, command=gamemode)
        gamemode.place(x=20, y=60)

        operator = customtkinter.CTkButton(player_list_window, text="Operator", text_color='black', bg_color='#393E46',
                                           fg_color='#EEEEEE',
                                           width=210, height=30, command=operator)
        operator.place(x=20, y=105)

        ban = customtkinter.CTkButton(player_list_window, text="Ban", text_color='black', bg_color='#393E46',
                                           fg_color='#EEEEEE',
                                           width=210, height=30, command=ban)
        ban.place(x=20, y=150)

        kill = customtkinter.CTkButton(player_list_window, text="Kill", text_color='black', bg_color='#393E46',
                                           fg_color='#EEEEEE',
                                           width=210, height=30, command=kill)
        kill.place(x=20, y=195)

    combobox = customtkinter.CTkOptionMenu(player_list_window,
                                           width=210,
                                           height=30,
                                           values=list,
                                           fg_color="#222831",
                                           text_color="white",
                                           command=player_select)
    combobox.place(x=20, y=15)


main_menu.add_command(
    label='Settings',
    command=openSettings,
)

main_menu.add_command(
    label='Exit',
    command=window.destroy,
)

menubar.add_cascade(
    label="Main",
    menu=main_menu,
    underline=0
)

myFont = font.Font(size=12)

start = customtkinter.CTkButton(window, text="Start", text_color='black', bg_color='#00ADB5', fg_color='#EEEEEE',
                                width=88, height=38, command=start)
start.place(x=12, y=12)

stop = customtkinter.CTkButton(window, text="Stop", text_color='black', bg_color='#00ADB5', fg_color='#EEEEEE',
                               width=88, height=38, command=stop)
stop.place(x=12, y=62)

timeset = customtkinter.CTkButton(window, text="Time", text_color='black', bg_color='#00ADB5', fg_color='#EEEEEE',
                                  width=88, height=38, command=settime)
timeset.place(x=12, y=250)

weatherset = customtkinter.CTkButton(window, text="Weather", text_color='black', bg_color='#00ADB5', fg_color='#EEEEEE',
                                     width=88, height=38, command=setweather)
weatherset.place(x=12, y=300)

playerlist = customtkinter.CTkButton(window, text="Players", text_color='black', bg_color='#00ADB5', fg_color='#EEEEEE',
                                     width=88, height=38, command=player_list_def)
playerlist.place(x=12, y=350)

file = customtkinter.CTkButton(window, text="File", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                               width=50, height=28, command=fileplacedef)
file.place(x=635, y=12)

run = customtkinter.CTkButton(window, text="Run", text_color='black', bg_color='#393E46', fg_color='#EEEEEE',
                              width=50, height=28, command=runcommand)
run.place(x=635, y=358)

window.resizable(width=False, height=False)
window.mainloop()
