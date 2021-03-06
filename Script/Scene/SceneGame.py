# -*- coding: utf-8 -*-

from .Scene import *
import random

class SceneGame(SceneBase):
    GAME_QUESTION_TIME_JOB = "GAME_QUESTION_TIME_JOB"
    GAME_BINGO_TIME_JOB = "GAME_BINGO_TIME_JOB"
    GAME_OVER_TIME_JOB = "GAME_OVER_TIME_JOB"
    GAME_END_SCENE_CHANGE_TIME_JOB = "GAME_END_SCENE_CHANGE_TIME_JOB"

    _score = 0
    _count = 1

    _level = 1
    _tempo = 0.35
    _nextTime = 1.0
    _leftTime = 4.0

    _value = [0, 0]
    _selection = [0, 0]
    _canSelect = False

    _nowQuestionCountText = None

    _firstQuestionText = None
    _firstQuestionMoreText = None
    _secondQuestionText = None
    _secondQuestionMoreText = None

    _firstAnswerButton = None
    _secondAnswerButton = None
    _whatIsYourSelectionText = None

    _charImage = None
    _scoreText = None

    def __init__(self, type, win, sceneManager):
        super().__init__(type, win, sceneManager)

        self.createImageLabel(400, 300, "whiteBG.png")
        self._charImage = self.createImageLabel(630, 400, "normal.png")

        self.createTextData()
        self.createQuestionButton()

        # game start!
        self.registerTimer(self.GAME_BINGO_TIME_JOB, 0.5, self.reset)

    def createTextData(self):
        self._nowQuestionCountText = self.createText(30, 60, "문제 %d번" % self._count, 40, "black", W)

        self._firstQuestionText = self.createText(100, 200, "", 40) # value[0]
        self._firstQuestionText.setVisible(False)

        self._firstQuestionMoreText = self.createText(170, 200, "더하기", 20)
        self._firstQuestionMoreText.setVisible(False)

        self._secondQuestionText = self.createText(260, 200, "", 40) # value[1]
        self._secondQuestionText.setVisible(False)

        self._secondQuestionMoreText = self.createText(305, 200, "는", 20)
        self._secondQuestionMoreText.setVisible(False)

        self._whatIsYourSelectionText = self.createText(300, 370, "어느 쪽?", 20)

        self._scoreText = self.createText(30, 550, "뇌가 9가 된 정도 : %d" % self._score, 20, "black", W)

    def reset(self):
        self.resetTextData()
        self.resetQuestion()
        self.showFirstQuestion()
        self.changeCharImager("normal.png")

    def resetTextData(self):
        self._nowQuestionCountText.setTextConfigure("문제 %d번" % self._count)

        self._firstQuestionText.setVisible(False)
        self._firstQuestionMoreText.setVisible(False)
        self._secondQuestionText.setVisible(False)
        self._secondQuestionMoreText.setVisible(False)
        self._firstAnswerButton.setTextConfigure("")
        self._secondAnswerButton.setTextConfigure("")

    def resetQuestion(self):
        self._value[0] = random.randint(1, 8)
        self._value[1] = random.randint(1, 9 - self._value[0])

    def changeCharImager(self, name):
        img = self.createImage(name)
        self._charImage.object.configure(image=img)
        self._charImage.object.image = img

    def createQuestionButton(self):
        self._firstAnswerButton = self.createImageButton(200, 300, "circleButton.png", "", 30, self.selectQuestion, 0)
        self._secondAnswerButton = self.createImageButton(400, 300, "circleButton.png", "", 30, self.selectQuestion, 1)

    def showFirstQuestion(self):
        self._firstQuestionText.setTextConfigure(self._value[0])
        self._firstQuestionText.setVisible(True)

        self.registerTimer(self.GAME_QUESTION_TIME_JOB, self._tempo, self.showFirstQuestionMore)

    def showFirstQuestionMore(self):
        self._firstQuestionMoreText.setVisible(True)
        self.registerTimer(self.GAME_QUESTION_TIME_JOB, self._tempo, self.showSecondQuestion)

    def showSecondQuestion(self):
        self._secondQuestionText.setTextConfigure(self._value[1])
        self._secondQuestionText.setVisible(True)

        self.registerTimer(self.GAME_QUESTION_TIME_JOB, self._tempo, self.showSecondQuestionMore)

    def showSecondQuestionMore(self):
        self.makeRandomSelection()

        self._secondQuestionMoreText.setVisible(True)
        self._firstAnswerButton.setTextConfigure(self._selection[0])
        self._secondAnswerButton.setTextConfigure(self._selection[1])

        self._canSelect = True

        # 두번째 보기가 완전히 나오면 게임 오버 타이머도 등록
        self.registerTimer(self.GAME_OVER_TIME_JOB, self._leftTime, self.timeOver)

    def makeRandomSelection(self):
        sum = self._value[0] + self._value[1]
        while True:
            value = random.randint(1, 9)
            if sum != value:
                break

        self._selection = [sum, value]
        random.shuffle(self._selection)

    def selectQuestion(self, selection):
        if not self._canSelect:
            return

        answer = self._selection[selection[0]]
        sum = self._value[0] + self._value[1]

        # 정답 체크
        if sum == answer:
            if sum == 9:
                self.bingo()
            else:
                self.wrong()
        else:
            if sum == 9:
                self.wrong()
            else:
                self.bingo()

    def bingo(self):
        self._canSelect = False
        SoundManager.get().playFX("bingo.wav")
        self.changeCharImager("bingo.png")

        # 현재 레벨 만큼 스코어 상승
        self._score += self._level
        self._count += 1

        self.levelUp()

        # text 갱신
        self._scoreText.setTextConfigure("뇌가 9가 된 정도 : %d" % self._score)

        # 정답을 맞추면 게임 오버 타이머 제거
        self.unRegisterTimer(self.GAME_OVER_TIME_JOB)

        # 바로 다음 문제 타이머 등록
        self.registerTimer(self.GAME_BINGO_TIME_JOB, self._nextTime, self.reset)

    def levelUp(self):
       if self._score % 5 == 0:
            self._level += 1

            # tempo balance
            if self._tempo > 0:
                self._tempo -= 0.05

            if self._tempo < 0:
                self._tempo = 0

            # next time balance
            self._nextTime -= 0.25
            if self._nextTime < 0.1:
                self._nextTime = 0.1

            # left time balance
            self._leftTime -= 0.5
            if self._leftTime < 1.0:
                 self._leftTime = 1.0

    def wrong(self):
        # 걸려있던 게임 오버 타이머는 제거
        self.unRegisterTimer(self.GAME_OVER_TIME_JOB)

        self._canSelect = False
        SoundManager.get().playFX("wrong.wav")
        self.changeCharImager("wrong.png")

        self.registerTimer(self.GAME_END_SCENE_CHANGE_TIME_JOB, 2, self.goEnd)

    def timeOver(self):
        self._canSelect = False
        SoundManager.get().playFX("boom.wav")
        self.changeCharImager("timeOver.png")

        self.registerTimer(self.GAME_END_SCENE_CHANGE_TIME_JOB, 2, self.goEnd)

    def goEnd(self):
        Player.get().setScore(self._score)
        self.sceneManager.sceneChange(SceneType.END)
