# possible/ good features but too much work:
# Custom Alarm

# FEATURE TO ADD:
# Enter hotkey
# Add Tray Icon
# 1.) Proper "On-Top" Identifier
# 2.) Commands <show people; pm>

# import requests.exceptions --- I don't know why I added this

from tkinter import *
from decimal import *
from tkinter import messagebox
from tkinter import ttk
from pystray import MenuItem as item
from PIL import Image
import pystray
import _c_hidden_c_ as scram
import socket
import select
import errno
import sys
import subprocess
import threading
import requests
import winsound
import time
import math
import os

class Initialize_Chat():
    def __init__(self):
        self.screen = Tk()
        self.screen.title("Start Up")
        self.screen.resizable(0, 0)
        
        self.var_x = self.screen.winfo_screenwidth()
        self.var_y = self.screen.winfo_screenheight()
        self.def_w = self.var_x >> 1                # x >> 1 = math.floor(x / 2)
        self.def_h = self.var_y >> 1
        self.mid_place_x = self.def_w >> 1          # Shorter for "side - (math.floor(side/2))" -- MIDDLE
        self.mid_place_y = self.def_h >> 1

        self.screen.geometry(f"{self.def_w}x{self.def_h}+{self.mid_place_x}+{self.mid_place_y}")

        self.server_f = ""
        self.state_server_f = ""
        self.user_f = ""
        self.state_user_f = ""
        self.mode_f = ""
        self.state_mode_f = ""

        self.settings = open("settings.txt", "r")
        self.lines = self.settings.readlines()

        for lnum in range(len(self.lines)):
            if self.lines[lnum].strip() == "@ SERVER:":
                self.server_f = self.lines[lnum + 1].strip()
                self.state_server_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ USERNAME:":
                self.user_f = self.lines[lnum + 1].strip()
                self.state_user_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ MODE:":
                self.mode_f = self.lines[lnum + 1].strip()
                self.state_mode_f = self.lines[lnum + 2].strip()

        self.settings.close()

        ###
        self.screen.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.subprocesses = []
        self.terminator_off = True
        self.true_exit = False
        ###

        self.structure()
        self.screen.mainloop()

    def structure(self):
        # MAIN FRAME
        self.container = Frame(self.screen)
        self.frame_list = (For_Username, For_Mode, For_Server)
        self.frames = {}

        for frames in self.frame_list:
            frame = frames(self.container, self, self.def_h, self.def_w, self.screen, self.lines)
            self.frames[frames] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        if self.user_f == "<--NULL-->" or self.state_user_f == "<--MANUAL-->":
            self.show_frame(For_Username) # First Screen ### Start
        elif self.mode_f == "<--NULL-->" or self.state_mode_f == "<--MANUAL-->":
            self.show_frame(For_Mode)
        elif self.server_f == "<--NULL-->" or self.state_server_f == "<--MANUAL-->":
            self.show_frame(For_Server)
        else:
            self.screen.destroy()
            try:
                Chat_Room(self.user_f, self.mode_f, self.server_f)
            except ConnectionError:
                lines = ["The server you are trying to join is currently not available", "or it does not exist"]
                messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))

        #End System
        self.container.pack(fill = BOTH, expand = True) # side = TOP # to ensure

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def show_frame(self, framename):
            frame = self.frames[framename]
            frame.tkraise()

    def update_settings(self, lines):
        self.settings = open("settings.txt", "w")
        self.settings.writelines(lines)
        self.settings.close()

    def tempo_stop(self, event):
        self.terminator_off = False

        for process in self.subprocesses:
            process.terminate()

    def on_closing(self):
        self.terminator_off = False
        self.true_exit = True

        for process in self.subprocesses:
            process.terminate()

        self.screen.destroy()
        sys.exit()


































class For_Username(Frame):
    def __init__(self, parent, inupperclass, screen_height, screen_width, main_window, lines):
        Frame.__init__(self, parent)
        self.inherited = inupperclass
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen = main_window
    
        self.user_line = 0
        self.user_f = ""
        self.state_user_f = ""

        self.server_f = ""
        self.state_server_f = ""
        self.mode_f = ""
        self.state_mode_f = ""

        self.lines = lines

        for lnum in range(len(self.lines)):
            if self.lines[lnum].strip() == "@ USERNAME:":
                self.user_line = lnum
                self.user_f = self.lines[lnum + 1].strip()
                self.state_user_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ SERVER:":
                self.server_f = self.lines[lnum + 1].strip()
                self.state_server_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ MODE:":
                self.mode_f = self.lines[lnum + 1].strip()
                self.state_mode_f = self.lines[lnum + 2].strip()

        self.structure()

    def structure(self):
        self.color_theme = (240, 94, 35)
        self.user = StringVar()

        app_msg_lines = ["This window appears if: ", "1.) it's your first time launching the app", "2.) the setting parts is set to at least one <--MANUAL-->"]
        # MAIN FRAME
        self.screen_frame = Frame(self, bg = "black")
        # TOP
        self.top_frame = Frame(self.screen_frame, bg = "black")
        # TOP WIDGETS
        self.appearance_msg = Label(self.top_frame, text = "\n".join(app_msg_lines), font = ("Helvetica", self.font_size(0.1, 3, self.screen_height)), bg = "black", fg = "black", justify = "left", width = self.side_percent(1)[0], anchor = NW) # fg = "#%02x%02x%02x" % (240, 94, 35)
        self.username_label = Label(self.top_frame, text = "Username", font = ("Helvetica", self.font_size(0.20, 1, self.screen_height), "underline", "bold"), bg = "black", fg = "Lime")
        # ADD
        self.appearance_msg.pack()
        self.username_label.pack()
        # TOP
        self.top_frame.pack()
        # BOTTOM
        self.bottom_frame = Frame(self.screen_frame, bg = "black")
        # ADD
        ### FRAME DESIGN
        self.allowance = self.side_percent(0.05)[1]
        self.outer_box = LabelFrame(self.bottom_frame, bg = "black")
        self.inner_box = LabelFrame(self.outer_box, bg = "black")
        self.outer_box.pack(pady = self.allowance >> 1, padx = self.allowance >> 1)
        self.inner_box.pack(pady = self.allowance, padx = self.allowance)
        ### END OF FRAME DESIGN
        self.username = Entry(self.inner_box, font = ("Helvetica", self.font_size(0.1, 1, self.screen_height)), textvariable = self.user, width = self.side_percent(0.8)[0], exportselection = 0)
        self.set_username = Button(self.inner_box, text = "Set Username", font = ("Helvetica", self.font_size(0.1, 1, self.screen_height), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.change_username)

        self.widget_height1 = self.set_username.winfo_reqheight()
        self.widget_height2 = self.username.winfo_reqheight()

        self.username.pack(pady = self.widget_height2, padx = self.widget_height2)
        self.set_username.pack(pady = (0, self.widget_height1 >> 1), padx = self.widget_height1)
        # BIND
        self.username.bind("<FocusIn>", self.click_tbsend_area)
        self.username.bind("<FocusOut>", self.away_tbsend_area("<FocusOut>"))
        # self.screen.bind("<Return>", self.enter_key_user, "+")
        # BOTTOM
        self.bottom_frame.pack()
        # Show all
        self.screen_frame.pack(expand = True, fill = BOTH)

    def font_size(self, part, lines, height):
        total_font_height = math.floor(height * part)
        height_per_line = math.floor(total_font_height / (lines * 2))
        return height_per_line

    def side_percent(self, percent):
        height = math.floor(self.screen_height * percent)
        width = math.floor(self.screen_width * percent)
        return [width, height]

    def change_username(self):
        if self.username.cget("fg") != "grey" and len(self.user.get()) > 0:
            new_username = self.user.get()
            self.lines[self.user_line + 1] = new_username + "\n"    
            self.auto_OR_manual()

    def enter_key_user(self, event):
        if self.username.cget("fg") != "grey" and len(self.user.get()) > 0:
            self.change_username()

    def click_tbsend_area(self, event):
        if self.username.cget("fg") == "grey":
            self.username.delete(0, "end")
            self.username.insert(0, "")
            self.username.config(fg = "black")

    def away_tbsend_area(self, event):
        if self.user.get() == "":
            self.username.insert(0, "What do you want to be called?")
            self.username.config(fg = "grey")

    def auto_OR_manual(self):
        self.root = Tk()
        self.root.title("Auto or Manual?")
        self.root.resizable(0, 0)

        half_of_parent_w = self.screen_width >> 1
        half_of_parent_h = self.screen_height >> 1

        self.root.geometry(f"{half_of_parent_w}x{half_of_parent_h}+{(self.root.winfo_screenwidth() >> 1) - (self.screen_width >> 2)}+{(self.root.winfo_screenheight() >> 1) - (self.screen_height >> 2)}")
        
        self.for_state_body()
        self.root.mainloop()

    def for_state_body(self):
        main_frame = Frame(self.root, bg = "black")
        lines = ["Choose a state for this input", "Only use this\nfor this time", "Re-use this again\nfor the future"]
        prompt = Label(main_frame, text = lines[0], font = ("Helvetica", self.font_size(0.1, 1, self.screen_width >> 1), "bold"), bg = "black", fg = "Lime")
        or_l = Label(main_frame, text = "or", font = ("Helvetica", self.font_size(0.1, 1, self.screen_width >> 1), "bold"), bg = "black", fg = "Lime")
        manual_b = Button(main_frame, text = "MANUAL", font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 1), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.set_state_manual)
        auto_b = Button(main_frame, text = "AUTO", font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 1), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.set_state_auto)
        manual_l = Label(main_frame, text = lines[1], font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 2), "bold"), bg = "black", fg = "Lime")
        auto_l = Label(main_frame, text = lines[2], font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 2), "bold"), bg = "black", fg = "Lime")

        prompt.place(relwidth = 1, relheight = 0.25)
        or_l.place(relwidth = 0.1, relx = 0.45, rely = 0.38)
        manual_b.place(relwidth = 0.35, relheight = 0.25, relx = 0.05, rely = 0.35)
        auto_b.place(relwidth = 0.35, relheight = 0.25, relx = 0.6, rely = 0.35)
        manual_l.place(relwidth = 0.35, relheight = 0.1, relx = 0.05, rely = 0.65)
        auto_l.place(relwidth = 0.35, relheight = 0.1, relx = 0.6, rely = 0.65)

        main_frame.pack(expand = True, fill = BOTH)

    def set_state_manual(self):
        self.lines[self.user_line + 2] = "<--MANUAL-->\n"
        self.root.destroy()

        if self.mode_f == "<--NULL-->" or self.state_mode_f == "<--MANUAL-->":
            self.inherited.show_frame(For_Mode)
        elif self.server_f == "<--NULL-->" or self.state_server_f == "<--MANUAL-->":
            self.inherited.show_frame(For_Server)
        else:
            self.inherited.update_settings(self.lines)

            for lnum in range(len(self.lines)):
                if self.lines[lnum].strip() == "@ USERNAME:":
                    self.user_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ SERVER:":
                    self.server_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ MODE:":
                    self.mode_f = self.lines[lnum + 1].strip()

            self.screen.destroy()
            
            try:
                Chat_Room(self.user_f, self.mode_f, self.server_f)
            except ConnectionError:
                lines = ["The server you are trying to join is currently not available", "or it does not exist"]
                messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))
    
    def set_state_auto(self):
        self.lines[self.user_line + 2] = "<--AUTO-->\n"
        self.root.destroy()
        # self.screen.unbind("<Return>")

        if self.mode_f == "<--NULL-->" or self.state_mode_f == "<--MANUAL-->":
            self.inherited.show_frame(For_Mode)
        elif self.server_f == "<--NULL-->" or self.state_server_f == "<--MANUAL-->":
            self.inherited.show_frame(For_Server)
        else:
            self.inherited.update_settings(self.lines)

            for lnum in range(len(self.lines)):
                if self.lines[lnum].strip() == "@ USERNAME:":
                    self.user_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ SERVER:":
                    self.server_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ MODE:":
                    self.mode_f = self.lines[lnum + 1].strip()

            self.screen.destroy()

            try:
                Chat_Room(self.user_f, self.mode_f, self.server_f)
            except ConnectionError:
                lines = ["The server you are trying to join is currently not available", "or it does not exist"]
                messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))


































