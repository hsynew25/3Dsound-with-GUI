from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget, QMessageBox, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap, QPen
import sys, random
from audio import Make_3D_Audio
import winsound
# QDesktopWidget class 는 사용자 데스크탑에 대한 정보를 제공 ( 화면 사이즈 )

'''
                *** 2018년 4학년 1학기 ***
                멀티미디어 시스템 프로젝트
'''

class audioGame(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):       # initiates application UI

        # self.tboard = Board(self)
        # self.setCentralWidget(self.tboard)

        # self.statusbar = self.statusBar()
        # self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # self.tboard.start()
        # 이미지 선언
        self. backimg=QPixmap("back.png")
        self.frontimg=QPixmap("front.png")
        self.left=QPixmap("left.png")
        self.right=QPixmap("right.png")
        self.speaker=QPixmap("speaker.png")
        self.resize(900, 900)       #화면 size
        self.center()
        self.update()
        self.setWindowTitle('3d Audio Project')         #window name
        self.setWindowIcon(QIcon('3d_icon1.png'))       #icon
        self.show()
        self.CH_list=[self.frontimg, self.backimg, self.left, self.right, self.speaker]       #이미지 리스트

        # 변수선언
        self.curX = 260
        self.curY = 260
        self.cursX = 260
        self.cursY = 260
        self.flag=self.CH_list[0]       #방향키에 따른 이미지변화 by flag
        self.flag2 = False
        self.flag_play = False
        self.disnum = 0
        self.dirtime =0



    def center(self):

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


    # quit button 처리
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Quit MSG',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)            # 마지막 parameter 는 디폴트 버튼

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    # 화면 그리기
    def paintEvent(self, event):

        char_img = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        textin = "*** 3D Audio Test Program ***"
        char_img.drawText(360, 870, textin)

        pen.setStyle(Qt.DashDotLine)
        char_img.setPen(pen)
        char_img.drawLine(20,10,868,10)
        char_img.drawLine(20, 110, 868, 110)
        char_img.drawLine(20, 10, 20, 110)
        char_img.drawLine(868, 10, 868, 110)

        howto = "< 조작법 >"
        key_udlr = "* 방향키 : Spider man 위치이동"
        key_p = "* P : sound Play"
        key_space = "* Space bar : Speaker 내려놓기/들기"
        char_img.drawText(700, 35, howto)
        char_img.drawText(640, 60, key_udlr)
        char_img.drawText(640, 75, key_space)
        char_img.drawText(640, 90, key_p)

        flagprint = "Flagprint = " + str(self.flag2)
        flagprint_play = "Flag_play = " + str(self.flag_play)
        position = "SPIDER X = " + str(self.curX) + ", Y = " + str(self.curY)      #좌표값 출력
        position2 = "SPEAKER X = " + str(self.cursX) + ", Y = " + str(self.cursY)  # 좌표값 출력
        sp_angle = "Spider <-> Speaker = " + str(self.dirtime) + "시 방향(Spider man 기준)"
        char_img.drawText(40, 35, position)         #좌표값 출력
        char_img.drawText(40, 50, position2)  # 좌표값 출력
        char_img.drawText(40, 65, flagprint)  # 좌표값 출력
        char_img.drawText(40, 80, flagprint_play)  # 좌표값 출력
        char_img.drawText(40, 95,  sp_angle)  # 좌표값 출력

        char_img.drawPixmap(self.cursX+80,self.cursY+80, 80, 80,self.CH_list[4])     # speaker 출력
        char_img.drawPixmap(self.curX,self.curY, 300,300,self.flag)       # x,y좌표, 그림사이즈

        '''
        # Speaker 기준 Spider man의 위치
        if self.cursX+60 < self.curX and self.cursY-130 > self.curY:
            self.disnum = 10    # 1시방향
        elif self.cursX-130 > self.curX and self.cursY-130 > self.curY:
            self.disnum = 87    # 11시방향
        elif self.cursX < self.curX and (self.cursY-130 <= self.curY and self.cursY+80 >= self.curY):
            self.disnum = 25     #  3시방향
        elif self.cursX > self.curX and (self.cursY - 130 <= self.curY and self.cursY + 80 >= self.curY):
            self.disnum = 75     #  9시방향
        elif self.cursX < self.curX and self.cursY+80 < self.curY:
            self.disnum = 37    #  5시방향
        elif self.cursX > self.curX+130 and self.cursY+80 < self.curY:
            self.disnum = 62     # 7시방향
        elif (self.cursX+60 > self.curX or self.cursX-130 < self.curX) and self.cursY > self.curY:
            self.disnum = 0    # 12시방향
        elif (self.cursX+60 > self.curX or self.cursX-130 <= self.curX) and self.cursY < self.curY:
            self.disnum = 50    # 6시방향
        '''

        # 모든 방향은 Spider man 기준 Speaker의 위치다.
        if self.curX+60 < self.cursX and self.curY-80 > self.cursY:
            self.disnum = 5    # 1시방향
            if self.disnum == 5:
                self.dirtime = 1
        elif self.curX > self.cursX+60 and self.curY-80 > self.cursY:
            self.disnum = 75    # 11시방향
            if self.disnum == 75:
                self.dirtime = 11
        elif self.curX < self.cursX and (self.curY-80 <= self.cursY and self.curY+80 >= self.cursY):
            self.disnum = 19     #  3시방향
            if self.disnum == 19:
                self.dirtime = 3
        elif self.curX > self.cursX and (self.curY - 80 <= self.cursY and self.curY + 80 >= self.cursY):
            self.disnum = 66     #  9시방향
            if self.disnum == 66:
                self.dirtime = 9
        elif self.curX+130 < self.cursX and self.curY+80 < self.cursY:
            self.disnum = 37    #  5시방향
            if self.disnum == 37:
                self.dirtime = 5
        elif self.curX-60 > self.cursX and self.curY+80 < self.cursY:
            self.disnum = 52     # 7시방향
            if self.disnum == 52:
                self.dirtime = 7
        elif (self.curX+120 > self.cursX or self.curX < self.cursX+50) and self.curY > self.cursY:
            self.disnum = 0    # 12시방향
            if self.disnum == 0:
                self.dirtime = 12
        elif (self.curX+120 > self.cursX or self.curX < self.cursX+50) and self.curY < self.cursY:
            self.disnum = 45    # 6시방향
            if self.disnum == 45:
                self.dirtime = 6

        # 이동범위 설정
        if self.curX <= -60:
            self.curX = -60
        if self.curX >= 700:
            self.curX = 700
        if self.curY <= -50:
            self.curY = -40
        if self.curY >=680:
            self.curY = 680


    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Left:
            self.curX-=10
            self.flag=self.CH_list[2]
            if self.flag2 == False:
                self.cursX = self.curX
                self.cursY = self.curY
                self.update()
            elif self.flag2 == True:
                self.cursX = self.cursX
                self.cursY = self.cursY
                self.update()
            self.update()

        elif key == Qt.Key_Right:
            self.curX +=10
            self.flag = self.CH_list[3]
            if self.flag2 == False:
                self.cursX = self.curX
                self.cursY = self.curY
                self.update()
            elif self.flag2 == True:
                self.cursX = self.cursX
                self.cursY = self.cursY
                self.update()
            self.update()

        elif key == Qt.Key_Down:
            self.curY+=10
            self.flag = self.CH_list[0]
            #if self.curY == (self.cursY+20):
            if self.flag2 == False:
                self.cursX = self.curX
                self.cursY = self.curY
                self.update()
            elif self.flag2 == True:
                self.cursX = self.cursX
                self.cursY = self.cursY
                self.update()
            self.update()

        elif key == Qt.Key_Up:
            self.curY-=10
            self.flag = self.CH_list[1]

            #if self.curY == (self.cursY - 20):
            if self.flag2 == False:
                    self.cursX = self.curX
                    self.cursY = self.curY
                    self.update()
            elif self.flag2 == True:
                self.cursX = self.cursX
                self.cursY = self.cursY
                self.update()
            self.update()

        # speaker 들었다가 내려놨다가
        elif key == Qt.Key_Space:
            if self.flag == self.CH_list[3]:
                if (self.cursX-10 <= self.curX < self.cursX + 50 or self.cursX-120 <= self.curX <= self.cursX-70) and (self.cursY-40 <= self.curY <= self.cursY + 20):
                    self.flag2 = not self.flag2
                else:
                    self.flag2 = True
            elif self.flag == self.CH_list[2]:
                if (self.cursX-10 <= self.curX < self.cursX + 50 or self.cursX - 120 < self.curX <= self.cursX - 50) and (self.cursY-40 <= self.curY <= self.cursY + 20):
                    self.flag2 = not self.flag2
                else:
                    self.flag2 = True
            elif self.flag == self.CH_list[1]:
                if (self.cursY-40 <= self.curY <= self.cursY + 20) and (self.cursX <= self.curX < self.cursX + 60 or self.cursX-120 <= self.curX <= self.cursX-70):
                    self.flag2 = not self.flag2
                else:
                    self.flag2 = True
            elif self.flag == self.CH_list[0]:
                if (self.cursY - 40 <= self.curY <= self.cursY + 20) and (self.cursX <= self.curX < self.cursX + 60 or self.cursX-120 <= self.curX <= self.cursX-70):
                    self.flag2 = not self.flag2
                else:
                    self.flag2 = True
            else:
                self.flag2 = True

           # self.dropDown()
            self.update()

        # Sound Play button
        elif key == Qt.Key_P:
            filename="spi3sound_" + str(self.disnum)+".wav"
            # Make_3D_Audio(self.disnum,'fin.wav')
            winsound.PlaySound(filename, winsound.SND_FILENAME)


        else:
            super(audioGame, self).keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    Audiogame = audioGame()
    sys.exit(app.exec_())
