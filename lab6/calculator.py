import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import QEvent


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_result)

        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        self.clear = QPushButton('clear', self)
        self.hbox_input.addWidget(self.clear)

        self.b_1 = QPushButton("1", self)
        self.hbox_first.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_first.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_first.addWidget(self.b_3)

        self.b_plus = QPushButton("+", self)
        self.hbox_first.addWidget(self.b_plus)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_minus = QPushButton("-", self)
        self.hbox_second.addWidget(self.b_minus)

        self.b_7 = QPushButton("7", self)
        self.hbox_third.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_third.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_third.addWidget(self.b_9)

        self.b_mult = QPushButton("х", self)
        self.hbox_third.addWidget(self.b_mult)

        self.b_0 = QPushButton("0", self)
        self.hbox_result.addWidget(self.b_0)

        self.b_point = QPushButton(".", self)
        self.hbox_result.addWidget(self.b_point)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_divide = QPushButton("/", self)
        self.hbox_result.addWidget(self.b_divide)

        self.input.textEdited.connect(lambda: self.text_edited())
        self.clear.clicked.connect(lambda: self.clean())

        self.b_result.clicked.connect(lambda: self._button("="))
        self.b_divide.clicked.connect(lambda: self._button("/"))
        self.b_mult.clicked.connect(lambda: self._button("*"))
        self.b_minus.clicked.connect(lambda: self._button("-"))
        self.b_plus.clicked.connect(lambda: self._button("+"))
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_point.clicked.connect(lambda: self._button("."))
        self.u = 0

    def clean(self):
        self.input.setText('')

    def _button(self, param):
        line = self.input.text()
        self.input.setText(line + param)
        self.countcheck('.')
        self.operationcheck('+')
        self.operationcheck('-')
        self.operationcheck('*')
        self.operationcheck('/')
        self.operationcheck('=')

    def exaptble(self):
        li = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*', '=', '+', '-', '/', '.']
        x = self.input.text()
        for i in x:
            if i not in li:
                self.input.setText("error1")

    def operationcheck(self, sym):
        if sym in self.input.text():
            if sym != '=':
                self.u = 1
            x = list(self.input.text())
            print(x)
            n = len(x)
            for i in range(n):
                if x[i] == sym:
                    x[i] = ''
            x = ''.join(x)
            if sym == '=' and self.u != 1:
                self.input.setText('error6')
            elif sym == '=':
                self.input.setText(x)
                self._result()
            else:
                self.input.setText(x)
                self._operation(sym)

    def countcheck(self, sym):
        if self.input.text().count(sym) > 1:
            self.input.setText("error")
        elif self.input.text() == 'error.' or self.input.text() == '.':
            self.input.setText("error")

    def text_edited(self):
        self.exaptble()
        self.countcheck('.')
        self.operationcheck('+')
        self.operationcheck('-')
        self.operationcheck('*')
        self.operationcheck('/')
        self.operationcheck('=')

    def _operation(self, op):
        if self.input.text() == '':
            self.input.setText("error")
        elif self.input.text() != 'error':
            self.num_1 = float(self.input.text())
            self.op = op
            self.input.setText("")
        else:
            self.input.setText('error')

    def _result(self):
        self.u = 0
        if self.input.text() == '':
            self.input.setText(str(self.num_1))
        else:
            self.num_2 = float(self.input.text())
            if self.op == "+":
                self.input.setText(str(self.num_1 + self.num_2))
            if self.op == "-":
                self.input.setText(str(self.num_1 - self.num_2))
            if self.op == "/" and self.num_2 != 0:
                self.input.setText(str(self.num_1 / self.num_2))
            elif self.op == "/" and self.num_2 == 0:
                self.input.setText("error")
            if self.op == "*":
                self.input.setText(str(self.num_1 * self.num_2))


def application():
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
