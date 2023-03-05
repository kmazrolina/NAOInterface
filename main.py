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
import theaterAnimTags as ta
import animations_build as ab
import group_projects

GROUP = '4'

IP = '192.168.0.221'
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
    global audioPlayer
 

    textToSpeech = getProxy("ALTextToSpeech")
    animatedSpeech = getProxy("ALAnimatedSpeech")
    robotPosture = getProxy("ALRobotPosture")
    animationPlayer = getProxy("ALAnimationPlayer")
    videoService = getProxy("ALVideoDevice")
    autonomousLife = getProxy("ALAutonomousLife")
    systemProxy = getProxy("ALSystem")
    leds = getProxy("ALLeds")
    motion = getProxy("ALMotion")
    audioPlayer = getProxy("ALAudioPlayer")

    


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
   
    for i in ab.animations:
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
        try:
            setLanguage('Polish')
        except BaseException as err:
            print("Error:")
            print(err)

        self.window = window
        self.window.title(window_title)


        #colors
        self.bgColor = '#2A2A2A' #dark grey
        self.lightGrey = '#3a4750' #dark grey
        self.lightLightGrey = '#f5f5f5' #offwhite
        self.greenCol = '#64a225'  #light green
        self.offWhite = '#E0E2E2' #offwhite
        self.greenGrey = "#8d989c"
        self.pinkCol = "#936A7C"
        self.redCol = "#F56141"
        self.blueCol = "#5178AF"

        
        self.colorOff = "white"
        self.colorOn = "#64a225"
       
    
        self.window.minsize(height = 800, width = 1100)
        self.window.geometry("1100x800")
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, bg =self.bgColor, bd = 0)
        self.canvas.pack(expand = True, fill = tk.BOTH, side = tk.LEFT)
        

        #top frame
        topFrame = tk.Frame(self.canvas, bg =self.bgColor, bd = 0)
        topFrame.pack(fill = tk.BOTH, side = tk.TOP, pady = (20,10), padx = (20,20))
        
        
        #IP
        ipBorder = tk.Frame(topFrame, bg="white", bd = 0 )
        ipBorder.pack(side = tk.RIGHT, fill = tk.X, padx = (0,10))
        IPLabelText = "Change IP"
        butIp = tk.Button(ipBorder,text = IPLabelText, bd = 0, command = self.changeIP, bg =self.lightGrey,fg = "white",font = ("Verdana", 10),padx = 3)
        butIp.pack(pady = (1,1), padx = (1,1), fill = tk.X)
        

        #bottom frame 
        bottomFrame = tk.Frame(self.canvas, bg=self.bgColor, bd = 0)
        bottomFrame.pack(expand = True,fill = tk.BOTH, side = tk.TOP)
        # buttons with animations
        buttonsLabel = tk.Label(bottomFrame,text= "Grupa " + GROUP, bg =self.bgColor, font = ("Verdana", 12), fg = "white")
        buttonsLabel.pack(fill = tk.BOTH, pady = (0,5))


        #left collumn of bottom frame
        leftCol = tk.Frame(bottomFrame, bg=self.bgColor, bd = 0)
        leftCol.pack(pady = (10,10), padx = (20,20), side = tk.LEFT, fill = tk.BOTH)
        #center collumn of bottom frame
        centerCol = tk.Frame(bottomFrame, bg=self.bgColor, bd = 0)
        centerCol.pack(pady = (10,10), padx = (20,20), side = tk.LEFT, fill = tk.BOTH)
        #left collumn of bottom frame
        rightCol = tk.Frame(bottomFrame, bg=self.bgColor, bd = 0)
        rightCol.pack(pady = (10,10), padx = (20,20), side = tk.LEFT, fill = tk.BOTH)
        
        
       
        
        #=========================== Commands ==============================
        self.commands = group_projects.commands[int(GROUP)-1]

        commandCounter = 0
        
        
        for i in self.commands:
            
            try:
                #przyciski z obrazkami
                if commandCounter <= 4 :
                    button = tk.Button(leftCol,  bd = 0, bg = self.bgColor, activebackground = self.bgColor)
                elif commandCounter <= 8:
                    button = tk.Button(centerCol, bd = 0,bg = self.bgColor, activebackground = self.bgColor )
                else:
                    button = tk.Button(rightCol, bd = 0,bg = self.bgColor, activebackground = self.bgColor)
                path = "button_graphics\\" +group_projects.commands_no_utf[int(GROUP)-1][self.commands.index(i)] +".png"
                butIm = PIL.Image.open(path)
                butIm = butIm.resize((476,100))
                butIm =  PIL.ImageTk.PhotoImage(butIm)
                button.configure(image = butIm)
                button.image = butIm
            except BaseException as e:
                #przyciski bez obrazkow
                print(e)
                if commandCounter <= 4 :
                    button = tk.Button(centerCol,text = i,  bd = 0, bg = ta.animTags[ta.getIndex( ta.animTags, i )][2], fg = "white", font = ("Verdana", 12), padx = 100, pady = 10)
                elif commandCounter <= 8:
                    button = tk.Button(centerCol,text = i,  bd = 0, bg = ta.animTags[ta.getIndex( ta.animTags, i )][2], fg = "white", font = ("Verdana", 12), padx = 100, pady = 10)
                else:
                    button = tk.Button(rightCol,text = i,  bd = 0, bg = ta.animTags[ta.getIndex( ta.animTags, i )][2], fg = "white", font = ("Verdana", 12), padx = 100, pady = 10)
            
            button.configure(command = lambda i=i: self.executeCommand(i))
            button.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
            commandCounter = commandCounter + 1
    
        
        window.mainloop()

     
    #Change IP
    def confirmIP(self,textField, IPwindow):
        global IP
        getIP = textField.get()
        IP = getIP
        print("IP changed to "+IP)
        setNAO()
        IPwindow.destroy()

  
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
      

           
    # ====================================================================================================
      
    def executeMovement(self, movementTag):

            i = ab.getIndex(ab.animations, movementTag)
       
            names = ab.animations[i].movement[0]
            times = ab.animations[i].movement[1]
            keys = ab.animations[i].movement[2]   

            print(movementTag)
            if movementTag == 'Dead':
                try:
                    leds.setIntensity("AllLeds", 0)
                except BaseException as err:
                    print(err)
            try:
                motion.post.angleInterpolationBezier(names, times, keys)
            except BaseException as err:
                print(err)
            if movementTag == 'Dead':
                try:
                    leds.setIntensity("AllLeds", 1)
                except BaseException as err:
                    print(err)

            
            
            

            

    #Execute commands
    def executeCommand(self, command):
        

        if command == 'trąbka':
            try:
                animatedSpeech.say("^run(trumpet-89fce9/trumpet_dir) ^wait(trumpet-89fce9rumpet/trumpet_dir)")
                
            except BaseException as err:
                print("Error:")
                print(err)
            try:
                leds.on("AllLeds")
            except BaseException as err:
                print(err)
        elif command == 'picie':
            try:
                animatedSpeech.say("^run(drink-695af8/drink_dir) ^wait(drink-695af8/drink_dir)")
            except BaseException as err:
                print("Error:")
                print(err)
        elif command == 'ptak':
            self.executeMovement('Bird')
        elif command == 'śmierć':
            self.executeMovement('Dead')
        elif command == 'diabeł':
            try:
                leds.fadeRGB("AllLeds",'red', 1)
            except BaseException as err:
                print(err)
            
            try:
                animationPlayer.runTag(ta.animTags[ta.getIndex(ta.animTags,command)][1])
            except BaseException as err:
                print("Error:")
                print(err)
            try:
                leds.fadeRGB("AllLeds",'red', 1)
                leds.fadeRGB("AllLeds", 'white',1)
            except BaseException as err:
                print(err)
            

        elif command[0:7] == 'powiedz':
            try:
                animatedSpeech.say(command[8 : len(command)])
            except BaseException as err:
                print("Error:")
                print(err)
        else:
            try:
                animationPlayer.runTag(ta.animTags[ta.getIndex(ta.animTags,command)][1])
            except BaseException as err:
                print("Error:")
                print(err)


   
# Create a window and pass it to the Application object
App(tk.Tk(), "Robotyczne przedstawienie: GRUPA " + GROUP)

