import imageio

imageio.plugins.ffmpeg.download()
from PyQt5 import QtGui, QtWebEngineWidgets
from PyQt5.QtGui import QImage, QPixmap
import threading
import sys,os,time,cv2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtGui import *
import json

from moviepy.editor import *

BASE_DIR = os.path.dirname(__file__)
isplay=True

#https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv
class SourceThread(QThread):  # Using QThread to play the video for not blocking the Main window instead
    sourceChangePixmap = pyqtSignal(QtGui.QImage)
    def run(self):
        cap = cv2.VideoCapture(sourceVideoName)
        while (cap.isOpened() == True):
            if (cutSource == False):
                break
            while (isplay == False):
                time.sleep(1)

            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QImage.Format_RGB888)  # covert to Qt format for each frame read from openCV，
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.sourceChangePixmap.emit(p)
                time.sleep(0.02)  # Control the playing speed of the video
            else:
                break

class TargetThread(QThread):  # Use QThread to play instead of loop
    targetChangePixmap = pyqtSignal(QtGui.QImage)
    def run(self):
        cap = cv2.VideoCapture(targetVideoName)
        while (cap.isOpened() == True):
            if(cutTarget==False):
                break
            while(isplay==False):
                time.sleep(1)

            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QImage.Format_RGB888)  
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.targetChangePixmap.emit(p)
                time.sleep(0.02)  # Control the playing speed of the video
            else:
                break

class TInteractObj(QObject):
    SigReceivedMessFromJS = pyqtSignal(str)
    SigSendMessageToJS = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('JSSendMessage(%s) from Html' % strParameter)
        self.SigReceivedMessFromJS.emit(strParameter)

    @pyqtSlot(result=str)
    def fun(self):
        print('TInteractObj.fun()')
        return 'hello'