class For_Mode(Frame):
    def __init__(self, parent, inupperclass, screen_height, screen_width, main_window, lines):
        Frame.__init__(self, parent)
        self.inherited = inupperclass
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen = main_window

        self.mode_line = 0
        self.mode_f = ""
        self.state_mode_f = ""
        ### IMPORTS
        self.user_f = ""
        self.state_user_f = ""

        self.server_f = ""
        self.state_server_f = ""
        ###

        self.lines = lines

        for lnum in range(len(self.lines)):
            if self.lines[lnum].strip() == "@ USERNAME:":
                self.user_f = self.lines[lnum + 1].strip()
                self.state_user_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ MODE:":
                self.mode_line = lnum
                self.mode_f = self.lines[lnum + 1].strip()
                self.state_mode_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ SERVER:":
                self.server_f = self.lines[lnum + 1].strip()
                self.state_server_f = self.lines[lnum + 2].strip()

        self.structure()

    def structure(self):
        self.color_theme = (240, 94, 35)

        app_msg_lines = ["This window appears if: ", "1.) it's your first time launching the app", "2.) the setting parts is set to at least one <--MANUAL-->"]
        # MAIN FRAME
        self.screen_frame = Frame(self, bg = "black")
        # TOP
        self.top_frame = Frame(self.screen_frame, bg = "black")
        # TOP WIDGETS
        self.appearance_msg = Label(self.top_frame, text = "\n".join(app_msg_lines), font = ("Helvetica", self.font_size(0.1, 3, self.screen_height)), bg = "black", fg = "black", justify = "left", width = self.side_percent(1)[0], anchor = NW) # prev: fg = "SkyBlue"
        self.mode_label = Label(self.top_frame, text = "Mode", font = ("Helvetica", self.font_size(0.20, 1, self.screen_height), "underline", "bold"), bg = "black", fg = "Lime")
        # ADD
        self.appearance_msg.pack()
        self.mode_label.pack()
        # TOP
        self.top_frame.pack()
        # BOTTOM
        self.bottom_frame = Frame(self.screen_frame, bg = "black")
        # ADD
        ### FRAME DESIGN
        self.allowance = self.side_percent(0.05)[1]
        self.outer_box = LabelFrame(self.bottom_frame, bg = "black")
        self.inner_box = LabelFrame(self.outer_box, bg = "black")
        self.outer_box.pack(pady = self.allowance >> 1, padx = self.allowance >> 1)
        self.inner_box.pack(pady = self.allowance, padx = self.allowance)
        ### END OF FRAME DESIGN
        self.show = Button(self.inner_box, text = "Show Icon (Taskbar)", font = ("Helvetica", self.font_size(0.1, 1, self.screen_height), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.show_icon)
        self.not_show = Button(self.inner_box, text = "Don't Show Icon (Taskbar)", font = ("Helvetica", self.font_size(0.1, 1, self.screen_height), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.not_show_icon)

        self.widget_height1 = self.show.winfo_reqheight()
        self.same_width = self.not_show.winfo_reqwidth()

        self.show.config(width = self.same_width)
        self.not_show.config(width = self.same_width)

        self.show.pack(pady = self.widget_height1 >> 1, padx = self.widget_height1)
        self.not_show.pack(pady = (0, self.widget_height1 >> 1), padx = self.widget_height1)
        # BOTTOM
        self.bottom_frame.pack()
        # Show all
        self.screen_frame.pack(expand = True, fill = BOTH)

    def show_icon(self):
        self.lines[self.mode_line + 1] = "<--SHOW-->\n"
        self.auto_OR_manual()

    def not_show_icon(self):
        self.lines[self.mode_line + 1] = "<--DISABLE-->\n"
        self.auto_OR_manual()

    def font_size(self, part, lines, height):
        total_font_height = math.floor(height * part)
        height_per_line = math.floor(total_font_height / (lines * 2))
        return height_per_line

    def side_percent(self, percent):
        height = math.floor(self.screen_height * percent)
        width = math.floor(self.screen_width * percent)
        return [width, height]

    def auto_OR_manual(self):
        self.root = Tk()
        self.root.title("Auto or Manual?")
        self.root.resizable(0, 0)

        half_of_parent_w = self.screen_width >> 1
        half_of_parent_h = self.screen_height >> 1

        self.root.geometry(f"{half_of_parent_w}x{half_of_parent_h}+{(self.root.winfo_screenwidth() >> 1) - (self.screen_width >> 2)}+{(self.root.winfo_screenheight() >> 1) - (self.screen_height >> 2)}")
        
        self.for_state_body()
        self.root.mainloop()

    def for_state_body(self):
        main_frame = Frame(self.root, bg = "black")
        lines = ["Choose a state for this input", "Only use this\nfor this time", "Re-use this again\nfor the future"]
        prompt = Label(main_frame, text = lines[0], font = ("Helvetica", self.font_size(0.1, 1, self.screen_width >> 1), "bold"), bg = "black", fg = "Lime")
        or_l = Label(main_frame, text = "or", font = ("Helvetica", self.font_size(0.1, 1, self.screen_width >> 1), "bold"), bg = "black", fg = "Lime")
        manual_b = Button(main_frame, text = "MANUAL", font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 1), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.set_state_manual)
        auto_b = Button(main_frame, text = "AUTO", font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 1), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.set_state_auto)
        manual_l = Label(main_frame, text = lines[1], font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 2), "bold"), bg = "black", fg = "Lime")
        auto_l = Label(main_frame, text = lines[2], font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 2), "bold"), bg = "black", fg = "Lime")

        prompt.place(relwidth = 1, relheight = 0.25)
        or_l.place(relwidth = 0.1, relx = 0.45, rely = 0.38)
        manual_b.place(relwidth = 0.35, relheight = 0.25, relx = 0.05, rely = 0.35)
        auto_b.place(relwidth = 0.35, relheight = 0.25, relx = 0.6, rely = 0.35)
        manual_l.place(relwidth = 0.35, relheight = 0.1, relx = 0.05, rely = 0.65)
        auto_l.place(relwidth = 0.35, relheight = 0.1, relx = 0.6, rely = 0.65)

        main_frame.pack(expand = True, fill = BOTH)

    def set_state_manual(self):
        self.lines[self.mode_line + 2] = "<--MANUAL-->\n"
        self.root.destroy()

        if self.server_f == "<--NULL-->" or self.state_server_f == "<--MANUAL-->":
            self.inherited.show_frame(For_Server)
        else:
            self.inherited.update_settings(self.lines)

            for lnum in range(len(self.lines)):
                if self.lines[lnum].strip() == "@ USERNAME:":
                    self.user_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ SERVER:":
                    self.server_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ MODE:":
                    self.mode_f = self.lines[lnum + 1].strip()

            self.screen.destroy()

            try:
                Chat_Room(self.user_f, self.mode_f, self.server_f)
            except ConnectionError:
                lines = ["The server you are trying to join is currently not available", "or it does not exist"]
                messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))

    def set_state_auto(self):
        self.lines[self.mode_line + 2] = "<--AUTO-->\n"
        self.root.destroy()

        if self.server_f == "<--NULL-->" or self.state_server_f == "<--MANUAL-->":
            self.inherited.show_frame(For_Server)
        else:
            self.inherited.update_settings(self.lines)

            for lnum in range(len(self.lines)):
                if self.lines[lnum].strip() == "@ USERNAME:":
                    self.user_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ SERVER:":
                    self.server_f = self.lines[lnum + 1].strip()

                if self.lines[lnum].strip() == "@ MODE:":
                    self.mode_f = self.lines[lnum + 1].strip()

            self.screen.destroy()

            try:
                Chat_Room(self.user_f, self.mode_f, self.server_f)
            except ConnectionError:
                lines = ["The server you are trying to join is currently not available", "or it does not exist"]
                messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))




























