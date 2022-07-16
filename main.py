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
settings_cfg = config.get_config('settings_server')

statistics_config = Config(os.path.join('.', 'plugins/Control-Panel-Addition/config.yml'))

fileplace = settings_cfg['fileplace']
maxmemory = settings_cfg['maxmemory']
minmemory = settings_cfg['minmemory']
server_ip = settings_cfg['server_ip']
server_port = settings_cfg['server_port']
rcon_port = settings_cfg['rcon_port']
rcon_password = settings_cfg['rcon_password']
player_name = ''
server_status_online = False
statustext = ""
statuscolor = ""
print_text = False
java_restart = False

window = tk.Tk()
window.title("Minecraft Server Control Panel")
window.geometry('700x400')
main_icon = PhotoImage(file="assets_py/main_icon.png")
window.iconphoto(False, main_icon)

window.image = PhotoImage(file='assets_py/background.png')
bg_logo = Label(window, image=window.image)
bg_logo.grid(row=0, column=0)

commandline = Listbox(window,
                      width=62,
                      fg='white',
                      bd=0,
                      height=16,
                      bg='#222831')
commandline.place(x=125, y=70)

fileentey = customtkinter.CTkEntry(window,
                                   width=500,
                                   height=28,
                                   bg_color='#393E46',
                                   fg_color='#222831',
                                   text_color='white',
                                   placeholder_text="Please, select a server.jar file")
fileentey.place(x=125, y=12)
fileentey.insert(0, fileplace)

commandentey = customtkinter.CTkEntry(window, width=500,
                                      height=28,
                                      bg_color='#393E46',
                                      fg_color='#222831',
                                      text_color='white')
commandentey.place(x=125, y=360)

serverlable = customtkinter.CTkLabel(window,
                                     width=40,
                                     height=20,
                                     bg_color='#393E46',
                                     text='Server status:',
                                     text_color='white')
serverlable.place(x=210, y=43)

infolable = customtkinter.CTkLabel(window,
                                   width=40,
                                   height=20,
                                   bg_color='#393E46',
                                   text='', )
infolable.place(x=310, y=43)

playerlable = customtkinter.CTkLabel(window,
                                     width=40,
                                     height=20,
                                     bg_color='#393E46',
                                     text='Players online:',
                                     text_color='white')
playerlable.place(x=410, y=43)

infoplayerlable = customtkinter.CTkLabel(window,
                                         width=40,
                                         height=20,
                                         bg_color='#393E46',
                                         text='')
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

    server_status1 = Config(os.path.join('.', 'server_status.yaml'))
    properties = server_status1.get_config('server_status')
    server_status_online_prop = properties['online']

    if not status() and server_status_online_prop == False:
        infolable.config(text='Stopped', fg='red')
        infoplayerlable.config(text='0/0', fg='red')
        if print_text:
            commandline.insert(END, '  Server stopped')
            print_text = False
    if status() and server_status_online_prop == False:
        infolable.config(text='Starting', fg='yellow')
        infoplayerlable.config(text='0/0', fg='red')
        commandline.insert(END, '  Server Starting, please wait')
        print_text = True
    if status() and server_status_online_prop == True:
        infolable.config(text='Started', fg='green')
        players_online_now = properties['players_online_now']
        players_online_max = properties['players_online_max']
        infoplayerlable.config(text=f'{players_online_now}/{players_online_max}', fg='green')
        if print_text:
            commandline.insert(END, '  Server started')
            print_text = False
    if not status() and server_status_online_prop == True:
        infolable.config(text='Stopping', fg='yellow')
        infoplayerlable.config(text='0/0', fg='red')
        commandline.insert(END, '  Server Stopping, please wait')
        print_text = True


def Thread_Status():
    while True:
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
    with open(os.path.join('.', 'config.yaml'), 'w+') as file_1:
        yaml.dump({"settings_server": {
            "fileplace": f"{filename}",
            "maxmemory": f"{maxmemory}",
            "minmemory": f"{minmemory}",
            "server_ip": f"{server_ip}",
            "server_port": f"{server_port}",
            "rcon_port": f"{rcon_port}",
            "rcon_password": f"{rcon_password}"}}, file_1)


