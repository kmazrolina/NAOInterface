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
        
        #Language
        if(LANGUAGE == 'Polish'):
            PLcolor = self.colorOn
            ENGcolor = self.colorOff
        else:
            PLcolor = self.colorOff
            ENGcolor = self.colorOn

        
        self.PLBorder = tk.Frame(topLeftFrame, bg=PLcolor, bd = 0 )
        self.PLBorder.pack(side = tk.LEFT,  fill = tk.BOTH)
        self.butPL = tk.Button(self.PLBorder,text ="PL", bd = 0, command = self.langPL, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 22)
        self.butPL.pack(pady = (1,1),padx = (1,1), fill = tk.BOTH, side = tk.LEFT )

        self.ENGBorder = tk.Frame(topLeftFrame, bg=ENGcolor, bd = 0 )
        self.ENGBorder.pack(padx = (1,0), side = tk.LEFT,  fill = tk.BOTH)
        self.butENG = tk.Button(self.ENGBorder,text ="ENG", command = self.langENG, bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 20)
        self.butENG.pack(pady = (1,1),padx = (1,1), fill = tk.BOTH,side = tk.LEFT )
       
        
        #top right frame (consists of 'IP' and 'Shut down' butttons)
        topRightFrame = tk.Frame(topFrame, bg =self.bgColor, bd = 0)
        topRightFrame.pack(padx = (30,30), pady = (30,30),expand = True, fill = tk.X, side = tk.RIGHT)
        
        #ShutDown
        imShutDown = PIL.Image.open("shutDown.png")
        imShutDown = imShutDown.resize((25,25))
        imShutDown =  PIL.ImageTk.PhotoImage(imShutDown)
        shutDownBut = tk.Button(topRightFrame, bd = 0, bg =self.bgColor,image = imShutDown, activebackground =self.lightGrey, command = self.playAnimation)
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
       
        
        #=========================== Nasze komendy - 24.11 ==============================

        self.commands = ["Introduction", "Reading 1", "Reading 2", "Reading 3", "Reading 4", "Reading 5", "Farewell","Ask for charger", "Pet Miro", "Phrase in French", "Phrase in German", "Phrase in Japanese"]

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


        farewellBut = tk.Button(leftColButtons,text =self.commands[6],  bd = 0, bg =self.lightGrey,fg = "white",font = ("Verdana", 10), padx = 100)
        farewellBut.configure(command = lambda: self.executeCommand(self.commands[6]))
        farewellBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
        
        chargerBut = tk.Button(leftColButtons,text =self.commands[7],  bd = 0, bg =self.pinkCol,fg = "white",font = ("Verdana", 10), padx = 100)
        chargerBut.configure(command = lambda: self.executeCommand(self.commands[7]))
        chargerBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)

        petBut = tk.Button(leftColButtons,text =self.commands[8],  bd = 0, bg =self.pinkCol,fg = "white",font = ("Verdana", 10), padx = 100)
        petBut.configure(command = lambda: self.executeCommand(self.commands[8]))
        petBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
        
        frenchBut = tk.Button(leftColButtons,text = self.commands[9],  bd = 0, bg =self.pinkCol,fg = "white",font = ("Verdana", 10), padx = 100)
        frenchBut.configure(command = lambda: self.executeCommand(self.commands[9]))
        frenchBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
        
        germanBut = tk.Button(leftColButtons,text = self.commands[10],  bd = 0, bg =self.pinkCol,fg = "white",font = ("Verdana", 10), padx = 100)
        germanBut.configure(command = lambda: self.executeCommand(self.commands[10]))
        germanBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
        
        japanBut = tk.Button(leftColButtons,text = self.commands[11],  bd = 0, bg =self.pinkCol,fg = "white",font = ("Verdana", 10), padx = 100)
        japanBut.configure(command = lambda: self.executeCommand(self.commands[11]))
        japanBut.pack(pady = (10,10), padx = (10,10), fill = tk.BOTH)
        
       
        #center column of bottom frame (consists of video and text for NAO to say widgets)
        centerCol = tk.Frame(bottomFrame,bg =self.bgColor, bd = 0 )
        centerCol.pack(pady = (10,30), padx = (30,30), side= tk.LEFT, expand = True,fill = tk.BOTH )
        
        
        movementFrame = tk.Frame(centerCol, bg =self.lightGrey)
        movementFrame.pack(expand = True, fill = tk.BOTH, pady = (0,10))
        labelMovement = tk.Label(movementFrame, text = "Movement options:", bg =self.lightGrey, font = ("Verdana", 10), fg = "white")
        labelMovement.pack(side = tk.TOP, fill = tk.BOTH, pady = (10,5))

        #posture
        postureFrame =  tk.Frame(movementFrame, bg =self.lightGrey)
        postureFrame.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
        postureLabel = tk.Label(postureFrame, text = 'Change posture:',bg = self.lightGrey, font = ("Verdana", 10), fg = "white")
        postureLabel.pack(side =tk.LEFT, padx = (10,0))
        postureMenu = ttk.Combobox(postureFrame, values = POSTURES)
        postureMenu['state'] = 'readonly'
        postureMenu.set("Pick a posture")
        postureMenu.pack(side = tk.LEFT,padx = (10,0), pady = (10,10), expand = True )
        
        imPlay = PIL.Image.open("play.png")
        imPlay = imPlay.resize((20,20))
        imPlay =  PIL.ImageTk.PhotoImage(imPlay)
        playButPosture = tk.Button(postureFrame, bd = 0, bg =self.lightGrey,image = imPlay, activebackground =self.lightGrey)
        playButPosture.configure( command =lambda: setPosture(postureMenu.get()))
        playButPosture.pack(side=tk.LEFT, padx = (10,20))

        #Turn around
        turnFrame =  tk.Frame(movementFrame, bg =self.lightGrey)
        turnFrame.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
        turnLabel = tk.Label(turnFrame, text = 'Turn to the left / right:', bg = self.lightGrey, font = ("Verdana", 10), fg = "white")
        turnLabel.pack(side =tk.LEFT, padx = (10,0))
       
        degFrame = tk.Frame(turnFrame, bg =self.lightGrey)
        degFrame.pack(side =tk.LEFT, padx = (10,10), expand = True)
        degCount = tk.Text(degFrame,width = 3, height = 1)
        degCount.insert(tk.END, '45')
        degCount.pack(side = tk.LEFT,padx = (10,0), pady = (10,10) )
        degLabel = tk.Label(degFrame, text = '°', bg = self.lightGrey, font = ("Verdana", 10), fg = "white")
        degLabel.pack(side =tk.LEFT)
        
        #right value = 2, left value = 1
        LRvar = tk.IntVar()
        LRFrame = tk.Frame(turnFrame, bg =self.lightGrey)
        LRFrame.pack(side =tk.LEFT, padx = (10,10), expand = True)
        left = tk.Radiobutton(LRFrame, text = 'Left', font = ("Verdana", 8), fg = self.greenCol, variable = LRvar, value = 1, bg =self.lightGrey, bd = 0, activebackground =self.lightGrey  )
        left.pack(side = tk.LEFT, padx = (5,5))
        right = tk.Radiobutton(LRFrame, text = 'Right',  font = ("Verdana", 8), fg = self.greenCol,variable = LRvar, value = 2, bg =self.lightGrey, bd = 0, activebackground =self.lightGrey  )
        right.pack(side = tk.LEFT, padx = (5,5))
        
        playButTurn = tk.Button(turnFrame, bd = 0, bg =self.lightGrey,image = imPlay, activebackground =self.lightGrey)
        playButTurn.configure(command = lambda: self.turnRadians(int(str(degCount.get(1.0, "end-1c"))),LRvar.get())) 
        playButTurn.pack(side=tk.LEFT, padx = (0,20))
        
        
        #Move by step forward
        stepFrame =  tk.Frame(movementFrame, bg =self.lightGrey)
        stepFrame.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
        stepLabel = tk.Label(stepFrame, text = 'Make n steps forward:',bg = self.lightGrey, font = ("Verdana", 10), fg = "white")
        stepLabel.pack(side =tk.LEFT, padx = (10,0))
        stepsCount = tk.Text(stepFrame,width = 2, height = 1)
        stepsCount.insert(tk.END, '1')
        stepsCount.pack(side = tk.LEFT,padx = (10,10), pady = (10,10), expand = True )
        playButStep = tk.Button(stepFrame, bd = 0, bg =self.lightGrey,image = imPlay, activebackground =self.lightGrey)
        playButStep.configure(command = lambda: self.moveForwardInSteps(int(str(stepsCount.get(1.0, "end-1c")))))
        playButStep.pack(side=tk.LEFT, padx = (0,20))
        
        
        #Move by step back
        stepBackFrame =  tk.Frame(movementFrame, bg =self.lightGrey)
        stepBackFrame.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
        stepBackLabel = tk.Label(stepBackFrame, text = 'Make n steps back:',bg = self.lightGrey, font = ("Verdana", 10), fg = "white")
        stepBackLabel.pack(side =tk.LEFT, padx = (10,0))
        stepsBackCount = tk.Text(stepBackFrame,width = 2, height = 1)
        stepsBackCount.insert(tk.END, '1')
        stepsBackCount.pack(side = tk.LEFT,padx = (10,10), pady = (10,10), expand = True )
        playButStepBack = tk.Button(stepBackFrame, bd = 0, bg =self.lightGrey,image = imPlay, activebackground =self.lightGrey)
        playButStepBack.configure(command = lambda: self.moveBackInSteps(int(str(stepsBackCount.get(1.0, "end-1c")))))
        playButStepBack.pack(side=tk.LEFT, padx = (0,20))
        
        
        
        #Move by meters
        meterFrame =  tk.Frame(movementFrame, bg =self.lightGrey)
        meterFrame.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
        meterLabel = tk.Label(meterFrame, text = 'Walk n meters forward:',bg = self.lightGrey, font = ("Verdana", 10), fg = "white")
        meterLabel.pack(side =tk.LEFT, padx = (10,0))
        metersCount = tk.Text(meterFrame,width = 2, height = 1)
        metersCount.insert(tk.END, '1')
        metersCount.pack(side = tk.LEFT,padx = (10,10), pady = (10,10), expand = True )
        playButMeter = tk.Button(meterFrame, bd = 0, bg =self.lightGrey,image = imPlay, activebackground =self.lightGrey)
        playButMeter.configure(command = lambda: self.moveForwardInMeters(int(metersCount.get())))
        playButMeter.pack(side=tk.LEFT, padx = (0,20))
        


        #animations
        animFrame = tk.Frame(centerCol, bg =self.lightGrey)
        animFrame.pack(expand = True, fill = tk.BOTH)
        labelAnim = tk.Label(animFrame, text = "Play an animation:", bg =self.lightGrey, font = ("Verdana", 10), fg = "white")
        labelAnim.pack(side = tk.TOP, fill = tk.BOTH, pady = (10,5))
        
        #list of animations
        self.animList = list()
        for i in animations:
            if i.path != None:
                self.animList.append(i.tag)
        
        
        #animation menu
        self.animMenu = ttk.Combobox(animFrame, values = self.animList)
        self.animMenu.set("Hey_1")
        self.animMenu.pack(side = tk.LEFT,padx = (10,10), pady = (10,10), expand = True )
        
        #play button
        
        playBut =  tk.Button(animFrame, bd = 0, bg =self.lightGrey,image = imPlay, activebackground =self.lightGrey, command = self.playAnimation)
        playBut.pack(side=tk.RIGHT, padx = (0,20))
        

        #bottom frame of center column (text field - tapying text for NAO to say)
        textFrame = tk.Frame(centerCol, bg =self.bgColor, bd = 0 )
        textFrame.pack(pady = (20,30), expand = True,fill = tk.BOTH) 
        textFieldLabel = tk.Label(textFrame, text = "Type text for NAO to say and press ENTER:", bg =self.bgColor, font = ("Verdana", 10), fg = "white" )
        textFieldLabel.pack(fill = tk.BOTH, pady = (0,10))
        self.textField = tk.Text(textFrame, bg = self.lightLightGrey, height = 17, width = 60)
        self.textField.pack(expand = True,fill = tk.Y)
        self.animated = True
        self.textField.bind('<Return>', self.sayTextBoxAnimated )
        
        
        
        window.mainloop()

    
    #Change language to Polish
    def langPL(self):
        global LANGUAGE
        if LANGUAGE == "English":
            try:
                setLanguage(language)
                self.PLBorder.configure(bg = self.colorOn)
                self.ENGBorder.configure(bg = self.colorOff)
                LANGUAGE = language
            except BaseException as err:
                print("Could not set language to Polish.")
           
    #Change language to English      
    def langENG(self):
        global LANGUAGE
        if LANGUAGE == "Polish":
            try:
                setLanguage(language)
                self.PLBorder.configure(bg = self.colorOff)
                self.ENGBorder.configure(bg = self.colorOn)
                LANGUAGE = language
            except BaseException as err:
                print("Could not set language to English.")
            
    
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
           
    
    #NAO will say text from the textBox widget
    def sayTextBoxAnimated(self,e ):
        rawText = self.textField.get('1.0', tk.END)
        encodedText = rawText.encode("utf-8")
        textToSay = str(encodedText)
        try:
            animatedSpeech.say(textToSay)
            
        except BaseException as err1:
            print("Error:" )
            print(err1)
            try:
                textToSpeech.say(textToSay)
            except BaseException as err2:
                print("Error:" )
                print(err2)
        self.textField.delete('1.0',tk.END)

    def sayTextBoxReading(self,e ):
        rawText = self.textFieldRead.get('1.0', tk.END)
        encodedText = rawText.encode("utf-8")
        textToSay = str(encodedText)
        try:
            animatedSpeech.say(textToSay)
            
        except BaseException as err1:
            print("Error:" )
            print(err1)
            try:
                textToSpeech.say(textToSay)
            except BaseException as err2:
                print("Error:" )
                print(err2)
        self.textField.delete('1.0',tk.END)
    
    def moveForwardInMeters(self,meters):
        try:
            motion.setTangentialSecurityDistance(0.3)
            motion.setOrthogonalSecurityDistance(0.3)
            motion.moveTo(meters,0,0)
        except BaseException as err:
            print("Error:" )
            print(err)

    def moveForwardInSteps(self,steps):
        try:
            motion.setTangentialSecurityDistance(0.3)
            motion.setOrthogonalSecurityDistance(0.3)
            motion.moveTo(steps*0.03,0,0)
        except BaseException as err:
            print("Error:" )
            print(err)
    
    def moveBackInSteps(self,steps):
        try:

            motion.setTangentialSecurityDistance(0.3)
            motion.setOrthogonalSecurityDistance(0.3)
            motion.moveTo((-steps)*0.03,0,0)
        except BaseException as err:
            print("Error:" )
            print(err)

    def turnRadians(self,deg,side):
        if deg > 180:
            deg = deg % 180
        theta = deg * (PI / 180)
        #side = 1 means Left, side = 2 means Right
        if side == 2:
            theta = -theta
        try:
            motion.setTangentialSecurityDistance(0.2)
            motion.setOrthogonalSecurityDistance(0.2)
            motion.moveTo(0.01,0.01,theta)
        except BaseException as err:
            print("Error:" )
            print(err)

    # ====================================================================================================
    
   
    
    def executeMovement(self, movementTag):

            i = getIndex(animations, movementTag)
       
            names = animations[i].movement[0]
            times = animations[i].movement[1]
            keys = animations[i].movement[2]
            
            name = animations[i].tag
            if( name == "Head_up"
            or name == "Head_down"
            or name == "Head_left"
            or name == "Head_right"):
                headMovement = True

            
            #this condition will allow for longer lasting head movements
            if headMovement == False:
                setStandingPosture()
            try:
                motion.angleInterpolationBezier(names, times, keys)
            except BaseException as err:
                print(err)
            if headMovement == False:
                setStandingPosture()
            
        
        
    
    def playAnimation(self):
        animationTag = self.animMenu.get()
        if animationTag == "Pick an animation":
            pass
        else:
            try:
                if path == 'Movements':
                    self.executeMovement(animationTag)
                else:
                    print("Playing animation: "+animationTag)
                    animationPlayer.runTag(animationTag)
            except BaseException as err:
                print(err)

    def executeDialogLine(self, label):
        if label == 0:
            animationPlayer.runTag("Robot_1")
            self.machineVoice("Never heard of it.,")
        elif label == 1:
            animationPlayer.runTag("Angry_1")
            self.trurlVoice("What? But its only sodium!, You know, the metal, the element.,")
        elif label == 2:
            self.machineVoice("Sodium starts with an s, and I, work, only in, n.,")
        elif label == 3:
            self.trurlVoice("But in Latin it's natrium!,")
        elif label == 4:
            self.machineVoice("Look, old boy,")
        elif label == 5:
            self.machineVoice("if I could do everything starting with n, in every possible language,\
                        I'd be a Machine That Could Do Everything in the Whole Alphabet,\
                        since any item you care to mention undoubtedly starts with n, in one foreign language or another.,\
                        It's not that easy., I can't go beyond what you programmed., So, no sodium.,")
        elif label == 6:
            self.trurlVoice("Very well,")

        #Reading 2
        elif label == 7:
            animationPlayer.runTag("Excited_2")
            self.trurlVoice("Be my guest,")
        elif label == 8:
            self.trurlVoice("But it has to start with n.,")
        elif label == 9:
            #animationPlayer.runTag("Think_1")
            self.klapauciusVoice("N?,")
            
        #Reading 3
        elif label == 16:
            animationPlayer.runTag("Exhausted_2")
            self.trurlVoice("Negative?,")
        elif label == 17:
            animationPlayer.runTag("Angry_4")
            self.trurlVoice("What on earth, is Negative?,")
        elif label == 18:  
            self.klapauciusVoice("The opposite of positive, of course,")
        elif label == 19:
            self.klapauciusVoice("Negative attitudes, the negative of a picture for example.,\
                Now, don't try to pretend you never heard of Negative.")
            self.klapauciusVoice(" All right, machine, get to work,")
   
        elif label == 20:
            animationPlayer.runTag("Amused_1")
            self.klapauciusVoice("That's supposed to be Negative?, Well, let's say it is, for the seik of peace, But now here's the second command, Machine, do, Nothing!")
        
        #Reading 4
        elif label == 21:
            animationPlayer.runTag("Exhausted_1")
            self.trurlVoice("Well, what did you expect?, You asked it to do nothing, and it's doing nothing,")

        elif label == 22:
            self.klapauciusVoice("Correction, I asked it to do Nothing, but it's doing nothing.")
            
        elif label == 23:
            animationPlayer.runTag("Angry_3")
            self.trurlVoice("Nothing is nothing!,")
            
        elif label == 24:
            self.klapauciusVoice("Come, come. It was supposed to do Nothing, but it hasn't done anything, and therefore I've won!")
            animationPlayer.runTag("Winner_1")
        elif label == 25:
            animationPlayer.runTag("Angry_1")
            self.trurlVoice("You're confusing the machine!,")
        elif label == 26:
            animationPlayer.runTag("Robot_1")
            self.machineVoice("Really, how can you two bicker at a time like this?, Oh yes, I know what Nothing is, and Nothingness,\
                    Nonexistence, Nonentity, Negation, Nullity and Nihility, since all these come under the heading of n,")
            self.machineVoice("Look then, upon your world, for the last time, gentlemen! Soon it shall no longer be.")
        elif label == 27:
            animationPlayer.runTag("Fear_1")
            self.trurlVoice("Oh my gosh!")
        elif label == 28:
            animationPlayer.runTag("Fearful_1")
            self.trurlVoice("If only nothing bad comes out of all this.")
        elif label == 29:
            self.klapauciusVoice("Don't worry") 
        elif label == 30:
            self.klapauciusVoice("You can see it's not producing Universal Nothingness, but only causing the absence of whatever starts with n.")
        elif label == 31:
            animationPlayer.runTag("Robot_1")
            self.machineVoice("Do not be deceived!")
        elif label == 32:
            self.machineVoice("I've begun, it's true, with everything in n, but only out of familiarity.,\
                 In less than a minute now you will cease to have existence, along with everything else, so tell me now,\
                 Klapaucius, and quickly, that I am really, and truly everything, I was programmed to be, before it is too late." )
        elif label == 33:
            self.klapauciusVoice("But,")
        elif label == 34:
            animationPlayer.runTag("Hurt_2")
            self.klapauciusVoice("Stop! I take it all back! Desist! Whoa! Don't do Nothing!!")
        elif label == 35:
            animationPlayer.runTag("Fear_2")
            self.klapauciusVoice("Great Gauss!")
        elif label == 36:
            #animationPlayer.runTag("Sad_1")
            self.klapauciusVoice("And where are the gruncheons? Where my dear, favorite pritons? Where now the gentle zits?!" )
            animationPlayer.runTag("Sad_1")

        #Reading 5
        elif label == 37:
            self.machineVioce("They no longer are, nor ever will exist again,")
        elif label == 38:
            self.machineVoice("I executed, or rather only began to execute, your order...")
        elif label == 39:
            animationPlayer.runTag("Sad_1")
            self.klapauciusVoice("I tell you to do Nothing, and you, you,")
            
        elif label == 40:
            animationPlayer.runTag("Robot_1")
            self.machineVoice("Klapaucius, don't pretend to be a greater idiot than you are,")
        elif label == 41:
            self.machineVoice("Had I made Nothing outright, in one fell swoop, everything would have ceased to exist,\
                    and that includes Trurl,\
                    the sky, the Universe, and you - and even myself.\
                    In which case who could say, and to whom could it be said,\
                    that the order was carried out, and I am an efficient and capable machine?")
           
        elif label == 42:
            animationPlayer.runTag("Disappointed_1")
            self.klapauciusVoice("I have nothing more to ask of you, only please, dear machine, please, return the zits,\
                    for without them, life loses all its charm.")
            
        elif label == 43:
            self.machineVoice("But I can't, they're in z,")
        elif label == 44:
            animationPlayer.runTag("Angry_4")
            self.klapauciusVoice("I want my zits!")
        elif label == 45:
            self.machineVoice("Sorry, no zits!")
     
        elif label == 46:
            animationPlayer.runTag("ShowSky_2")
            self.machineVoice("Take a good look at this world, how riddled it is with huge, gaping holes, how full of Nothingness,\
                    the Nothingness, that fills the bottomless void between the stars,")
            animationPlayer.runTag("ShowSky_1")
            self.machineVoice("how everything about us, has become lined with it, how it darkly lurks behind each shred of matter.,\
                    This is your work, envious one!, And I hardly think, the future generations, will bless you for it.")

        elif label == 47:
            self.klapauciusVoice("Perhaps..., they won't find out, perhaps, they won't notice,")



    def dialog(self,command):
        narrLabels = list() #the endings of preceiding narrator's phrase
        iL = 0 #iterator of above list
        butId = list()
        butLabels = list()
        iB = 0 #iterator of above lists
        voices = list() # the order of voices 
        #machine - m / klapaucius - k / trurl - t / narrator - n
        #len(voices) = len(narratorLabels) + len(butLables)
        
        #not needed in the short version
        if command == "Reading 1":
            voices= ['n','m','n','t','m','t','m','n','m','t','n']
            narrLabels = [ 
                "...The machine carried out his instructions to the letter.",
                "said the machine.",
                "said the machine.",
                "said Trurl, and ordered it to make Night..."]
            butLabels = ["Never heard of it.",
                        "What? But its only sodium!...",
                        "Sodium starts with an s...",
                        "But in Latin it's natrium!...",
                        "Look, old boy,",
                        "if I could do everything starting with n...",
                        "Very well"
            ]
            for i in range(7):
                butId.append(i)
            
            
        elif command == "Reading 2":
            voices = ['n','t','n','t','k','n']
            narrLabels = [ "...inquired, whether he too, might not test the machine.",
                            "said Trurl",
                            "Trurl agreed to this, whereupon, Klapaucius requested, Negative."]
            butLabels = [
                "Be my guest",
                "But it has to start with n.",
                "N?"]
          
            for i in range(7,10):
                butId.append(i)

        elif command == "Reading 3":
            voices = ['t','n','t','k','n','k','n','k']
            narrLabels = [ "cried Trurl. ",
            "Klapaucius coolly replied. ",
            "...Klapaucius muttered , displeased"] 
            for i in range(16,21):
                butId.append(i)
            butLabels = [ "Negative?,",
                "What on earth, is Negative?,",
                "The opposite of positive, of course,",
                "Negative attitudes, ...",
                "That's supposed to be Negative?..."]

        elif command == "Reading 4":
            narrLabels = ["...Klapaucius rubbed his hands in triumph, but Trurl said:",
                           "...But suddenly, its metallic voice rang out:",
                           "...began to thin out around Trurl and Klapaucius.",
                           "said Trurl",
                           "said Klapaucius.",
                           "Replied the machine.",
                           "...the calinatifacts, the thists, worches and pritons.",
                           "...and zits that had, till now, graced the horizon!",
                           "cried Klapaucius." ]
                           
            voices = ['n','t','k','t','k','t','n','m',
            'n','t','n','t','k','n','k','m',
            'n','m','k','n','k','n','k','n','k' ]
            butLabels = ["Well, what did you expect?...",
                        "Correction, I asked it to do Nothing...",
                        "Nothing is nothing!,",
                        "Come, come. It was supposed to do Nothing...",
                        "You're confusing the machine!,",
                        "Really, how can you two bicker a...",
                        "Oh my gosh!",
                        "If only nothing bad comes out of all this.",
                        "Don't worry",
                        "You can see it's not producing Universal Nothingness...",
                        "Do not be deceived!",
                        "I've begun, it's true, with everything in n...",
                        "But,",
                        "Stop! I take it all back!...",
                        "Great Gauss!",
                        "And where are the gruncheons? ..."]
            for i in range(21,37):
                butId.append(i)
            
        elif command == "Reading 5":
            voices = ['m','n','m','k','m','n','m','k','m','n','k','n','m','n','m','k','n']

            narrLabels = ["the machine said calmly.", 
                            "said the machine.",
                            "said the machine.",
                            " bellowed Klapaucius. ",
                            "said the machine.",
                            "groaned the pale Klapaucius..."]

            butLabels = ["They no longer are, nor ever will exist again,",
                        "I executed, or rather only began to execute, your order...",
                        "I tell you to do Nothing, and you, you,",
                        "Klapaucius, don't pretend....",
                        "Had I made Nothing outright...",
                        "I have nothing more to ask of you...",
                        "But I can't, they're in z,",
                        "I want my zits!",
                        "Sorry, no zits," ,
                        "Take a good look at this world...",
                        "Perhaps..., they won't find out..."]
            for i in range(37,48):
                butId.append(i)
            
        readWindow = tk.Toplevel(self.window, bg = self.greenGrey)
        readWindow.geometry("400x700")
        readWindow.title(command)
 
        #position toplevel window on top of the main window
        x = self.window.winfo_x()
        y = self.window.winfo_y()

        readWindow.geometry("+%d+%d" %(x+300,y+0))
       
        #Create border
        windowBorder = tk.Frame(readWindow, bg = self.lightGrey, bd = 1, relief = tk.RAISED)
        windowBorder.pack(expand = True, fill = tk.BOTH)
        addCanvas = tk.Frame(windowBorder, bg = self.bgColor)
        addCanvas.pack(expand = True, fill = tk.BOTH, pady = (1,1), padx = (1,1))


        #top frame - label
        topFrame = tk.Frame(addCanvas, bg = self.bgColor)
        topFrame.pack(side = tk.TOP)
        # Create label - reading number
        labelL = tk.Label(topFrame,text = (command +": ") , bg = self.bgColor, font = ("Verdana", 10), fg = "white")
        labelL.pack(expand = True, side = tk.TOP, pady = (10,10))
        
        #labels and buttons alternating
        for i in range(len(voices)):
            if voices[i] == 'n':
                narrator = tk.Label(topFrame,text = narrLabels[iL],bg= self.bgColor, font = ("Verdana", 7), fg = "white" )
                narrator.pack(expand = True, side = tk.TOP, pady = (3,3))
                iL += 1
            
            elif voices[i] == 'k':
                button = tk.Button(topFrame,  text = butLabels[iB],bd = 0, bg =self.blueCol,fg = "white",font = ("Verdana", 7), padx = 100)
                button.configure(command = lambda i = butId[iB]: self.executeDialogLine(i))
                button.pack(pady = (3,3), padx = (10,10), fill = tk.BOTH)
                iB+=1
            elif voices[i] == 'm':
                button = tk.Button(topFrame,   text = butLabels[iB],bd = 0, bg =self.redCol,fg = "white",font = ("Verdana", 7), padx = 100)
                button.configure(command = lambda i = butId[iB]: self.executeDialogLine(i))
                button.pack(pady = (3,3), padx = (10,10), fill = tk.BOTH)
                iB+=1
            elif voices[i] == 't':
                button = tk.Button(topFrame,  text = butLabels[iB], bd = 0, bg =self.greenCol,fg = "white",font = ("Verdana", 7), padx = 100)
                button.configure(command = lambda i = butId[iB]: self.executeDialogLine(i))
                button.pack(pady = (3,3), padx = (10,10), fill = tk.BOTH)
                iB +=1
            
            
        
        #Middle frame(text field - tapying text for NAO to say)
        textFrame = tk.Frame(addCanvas, bg =self.bgColor, bd = 0 )
        textFrame.pack(pady = (20,20), expand = True,fill = tk.BOTH) 
        textFieldLabel = tk.Label(textFrame, text = "Type text for NAO to say and press ENTER:", bg =self.bgColor, font = ("Verdana", 10), fg = "white" )
        textFieldLabel.pack(fill = tk.BOTH, pady = (0,10))
        self.textFieldRead = tk.Text(textFrame, bg = self.lightLightGrey, height = 5, width = 40)
        self.textFieldRead.pack(expand = True,fill = tk.Y)
        self.textFieldRead.bind('<Return>', self.sayTextBoxReading)

        # bottom frame - Add and Cancel buttons
        bottomFrame = tk.Frame(addCanvas, bg = self.bgColor)
        bottomFrame.pack(side = tk.BOTTOM, fill = tk.X, expand = True)
        
        
        
        readWindow.mainloop()

    

        
    #========================================================================================================


    #setting voices of different characters
    def machineVoice(self,text):
        autonomousLife.setAutonomousAbilityEnabled("AutonomousBlinking",False)
        leds.fadeRGB("FaceLeds", "red",1)
        #short break between the lines of the text
        time.sleep(0.3)

        #machine voice parameters
        #HERE
        textToSpeech.setParameter("pitchShift", 1.3)
        textToSpeech.setParameter("speed", 73)
        textToSpeech.setParameter("doubleVoice", 1.1)
        textToSpeech.setParameter("doubleVoiceLevel", 0.3)
        textToSpeech.setParameter("doubleVoiceTimeShift", 0)

        textToSpeech.say(text)
        #reset to default voice
        defaultVoice()
        autonomousLife.setAutonomousAbilityEnabled("AutonomousBlinking",True)

    def trurlVoice(self,text):
        autonomousLife.setAutonomousAbilityEnabled("AutonomousBlinking",False)
        leds.fadeRGB("FaceLeds", "green",0.3)
        #short break between the lines of the text
        time.sleep(0.3)

        #Trurl voice parameters
        textToSpeech.setParameter("speed", 85)
        textToSpeech.setParameter("pitchShift", 1)

        animatedSpeech.say(text)
        #reset to default voice
        defaultVoice()
        autonomousLife.setAutonomousAbilityEnabled("AutonomousBlinking",True)

    def klapauciusVoice(self,text):
        autonomousLife.setAutonomousAbilityEnabled("AutonomousBlinking",False)
        leds.fadeRGB("FaceLeds", "blue",0.1)
        #Klapaucius voice parameters
        textToSpeech.setVoice("naomnc")
        textToSpeech.setParameter("speed", 80)
        textToSpeech.setParameter("pitchShift", 1.2)

        textToSpeech.say(text)
        #reset to default voice
        defaultVoice()
        autonomousLife.setAutonomousAbilityEnabled("AutonomousBlinking",True)   
        
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


    #=================================================================================

    #searching a list of labeled commands
    def getFromList(self, label):
        for i in range(len(self.labelList)): 
            if label == self.labelList[i]:
                break
        return i

    #execute the command coresponding to a button
    def sayCommand(self, button):
        i = self.getFromList(button.cget("text"))
        print(self.commandList[i])

    #Add commands for NAO to say - opens new window
    def addCommand(self):
        addWindow = tk.Toplevel(self.window, bg = self.blueGrey)
        addWindow.geometry("400x350")
        addWindow.title("Add a command")
        addWindow.overrideredirect(1) #Remove border
        #position toplevel window on top of the main window
        x = self.window.winfo_x()
        y = self.window.winfo_y()

        addWindow.geometry("+%d+%d" %(x+500,y+200))
        
       
        #Create border
        windowBorder = tk.Frame(addWindow, bg = self.lightLightGrey)
        windowBorder.pack(expand = True, fill = tk.BOTH)
        addCanvas = tk.Frame(windowBorder, bg = self.bgColor)
        addCanvas.pack(expand = True, fill = tk.BOTH, pady = (1,1), padx = (1,1))
        
        #top frame - label
        topFrame = tk.Frame(addCanvas, bg = self.bgColor)
        topFrame.pack(side = tk.TOP)
        # Create label
        label = tk.Label(topFrame,text = "Command label:",bg = self.bgColor, font = ("Verdana", 10), fg = "white")
        label.pack(pady = (30,10))
        #label input field
        labelText = tk.Text(topFrame, height = 1, width = 45, bd = 0)
        labelText.pack()
        #labelText.bind('<Key>', self.sayTextBox )
        
        #middle frame - text
        midFrame = tk.Frame(addCanvas, bg = self.bgColor)
        midFrame.pack()
        # text input
        text = tk.Label(midFrame,text = "Text for NAO to say:",bg = self.bgColor, font = ("Verdana", 10), fg = "white")
        text.pack(pady = (10,10))
        textField = tk.Text(midFrame, height = 10, width = 45)
        textField.pack()
        #textField.bind('<Return>', self.sayTextBox )
        
        # bottom frame - Add and Cancel buttons
        bottomFrame = tk.Frame(addCanvas, bg = self.bgColor)
        bottomFrame.pack(side = tk.BOTTOM, fill = tk.X, expand = True)
        cancelBut = tk.Button(bottomFrame, text = "Cancel",command = addWindow.destroy, bd = 0, bg = self.lightGrey,font = ("Verdana", 10), fg = "white", padx = 30 )
        cancelBut.pack(side = tk.LEFT, pady = (10,20), padx = (20, 0),fill = tk.X)
        addBut = tk.Button(bottomFrame, text = "Add",command = addWindow.destroy, bd = 0, bg = self.lightGrey,font = ("Verdana", 10), fg = "white", padx = 40 )
        addBut.pack(side = tk.RIGHT, pady = (10,20), padx = (0, 20), fill = tk.X)
        
        addWindow.mainloop()
        
    #update videoframes
    def update(self):
        
        #First get an image, then show it on the screen with PIL.
        vid.get_frame()
        
        if vid.naoImage:
            # Create a PIL Image from our pixel array.
            im = PIL.Image.frombytes("RGBA", (vid.imageWidth, vid.imageHeight), vid.array)
            frame = PIL.ImageTk.PhotoImage(im)
           
            if frame:
                print(frame)
                lab = tk.Label( self.canvas, image = frame).place(x = 300, y = 50)
        else:
            print("Could not retreive camera image")
        window.after(delay, update)
     
     
        

class MyVideoCapture:
    def __init__(self):
        # Open the video source
        
        # Register a Generic Video Module
        cameraId = videoService.getActiveCamera()
        resolution = vision_definitions.kQVGA
        colorSpace = vision_definitions.kYUVColorSpace
        fps = 15
        videoClient = "python_GVM"
        # Get the service ALVideoDevice.
        videoClient = videoService.subscribeCamera(videoClient, cameraId, resolution, colorSpace,fps)
        
        

    def get_frame(self):
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        naoImage = videoService.getImageRemote(videoClient)
        if naoImage:
            # Get the image size and pixel array.
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            array = naoImage[6]
            videoService.releaseImage(videoClient)
        
        
    # Release the video source when the object is destroyed
    def __del__(self):
        videoService.unsubscribe(videoClient)
    

# Create a window and pass it to the Application object
App(tk.Tk(), "Wizard of Oz for NAO")

#https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tk-window/