class For_Server(Frame):
    def __init__(self, parent, inupperclass, screen_height, screen_width, main_window, lines):
        Frame.__init__(self, parent)
        self.inherited = inupperclass
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen = main_window
    
        self.server_line = 0
        self.server_f = ""
        self.state_server_f = ""

        ### IMPORTS
        self.user_f = ""
        self.state_user_f = ""
        self.mode_f = ""
        self.state_mode_f = ""
        ###

        self.lines = lines

        for lnum in range(len(self.lines)):
            if self.lines[lnum].strip() == "@ USERNAME:":
                self.user_f = self.lines[lnum + 1].strip()
                self.state_user_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ SERVER:":
                self.server_line = lnum
                self.server_f = self.lines[lnum + 1].strip()
                self.state_server_f = self.lines[lnum + 2].strip()

            if self.lines[lnum].strip() == "@ MODE:":
                self.mode_f = self.lines[lnum + 1].strip()
                self.state_mode_f = self.lines[lnum + 2].strip()

        self.inherited.screen.bind("<Escape>", self.inherited.tempo_stop)

        self.structure()

    def structure(self):
        self.color_theme = (240, 94, 35)
        self.server_id = StringVar()

        # MAIN FRAME
        self.screen_frame = Frame(self, bg = "black")
        # TOP
        self.top_frame = Frame(self.screen_frame, bg = "black")
        # TOP WIDGETS
        self.server_label = Label(self.top_frame, text = "Server", font = ("Helvetica", self.font_size(0.20, 1, self.screen_height), "underline", "bold"), bg = "black", fg = "Lime")
        # ADD
        self.server_label.pack(pady = (0, self.server_label.winfo_reqheight() >> 2))
        # TOP
        self.top_frame.pack()
        # MID
        self.middle_frame = Frame(self.screen_frame, bg = "black")
        self.mid_filler = Frame(self.middle_frame, bg = "black", width = self.screen_width, height = self.side_percent(0.075)[1])
        # ADD
        self.server = Entry(self.mid_filler, font = ("Helvetica", self.font_size(0.06, 1, self.screen_height)), textvariable = self.server_id, exportselection = 0, relief = RIDGE)
        self.set_server = Button(self.mid_filler, text = "Set Server", font = ("Helvetica", self.font_size(0.06, 1, self.screen_height), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.change_server, relief = RIDGE)
        self.direct = Button(self.mid_filler, text = "Direct Connect: ", font = ("Helvetica", self.font_size(0.06, 1, self.screen_height), "bold"), bg = "black", fg = "#%02x%02x%02x" % self.color_theme, state = DISABLED, relief = RIDGE)

        self.server.place(relheight = 1, relwidth = 0.6, relx = 0.2)
        self.set_server.place(relheight = 1, relwidth = 0.2, relx = 0.8)
        self.direct.place(relheight = 1, relwidth = 0.2)
        # MID
        self.mid_filler.pack()
        self.middle_frame.pack()
        # BOTTOM
        self.bottom_frame = Frame(self.screen_frame, bg = "black")
        # ADD
        ### FRAME DESIGN
        self.allowance = self.side_percent(0.05)[1]
        self.outer_box = LabelFrame(self.bottom_frame, bg = "black")
        ###
        self.inner_box = LabelFrame(self.outer_box, bg = "black")
        ### SEARCHER COMBOBOX --- OUTERBOX
        self.choose_frame = Frame(self.outer_box, bg = "black", height = self.allowance)
        self.searchers = ["Quick Scan", "Nmap Scan"]
        self.searcher = StringVar()
        self.searcher.set(self.searchers[0])

        self.choose_searcher = ttk.Combobox(self.choose_frame, textvariable = self.searcher)
        self.choose_searcher["values"] = self.searchers
        self.choose_searcher["state"] = "readonly"
        # SEARCH BUTTON
        self.search = Button(self.choose_frame, text = "Scan", font = ("Helvetica", self.font_size(0.06, 1, self.screen_height), "bold"), bg = "black", fg = "#%02x%02x%02x" % (0, 158, 96), relief = RIDGE, command = self.search_scan)
        # ADD
        self.search.place(relheight = 1, relwidth = 0.1, relx = 0.9)
        self.choose_searcher.place(relheight = 1, relwidth = 0.2, relx = 0.7)

        self.choose_frame.pack(side = TOP, anchor = NE, pady = self.allowance >> 1, fill = X)
        ### MAIN!!!
        self.main_frame = Frame(self.inner_box, bg = "black", width = self.screen_width, height = self.screen_height)
        self.main_frame.pack(padx = self.allowance, pady = self.allowance)
        
        self.first_time_scan = True
        self.search_scan()
        ###
        self.outer_box.pack(pady = self.allowance >> 1, padx = self.allowance >> 1)
        self.inner_box.pack(pady = (0, self.allowance), padx = self.allowance)
        ### END OF FRAME DESIGN
        # BIND
        self.server.bind("<FocusIn>", self.click_tbsend_area)
        self.server.bind("<FocusOut>", self.away_tbsend_area("<FocusOut>"))
        # self.screen.bind("<Return>", self.enter_key_server, "+")
        # BOTTOM
        self.bottom_frame.pack()
        # Show all
        self.screen_frame.pack(expand = True, fill = BOTH)

    def animate_infi_bouncy_ball(self, parent, canvas, xinc, yinc, x, y, radius, color, interval, window_height, window_width):
        # start pos
        ball = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill = color)
        
        while self.loading:
            canvas.move(ball, xinc, yinc)
            parent.update()

            time.sleep(interval)
            ball_pos = canvas.coords(ball)
            # coords
            xl, yl, xr, yr = ball_pos
            if xl < abs(xinc) or xr > window_width - abs(xinc):
                xinc = -xinc
            # if yl < abs(yinc) or yr > window_height - abs(yinc):
            #     yinc = -yinc

    def isolate_frame(self, parent_frame):
        for frame in self.in_main_frames:
            if frame != parent_frame:
                frame.place_forget()
                continue
            else:
                frame.place(relheight = 1, relwidth = 1)

    def show_result_screen(self):
        self.load_thread.join()

        if len(self.scan_results) == 0:
            self.isolate_frame(self.in_main_frames[0])
            self.no_results()
        else:
            self.isolate_frame(self.in_main_frames[1])
            self.show_scan_results()

    def loading_screen(self):
        parent = self.in_main_frames[2]
        search_label = Label(parent, text = "Searching...", fg = "skyblue", font = ("Helvetica", self.font_size(0.15, 1, self.screen_height), "bold"), bg = parent.cget("bg"))
        loading_canvas = Canvas(parent, bg = "black", borderwidth = 0, highlightthickness = 0, width = search_label.winfo_reqwidth())

        # warning = Label(parent, text = "Warning: Don't exit while scanning, errors may occur", fg = "skyblue", font = ("Helvetica", self.font_size(0.035, 1, self.screen_height)), bg = self.in_main_frames[2].cget("bg"))
        ###
        search_label.place(relheight = 0.8, relx = 0.5, rely = 0.35, anchor = CENTER)
        loading_canvas.place(relheight = 0.2, relx = 0.5, rely = 0.6, anchor = CENTER)

        # warning.place(relheight = 0.1, relx = 0.5, rely = 0.9, anchor = CENTER)

        height = loading_canvas.winfo_reqheight() * 0.05
        self.animate_infi_bouncy_ball(parent, loading_canvas, 2.5, 0, height + 1, height + 1, height, "skyblue", 0.01, loading_canvas.winfo_reqheight(), loading_canvas.winfo_reqwidth())

        self.search.config(state = NORMAL)
        self.choose_searcher.config(state = "readonly")

    def no_results(self):
        parent = self.in_main_frames[0]
        message_null = Label(parent, text = "No Servers Found", fg = "skyblue", font = ("Helvetica", self.font_size(0.15, 1, self.screen_height), "bold"), bg = parent.cget("bg"))

        message_null.place(relheight = 0.8, relx = 0.5, rely = 0.35, anchor = CENTER)

    def scroller(self, canvas):
        canvas.configure(scrollregion = canvas.bbox("all"))

    def frame_expander(self, event):
        canvas_width = event.width
        # self.frame.config(width=canvas_width)
        self.canvas.itemconfig(self.frame_item, width=canvas_width)
 
    def show_scan_results(self):
        parent = self.in_main_frames[1]

        try:
            prev_ips = self.frame.winfo_children()

            for prev_ip in prev_ips:
                prev_ip.destroy()

        except AttributeError:
            self.canvas = Canvas(parent, bg = parent.cget("bg"), highlightthickness = 0, relief = RAISED)
            self.frame = Frame(self.canvas, bg = parent.cget("bg"))

            myscrollbar = Scrollbar(parent, orient = "vertical", command = self.canvas.yview)
            self.canvas.configure(yscrollcommand = myscrollbar.set)

            myscrollbar.pack(side = RIGHT, fill = Y)

            self.canvas.pack(side = LEFT, fill = BOTH, expand = True)

            self.frame_item = self.canvas.create_window((0, 0), window = self.frame)

            self.frame.bind("<Configure>", lambda event, canvas = self.canvas: self.scroller(self.canvas))
            self.canvas.bind("<Configure>", self.frame_expander)

            # for num_columns in range(3):
                # self.frame.columnconfigure(num_columns, weight = 1)
        
            #.grid(columnspan = ) can also be used
            self.frame.columnconfigure(0, weight = 1)
            self.frame.columnconfigure(1, weight = 5)
            self.frame.columnconfigure(2, weight = 1)

        for place in range(len(self.scan_results)):
            Button(self.frame, text = self.scan_results[place], font = ("Helvetica", self.font_size(0.06, 1, self.screen_height), "bold"), bg = "#%02x%02x%02x" % self.color_theme, fg = "black", relief = RIDGE, command = lambda: self.join_server(self.scan_results[place])).grid(row = place, column = 1, sticky = "NSEW", ipady = self.font_size(0.025, 1, self.screen_height), pady = (0, self.font_size(0.025, 1, self.screen_height)))

    def send(self, msg, client_socket):
        username = msg.encode("utf-8")
        username_header = f"{len(username):<{64}}".encode("utf-8")
        client_socket.send(username_header + username)

    def notify_server(self, SERVER):
        PORT = 5050
        ADDR = (SERVER, PORT)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)

        # client_socket.settimeout(0.5)

        client_socket.setblocking(0)

        not_sent = True

        while not_sent and self.inherited.terminator_off:
            self.send(scram.searcher_name, client_socket)

            scan_check = select.select([client_socket], [], [], 0.1)
            if scan_check[0]:
                recvd_msg = client_socket.recv(64).decode("utf-8")

                if scram.decrypt(recvd_msg) == scram.entry_pass:
                    not_sent = False
                    client_socket.close()
            
    def test_ips(self, ips):
        for server in ips:
            try:
                self.notify_server(server)
                self.scan_results.append(server)
            except (Exception, ConnectionError, ConnectionRefusedError):
                pass

            if not self.inherited.terminator_off:
                break
        if self.inherited.true_exit:
            os._exit(0)
        else:
            self.loading = False
            self.inherited.terminator_off = True

    def arp_scan(self):
        process_arp = subprocess.Popen(["arp", "-a"], stdout = subprocess.PIPE)
        
        self.inherited.subprocesses.append(process_arp)

        raw_data = process_arp.communicate()[0].decode("utf-8").split("\n")

        tempo_list_ip = []
        tempo_list_ip.append(socket.gethostbyname(socket.gethostname()))

        for line in raw_data:
            if "dynamic" in line:
                place = 0
                for _ in line:
                    if line[place] == "1":
                        start_position = place
                        break
                    place += 1
                for _ in line:
                    if line[place] == " ":
                        end_position = place
                        break
                    place += 1

                if line[start_position:end_position] != self.gateway_ip:
                    tempo_list_ip.append(line[start_position:end_position])

        self.test_ips(tempo_list_ip)

        self.loading = False
        self.inherited.subprocesses.remove(process_arp)

        self.show_result_screen()

    def nmap_scan(self):
        try:
            process_nmap = subprocess.Popen(["nmap", "-sP", f"{self.gateway_ip}/24"], stdout = subprocess.PIPE)
        
            raw_data = process_nmap.communicate()[0].decode("utf-8").split("\n")

            self.inherited.subprocesses.append(process_nmap)

            tempo_list_ip = []

            for line in raw_data:
                if "Nmap scan report for" in line:
                    ip_line = line[21:len(line) - 1] # -1 for strip
                    if ip_line != self.gateway_ip:
                        tempo_list_ip.append(ip_line)

            self.test_ips(tempo_list_ip)

            self.inherited.subprocesses.remove(process_nmap)

            self.show_result_screen()

        except FileNotFoundError:
            lines = ["NMAP is not installed or not seen", "Try again"]
            messagebox.showerror("NMAP Not Found", "\n".join(lines))
        
        self.loading = False

    def current_gateway(self):
        ip_info = subprocess.check_output(["ipconfig"]).decode("utf-8").split("\n")
        for i in range(len(ip_info)):
            current_line = ip_info[i]
            if "Default Gateway" in current_line:
                maybe_the_ip = ip_info[i + 1]
                if len(maybe_the_ip) == 1:
                    maybe_the_ip = ip_info[i]

                for i2 in range(len(maybe_the_ip)):
                    if maybe_the_ip[i2] == "1":
                        self.gateway_ip = maybe_the_ip[i2:len(maybe_the_ip) - 1]
                        break

    def search_scan(self):
        if self.first_time_scan:
            self.current_gateway()
            
            try:
                len(self.gateway_ip)
            except AttributeError:
                lines = ["No internet connection!", "Try again"]
                messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))
                self.inherited.on_closing()

            self.no_result_frame = Frame(self.main_frame, bg = "black")
            self.result_frame = Frame(self.main_frame, bg = "black")
            self.loading_frame = Frame(self.main_frame, bg = "black")
            self.in_main_frames = [self.no_result_frame, self.result_frame, self.loading_frame]
            self.first_time_scan = False

        self.scan_results = []
        self.search.config(state = DISABLED)
        self.choose_searcher.config(state = DISABLED)

        self.arp_scan_now = threading.Thread(target = self.arp_scan)
        self.nmap_scan_now = threading.Thread(target = self.nmap_scan)

        self.loading = True
        self.isolate_frame(self.in_main_frames[2])
        self.load_thread = threading.Thread(target = self.loading_screen)
        self.load_thread.start()

        if self.choose_searcher.get() == self.searchers[0]:
            self.arp_scan_now.start()
        elif self.choose_searcher.get() == self.searchers[1]:
            self.nmap_scan_now.start()

        # threading.Thread(target = self.show_result_screen).start()

    def font_size(self, part, lines, height):
        total_font_height = math.floor(height * part)
        height_per_line = math.floor(total_font_height / (lines * 2))
        return height_per_line

    def side_percent(self, percent):
        height = math.floor(self.screen_height * percent)
        width = math.floor(self.screen_width * percent)
        return [width, height]

    def join_server(self, server):
        new_server = server
        self.lines[self.server_line + 1] = new_server + "\n"
        self.auto_OR_manual()

    def change_server(self):
        self.inherited.tempo_stop(None)
        
        if self.server.cget("fg") != "grey" and len(self.server_id.get()) > 0:
            new_server = self.server_id.get()
            self.lines[self.server_line + 1] = new_server + "\n"
            self.auto_OR_manual()

    def enter_key_server(self, event):
        if self.server.cget("fg") != "grey" and len(self.server_id.get()) > 0:
            self.change_server()

    def click_tbsend_area(self, event):
        if self.server.cget("fg") == "grey":
            self.server.delete(0, "end")
            self.server.insert(0, "")
            self.server.config(fg = "black")

    def away_tbsend_area(self, event):
        if self.server_id.get() == "":
            self.server.insert(0, "Input Host's IP")
            self.server.config(fg = "grey")

    def auto_OR_manual(self):
        self.root = Tk()
        self.root.title("Auto or Manual?")
        self.root.resizable(0, 0)

        half_of_parent_w = self.screen_width >> 1
        half_of_parent_h = self.screen_height >> 1

        self.root.geometry(f"{half_of_parent_w}x{half_of_parent_h}+{(self.root.winfo_screenwidth() >> 1) - (self.screen_width >> 2)}+{(self.root.winfo_screenheight() >> 1) - (self.screen_height >> 2)}")
        
        self.for_state_body()
        self.root.mainloop()

    def for_state_body(self):
        main_frame = Frame(self.root, bg = "black")
        lines = ["Choose a state for this input", "Only use this\nfor this time", "Re-use this again\nfor the future"]
        prompt = Label(main_frame, text = lines[0], font = ("Helvetica", self.font_size(0.1, 1, self.screen_width >> 1), "bold"), bg = "black", fg = "Lime")
        or_l = Label(main_frame, text = "or", font = ("Helvetica", self.font_size(0.1, 1, self.screen_width >> 1), "bold"), bg = "black", fg = "Lime")
        manual_b = Button(main_frame, text = "MANUAL", font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 1), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.set_state_manual)
        auto_b = Button(main_frame, text = "AUTO", font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 1), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.set_state_auto)
        manual_l = Label(main_frame, text = lines[1], font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 2), "bold"), bg = "black", fg = "Lime")
        auto_l = Label(main_frame, text = lines[2], font = ("Helvetica", self.font_size(0.09, 1, self.screen_width >> 2), "bold"), bg = "black", fg = "Lime")

        prompt.place(relwidth = 1, relheight = 0.25)
        or_l.place(relwidth = 0.1, relx = 0.45, rely = 0.38)
        manual_b.place(relwidth = 0.35, relheight = 0.25, relx = 0.05, rely = 0.35)
        auto_b.place(relwidth = 0.35, relheight = 0.25, relx = 0.6, rely = 0.35)
        manual_l.place(relwidth = 0.35, relheight = 0.1, relx = 0.05, rely = 0.65)
        auto_l.place(relwidth = 0.35, relheight = 0.1, relx = 0.6, rely = 0.65)

        main_frame.pack(expand = True, fill = BOTH)

    def set_state_manual(self):
        self.lines[self.server_line + 2] = "<--MANUAL-->\n"
        self.root.destroy()

        self.inherited.update_settings(self.lines)

        for lnum in range(len(self.lines)):
            if self.lines[lnum].strip() == "@ USERNAME:":
                self.user_f = self.lines[lnum + 1].strip()

            if self.lines[lnum].strip() == "@ SERVER:":
                self.server_f = self.lines[lnum + 1].strip()

            if self.lines[lnum].strip() == "@ MODE:":
                self.mode_f = self.lines[lnum + 1].strip()

        self.screen.destroy()

        try:
            Chat_Room(self.user_f, self.mode_f, self.server_f)
        except ConnectionError:
            lines = ["The server you are trying to join is currently not available", "or it does not exist"]
            messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))
    
    def set_state_auto(self):
        self.lines[self.server_line + 2] = "<--AUTO-->\n"
        self.root.destroy()

        self.inherited.update_settings(self.lines)

        for lnum in range(len(self.lines)):
            if self.lines[lnum].strip() == "@ USERNAME:":
                self.user_f = self.lines[lnum + 1].strip()

            if self.lines[lnum].strip() == "@ SERVER:":
                self.server_f = self.lines[lnum + 1].strip()

            if self.lines[lnum].strip() == "@ MODE:":
                self.mode_f = self.lines[lnum + 1].strip()

        self.screen.destroy()
 
        try:
            Chat_Room(self.user_f, self.mode_f, self.server_f)
        except ConnectionError:
            lines = ["The server you are trying to join is currently not available", "or it does not exist"]
            messagebox.showerror(title = "Connection Error!", message = "\n".join(lines))
    






