def runcommand():
    with r(f'{server_ip}', f'{rcon_password}') as mcr:
        command = mcr.command(f'{commandentey.get()}')
    commandline.insert(END, f'  {command}')
    commandentey.delete(0, 'end')


def runcommand_event(event):
    with r(f'{server_ip}', f'{rcon_password}') as mcr:
        command = mcr.command(f'{commandentey.get()}')
    commandline.insert(END, f'  {command}')
    commandentey.delete(0, 'end')


window.bind('<Return>', runcommand_event)


def Status_Thread():
    exec(open("server_online.py").read())


th1 = Thread(target=Status_Thread)
th1.daemon = True
th1.start()

def info():
    info_window = tk.Toplevel()
    info_window.title("About Control-Panel")
    info_window.geometry("320x160")
    info_window.config(bg='#393E46')

    program_image = PhotoImage(file='assets_py/program_icon.png')
    button = customtkinter.CTkButton(info_window,
                                     width=15,
                                     height=15,
                                     text='',
                                     fg_color='#393E46',
                                     border_color='#393E46',
                                     image=program_image)
    button.place(x=135, y=15)

    program_name = customtkinter.CTkLabel(info_window,
                                          width=260,
                                          height=20,
                                          bg_color='#393E46',
                                          text='Server-Control_Panel')
    program_name.place(x=30, y=75)

    program_type = customtkinter.CTkLabel(info_window,
                                          width=260,
                                          height=20,
                                          bg_color='#393E46',
                                          text='(With plugin Bukkit/Spigot 1.19)')
    program_type.place(x=30, y=100)

    program_version = customtkinter.CTkLabel(info_window,
                                             width=260,
                                             height=20,
                                             bg_color='#393E46',
                                             text='Version (1.0)')
    program_version.place(x=30, y=125)



def start():
    if not status():
        os.system(f'screen -dmS "minecraft" java -Xmx{maxmemory}M -Xms{minmemory}M -jar {fileplace}')
    else:
        commandline.insert(END, "  Server already started")


def stop():
    if status():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            mcr.command('stop')
    else:
        commandline.insert(END, "  Server Stopped")


def restart_java():
    global java_restart

    if status():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            mcr.command('stop')

        while not java_restart:
            if status():
                java_restart = False
                print(1)
                time.sleep(1)
            else:
                os.system(f'screen -dmS "minecraft" java -Xmx{maxmemory}M -Xms{minmemory}M -jar {fileplace}')
                java_restart = True
                print(2)
                time.sleep(1)
        java_restart = False

    else:
        commandline.insert(END, "  Server Stopped")

