import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic


main = uic.loadUiType("main.ui")[0]
start = uic.loadUiType("start.ui")[0]
batch = uic.loadUiType("student_set.ui")[0]
result = uic.loadUiType("result.ui")[0]

check_array = [0] * 150
temp = []
student_table = [[0]*15 for j in range(10)]
min_intimacy = 0
max_intimacy = 0
class_intimacy = 0
student_number = 0
early_setting = []


class Start(QMainWindow,start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.myWindow = None
        self.buttons = []    #버튼 담을 배열
        self.checked = 0
        self.student_len = 40
        self.board.setAlignment(Qt.AlignCenter)
        self.board.setFont(QFont('아임크리수진', 20))
        self.return_home.clicked.connect(self.go_to_main)
        self.next_button.clicked.connect(self.go_to_next)
        for i,x in enumerate(check_array):
            if x==True:
                self.checked += 1
        self.exercise.setText(f'책상 {self.checked}개 선택되었습니다.')
        for i in range(150):       #버튼 배열로 받기
            s = f'QPushButton#btn_{i}'
            white = 'white'
            green = '#ABD643'
            green_sheet = f'background-color:#ABD654;{s}:hover{{ border-radius: 5px;border: 2px solid rgb(58, 134, 255);color: rgb(58, 134, 255);background-color:{green};text-shadow: 1px 1px 20px #000000;text-align: center;  }}'
            white_sheet = f'{s}:hover{{ border-radius: 5px;border: 2px solid rgb(58, 134, 255);color: rgb(58, 134, 255);background-color:{white};text-shadow: 1px 1px 20px #000000;text-align: center;  }}'
            self.buttons.append(getattr(self,f'btn_{i}'))
            getattr(self, f'btn_{i}').setStyleSheet(white_sheet)
            if check_array[i] == True:
                self.buttons[i].setStyleSheet(green_sheet)
        for i,btn in enumerate(self.buttons):    #버튼에 함수 연결
            btn.is_clicked = None
            btn.clicked.connect(lambda state, button = btn : self.btn_click(state,button))

    def btn_click(self,state,btn): # 버튼 클릭 콜백
        global check_array
        idx = self.buttons.index(btn)
        s = f'QPushButton#btn_{idx}'
        green = '#ABD643'
        white = 'white'
        green_sheet = f'background-color:#ABD654;{s}:hover{{ border-radius: 5px;border: 2px solid rgb(58, 134, 255);color: rgb(58, 134, 255);background-color:{green};text-shadow: 1px 1px 20px #000000;text-align: center;  }}'
        white_sheet = f'{s}:hover{{ border-radius: 5px;border: 2px solid rgb(58, 134, 255);color: rgb(58, 134, 255);background-color:{white};text-shadow: 1px 1px 20px #000000;text-align: center;  }}'
        if check_array[idx] == False:
            self.checked += 1
            check_array[idx] = True
            btn.setStyleSheet(green_sheet)
        else:
            check_array[idx] = False
            self.checked -= 1
            btn.setStyleSheet(white_sheet)
        self.exercise.setText(f'책상 {self.checked}개 선택되었습니다.')
    def go_to_main(self):
        if self.myWindow is None:
            self.myWindow = MainWindow()
            self.myWindow.show()
            self.close()
    def go_to_next(self):
        if not True in check_array:
            QMessageBox.information(self, "경고!", "책상을 클릭하세요")
            return
        if self.checked != self.student_len:
            QMessageBox.information(self, "경고!", "학생수만큼 책상을 입력하세요")
            return
        if self.myWindow is None:
            self.myWindow = Batch()
            self.myWindow.show()
            self.close()

class Batch(QMainWindow,batch):
    def __init__(self):
        global temp
        super().__init__()
        self.setupUi(self)
        self.myWindow = None
        self.board.setAlignment(Qt.AlignCenter)
        self.board.setFont(QFont('아임크리수진', 20))
        self.go_main.clicked.connect(self.go_to_start)
        self.start_set.clicked.connect(self.go_to_next)
        self.seats = []
        self.complete = False
        for i in range(150):  # 자리에 색 칠하기
            self.seats.append(getattr(self, f'text_{i}'))
            if check_array[i]:
                getattr(self,f'text_{i}').setStyleSheet("background-color:#ABD643;")
                if student_table[i//15][i%15] != 0:
                    self.seats[i].setText(student_table[i//15][i%15])
            else:
                getattr(self, f'text_{i}').setReadOnly(True)
        ###########################
        lst = [[0]*15 for i in range(10)]
        for i in range(150):
            if check_array[i] == True:
                lst[i//15][i%15] = 1
        temp = lst

    def go_to_start(self):
        if self.myWindow is None:
            self.myWindow = Start()
            self.myWindow.show()
            self.close()

    def go_to_next(self):
        if self.myWindow is None:
            seat_text_array = []
            for i in range(150):
                if self.seats[i].text():
                    seat_text_array.append(self.seats[i].text())
                    student_table[i // 15][i % 15] = self.seats[i].text()
            QMessageBox.information(self, "설정", "설정되었습니다.")
            k = 0
            del early_setting[:]
            for i in student_table:
                print(i)
            for i, row in enumerate(student_table):
                for j, number in enumerate(row):
                    if temp[i][j]==1:
                        if number != 0:
                            early_setting.append(list((int(number) - 1, k)))
                        k += 1

            completed_setting = logic.start_seating(early_setting)
            print(early_setting)
            print(completed_setting)
            g = 0
            for i, value in enumerate(check_array):
                if value == 0:
                    continue
                if g >= 40:
                    continue
                student_table[i // 15][i % 15] = str(completed_setting.index(g) + 1)
                g += 1

            self.complete = True
            self.myWindow = Result()
            self.myWindow.show()
            self.close()

class Result(QMainWindow, result):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.myWindow = None
        self.seats = []
        self.go_batch.clicked.connect(self.go_to_batch)
        self.return_main.clicked.connect(self.go_to_main)
        self.switch_name.clicked.connect(self.switching)
        self.namelist = []
        self.switch = False
        f = open('student_name_data.txt', 'r')
        while True:
            name = f.readline().strip()
            if not name: break
            self.namelist.append(name)
        f.close()
        self.student_dictionary = {string: i + 1 for i, string in enumerate(self.namelist)}
        for i in range(1,151):
            self.seats.append(getattr(self, f'label_{i}'))
            getattr(self, f'label_{i}').setAlignment(Qt.AlignCenter)
            if check_array[i-1]:
                getattr(self,f'label_{i}').setStyleSheet(
                                "color: blue;"
                                "background-color: #ABD643;"
                                "border-style: dashed;"
                                "border-width: 3px;"
                                "border-color: #1E90FF;"
                                "font-family: 아임크리수진;"
                                "font-size: 20px;")
                getattr(self, f'label_{i}').setAlignment(Qt.AlignCenter)
            j = i - 1
            if student_table[j//15][j%15] == 0:
                self.seats[j].setText('X')
                continue
            self.seats[j].setText(student_table[j//15][j%15])

    def switching(self):
        if self.switch == True:          # 학생이름 -> 학생번호
            self.switch = False
            QMessageBox.information(self, "설정", "교번으로 출력합니다.")
            self.switch_name.setText('학생 이름으로 보기')
            for i in range(150):
                if str(type(self.seats[i].text())) == "<class 'str'>":  #학생 이름으로 되어있으면
                    if self.seats[i].text() == 'X':
                        continue
                    self.seats[i].setText(str(self.student_dictionary[self.seats[i].text()]))
        else:                    # 학생번호 -> 학생이름
            self.switch = True
            QMessageBox.information(self, "설정", "이름으로 출력합니다.")
            self.switch_name.setText('학생 교번으로 보기')
            for i in range(150):
                if student_table[i//15][i%15] == 0:
                    continue
                for name,number in self.student_dictionary.items():
                    if number == int(student_table[i//15][i%15]):
                        self.seats[i].setText(name)

    def go_to_batch(self):
        if self.myWindow is None:
            global student_table,early_setting
            student_table = [[0]*15 for j in range(10)]
            early_setting=[]
            self.myWindow = Batch()
            self.myWindow.show()
            self.close()

    def go_to_main(self):
        if self.myWindow is None:
            global student_table, early_setting
            student_table = [[0]*15 for j in range(10)]
            early_setting = []
            self.myWindow = MainWindow()
            self.myWindow.show()
            self.close()

class MainWindow(QMainWindow, main):
    def __init__(self):
        super().__init__()
        self.myWindow = None
        self.setupUi(self)
        self.start_button.clicked.connect(self.start)

    def setting(self):
        if self.myWindow is None:
            self.myWindow.show()
            self.close()
        else:
            self.myWindow.close()
            self.myWindow = None
    def start(self):
        if self.myWindow is None:
            self.myWindow = Start()
            self.myWindow.show()
            self.close()
        else:
            self.myWindow.close()
            self.myWindow = None

if __name__ == '__main__':
    import sys
    import logic
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    sys.exit(app.exec_())