class login(QWidget):
    SigSendMessageToJS = pyqtSignal(str)
    def __init__(self):
        super(login,self).__init__()
        self.initUI()

    def initUI(self):
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        #源文件选择按钮和选择编辑框
        self.play_btn = QPushButton('play', self)
        self.play_btn.move(50, 400)
        self.play_btn.resize(80, 30)
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.play_video)

        self.pause_btn = QPushButton('pause', self)
        self.pause_btn.move(240, 400)
        self.pause_btn.resize(80, 30)
        self.pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pause_btn.clicked.connect(self.pause_video)

        self.source_btn = QPushButton('source', self)
        self.source_btn.move(30, 450)
        self.source_btn.resize(80,30)
        self.source_btn.clicked.connect(self.select_source)
        self.source_le = QLineEdit(self.centralwidget)
        self.source_le.move(120, 450)
        self.source_le.resize(250,30)

        '''
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.select_source)

        vbox = QVBoxLayout()
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu('File')
        #edit_menu = menu_bar.addMenu('Fi')
        #exit_action = QAction('Exit', self)
        #exit_action.triggered.connect(exit)
        file_menu.addAction(openAction)
 
        self.setLayout(vbox)
        vbox.addWidget(menu_bar)

        #menuBar = self.QtGui.QMenuBar(self)
        #fileMenu = self.menuBar.addMenu("File")
        #self.menuBar.show()
        #fileMenu.addAction(newAction)
        #fileMenu.addAction(openAction)
        #fileMenu.addAction(exitAction)
        '''

        # save button and selecg box
        self.target_btn = QPushButton('target', self)
        self.target_btn.move(30, 510)
        self.target_btn.resize(80, 30)
        self.target_btn.clicked.connect(self.select_target)
        self.target_le = QLineEdit(self)
        self.target_le.move(120, 510)
        self.target_le.resize(250, 30)

        #start time input box and prompt info
        self.startLabel = QLabel(self)
        self.startLabel.setFont(QtGui.QFont('Roman times', 14))
        self.startLabel.move(30, 570)
        self.startLabel.resize(70,30)
        self.startLabel.setText("start:")
        self.start_le = QLineEdit(self)
        self.start_le.move(120,570)
        self.start_le.resize(70,30)
        self.startLabel1 = QLabel(self)
        self.startLabel1.setFont(QtGui.QFont('Roman times', 16))
        self.startLabel1.move(200, 570)
        self.startLabel1.resize(30, 30)
        self.startLabel1.setText("s")

        # fjnish time input box and prompt info
        self.stopLabel = QLabel(self)
        self.stopLabel.setFont(QtGui.QFont('Roman times', 14))
        self.stopLabel.move(230, 570)
        self.stopLabel.resize(70,30)
        self.stopLabel.setText("  end:")
        self.stop_le = QLineEdit(self)
        self.stop_le.move(320,570)
        self.stop_le.resize(70,30)
        self.stopLabel1 = QLabel(self)
        self.stopLabel1.setFont(QtGui.QFont('Roman times',16))
        self.stopLabel1.move(400, 570)
        self.stopLabel1.resize(30, 30)
        self.stopLabel1.setText("s")

        #label name
        self.videoLabel = QLabel(self)
        self.videoLabel.setFont(QtGui.QFont('Roman times', 14))
        self.videoLabel.move(30, 630)
        self.videoLabel.resize(70, 30)
        self.videoLabel.setText("label:")
        self.videoLabelEdit = QLineEdit(self)
        self.videoLabelEdit.move(120, 630)
        self.videoLabelEdit.resize(250, 30)

        #save button
        self.save_btn = QPushButton('cut',self)
        self.save_btn.move(30, 670)
        self.save_btn.resize(140, 30)
        self.save_btn.clicked.connect(self.doEdit)

        #exit button
        self.cancle_btn = QPushButton('cancle',self)
        self.cancle_btn.move(230,670)
        self.cancle_btn.resize(140, 30)
        self.cancle_btn.clicked.connect(QCoreApplication.quit)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 1500, 400))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.videoLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLayout.setObjectName("videoLayout")

        self.sourceLabel =QLabel(self.horizontalLayoutWidget)
        self.sourceLabel.setMinimumSize(QSize(600, 400))
        self.sourceLabel.setText("")
        self.sourceLabel.setObjectName("sourceLabel")
        self.videoLayout.addWidget(self.sourceLabel)


        self.targetLabel = QLabel(self.horizontalLayoutWidget)
        self.targetLabel.setMinimumSize(QSize(600, 400))
        self.targetLabel.setText("")
        self.targetLabel.setObjectName("targetLabel")
        self.videoLayout.addWidget(self.targetLabel)

        # setting html view and start channel with js
        self.browser = QWebEngineView(self)
        self.browser.move(500, 440)
        self.browser.resize(1000, 350)

        #hide scrolling bar 
        self.browser.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)
        self.pWebChannel = QWebChannel(self.browser.page())
        self.pInteractObj = TInteractObj(self)
        self.pWebChannel.registerObject("interactObj", self.pInteractObj)
        self.browser.page().setWebChannel(self.pWebChannel)
        self.pInteractObj.SigReceivedMessFromJS.connect(self.OnReceiveMessageFromJS)
        self.SigSendMessageToJS.connect(self.pInteractObj.SigSendMessageToJS)
        self.is_cut = False

        #Over UI setting 
        self.setGeometry(200, 100, 1600, 800)
        self.setWindowTitle('Video Annotation')#Title
        self.show()

    def play_video(self):
        global isplay
        isplay=True
    def pause_video(self):
        global isplay
        isplay=False

    #set output {"start": 12,"end": 36,"total":80,"label":"labename"}
    def OnReceiveMessageFromJS(self, strParameter):
        print('OnReceiveMessageFromJS()'+strParameter)
    def OnSendMessageByInteractObj(self):
        strMessage = self.mpQtSendLineEdit.text()
        if not strMessage:
            return
        self.SigSendMessageToJS.emit(strMessage)

    #refresh timeline label
    def refresh_labels(self):
        file = open(self.source_le.text().strip()+".txt", 'r')
        str_lines = file.readlines()
        file.close()
        label_arr = []
        for i in range(0, len(str_lines)):
            tmp_str = str_lines[i].strip()
            if (tmp_str != ''):
                label_arr.append(json.loads(tmp_str))
        labels_str = json.dumps(label_arr)
        self.SigSendMessageToJS.emit(labels_str)

    # file name for video
    def select_source(self):
        try:
            global sourceVideoName
            global sourceTh
            global cutSource
            cutSource = False
            self.browser.load(QUrl(r"" + BASE_DIR + '/html/index.html'))
            target,fileType = QFileDialog.getOpenFileName(self, "select the source file", "C:\\Users\\lenovo\\Videos", "*mp4")

            self.source_le.setText(str(target))
            sourceVideoName=str(target)
            time.sleep(0.5)
            cutSource = True
            sourceTh = SourceThread(self)
            sourceTh.sourceChangePixmap.connect(self.setSourceImage)
            sourceTh.start()
            self.refresh_labels()
        except Exception as e:
            print(e)

    #source preview video
    def setSourceImage(self, image):
        self.sourceLabel.setPixmap(QPixmap.fromImage(image))

    # target preview video
    def setTargetImage(self, image):
        self.targetLabel.setPixmap(QPixmap.fromImage(image))

    # name the saved video with mp4 format
    def select_target(self):
        target,fileType = QFileDialog.getSaveFileName(self, "select the save file", "C:\\Users\\lenovo\\Videos","*mp4")
        self.target_le.setText(str(target)+".mp4")
        global targetVideoName
        targetVideoName=str(target)+".mp4"
        global cutTarget
        cutTarget=False
    def setResultPic(self):
        th = TargetThread(self)
        th.targetChangePixmap.connect(self.setTargetImage)
        th.start()

    def doSubclip(self):
        source = self.source_le.text().strip()  # get the cut file 
        target = self.target_le.text().strip()  # save the cut file
        start_time = self.start_le.text().strip()  # get the start cut time 
        stop_time = self.stop_le.text().strip()  # get the finish cut time 
        video = VideoFileClip(source)  # 视频文件加载
        video = video.subclip(int(start_time), int(stop_time))  # 
        video.to_videofile(target, fps=20, remove_temp=True)  # output file
    def doEdit(self):
        self.SigSendMessageToJS.emit("0")#display start
        if(self.is_cut):
            return
        self.is_cut=True
        global cutTarget
        cutTarget=True
        file = open(str(self.source_le.text()) + '.txt', 'a+')
        source_file=self.source_le.text()
        clip = VideoFileClip(source_file)
        total=round(clip.duration)
        stopTime=self.stop_le.text()
        startTime=self.start_le.text()
        labelName=self.videoLabelEdit.text()
        # define output{"start": 12,"end": 36,"total":80,"label":"labename"}
        dict = {"start": startTime, "end": stopTime,"total":total,"label":labelName}
        file.write('\n'+json.dumps(dict))
        file.close()
        thread_doOrder = threading.Thread(target=self.doSubclip, args=(), kwargs={})
        thread_doOrder.start()
        thread_doOrder.join()
        self.refresh_labels()
        self.setResultPic()
        self.SigSendMessageToJS.emit("1")#display end
        self.is_cut =False


if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = login()
    sys.exit(app.exec_())