def openSettings():
    config_1 = Config(os.path.join('.', 'config.yaml'))
    settings_cfg_1 = config_1.get_config('settings_server')

    global fileplace
    global maxmemory
    global minmemory
    global server_ip
    global server_port
    global rcon_port
    global rcon_password

    fileplace = settings_cfg_1['fileplace']
    maxmemory = settings_cfg_1['maxmemory']
    minmemory = settings_cfg_1['minmemory']
    server_ip = settings_cfg_1['server_ip']
    server_port = settings_cfg_1['server_port']
    rcon_port = settings_cfg_1['rcon_port']
    rcon_password = settings_cfg_1['rcon_password']

    settings = tk.Tk()
    settings.title("Settings")
    settings.geometry("380x400")
    settings.config(bg='#393E46')

    server_ip_lable = customtkinter.CTkLabel(settings,
                                             width=40,
                                             height=28,
                                             bg_color='#393E46',
                                             text='Server ip',
                                             text_color='white')
    server_ip_lable.place(x=10, y=8)

    server_port_lable = customtkinter.CTkLabel(settings,
                                               width=40,
                                               height=28,
                                               bg_color='#393E46',
                                               text='Server port',
                                               text_color='white')
    server_port_lable.place(x=10, y=48)

    maxmemlable = customtkinter.CTkLabel(settings,
                                         width=40,
                                         height=28,
                                         bg_color='#393E46',
                                         text='Max memory',
                                         text_color='white')
    maxmemlable.place(x=10, y=88)

    minmemlable = customtkinter.CTkLabel(settings,
                                         width=40,
                                         height=28,
                                         bg_color='#393E46',
                                         text='Min memory',
                                         text_color='white')
    minmemlable.place(x=10, y=128)

    rcon_port_lable = customtkinter.CTkLabel(settings,
                                             width=40,
                                             height=28,
                                             bg_color='#393E46',
                                             text='Rcon port',
                                             text_color='white')
    rcon_port_lable.place(x=10, y=168)

    rcon_password_lable = customtkinter.CTkLabel(settings,
                                                 width=40,
                                                 height=28,
                                                 bg_color='#393E46',
                                                 text='Rcon password',
                                                 text_color='white')
    rcon_password_lable.place(x=10, y=208)

    server_ip_entry = customtkinter.CTkEntry(settings,
                                             width=250,
                                             height=28,
                                             bg_color='#393E46',
                                             fg_color='#222831',
                                             text_color='white')
    server_ip_entry.place(x=120, y=8)
    server_ip_entry.insert(0, server_ip)

    server_port_entry = customtkinter.CTkEntry(settings,
                                               width=250,
                                               height=28,
                                               bg_color='#393E46',
                                               fg_color='#222831',
                                               text_color='white')
    server_port_entry.place(x=120, y=48)
    server_port_entry.insert(0, server_port)

    maxmementry = customtkinter.CTkEntry(settings,
                                         width=250,
                                         height=28,
                                         bg_color='#393E46',
                                         fg_color='#222831',
                                         text_color='white')
    maxmementry.place(x=120, y=88)
    maxmementry.insert(0, maxmemory)

    minmementry = customtkinter.CTkEntry(settings,
                                         width=250,
                                         height=28,
                                         bg_color='#393E46',
                                         fg_color='#222831',
                                         text_color='white')
    minmementry.place(x=120, y=128)
    minmementry.insert(0, minmemory)

    rcon_port_entry = customtkinter.CTkEntry(settings,
                                             width=250,
                                             height=28,
                                             bg_color='#393E46',
                                             fg_color='#222831',
                                             text_color='white')
    rcon_port_entry.place(x=120, y=168)
    rcon_port_entry.insert(0, rcon_port)

    rcon_password_entry = customtkinter.CTkEntry(settings,
                                                 width=250,
                                                 height=28,
                                                 bg_color='#393E46',
                                                 fg_color='#222831',
                                                 text_color='white')
    rcon_password_entry.place(x=120, y=208)
    rcon_password_entry.insert(0, rcon_password)

    def save():
        global fileplace
        global maxmemory
        global minmemory
        global server_ip
        global server_port
        global rcon_port
        global rcon_password

        max = maxmementry.get()
        min = minmementry.get()
        ip_server = server_ip_entry.get()
        port = server_port_entry.get()
        port_rcon = rcon_port_entry.get()
        password = rcon_password_entry.get()

        maxmemory = max
        minmemory = min

        with open(os.path.join('.', 'config.yaml'), 'w+') as file_2:
            yaml.dump({"settings_server": {
                "fileplace": f"{fileplace}",
                "maxmemory": f"{max}",
                "minmemory": f"{min}",
                "server_ip": f"{ip_server}",
                "server_port": f"{port}",
                "rcon_port": f"{port_rcon}",
                "rcon_password": f"{password}"}}, file_2)
        settings.destroy()

    def default():
        server_ip_entry.delete(0, 'end')
        server_port_entry.delete(0, 'end')
        maxmementry.delete(0, 'end')
        minmementry.delete(0, 'end')
        rcon_password_entry.delete(0, 'end')
        rcon_port_entry.delete(0, 'end')
        server_ip_entry.insert(0, '')
        server_port_entry.insert(0, 25565)
        maxmementry.insert(0, 2048)
        minmementry.insert(0, 1024)
        rcon_password_entry.insert(0, '')
        rcon_port_entry.insert(0, '25575')

    ok = customtkinter.CTkButton(settings,
                                 text="Save",
                                 text_color='black',
                                 bg_color='#393E46',
                                 fg_color='#EEEEEE',
                                 width=80,
                                 height=26,
                                 command=save)
    ok.place(x=285, y=360)

    cancel = customtkinter.CTkButton(settings,
                                     text="Cancel",
                                     text_color='black',
                                     bg_color='#393E46',
                                     fg_color='#EEEEEE',
                                     width=80,
                                     height=26,
                                     command=settings.destroy)
    cancel.place(x=190, y=360)

    default = customtkinter.CTkButton(settings,
                                      text="Default",
                                      text_color='black',
                                      bg_color='#393E46',
                                      fg_color='#EEEEEE',
                                      width=80,
                                      height=26,
                                      command=default)
    default.place(x=14, y=360)

    settings.resizable(width=False, height=False)
    settings.mainloop()


