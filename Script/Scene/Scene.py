import enum
from tkinter import *
from Script.Utility.SoundManager import *

FONT = "휴먼엑스포"

class SceneType(enum.Enum):
    INTRO = 1
    MENU = 2
    DESC = 3
    GAME = 4

class Timer():
    time = 0
    callback = None

    def __init__(self, time, callback):
        self.time = time
        self.callback = callback

class SceneBase():
    type = None

    win = None
    canvas = None
    sceneManager = None

    timer = {}

    def __init__(self, type, win, canvas, sceneManager):
        self.type = type
        self.win = win
        self.canvas = canvas
        self.sceneManager = sceneManager
        self.clearScene()

    def update(self, dt):
        self._updateTimer(dt)

    def _updateTimer(self, dt):
        run = []
        for t in self.timer:
            if self.timer[t] is None:
                continue

            self.timer[t].time -= dt
            if self.timer[t].time <= 0:
                run.append(t)

        for i in run:
            callback = self.timer[i].callback
            del self.timer[i]
            callback()

    def getNotUseTimeJob(self):
        # get Time Job
        timeJob = 0
        while True:
            if not (timeJob in self.timer):
                break

            timeJob -= 1

        return timeJob

    def registerTimer(self, jobID, time, callback):
        self.timer[jobID] = Timer(time, callback)

    def unRegisterTimer(self, jobID):
        del self.timer[jobID]

    def pressKeyHandler(self, key):
        pass

    def createImage(self, posX, posY, name):
        img = PhotoImage(file='Resources/Assets/' + name)
        imgLabel = Label(self.win, image=img)
        imgLabel.image = img

        self.canvas.create_window(posX, posY, anchor=CENTER, window=imgLabel)
        return imgLabel

    def createText(self, posX, posY, text, size, *args):
        textColor = "black"
        anchor = CENTER
        if args:
            if len(args) >= 1:
                textColor = args[0]
            if len(args) >= 2:
                anchor = args[1]

        t = Label(self.win, text=text, font=(FONT, size), fg=textColor, bg="white", anchor=anchor)
        self.canvas.create_window(posX, posY, window=t, anchor=anchor)
        return t
    
    def createButton(self, posX, posY, width, height, text, textSize, callback, *param):
        if param:
            button = Button(self.win, width=width, height=height, text=text, font=(FONT, textSize), command=lambda : callback(param), anchor=CENTER)
        else:
            button = Button(self.win, width=width, height=height, text=text, font=(FONT, textSize), command=callback, anchor=CENTER)

        self.canvas.create_window(posX, posY, anchor=CENTER, window=button)
        return button

    def createImageButton(self, posX, posY, name, text, textSize, callback, *param):
        img = PhotoImage(file='Resources/Assets/' + name)
        if param:
            button = Button(self.win, text=text, font=(FONT, textSize), image=img, compound=CENTER, command=lambda : callback(param), bg="white", borderwidth=0, padx=0, pady=0)
        else:
            button = Button(self.win, text=text, font=(FONT, textSize), image=img, compound=CENTER, command=callback, bg="white", borderwidth=0, padx=0, pady=0)

        button.image = img
        self.canvas.create_window(posX, posY, anchor=CENTER, window=button)
        return button

    def clearScene(self):
        self.canvas.delete("all")
