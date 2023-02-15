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

GROUP = 0

IP = '192.168.1.221'
PORT = 9559

#LANGUAGE = "English"
LANGUAGE = "Polish"


POSTURES = ['Stand', 'SitRelax', 'Crouch', 'LyingBack', 'LyingBelly', 'StandInit', 'StandZero']

#proxtName (str): name of proxy we want to get
#returns: proxy for given proxyName, set NAO IP and PORT
def getProxy(proxyName):
    if (proxyName == None):
        print("func 'getProxy(proxyName)' lacking arg proxyName")
        raise Exception("func 'ALProxy(proxyName, ip, port)' failed for empty proxyName")
    try:
        proxy = ALProxy(proxyName, IP, PORT)
    except:
        print("Could not get proxy: " + proxyName)
    else:
        return proxy

#initiates all needed AL proxies
def setProxies():
    global textToSpeech
    global animatedSpeech
    global robotPosture
    global videoService
    global animationPlayer
    global systemProxy
    global autonomousLife
    global leds
    global motion
 

    textToSpeech = getProxy("ALTextToSpeech")
    animatedSpeech = getProxy("ALAnimatedSpeech")
    robotPosture = getProxy("ALRobotPosture")
    animationPlayer = getProxy("ALAnimationPlayer")
    videoService = getProxy("ALVideoDevice")
    autonomousLife = getProxy("ALAutonomousLife")
    systemProxy = getProxy("ALSystem")
    leds = getProxy("ALLeds")
    motion = getProxy("ALMotion")

    


#posture (str): a posture which will be applied to NAO
#   possible values: ['Crouch', 'LyingBack', 'LyingBelly', 'SitRelax', 'Stand', 'StandInit', 'StandZero']
def setPosture(posture):
    if (posture == None):
        print("func 'setPosture(posture, speed)' lacking arg 'posture'")
        return
    elif (not posture in POSTURES):
        print("func 'setPosture(posture, speed)' arg 'posture' has unsupported value")
        return
    speed = 0.4
    robotPosture.goToPosture(posture, speed)


#sets a default voice
def defaultVoice():
    textToSpeech.setVoice("naoenu")
    textToSpeech.setParameter("pitchShift", 1.1)
    textToSpeech.setParameter("speed", 85)
    textToSpeech.setParameter("doubleVoice", 0)
    textToSpeech.setParameter("doubleVoiceLevel", 0)
    #reset leds
    leds.fadeRGB("FaceLeds", "white",0.2)
    

#changes NAOs posture to standing if it wasnt before
def setStandingPosture():
    if (robotPosture.getPosture() != "Stand"):
        setPosture("Stand")


#sets Speech speed and language preferences
def setSpeechSettings():
    animatedSpeech.setBodyLanguageModeFromStr("contextual")
    textToSpeech.setLanguage(LANGUAGE)
    defaultVoice()

#language (str): str representing the language for NAO to speak
#   possible values: ['Polish', 'English']
def setLanguage(language):
    if (language == None):
        print("func 'setLanguage(language)' lacking arg 'language'")
        return
    textToSpeech.setLanguage(language)
    LANGUAGE = language
    print("Language changed to: " + LANGUAGE)

def setTags():
    
    tagToAnims = {}
   
    for i in animations:
        if (i.path != None) and (i.path != "Movements"):
            tagToAnims[i.tag] = [i.path]
    
    animationPlayer.addTagForAnimations(tagToAnims)


def setNAO():
    
    try:
        setProxies()
        setLanguage(LANGUAGE)
        setSpeechSettings()
        setTags()
        setStandingPosture()
        autonomousLife.setState("solitary")
        motion.setExternalCollisionProtectionEnabled("All",True)
        
    except BaseException as err:
        print("Error:")
        print(err)

class App:
    def __init__(self, window, window_title):
       
        setNAO()

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
        
        
        #top frame (consits of top left and top right frame)
        topFrame = tk.Frame(self.canvas, bg =self.bgColor, bd = 0)
        topFrame.pack(expand = True, fill = tk.X, side = tk.TOP)
        #top left frame (consists of 'language' and 'tutorial' butttons)
        topLeftFrame = tk.Frame(topFrame, bg =self.bgColor, bd = 0)
        topLeftFrame.pack( expand = True, fill = tk.X,side = tk.LEFT, padx = (30,30), pady = (30,30))
        
        
        #top right frame (consists of 'IP' and 'Shut down' butttons)
        topRightFrame = tk.Frame(topFrame, bg =self.bgColor, bd = 0)
        topRightFrame.pack(padx = (30,30), pady = (30,30),expand = True, fill = tk.X, side = tk.RIGHT)
        
        #ShutDown
        imShutDown = PIL.Image.open("shutDown.png")
        imShutDown = imShutDown.resize((25,25))
        imShutDown =  PIL.ImageTk.PhotoImage(imShutDown)
        shutDownBut = tk.Button(topRightFrame, bd = 0, bg =self.bgColor,image = imShutDown, activebackground =self.lightGrey)
        shutDownBut.configure(command = self.turnOff)
        shutDownBut.pack(side=tk.RIGHT, padx = (30,0))
        
        #IP
        ipBorder = tk.Frame(topRightFrame, bg="white", bd = 0 )
        ipBorder.pack(side = tk.RIGHT, fill = tk.X, padx = (10,0))
        IPLabelText = "Change IP"
        butIp = tk.Button(ipBorder,text = IPLabelText, bd = 0, command = self.changeIP, bg =self.lightGrey,fg = "white",font = ("Verdana", 10),padx = 3)
        butIp.pack(pady = (1,1), padx = (1,1), fill = tk.X)
        

        #bottom frame (consists of: collumn right, collumn middle)
        bottomFrame = tk.Frame(self.canvas, bg=self.bgColor, bd = 0)
        bottomFrame.pack(expand = True,fill = tk.BOTH, side = tk.BOTTOM)
    
        #left collumn of bottom frame (cnsists of 'custom commands butttons' and )
        leftCol = tk.Frame(bottomFrame, bg=self.bgColor, bd = 0)
        leftCol.pack(pady = (10,30), padx = (30,30), side = tk.LEFT, fill = tk.BOTH)
        # buttons with phrases to be spoken by NAO
        buttonsLabel = tk.Label(leftCol,text= "What NAO can say:", bg =self.bgColor, font = ("Verdana", 10), fg = "white")
        buttonsLabel.pack(fill = tk.BOTH, pady = (0,5))
        
        leftColButtons = tk.Text(leftCol, bg =self.bgColor, bd = 0, cursor = 'arrow' )
        leftColButtons.pack(side = tk.TOP,expand = True, fill = tk.BOTH)
       
        
        #=========================== Commands ==============================

        self.commands = ["x"]

        introBut = tk.Button(leftColButtons,text =self.commands[0],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        introBut.configure(command = lambda: self.executeCommand(self.commands[0]))
        introBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
        
    
        
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
      
    #Turn off the robot    
    def turnOff(self):
        tkMessageBox.askquestion("Turn off NAO", "Are you sure you want to turn off the robot?")
        systemProxy.shutdown()
        print("Bye bye NAO")
        self.destroy()
           
    
    
    # ====================================================================================================
      
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
App(tk.Tk(), "Wizard of Oz for NAO")