def settime():
    time_window = tk.Tk()
    time_window.title("Time")
    time_window.geometry("140x182")
    time_window.config(bg='#393E46')

    def day():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set day')
        commandline.insert(END, f'  {command}')
        time_window.destroy()

    def midnight():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set midnight')
        commandline.insert(END, f'  {command}')
        time_window.destroy()

    def night():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set night')
        commandline.insert(END, f'  {command}')
        time_window.destroy()

    def noon():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('time set noon')
        commandline.insert(END, f'  {command}')
        time_window.destroy()

    setday = customtkinter.CTkButton(time_window,
                                     text="Day",
                                     text_color='black',
                                     bg_color='#393E46',
                                     fg_color='#EEEEEE',
                                     width=110,
                                     height=28,
                                     command=day)
    setday.place(x=14, y=14)

    setmidnight = customtkinter.CTkButton(time_window,
                                          text="Midnight",
                                          text_color='black',
                                          bg_color='#393E46',
                                          fg_color='#EEEEEE',
                                          width=110,
                                          height=28,
                                          command=midnight)
    setmidnight.place(x=14, y=140)

    setnight = customtkinter.CTkButton(time_window,
                                       text="Night",
                                       text_color='black',
                                       bg_color='#393E46',
                                       fg_color='#EEEEEE',
                                       width=110,
                                       height=28,
                                       command=night)
    setnight.place(x=14, y=98)

    setnoon = customtkinter.CTkButton(time_window,
                                      text="Noon",
                                      text_color='black',
                                      bg_color='#393E46',
                                      fg_color='#EEEEEE',
                                      width=110,
                                      height=28,
                                      command=noon)
    setnoon.place(x=14, y=56)

    time_window.mainloop()


