

from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,  # Диалог открытия файлов (и папок)
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt # потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
from PyQt5.QtGui import QPixmap
import os

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
from qss import *

app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle("Easy Editor")
win.setStyleSheet(QSS)

btn_left = QPushButton("Вліво")
btn_left.setStyleSheet(left)
btn_right = QPushButton("Вправо")
btn_right.setStyleSheet(right)
btn_flip = QPushButton("Зеркало")
btn_smoth = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")
btn_bw.setStyleSheet(QSS_OK)



btn_dir = QPushButton("Папка")
btn_dir.setStyleSheet(
            "QPushButton {border-radius : 30; border : 2px solid black; background-color: rgb(155, 108, 108)}"
            "QPushButton:pressed {background-color: rgb(10, 80, 80)}")
lw_files = QListWidget()
lb_image = QLabel("Картинка")


col1 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)


col2 = QVBoxLayout()
col2.addWidget(lb_image)

row = QVBoxLayout()
row.addWidget(btn_left)
row.addWidget(btn_right)
row.addWidget(btn_flip)
row.addWidget(btn_smoth)
row.addWidget(btn_bw)

col2.addLayout(row)

mainlayout = QHBoxLayout()
mainlayout.addLayout(col1,20)
mainlayout.addLayout(col2,80)

win.setLayout(mainlayout)

#---------класи-----------
class ImageProcess():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modifiled/"
    
    def load(self, dir, filename):
        self.dir = dir
        self.filename = filename
        path = os.path.join(dir, filename)
        self.image = Image.open(path)
 
    def show(self, path):
        lb_image.hide()
        pix = QPixmap(path)
        w,h = lb_image.width(), lb_image.height()
        pix = pix.scaled(w,h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pix)
        lb_image.show()

    def save(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
        self.show(fullname)

    
    def do_bw(self):
        self.image = self.image.convert("L")
        self.save()
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save()
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save()
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save()
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.save()


#---------Додаткові функції-----------
workdir = ""

def filter(filenames, extensions):
    result = []
    for name in filenames:
        for ext in extensions:
            if name.endswith(ext):
                result.append(name)

    return result

def chooseWorkdir():
    global  workdir
    workdir = QFileDialog.getExistingDirectory()
 
def showFilenamesList():
    try:
        extensions = [".jpg",".jpeg", ".png", ".bmp",".gif",".webp"]
        chooseWorkdir()
        filenames = os.listdir(workdir)
        filenames = filter(filenames, extensions)
        lw_files.clear()
        lw_files.addItems(filenames)
    except:
        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Information) 
        msg.setText("Ви не обрали папку із картинками") 
        msg.setWindowTitle("Information MessageBox") 
        msg.setStandardButtons(QMessageBox.Ok) 
        retval = msg.exec_() 

workImage = ImageProcess()

def showImageItem():
    if lw_files.currentRow()>=0:
        filename = lw_files.currentItem().text()
        workImage.load(workdir, filename)
        workImage.show(os.path.join(workdir,filename))


#---------Обробка кнопок-----------
lw_files.currentRowChanged.connect(showImageItem)
btn_dir.clicked.connect(showFilenamesList)
btn_bw.clicked.connect(workImage.do_bw)
btn_left.clicked.connect(workImage.do_left)
btn_right.clicked.connect(workImage.do_right)
btn_flip.clicked.connect(workImage.do_flip)
btn_smoth.clicked.connect(workImage.do_sharpen)

win.show()
app.exec()


