# -*- encoding: UTF-8 -*-
from tabnanny import check
from timeit import repeat
#from naoqi import ALProxy
import sys
import time
from turtle import bgcolor
import PIL.Image, PIL.ImageTk
import Tkinter as tk
import ttk
import tkMessageBox
import random
from animations import animations, getIndex

import interface_WoOz as IWO

IP = '192.168.1.221'
PORT = 9559
LANGUAGE = "Polish"
PROGRAM = 1


class App:
    def __init__(self, window, window_title):
       
        IWO.setNAO()

        self.window = window
        self.window.title(window_title)


        #colors
        self.bgColor = '#303841' #dark grey
        self.lightGrey = '#3a4750' #dark grey
        self.lightLightGrey = '#f5f5f5' #offwhite
        self.greenCol = '#64a225'  #light green
        self.offWhite = '#E0E2E2' #ofwhite
        self.greenGrey = "#8d989c"
        self.pinkCol = "#936A7C"
        self.redCol = "#F56141"
        self.blueCol = "#5178AF"

        
        self.colorOff = "white"
        self.colorOn = "#64a225"
       
        
        self.window.minsize(height = 700, width = 900)
        self.window.geometry("900x700")
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, bg =self.bgColor, bd = 0)
        self.canvas.pack(expand = True, fill = tk.BOTH, side = tk.LEFT)
        

        #top right frame (consists of 'IP' buttton)
        topRightFrame = tk.Frame(topFrame, bg =self.bgColor, bd = 0)
        topRightFrame.pack(padx = (30,30), pady = (30,30),expand = True, fill = tk.X, side = tk.RIGHT)
        

        #IP
        ipBorder = tk.Frame(topRightFrame, bg="white", bd = 0 )
        ipBorder.pack(side = tk.RIGHT, fill = tk.X, padx = (10,0))
        IPLabelText = "Change IP"
        butIp = tk.Button(ipBorder,text = IPLabelText, bd = 0, command = self.changeIP, bg =self.lightGrey,fg = "white",font = ("Verdana", 10),padx = 3)
        butIp.pack(pady = (1,1), padx = (1,1), fill = tk.X)
        

        #bottom frame
        bottomFrame = tk.Frame(self.canvas, bg=self.bgColor, bd = 0)
        bottomFrame.pack(expand = True,fill = tk.BOTH, side = tk.BOTTOM)
    
        #left collumn of bottom frame (cnsists of 'custom commands butttons' and )
        leftCol = tk.Frame(bottomFrame, bg=self.bgColor, bd = 0)
        leftCol.pack(pady = (10,30), padx = (30,30), side = tk.LEFT, fill = tk.BOTH)
        # buttons with phrases to be spoken by NAO
        buttonsLabel = tk.Label(leftCol, bg =self.bgColor, font = ("Verdana", 10), fg = "white")
        buttonsLabel.pack(fill = tk.BOTH, pady = (0,5))
        
        leftColButtons = tk.Text(leftCol, bg =self.bgColor, bd = 0, cursor = 'arrow' )
        leftColButtons.pack(side = tk.TOP,expand = True, fill = tk.BOTH)
       
        
        #=========================== Buttons ==============================

        self.commands = getCommands(PROGRAM)

        introBut = tk.Button(leftColButtons,text =self.commands[0],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        introBut.configure(command = lambda: self.executeCommand(self.commands[0]))
        introBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)

        r1But = tk.Button(leftColButtons,text =self.commands[1],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        r1But.configure(command = lambda: self.dialog(self.commands[1]))
        r1But.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)

        r2But = tk.Button(leftColButtons,text =self.commands[2],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        r2But.configure(command = lambda: self.dialog(self.commands[2]))
        r2But.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)

        r3But = tk.Button(leftColButtons,text =self.commands[3],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        r3But.configure(command = lambda: self.dialog(self.commands[3]))
        r3But.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)

        r4But = tk.Button(leftColButtons,text =self.commands[4],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        r4But.configure(command = lambda: self.dialog(self.commands[4]))
        r4But.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)

        r5But = tk.Button(leftColButtons,text =self.commands[5],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        r5But.configure(command = lambda: self.dialog(self.commands[5]))
        r5But.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
        
        
        window.mainloop()

    
    #Change IP
    def confirmIP(self,textField, IPwindow):
        global IP
        getIP = textField.get()
        IP = getIP
        print("IP changed to "+IP)
        setNAO()
        IPwindow.destroy()

    #Add commands for NAO to say - opens new window
    def changeIP(self):
        ipWindow = tk.Toplevel(self.window, bg = self.greenGrey)
        ipWindow.geometry("250x150")
        ipWindow.title("Change IP address")
        ipWindow.overrideredirect(1) #Remove border
        #position toplevel window on top of the main window
        x = self.window.winfo_x()
        y = self.window.winfo_y()

        ipWindow.geometry("+%d+%d" %(x+500,y+200))
        
        #Create border
        windowBorder = tk.Frame(ipWindow, bg = self.lightGrey, bd = 1, relief = tk.RAISED)
        windowBorder.pack(expand = True, fill = tk.BOTH)
        addCanvas = tk.Frame(windowBorder, bg = self.bgColor)
        addCanvas.pack(expand = True, fill = tk.BOTH, pady = (1,1), padx = (1,1))
        #top frame - label
        topFrame = tk.Frame(addCanvas, bg = self.bgColor)
        topFrame.pack(side = tk.TOP)
        # Create label
        label = tk.Label(topFrame,text = "Change IP address:",bg = self.bgColor, font = ("Verdana", 10), fg = "white")
        label.pack(pady = (30,10))
        #middle frame - text
        midFrame = tk.Frame(addCanvas, bg = self.bgColor)
        midFrame.pack()
        # text input - IP
        global IP
        textField = tk.Entry(midFrame,  width = 20, font = ("Verdana", 10))
        textField.insert(tk.END,IP)
        textField.pack()
        
        # bottom frame - Add and Cancel buttons
        bottomFrame = tk.Frame(addCanvas, bg = self.bgColor)
        bottomFrame.pack(side = tk.BOTTOM, fill = tk.X, expand = True)
        cancelBut = tk.Button(bottomFrame, text = "Cancel",command = ipWindow.destroy, bd = 0, bg = self.lightGrey,font = ("Verdana", 10), fg = "white", padx = 20 )
        cancelBut.pack(side = tk.LEFT, pady = (10,20), padx = (20, 0),fill = tk.X)
        okBut = tk.Button(bottomFrame, text = "Ok",bd = 0, bg = self.lightGrey,font = ("Verdana", 10), fg = "white", padx = 30 )
        okBut.configure(command = lambda: self.confirmIP(textField, ipWindow))
        okBut.pack(side = tk.RIGHT, pady = (10,20), padx = (0, 20), fill = tk.X)
        
        ipWindow.mainloop()
     
    #Execute commands
    def executeCommand(self, command):
        if command == "Introduction":
            animatedSpeech.say("Hello!,")
            animationPlayer.runTag("Hey_1")
            animatedSpeech.say("Nice to meet you all!")
            animatedSpeech.say("I think I already know some of you!")
            animatedSpeech.say("Thank you for letting me come here to play with you today!")
            animatedSpeech.say("Would you like to see what robots can do?")
            time.sleep(3)
            animatedSpeech.say("Look at my robotic moves!,")
            animationPlayer.runTag("Robot_1")
            time.sleep(3)
            animatedSpeech.say("I really enjoy juggling.,")
            animationPlayer.runTag("AirJuggle_1")
            animatedSpeech.say("Can you juggle?, I definitely can!,")
            time.sleep(3)
            animatedSpeech.say("I can drive a car!, Look!,")
            animationPlayer.runTag("DriveCar_1")
            animatedSpeech.say("Sometimes others can't drive as well as me.,")
            time.sleep(3)
            animatedSpeech.say("I love to take pictures!,")
            animationPlayer.runTag("TakePicture_1")
            time.sleep(3)
            animatedSpeech.say("I also love to play guitar!")
            animationPlayer.runTag("AirGuitar_1")
            time.sleep(3)

            animatedSpeech.say("And what are your skills?, What do you like to do?")
        elif command == 'Farewell':
            animatedSpeech.say("Thank you for playing with me today!") 
            animatedSpeech.say("It was a great pleasure to meet all of you!")
            animationPlayer.runTag("LoveYou_1")
            animatedSpeech.say("I hope we will meet together again!")
            animatedSpeech.say("Good bye!")
            animationPlayer.runTag("Hey_1")
        elif command == "Ask for charger":
            i = random.randint(0,2)
            if i == 0:
                textToSpeech.say("Could somebody plug my charger in, please?")
            elif i == 1:
                textToSpeech.say("Excuse me, my battery is low, could someone, plug my charger in, please?")
        elif command == 'Pet Miro':
            animatedSpeech.say("What a cutie!")
            try:
                motion.angleInterpolationBezier(namesMiro, timesMiro, keysMiro)
            except BaseException as err:
                print("Error: ")
                print(err)
            animatedSpeech.say("Good boy!")
            
        elif command == "Phrase in French":
            setLanguage("Polish")

            i = random.randint(0,2)
            if i == 0:
                animatedSpeech.say("Bą żur")
            elif i == 1:
                animatedSpeech.say("Kel bel żurne nuzawą ożordui!")
            else:
                animatedSpeech.say("Komo, sawa?")

            setLanguage(LANGUAGE)
          
        elif command == "Phrase in German":
            setLanguage("Polish")
            i = random.seed(2)
            if i == 0:
                animatedSpeech.say("Hallo, wij gejts ir?")
            elif i == 1:
                animatedSpeech.say("Majn Name ist NAO.")
            else:
                animatedSpeech.say("Ales hat ajnen ende, nur dij wurst hat cwaj.")
            setLanguage(LANGUAGE)
         
        elif command == "Phrase in Japanese":
            setLanguage("Polish")
            i = random.randint(0,1)
            if i == 0:
                animatedSpeech.say("konniczuła")
            elif i == 1:
                animatedSpeech.say("arigato gozajimasu")
            setLanguage(LANGUAGE)


# Create a window and pass it to the Application object
App(tk.Tk(), "NAO na scenie! Grupa " + PROGRAM)