def setweather():
    weather = tk.Tk()
    weather.title("Weather")
    weather.geometry("140x140")
    weather.config(bg='#393E46')

    def clear():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('weather clear')
        commandline.insert(END, f'  {command}')
        weather.destroy()

    def rain():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('weather rain')
        commandline.insert(END, f'  {command}')
        weather.destroy()

    def thunder():
        with r(f'{server_ip}', f'{rcon_password}') as mcr:
            command = mcr.command('weather thunder')
        commandline.insert(END, f'  {command}')
        weather.destroy()

    setclear = customtkinter.CTkButton(weather,
                                       text="Clear",
                                       text_color='black',
                                       bg_color='#393E46',
                                       fg_color='#EEEEEE',
                                       width=110,
                                       height=28,
                                       command=clear)
    setclear.place(x=14, y=14)

    setrain = customtkinter.CTkButton(weather,
                                      text="Rain",
                                      text_color='black',
                                      bg_color='#393E46',
                                      fg_color='#EEEEEE',
                                      width=110,
                                      height=28,
                                      command=rain)
    setrain.place(x=14, y=56)

    setthunder = customtkinter.CTkButton(weather,
                                         text="Thunder",
                                         text_color='black',
                                         bg_color='#393E46',
                                         fg_color='#EEEEEE',
                                         width=110,
                                         height=28,
                                         command=thunder)
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

        def gamemode_def():
            gamemode_window = tk.Tk()
            gamemode_window.title('Gamemode')
            gamemode_window.geometry("250x195")
            gamemode_window.config(bg='#393E46')

            def adventure():
                with r(f'{server_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode adventure {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode_window.destroy()

            def creative():
                with r(f'{server_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode creative {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode_window.destroy()

            def spectrator():
                with r(f'{server_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode spectrator {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode_window.destroy()

            def survival():
                with r(f'{server_ip}', f'{rcon_password}') as mcr:
                    command = mcr.command(f'gamemode survival {player_name}')
                commandline.insert(END, f'  {command}')
                gamemode_window.destroy()

            creative = customtkinter.CTkButton(gamemode_window, text="Creative", text_color='black',
                                               bg_color='#393E46',
                                               fg_color='#EEEEEE',
                                               width=210, height=30, command=creative)
            creative.place(x=20, y=15)

            survival = customtkinter.CTkButton(gamemode_window, text="Survival", text_color='black',
                                               bg_color='#393E46',
                                               fg_color='#EEEEEE',
                                               width=210, height=30, command=survival)
            survival.place(x=20, y=60)

            adventure = customtkinter.CTkButton(gamemode_window,
                                                text="Adventure",
                                                text_color='black',
                                                bg_color='#393E46',
                                                fg_color='#EEEEEE',
                                                width=210,
                                                height=30,
                                                command=adventure)
            adventure.place(x=20, y=105)

            spectrator = customtkinter.CTkButton(gamemode_window,
                                                 text="Spectrator",
                                                 text_color='black',
                                                 bg_color='#393E46',
                                                 fg_color='#EEEEEE',
                                                 width=210,
                                                 height=30,
                                                 command=spectrator)
            spectrator.place(x=20, y=150)

        def operator():
            with r(f'{server_ip}', f'{rcon_password}') as mcr:
                command = mcr.command(f'op {player_name}')
            if command == "Nothing changed. The player already is an operator":
                operator_info = tk.Tk()
                operator_info.title('Operator')
                operator_info.geometry("250x168")
                operator_info.config(bg='#393E46')

                def answer_yes():
                    with r(f'{server_ip}', f'{rcon_password}') as mcr_1:
                        command_1 = mcr_1.command(f'deop {player_name}')
                    commandline.insert(END, f'  {command_1}')
                    operator_info.destroy()

                def answer_no():
                    operator_info.destroy()

                lable1 = customtkinter.CTkLabel(operator_info,
                                                width=200,
                                                height=40,
                                                bg_color='#393E46',
                                                text=f'{player_name} already\nis an operator',
                                                text_color='white')
                lable1.place(x=25, y=10)

                lable2 = customtkinter.CTkLabel(operator_info,
                                                width=200,
                                                height=40,
                                                bg_color='#393E46',
                                                text=f'Revokes operator\nstatus from {player_name}?',
                                                text_color='white')
                lable2.place(x=25, y=60)

                yes = customtkinter.CTkButton(operator_info,
                                              text="Yes",
                                              text_color='black',
                                              bg_color='#393E46',
                                              fg_color='#EEEEEE',
                                              width=50,
                                              height=28,
                                              command=answer_yes)
                yes.place(x=180, y=120)

                no = customtkinter.CTkButton(operator_info,
                                             text="No",
                                             text_color='black',
                                             bg_color='#393E46',
                                             fg_color='#EEEEEE',
                                             width=50,
                                             height=28,
                                             command=answer_no)
                no.place(x=20, y=120)

            else:
                commandline.insert(END, f'  {command}')

        def ban():
            with r(f'{server_ip}', f'{rcon_password}') as mcr:
                command = mcr.command(f'ban {player_name}')
            commandline.insert(END, f'  {command}')

        def kill():
            with r(f'{server_ip}', f'{rcon_password}') as mcr:
                command = mcr.command(f'kill {player_name}')
            commandline.insert(END, f'  {command}')

        gamemode = customtkinter.CTkButton(player_list_window,
                                           text="Gamemode",
                                           text_color='black',
                                           bg_color='#393E46',
                                           fg_color='#EEEEEE',
                                           width=210,
                                           height=30,
                                           command=gamemode_def)
        gamemode.place(x=20, y=60)

        operator = customtkinter.CTkButton(player_list_window,
                                           text="Operator",
                                           text_color='black',
                                           bg_color='#393E46',
                                           fg_color='#EEEEEE',
                                           width=210,
                                           height=30,
                                           command=operator)
        operator.place(x=20, y=105)

        ban = customtkinter.CTkButton(player_list_window,
                                      text="Ban",
                                      text_color='black',
                                      bg_color='#393E46',
                                      fg_color='#EEEEEE',
                                      width=210,
                                      height=30,
                                      command=ban)
        ban.place(x=20, y=150)

        kill = customtkinter.CTkButton(player_list_window,
                                       text="Kill",
                                       text_color='black',
                                       bg_color='#393E46',
                                       fg_color='#EEEEEE',
                                       width=210,
                                       height=30,
                                       command=kill)
        kill.place(x=20, y=195)

    combobox = customtkinter.CTkOptionMenu(player_list_window,
                                           width=210,
                                           height=30,
                                           values=list,
                                           fg_color="#222831",
                                           text_color="white",
                                           command=player_select)
    combobox.place(x=20, y=15)

def statistic_def():
    statistic_window = tk.Tk()
    statistic_window.title("Statistic")
    statistic_window.geometry("320x380")
    statistic_window.config(bg='#393E46')

    def load_statistic():
        diamond_int = statistics_config.get_config('Diamond')
        iron_int = statistics_config.get_config('Iron')
        emerald_int = statistics_config.get_config('Emerald')
        coal_int = statistics_config.get_config('Coal')
        gold_int = statistics_config.get_config('Gold')
        copper_int = statistics_config.get_config('Copper')
        redstone_int = statistics_config.get_config('Redstone')
        lapis_int = statistics_config.get_config('Lapis')
        deaths_int = statistics_config.get_config('Deaths')
        killings_int = statistics_config.get_config('Killings')

        mining = customtkinter.CTkLabel(statistic_window,
                                        width=320,
                                        height=20,
                                        bg_color='#393E46',
                                        text='Mining Statistic')
        mining.place(x=0, y=15)

        diamond = customtkinter.CTkLabel(statistic_window,
                                         width=160,
                                         height=20,
                                         bg_color='#393E46',
                                         text=f'Diamonds mined on the server: {diamond_int}')
        diamond.place(x=12, y=45)

        iron = customtkinter.CTkLabel(statistic_window,
                                      width=160,
                                      height=20,
                                      bg_color='#393E46',
                                      text=f'Iron mined on the server: {iron_int}')
        iron.place(x=12, y=75)

        emerald = customtkinter.CTkLabel(statistic_window,
                                         width=160,
                                         height=20,
                                         bg_color='#393E46',
                                         text=f'Emerald mined on the server: {emerald_int}')
        emerald.place(x=12, y=105)

        coal = customtkinter.CTkLabel(statistic_window,
                                      width=160,
                                      height=20,
                                      bg_color='#393E46',
                                      text=f'Coal mined on the server: {coal_int}')
        coal.place(x=12, y=135)

        gold = customtkinter.CTkLabel(statistic_window,
                                      width=160,
                                      height=20,
                                      bg_color='#393E46',
                                      text=f'Gold mined on the server: {gold_int}')
        gold.place(x=12, y=165)

        copper = customtkinter.CTkLabel(statistic_window,
                                        width=160,
                                        height=20,
                                        bg_color='#393E46',
                                        text=f'Copper mined on the server: {copper_int}')
        copper.place(x=12, y=195)

        redstone = customtkinter.CTkLabel(statistic_window,
                                          width=160,
                                          height=20,
                                          bg_color='#393E46',
                                          text=f'Redstone mined on the server: {redstone_int}')
        redstone.place(x=12, y=225)

        lapis = customtkinter.CTkLabel(statistic_window,
                                       width=160,
                                       height=20,
                                       bg_color='#393E46',
                                       text=f'Lapis mined on the server: {lapis_int}')
        lapis.place(x=12, y=255)

        players = customtkinter.CTkLabel(statistic_window,
                                         width=320,
                                         height=20,
                                         bg_color='#393E46',
                                         text='Players Statistic')
        players.place(x=0, y=285)

        killings = customtkinter.CTkLabel(statistic_window,
                                          width=50,
                                          height=20,
                                          bg_color='#393E46',
                                          text=f'Killings: {killings_int}')
        killings.place(x=12, y=315)

        deaths = customtkinter.CTkLabel(statistic_window,
                                        width=50,
                                        height=20,
                                        bg_color='#393E46',
                                        text=f'Deaths: {deaths_int}')
        deaths.place(x=12, y=345)

    load_statistic()

main_menu.add_command(
    label='About Control-Panel',
    command=info,
)

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

start = customtkinter.CTkButton(window,
                                text="Start",
                                text_color='black',
                                bg_color='#00ADB5',
                                fg_color='#EEEEEE',
                                width=88,
                                height=38,
                                command=start)
start.place(x=12, y=12)

stop = customtkinter.CTkButton(window,
                               text="Stop",
                               text_color='black',
                               bg_color='#00ADB5',
                               fg_color='#EEEEEE',
                               width=88,
                               height=38,
                               command=stop)
stop.place(x=12, y=62)

restart = customtkinter.CTkButton(window,
                                  text="Restart",
                                  text_color='black',
                                  bg_color='#00ADB5',
                                  fg_color='#EEEEEE',
                                  width=88,
                                  height=38,
                                  command=restart_java)
restart.place(x=12, y=112)

timeset = customtkinter.CTkButton(window,
                                  text="Time",
                                  text_color='black',
                                  bg_color='#00ADB5',
                                  fg_color='#EEEEEE',
                                  width=88,
                                  height=38,
                                  command=settime)
timeset.place(x=12, y=200)

weatherset = customtkinter.CTkButton(window,
                                     text="Weather",
                                     text_color='black',
                                     bg_color='#00ADB5',
                                     fg_color='#EEEEEE',
                                     width=88,
                                     height=38,
                                     command=setweather)
weatherset.place(x=12, y=250)

playerlist = customtkinter.CTkButton(window,
                                     text="Players",
                                     text_color='black',
                                     bg_color='#00ADB5',
                                     fg_color='#EEEEEE',
                                     width=88,
                                     height=38,
                                     command=player_list_def)
playerlist.place(x=12, y=300)

statistic = customtkinter.CTkButton(window,
                                    text="Statistic",
                                    text_color='black',
                                    bg_color='#00ADB5',
                                    fg_color='#EEEEEE',
                                    width=88,
                                    height=38,
                                    command=statistic_def)
statistic.place(x=12, y=350)

file = customtkinter.CTkButton(window,
                               text="File",
                               text_color='black',
                               bg_color='#393E46',
                               fg_color='#EEEEEE',
                               width=50,
                               height=28,
                               command=fileplacedef)
file.place(x=635, y=12)

run = customtkinter.CTkButton(window,
                              text="Run",
                              text_color='black',
                              bg_color='#393E46',
                              fg_color='#EEEEEE',
                              width=50,
                              height=28,
                              command=runcommand)
run.place(x=635, y=358)

window.resizable(width=False, height=False)
window.mainloop()