class Chat_Room():
    def __init__(self, username, mode, server):
        self.screen = Tk()
        self.screen.title("Local Messenger")

        self.join = server
        self.call_me = username

        self.server_temp = StringVar()
        self.server_temp.set(self.join)

        if mode == "<--SHOW-->":
            self.screen.resizable(0, 0)
            self.screen.protocol("WM_DELETE_WINDOW", self.on_closing)
        elif mode == "<--DISABLE-->":
            self.screen.resizable(0, 0)
            self.screen.attributes("-toolwindow", True)
            self.screen.protocol("WM_DELETE_WINDOW", self.tray_min)

        self.max_user_length = 20

        self.connected = True

        ### Universal class variables ###
        self.for_exit = False
        ### --- + --- + --- ###

        if len(username) > 0 and len(username) < self.max_user_length:
            if username == scram.searcher_name or username == scram.owner_tag:
                lines = [f"I'm sorry but the username {username} is not allowed", "Try Again."]
                messagebox.showinfo(title = "[ERROR]", message = "\n".join(lines))
                self.screen.quit()
                sys.exit()
            elif len(username) > self.max_user_length:
                lines = [f"Your username have exceeded the allowable number of characters ({self.max_user_length})", "Try Again."]
                messagebox.showinfo(title = "[ERROR]", message = "\n".join(lines))
                self.screen.quit()
                sys.exit()

        self.sock_sys()
        ### IMPORTS
        # self.my_username = StringVar()
        # self.SERVER = StringVar()
        ### IMPORTS

        self.msg_var = StringVar()
        
        self.var_x = self.screen.winfo_screenwidth()
        self.var_y = self.screen.winfo_screenheight()
        self.def_w = self.var_x >> 1
        self.def_h = self.var_y >> 1
        self.screenx = (self.var_x >> 1) - (self.var_x % 10)
        self.screeny = (self.var_y >> 1) - (self.var_y % 100)

        self.screen.geometry(f"{self.def_w}x{self.def_h}+{self.screenx}+{self.screeny}")
        self.structure()

        self.screen.bind("<Configure>", self.size_update)
        self.screen.bind("<Return>", self.enter_key)
        # self.screen.bind(#"<Esc>", self.on_closing)
        
        self.user_send()

        # self.to_send.insert(0, "Send a message to everyone")
        # self.to_send.config(fg = "grey")

        # self.show_msgs.config(state = NORMAL)
        # self.show_msgs.insert(END, f"Welcome {username}!\n", ("center", "bold_font", "color_theme"))
        # self.show_msgs.insert(END, f"You have joined the server {self.SERVER}\n\n", ("center", "norm_font", "white"))
        # self.show_msgs.insert(END, f"Available Commands:\n", ("left", "bold_font", "color_theme"))
        # self.show_msgs.insert(END, f"/peeps", ("left", "norm_font", "color_theme"))
        # self.show_msgs.insert(END, f"                   - show everyone connected to the server\n", ("left", "norm_font", "white"))
        # self.show_msgs.insert(END, f"/pmsg <target>: ", ("left", "norm_font", "color_theme"))
        # self.show_msgs.insert(END, f"   - whisper/ private message\n\n", ("left", "norm_font", "white"))
        # self.show_msgs.config(state = DISABLED)
        # self.show_msgs.see(END)

        self.screen.mainloop()

    def sock_sys(self):
        self.SERVER = self.join
        self.PORT = 5050
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.HEADER = 64
        
        self.my_username = StringVar()
        self.my_username.set(self.call_me)
        #####

        # self.msgs = StringVar()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

        self.client_socket.setblocking(False)

        self.m = "for name"
        ###
        self.to_recv_data = threading.Thread(target = self.recv_data)
        self.check_connection = threading.Thread(target = self.show_conn_state)
    
        self.to_recv_data.start()
        self.check_connection.start()

    def internet_on(self):
        url = "http://216.58.192.142"
        timeout = 1
        try:
            requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def show_conn_state(self):
        while self.connected:
            time.sleep(5)
            if self.internet_on == False:
                self.screen.update()
                self.show_msgs.config(state = NORMAL)
                self.show_msgs.insert(END, "Internet Connection Lost, Messages won't be received by Server\n\n")
                self.show_msgs.config(state = DISABLED)
                self.show_msgs.see(END)
                self.screen.update()
                while self.connected:
                    time.sleep(5)
                    if self.internet_on == True:
                        self.screen.update()
                        self.show_msgs.config(state = NORMAL)
                        self.show_msgs.insert(END, "You have reconnected, Messages can now be received by server\n\n")
                        self.show_msgs.config(state = DISABLED)
                        self.show_msgs.see(END)
                        self.screen.update()
                        break
                
    def enter_key(self, event):
        if self.m == "for name":
            self.user_send()
        elif self.m == "for msg":
            self.send_data()

    def user_send(self):
        if self.check_empty(self.my_username.get()) != True and len(self.my_username.get()) < self.max_user_length:
            if self.my_username.get() == scram.searcher_name or self.my_username.get() == scram.owner_tag:
                lines = [f"I'm sorry but the username {self.my_username.get()} is not allowed", "Try Again."]
                messagebox.showinfo(title = "[ERROR]", message = "\n".join(lines))

            else:
                self.screen.update()
                self.send(self.my_username.get(), self.m)
                
                self.server.insert(0, self.join)
                self.username.insert(0, self.my_username.get())
                self.username_t.config(state = DISABLED)
                self.username.config(state = DISABLED)
                self.set_user.config(state = DISABLED)
                self.server_t.config(state = DISABLED)
                self.server.config(state = DISABLED)
                self.set_server.config(state = DISABLED)

        elif len(self.my_username.get()) > self.max_user_length:
            lines = [f"Your username have exceeded the allowable number of characters ({self.max_user_length})", "Try Again."]
            messagebox.showinfo(title = "[ERROR]", message = "\n".join(lines))

    def recv_data(self):
        while self.connected:
            time.sleep(0.5)
            try:
                while self.connected:
                    self.receive_data()
                
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    lines = [f"Reading error: {str(e)}"]
                    self.custom_pop_up("[READING ERROR]", "\n".join(lines), ["Close", "Exit Server"], [self.exit_root, self.close_follow_up])
                    self.useless_room("an error")
                    self.connected = False
                    self.screen.quit()
                    sys.exit()

            except Exception as e:
                lines = [f"Reading error: {str(e)}"]
                self.custom_pop_up("[READING ERROR]", "\n".join(lines), ["Close", "Exit Server"], [self.exit_root, self.close_follow_up])
                self.useless_room("an error")
                self.connected = False
                self.screen.quit()
                sys.exit()

    def send_data(self):
        ### SENDING...
        message = self.to_send.get()
    
        if self.check_empty(message) != True and self.to_send.cget("fg") != "grey":
            self.send(message, self.m)

    def check_empty(self, tbc):
        c = 0
        for char in tbc:
            if char == " ":
                c = c + 1
        if len(tbc) == c:
            return True
        else:
            return False

    def receive_data(self):
        if self.m == "for name":
            recvd_header = self.client_socket.recv(self.HEADER)
            length = int(recvd_header.decode(self.FORMAT).strip())

            recvd_msg = self.client_socket.recv(length).decode(self.FORMAT)
            
            # if scram.decrypt(recvd_msg) == scram.entry_pass: # already checked
            lines = [f"Congratulations {self.my_username.get()}!", f"You have successfully connected to {self.SERVER}", "Welcome!"]
            messagebox.showinfo(title = "[CONNECTION SUCCESSFUL]", message = "\n".join(lines))
            self.m = "for msg"
            self.to_send.config(state = NORMAL)
            self.submit.config(state = NORMAL)

            self.to_send.insert(0, "Send a message to everyone")
            self.to_send.config(fg = "grey")

            self.show_msgs.config(state = NORMAL)
            self.show_msgs.insert(END, f"Welcome {self.call_me}!\n", ("center", "bold_font", "color_theme"))
            self.show_msgs.insert(END, f"You have joined the server {self.SERVER}\n\n", ("center", "norm_font", "white"))
            self.show_msgs.insert(END, f"Available Commands:\n", ("left", "bold_font", "color_theme"))
            self.show_msgs.insert(END, f"/peeps", ("left", "norm_font", "color_theme"))
            self.show_msgs.insert(END, f"                   - show everyone connected to the server\n", ("left", "norm_font", "white"))
            self.show_msgs.insert(END, f"/pmsg <target>: ", ("left", "norm_font", "color_theme"))
            self.show_msgs.insert(END, f"   - whisper/ private message\n\n", ("left", "norm_font", "white"))
            self.show_msgs.config(state = DISABLED)
            self.show_msgs.see(END)

        else:
            time.sleep(0.5)
            try:
                if not self.minimized:
                    for msg in self.follow_up_msgs:
                        a, b, c, d = msg
                        if a == "all":
                            self.normal_new_message((b, c, d))
                        elif a == "private":
                            self.private_new_message((b, c, d))
                    self.follow_up_msgs = []
            except AttributeError:
                pass

            username_header = self.client_socket.recv(self.HEADER)

            # If server closed, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                lines = ["Connection closed by the server"]
                self.custom_pop_up("[ERROR]", "\n".join(lines), ["Close", "Exit Server"], [self.exit_root, self.close_follow_up])
                self.useless_room("an error")
                self.connected = False
                self.screen.quit()
                sys.exit()

            username_length = int(username_header.decode(self.FORMAT).strip())

            self.user = self.client_socket.recv(username_length).decode(self.FORMAT)

            message_header = self.client_socket.recv(self.HEADER)
            message_length = int(message_header.decode(self.FORMAT).strip())
            self.message = self.client_socket.recv(message_length).decode(self.FORMAT)

            t = time.time()
            current_time = time.strftime('%H:%M', time.localtime(t))

            if scram.decrypt(self.message[0:len(scram.pm_code)]) == scram.pm_code:
                try:
                    if self.minimized:
                        self.icon.notify(self.message[len(scram.pm_code):len(self.message)], f"{self.user} whispered:")
                        self.follow_up_msgs.append(("private", self.user, current_time, self.message))
                    else:
                        self.private_new_message((self.user, current_time, self.message))
                except AttributeError:
                    self.private_new_message((self.user, current_time, self.message))
            
            elif scram.decrypt(self.message[0:len(scram.show_people_code) + 1]) == scram.show_people_code + "\n":
                self.show_msgs.config(state = NORMAL)
                self.show_msgs.insert(END, f"LIST OF USERS IN {self.SERVER}:\n\n", ("center", "bold_font", "color_theme"))
                self.show_msgs.insert(END, f"{self.message[len(scram.show_people_code) + 1:len(self.message)]}\n\n", ("center", "norm_font", "white"))
                self.show_msgs.config(state = DISABLED)
                self.show_msgs.see(END)

            elif scram.decrypt(self.message[0:len(scram.pm_error_code)]) == scram.pm_error_code:
                self.show_msgs.config(state = NORMAL)
                self.show_msgs.insert(END, "ERROR!\n", ("center", "bold_font", "red"))
                self.show_msgs.insert(END, f"User '{self.message[len(scram.pm_error_code):len(self.message)]}' could not be found\n\n", ("center", "norm_font", "red"))
                self.show_msgs.config(state = DISABLED)
                self.show_msgs.see(END)

            else:
                if self.user == scram.owner_tag:
                    self.show_msgs.config(state = NORMAL)
                    self.show_msgs.insert(END, f"{self.user} ", ("left", "bold_font", "white"))
                    self.show_msgs.insert(END, f"@{current_time}", ("left", "italic_font", "gray"))
                    self.show_msgs.insert(END, f":\n{self.message}\n\n", ("left", "norm_font", "white"))
                    self.show_msgs.config(state = DISABLED)
                    self.show_msgs.see(END)
                else:
                    try:
                        if self.minimized:
                            self.icon.notify(self.message, self.user)
                            self.follow_up_msgs.append(("all", self.user, current_time, self.message))
                        else:
                            self.normal_new_message((self.user, current_time, self.message))
                    except AttributeError:
                        self.normal_new_message((self.user, current_time, self.message))

    def normal_new_message(self, required):
        user, current_time, message = required

        self.show_msgs.config(state = NORMAL)
        self.show_msgs.insert(END, f"{user} ", ("left", "norm_font", "white"))
        self.show_msgs.insert(END, f"@{current_time}", ("left", "italic_font", "gray"))
        self.show_msgs.insert(END, f":\n{message}\n\n", ("left", "norm_font", "white"))
        self.show_msgs.config(state = DISABLED)
        self.show_msgs.see(END)

        if self.is_toplevel != True:
            self.pop_up()

    def private_new_message(self, required):
        user, current_time, message = required

        self.show_msgs.config(state = NORMAL)
        self.show_msgs.insert(END, f"{user} whispered", ("left", "italic_font", "white"))
        self.show_msgs.insert(END, f" @{current_time}", ("left", "italic_font", "gray"))
        self.show_msgs.insert(END, f":\n{message[len(scram.pm_code):len(message)]}\n\n", ("left", "norm_font", "white"))
        self.show_msgs.config(state = DISABLED)
        self.show_msgs.see(END) 
        
        if self.is_toplevel != True:
            self.pop_up()

    def is_toplevel(self):
        width, height, x, y = self.screen.winfo_width(), self.screen.winfo_height(), self.screen.winfo_rootx(), self.screen.winfo_rooty()

        if (width, height, x, y) != (1, 1, 0, 0):
            is_toplevel = self.screen.winfo_containing(x + (width // 2), y + (height // 2)) is not None

            return is_toplevel

    def send(self, data, mode):
        try:
            if mode == "for msg":
                t = time.time()
                current_time = time.strftime('%H:%M', time.localtime(t))
                
                message = data.encode(self.FORMAT)
                message_header = f"{len(message):<{self.HEADER}}".encode(self.FORMAT)
                self.client_socket.send(message_header + message)
                ####
                # self.qwerty = self.msgs.get()
                # self.qwerty += f"{self.my_username.get()} (You): \n{self.msg_var.get()}\n\n"
                # self.msgs.set(self.qwerty)
                #####
                self.show_msgs.config(state = NORMAL)
                self.show_msgs.insert(END, f"{self.my_username.get()} (You) ", ("left", "norm_font", "white"))               
                self.show_msgs.insert(END, f"@{current_time}", ("left", "italic_font", "gray"))
                self.show_msgs.insert(END, f":\n{data}\n\n", ("left", "norm_font", "white"))
                self.show_msgs.config(state = DISABLED)
                self.show_msgs.see(END)
                ####
                # self.msgs.set(f"{self.my_username.get()} (You): \n{self.msg_var.get()}\n\n")
                self.to_send.delete(0, "end")
                self.screen.geometry(f"{self.screen.winfo_width()}x{self.screen.winfo_height()}+{self.screen.winfo_x()}+{self.screen.winfo_y()}")
                self.screen.update()

            elif mode == "for name":
                username = data.encode(self.FORMAT)
                username_header = f"{len(username):<{self.HEADER}}".encode(self.FORMAT)
                self.client_socket.send(username_header + username)

        except ConnectionResetError:
            if not self.for_exit:
                lines = ["The server has stopped..."]
                messagebox.showerror(title = "[ERROR]", message = "\n".join(lines))
            self.connected = False
            self.screen.quit()
            sys.exit()

    def structure(self):
        color_theme = (0, 158, 96)
        base_texth = math.floor(self.new_wh("<Configure>")[1] / 10) >> 2
        # MAIN SCREEN
        self.for_msg_frame = Frame(self.screen, bg = "black")
        # Upper
        self.screen.update()
        self.msgs_frame = LabelFrame(self.for_msg_frame, relief = RIDGE)
        self.server_t = Label(self.for_msg_frame, text = "Server: ", font = ("Helvetica", base_texth, "bold"), fg = "#%02x%02x%02x" % color_theme, bg = "black", anchor = "e", relief = RIDGE)
        self.server = Entry(self.for_msg_frame, font = ("Helvetica", base_texth), fg = "#%02x%02x%02x" % color_theme, bg = "black", exportselection = 0, insertbackground = "#%02x%02x%02x" % color_theme)
        self.set_server = Button(self.for_msg_frame, text = "Set Server", font = ("Helvetica", base_texth, "bold"), fg = "#%02x%02x%02x" % color_theme, bg = "black", relief = RIDGE)
        self.username_t = Label(self.for_msg_frame, text = "Username: ", font = ("Helvetica", base_texth, "bold"), fg = "#%02x%02x%02x" % color_theme, bg = "black", anchor = "e", relief = RIDGE)
        self.username = Entry(self.for_msg_frame, font = ("Helvetica", base_texth), fg = "#%02x%02x%02x" % color_theme, bg = "black", exportselection = 0, insertbackground = "#%02x%02x%02x" % color_theme)
        self.set_user = Button(self.for_msg_frame, text = "Set Username", font = ("Helvetica", base_texth, "bold"), fg = "#%02x%02x%02x" % color_theme, bg = "black", relief = RIDGE, command = self.user_send)
        ### SPECIAL
        self.screen.update()
        self.show_msgs = Text(self.msgs_frame, relief = RAISED, font = ("Helvetica", math.floor(base_texth * 4/3)), bg = "black", fg = "white", wrap = WORD, state = DISABLED)
        self.msgs_scroll = Scrollbar(self.show_msgs, takefocus = 0)
        self.show_msgs.config(yscrollcommand = self.msgs_scroll.set)
        self.msgs_scroll.config(command = self.show_msgs.yview)
        ### SPECIAL
        # self.show_msgs = Label(self.msgs_frame, textvariable = self.msgs, relief = RAISED, justify = LEFT, anchor = "nw", font = ("Helvetica", 12), bg = "black", fg = "white")        
        # 14 for full screen
        # Lower
        self.to_send = Entry(self.for_msg_frame, textvariable = self.msg_var, font = ("Helvetica", base_texth), exportselection = 0, state = DISABLED)
        self.submit = Button(self.for_msg_frame, text = "SUBMIT!", relief = RAISED, font = ("Helvetica", base_texth, "bold"), bg = "#%02x%02x%02x" % color_theme, command = self.send_data, state = DISABLED)
        self.screen.update()
        # SHOW ALL WIDGETS
        self.for_msg_frame.pack(fill = BOTH, expand = True)
        self.msgs_frame.place(relwidth = 0.98, relheight = 0.78, relx = 0.01, rely = 0.11)
        self.to_send.place(relwidth = 0.83, relheight = 0.10, relx = 0.01, rely = 0.89)
        self.submit.place(relwidth = 0.15, relheight = 0.10, relx = 0.84, rely = 0.89)
        self.username_t.place(relwidth = (Decimal(0.98 / 3) / 2), relheight = 0.05, relx = 0.01, rely = 0.06)
        self.username.place(relwidth = (Decimal(0.98 / 3)) * 7 / 4, relheight = 0.05, relx = (Decimal(0.98 / 3)) / 2 + Decimal(0.01), rely = 0.06)
        self.set_user.place(relwidth = (Decimal(0.98 / 3)) * 3 / 4, relheight = 0.05, relx = (Decimal(0.98 / 3)) * 9 / 4 + Decimal(0.01), rely = 0.06)
        self.server_t.place(relwidth = (Decimal(0.98 / 3)) / 2, relheight = 0.05, relx = 0.01, rely = 0.01)
        self.server.place(relwidth = (Decimal(0.98 / 3)) * 7 / 4, relheight = 0.05, relx = (Decimal(0.98 / 3)) / 2 + Decimal(0.01), rely = 0.01)
        self.set_server.place(relwidth = (Decimal(0.98 / 3)) * 3 / 4, relheight = 0.05, relx = (Decimal(0.98 / 3)) * 9 / 4 + Decimal(0.01), rely = 0.01)
        self.show_msgs.pack(expand = True, fill = BOTH)
        self.msgs_scroll.pack(side = RIGHT, fill = Y)
        self.screen.update()
        # Text Tags
        self.show_msgs.tag_configure("center", justify = "center")
        self.show_msgs.tag_configure("left", justify = "left")
        self.show_msgs.tag_configure("norm_font", font = ("Helvetica", math.floor(base_texth * 4/3)))
        self.show_msgs.tag_configure("bold_font", font = ("Helvetica", math.floor(base_texth * 4/3), "bold"))
        self.show_msgs.tag_configure("italic_font", font = ("Helvetica", math.floor(base_texth * 4/3), "italic"))
        self.show_msgs.tag_configure("white", foreground = "white")
        self.show_msgs.tag_configure("color_theme", foreground = "#%02x%02x%02x" % color_theme)
        self.show_msgs.tag_configure("gray", foreground = "gray")
        self.show_msgs.tag_configure("red", foreground = "red")
        # BIND
        self.to_send.bind("<FocusIn>", self.click_send_area)
        self.to_send.bind("<FocusOut>", self.away_send_area)
        
    def size_update(self, event):
        self.new_wh(event)
        self.widgetwh(self.to_send)
        self.configs()

    def new_wh(self, event):
        self.screen.update()
        return [self.screen.winfo_width(), self.screen.winfo_height()]

    def widgetwh(self, widget):
        widget.update()
        return [widget.winfo_width(), widget.winfo_height()]

    def configs(self):
        self.bottom_size(self.to_send)
        self.bottom_size(self.submit)
        self.bottom_size(self.username_t)
        self.bottom_size(self.username)
        self.bottom_size(self.set_user)
        self.bottom_size(self.server_t)
        self.bottom_size(self.server)
        self.bottom_size(self.set_server)
        # self.bottom_size(self.show_msgs)

    def bottom_size(self, widget):
        if widget == self.to_send or widget == self.username or widget == self.server:
            widget.config(font = ("Helvetica", (self.widgetwh(self.to_send)[1] >> 2)))
        else:
            widget.config(font = ("Helvetica", (self.widgetwh(self.to_send)[1] >> 2), "bold"))

    def click_send_area(self, event):
        if self.to_send.cget("fg") == "grey":
            self.to_send.delete(0, "end")
            self.to_send.insert(0, "")
            self.to_send.config(fg = "black")

    def away_send_area(self, event):
        if self.to_send.get() == "":
            self.to_send.insert(0, "Send a message to everyone")
            self.to_send.config(fg = "grey")

    def on_closing(self):
        try:
            self.icon.stop()
            self.screen.after(0, self.screen.deiconify)
        except AttributeError:
            pass

        lines = [f"You have successfully disconnected from {self.SERVER}"]
        messagebox.showinfo(title = "[DISCONNECT]", message = "\n".join(lines))
        self.connected = False
        # self.to_recv_data.join()
        self.screen.quit()
        os._exit(0)
        # sys.exit()

    def new_win(self):
        t = time.time()
        current_time = time.strftime('%H:%M', time.localtime(t))

        self.REPLY = "Roger"

        self.screendimx2 = self.var_x >> 1
        self.screendimy2 = self.var_y >> 1
        self.screenw2 = self.def_w >> 1
        self.screenh2 = self.def_h >> 1
        self.root = Tk()
        ##### ##### PIN!!! FUTURE ME! This is equal to exact center ---------------------------------
        self.root.geometry(f"{self.screenw2}x{self.screenh2}+{(self.screendimx2) - (self.screenw2 >> 1)}+{(self.screendimy2) - (self.screenh2 >> 1)}")
        ##### ##### PIN!!! FUTURE ME! This is equal to exact center ---------------------------------
        self.pop_up_msg = Text(self.root, relief = RAISED, font = ("Helvetica", 12), bg = "black", fg = "white", wrap = WORD)
        self.open_window = Button(self.root, text = "See in Context", relief = RAISED, font = ("Helvetica", 9), bg = "black", fg = "white", command = self.context_see)
        self.close = Button(self.root, text = "Close", relief = RAISED, font = ("Helvetica", 9), bg = "black", fg = "white", command = self.exit_root)
        self.auto_reply = Button(self.root, text = f"Auto-Reply '{self.REPLY}'", relief = RAISED, font = ("Helvetica", 9), bg = "black", fg = "white", command = self.reply)
        self.quick_replier = Button(self.root, text = f"Quick Reply", relief = RAISED, font = ("Helvetica", 9), bg = "black", fg = "white", command = self.quick_reply)
        ###
        self.pop_up_msg.place(relwidth = 1, relheight = 0.6)
        self.quick_replier.place(relwidth = 1, relheight = 0.1, rely = 0.6)
        self.open_window.place(relwidth = 1, relheight = 0.1, rely = 0.7)
        self.auto_reply.place(relwidth = 1, relheight = 0.1, rely = 0.8)
        self.close.place(relwidth = 1, relheight = 0.1, rely = 0.9)
        
        self.pop_up_msg.tag_configure("italic_font", font = ("Helvetica", 12, "italic"))
        self.pop_up_msg.tag_configure("gray", foreground = "gray")

        if scram.decrypt(self.message[0:len(scram.pm_code)]) == scram.pm_code:
            self.pop_up_msg.insert(END, f"~New Private Message!~", ("left", "italic_font", "white"))
            self.pop_up_msg.insert(END, f" @{current_time}", ("left", "italic_font", "gray"))    
            self.pop_up_msg.insert(END, f"\n\nFrom {self.user}: \n{self.message[len(scram.pm_code):len(self.message)]}", ("left", "norm_font", "white"))
        else:
            self.pop_up_msg.insert(END, f"New Message!", ("left", "norm_font", "white"))
            self.pop_up_msg.insert(END, f" @{current_time}", ("left", "italic_font", "gray"))
            self.pop_up_msg.insert(END, f"\n\nFrom {self.user}: \n{self.message}", ("left", "norm_font", "white"))
        
        self.pop_up_msg.config(state = DISABLED)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', 1)
        self.root.mainloop()

    def context_see(self):
        self.root.destroy()
        self.screen.attributes('-topmost', 1)
        self.screen.attributes('-topmost', 0)

    def reply(self):
        self.root.destroy()
        self.to_send.delete(0, "end")

        if scram.decrypt(self.message[0:len(scram.pm_code)]) == scram.pm_code:
            self.to_send.insert(0, f"/pmsg <{self.user}>: {self.REPLY}")
        else:
            self.to_send.insert(0, f"{self.REPLY}")
        
        self.to_send.config(fg = "black")
        self.send_data()
        self.to_send.insert(0, "Send a message to everyone")
        self.to_send.config(fg = "grey")

    def quick_reply(self):
        self.root.destroy()
        
        self.to_send.delete(0, "end")

        self.screen.attributes('-topmost', 1)
        self.screen.attributes('-topmost', 0)

        self.to_send.focus()

        if scram.decrypt(self.message[0:len(scram.pm_code)]) == scram.pm_code:
            self.to_send.insert(0, f"/pmsg <{self.user}>: ")
        
        self.to_send.config(fg = "black")

    def exit_root(self):
        self.root.destroy()

    def pop_up(self):
        winsound.PlaySound("alarm.wav", winsound.SND_ASYNC)
        self.new_win()

    def custom_window(self, prompt, message, choices, respective_functions):
        color_theme = (0, 158, 96)
        self.screendimx2 = self.var_x >> 1
        self.screendimy2 = self.var_y >> 1
        self.screenw2 = self.def_w >> 1
        self.screenh2 = self.def_h >> 1
        self.root = Tk()
        ##### ##### PIN!!! FUTURE ME! This is equal to exact center ---------------------------------
        self.root.geometry(f"{self.screenw2}x{self.screenh2}+{(self.screendimx2) - (self.screenw2 >> 1)}+{(self.screendimy2) - (self.screenh2 >> 1)}")
        ##### ##### PIN!!! FUTURE ME! This is equal to exact center ---------------------------------
        self.pop_up_msg = Text(self.root, relief = RAISED, font = ("Helvetica", 12), bg = "black", fg = "white", wrap = WORD)
        
        length = 1 - (len(choices) / 10)
        
        self.pop_up_msg.place(relwidth = 1, relheight = length)
        
        for choice in range(len(choices)):
            self.new_choice = Button(self.root, text = choices[choice], relief = RAISED, font = ("Helvetica", 9), bg = "black", fg = "white", command = respective_functions[choice])
            self.new_choice.place(relwidth = 1, relheight = 0.1, rely = length)
            length += 0.1

        ###        
        self.pop_up_msg.tag_configure("bold_font", font = ("Helvetica", 12, "bold"))
        self.pop_up_msg.tag_configure("color_theme", foreground = "#%02x%02x%02x" % color_theme)
        
        self.pop_up_msg.insert(END, prompt, ("bold_font", "color_theme"))
        self.pop_up_msg.insert(END, f"\n{message}")
    
        self.pop_up_msg.config(state = DISABLED)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', 1)
        self.root.mainloop()

    def useless_room(self, reason):
        self.show_msgs.config(state = NORMAL)
        self.show_msgs.insert(END, "Attention!\n", ("center", "bold_font", "red"))
        self.show_msgs.insert(END, f"Due to {reason}, the chatroom is now rendered functionless", ("center", "norm_font", "red"))
        self.show_msgs.insert(END, "\nPlease manually exit", ("center", "norm_font", "red"))
        self.show_msgs.insert(END, "\nYou may also stay if you wish, although no functionalities will be accessed", ("center", "norm_font", "red"))
        self.show_msgs.config(state = DISABLED)
        self.show_msgs.see(END)

    def close_follow_up(self):
        self.root.destroy()
        self.to_send.delete(0, "end")
        self.to_send.insert(0, "error_exit")
        self.to_send.config(fg = "black")
        
        self.for_exit = True

        self.submit.invoke()

    def custom_pop_up(self, prompt, message, choices, respective_functions):
        winsound.PlaySound("alarm.wav", winsound.SND_ASYNC)
        self.custom_window(prompt, message, choices, respective_functions)

    def show_window(self):
        self.icon.stop()
        self.screen.after(0, self.screen.deiconify)
        self.minimized = False

    def tray_min(self):
        self.screen.withdraw()
        self.minimized = True
        self.follow_up_msgs = []

        image = Image.open("image.ico")
        test = pystray.Menu(item('Quit', self.on_closing), item('Show', self.show_window, default = True))
        self.icon = pystray.Icon("Name", image, "Local Messenger", test)
        self.icon.run()

















if __name__ == "__main__":
    Initialize_Chat()






