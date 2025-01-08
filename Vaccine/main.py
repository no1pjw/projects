import os
import time
import sys
from PyQt5.QtWidgets import *   
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtWidgets
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
print(os.getcwd())

form_class = uic.loadUiType("main_widget.ui")[0]

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):   
        label1 = QLabel('Label1', self)
        label1.move(20, 20)
        label2 = QLabel('Label2', self)
        label2.move(20, 60)
        
        btn1 = QPushButton('Button1', self)
        btn1.move(80, 13)
        btn2 = QPushButton('Button2', self)
        btn2.move(80, 53)
        
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 300, 400, 200)
        self.show()
def return_path(string):
    event_txt = list(str(string))
    path = ''
    writing = False
    for a in event_txt:
        if a == ',':
            break
        if writing:
            if a == '\'':
                continue
            path += a
        if a == '=':
            writing = True
    return path
class Target:
    watchDir = os.getcwd()
    #watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, 
                                                       recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함

    #파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        print(type(event))

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        path = return_path(event)
        if True:
            print("detected!")
            os.remove(path)
            print("removed!")
            
    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        print(type(event))

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        print(type(event))

if __name__ == '__main__': #본 파일에서 실행될 때만 실행되도록 함
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    w = Target()
    w.run()

