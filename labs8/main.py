import psycopg2
import sys
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget,
                            QTabWidget, QAbstractScrollArea,
                            QVBoxLayout, QHBoxLayout,
                            QTableWidget, QGroupBox,
                            QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Shedule")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()
        self._create_timetable_tab()
        self._create_subject_tab()
        self._create_teacher_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="timelab",
                                user="postgres",
                                password="пароль",
                                host="localhost",
                                port="5432")

        self.cursor = self.conn.cursor()

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")

        self.teachersbox = QVBoxLayout()
        self.teachersbox1 = QHBoxLayout()
        self.teachersbox2 = QHBoxLayout()

        self.teachersbox.addLayout(self.teachersbox1)
        self.teachersbox.addLayout(self.teachersbox2)

        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teacher_table.setColumnCount(4)
        self.teacher_table.setHorizontalHeaderLabels(['name','subject','Join','Delete'])
        self._update_teachers()
        self.teachersbox1.addWidget(self.teacher_table)

        self.update_teacher_button = QPushButton("Update")
        self.teachersbox2.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._update_shedule)

        self.teacher_tab.setLayout(self.teachersbox)

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subject")

        self.subjectsbox = QVBoxLayout()
        self.subjectsbox1 = QHBoxLayout()
        self.subjectsbox2 = QHBoxLayout()

        self.subjectsbox.addLayout(self.subjectsbox1)
        self.subjectsbox.addLayout(self.subjectsbox2)

        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(['subject','Join','Delete'])
        self._update_subjects()
        self.subjectsbox1.addWidget(self.subject_table)

        self.update_subject_button = QPushButton("Update")
        self.subjectsbox2.addWidget(self.update_subject_button)
        self.update_subject_button.clicked.connect(self._update_shedule)

        self.subject_tab.setLayout(self.subjectsbox)

    def _create_timetable_tab(self):
        self.timetable_tab = QWidget()
        self.tabs.addTab(self.timetable_tab, "Timetable")

        self.timesbox = QVBoxLayout()
        self.timebox1 = QHBoxLayout()
        self.timebox2 = QHBoxLayout()

        self.timesbox.addLayout(self.timebox1)
        self.timesbox.addLayout(self.timebox2)

        self.time_table = QTableWidget()
        self.time_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.time_table.setColumnCount(8)
        self.time_table.setHorizontalHeaderLabels(['week', 'day', 'nomer', 'subject', 'room_numb', 'start_time', 'Join','Delete'])
        self._update_timetable()
        self.timebox1.addWidget(self.time_table)

        self.update_timetable_button = QPushButton("Update")
        self.timebox2.addWidget(self.update_timetable_button)
        self.update_timetable_button.clicked.connect(self._update_shedule)

        self.timetable_tab.setLayout(self.timesbox)

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.sunday_gbox = QGroupBox("Sunday")


        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox1.addWidget(self.friday_gbox)
        self.shbox1.addWidget(self.sunday_gbox)

        self._create_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

    def _create_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(6)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_table('Понедельник')

        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tuesday_table.setColumnCount(6)
        self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_table('Вторник')

        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.wednesday_table.setColumnCount(6)
        self.wednesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_table('Среда')

        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.thursday_table.setColumnCount(6)
        self.thursday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_table('Четверг')

        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.friday_table.setColumnCount(6)
        self.friday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_table('Пятница')

        self.sunday_table = QTableWidget()
        self.sunday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.sunday_table.setColumnCount(6)
        self.sunday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_table('Суббота')

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

        self.mvbox1 = QVBoxLayout()
        self.mvbox1.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox1)

        self.mvbox2 = QVBoxLayout()
        self.mvbox2.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox2)

        self.mvbox3 = QVBoxLayout()
        self.mvbox3.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox3)

        self.mvbox4 = QVBoxLayout()
        self.mvbox4.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox4)

        self.mvbox5 = QVBoxLayout()
        self.mvbox5.addWidget(self.sunday_table)
        self.sunday_gbox.setLayout(self.mvbox5)

    def _update_table(self, day):
        wk = self.current_week()
        self.cursor.execute("""SELECT teacher.subject, start_time, room_numb,
            teacher.full_name, timetable.id FROM timetable INNER JOIN subject ON timetable.subject = subject.subject_name
            INNER JOIN teacher ON subject.subject_name = teacher.subject WHERE day = %s AND week = %s ORDER BY nomer""", (day, wk))
        records = list(self.cursor.fetchall())

        if day == 'Понедельник':
            self.monday_table.setRowCount(len(records))
            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                joinButton1 = QPushButton("Delete")
                self.monday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
                self.monday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
                self.monday_table.setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
                self.monday_table.setItem(i, 3,
                                          QTableWidgetItem(str(r[3])))
                self.monday_table.setCellWidget(i, 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=i:
                                           self._change_day_from_table(num, 'Понедельник', records[num][4]))
                self.monday_table.setCellWidget(i, 5, joinButton1)
                joinButton1.clicked.connect(lambda ch, num=i:
                                           self._delete_record_from_table(records[num][4]))
                self.monday_table.resizeRowsToContents()

            if len(records) != 5:
                self.monday_table.setRowCount(len(records)+1)
                joinButton = QPushButton("Create")
                self.monday_table.setCellWidget(len(records), 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=len(records):
                                           self._create_day_from_table(num, 'Понедельник'))

        if day == 'Вторник':
            self.tuesday_table.setRowCount(len(records))
            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                joinButton1 = QPushButton("Delete")
                self.tuesday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
                self.tuesday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
                self.tuesday_table.setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
                self.tuesday_table.setItem(i, 3,
                                           QTableWidgetItem(str(r[3])))
                self.tuesday_table.setCellWidget(i, 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=i:
                                           self._change_day_from_table(num, 'Вторник', records[num][4]))
                self.tuesday_table.setCellWidget(i, 5, joinButton1)
                joinButton1.clicked.connect(lambda ch, num=i:
                                            self._delete_record_from_table(records[num][4]))
                self.tuesday_table.resizeRowsToContents()

            if len(records) != 5:
                self.tuesday_table.setRowCount(len(records)+1)
                joinButton = QPushButton("Create")
                self.tuesday_table.setCellWidget(len(records), 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=len(records):
                                           self._create_day_from_table(num, 'Вторник'))


        if day == 'Среда':
            self.wednesday_table.setRowCount(len(records))
            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                joinButton1 = QPushButton("Delete")
                self.wednesday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
                self.wednesday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
                self.wednesday_table.setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
                self.wednesday_table.setItem(i, 3,
                                             QTableWidgetItem(str(r[3])))
                self.wednesday_table.setCellWidget(i, 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=i:
                                           self._change_day_from_table(num, 'Среда', records[num][4]))
                self.wednesday_table.setCellWidget(i, 5, joinButton1)
                joinButton1.clicked.connect(lambda ch, num=i:
                                            self._delete_record_from_table(records[num][4]))
                self.wednesday_table.resizeRowsToContents()

            if len(records) != 5:
                self.wednesday_table.setRowCount(len(records)+1)
                joinButton = QPushButton("Create")
                self.wednesday_table.setCellWidget(len(records), 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=len(records):
                                           self._create_day_from_table(num, 'Среда'))

        elif day == 'Четверг':
            self.thursday_table.setRowCount(len(records))
            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                joinButton1 = QPushButton("Delete")
                self.thursday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
                self.thursday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
                self.thursday_table.setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
                self.thursday_table.setItem(i, 3,
                                            QTableWidgetItem(str(r[3])))
                self.thursday_table.setCellWidget(i, 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=i:
                                           self._change_day_from_table(num, 'Четверг', records[num][4]))
                self.thursday_table.setCellWidget(i, 5, joinButton1)
                joinButton1.clicked.connect(lambda ch, num=i:
                                            self._delete_record_from_table(records[num][4]))
                self.thursday_table.resizeRowsToContents()

            if len(records) != 5:
                self.thursday_table.setRowCount(len(records)+1)
                joinButton = QPushButton("Create")
                self.thursday_table.setCellWidget(len(records), 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=len(records):
                                           self._create_day_from_table(num, 'Четверг'))

        elif day == 'Пятница':
            self.friday_table.setRowCount(len(records))
            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                joinButton1 = QPushButton("Delete")
                self.friday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
                self.friday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
                self.friday_table.setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
                self.friday_table.setItem(i, 3,
                                          QTableWidgetItem(str(r[3])))
                self.friday_table.setCellWidget(i, 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=i:
                                           self._change_day_from_table(num, 'Пятница', records[num][4]))
                self.friday_table.setCellWidget(i, 5, joinButton1)
                joinButton1.clicked.connect(lambda ch, num=i:
                                            self._delete_record_from_table(records[num][4]))
                self.friday_table.resizeRowsToContents()

            if len(records) != 5:
                self.friday_table.setRowCount(len(records)+1)
                joinButton = QPushButton("Create")
                self.friday_table.setCellWidget(len(records), 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=len(records):
                                           self._create_day_from_table(num, 'Пятница'))

        elif day == 'Суббота':
            self.sunday_table.setRowCount(len(records))
            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                joinButton1 = QPushButton("Delete")
                self.sunday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
                self.sunday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
                self.sunday_table.setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
                self.sunday_table.setItem(i, 3,
                                          QTableWidgetItem(str(r[3])))
                self.sunday_table.setCellWidget(i, 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=i:
                                           self._change_day_from_table(num, 'Суббота', records[num][4]))
                self.sunday_table.setCellWidget(i, 5, joinButton1)
                joinButton1.clicked.connect(lambda ch, num=i:
                                            self._delete_record_from_table(records[num][4]))
                self.sunday_table.resizeRowsToContents()

            if len(records) != 5:
                self.sunday_table.setRowCount(len(records)+1)
                joinButton = QPushButton("Create")
                self.sunday_table.setCellWidget(len(records), 4, joinButton)
                joinButton.clicked.connect(lambda ch, num=len(records):
                                           self._create_day_from_table(num, 'Суббота'))

    def _update_timetable(self):
        self.cursor.execute('SELECT week, day, nomer, subject, room_numb, start_time, id FROM timetable')
        records = list(self.cursor.fetchall())
        self.time_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            joinButton1 = QPushButton("Delete")
            self.time_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.time_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.time_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.time_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.time_table.setItem(i, 4,
                                    QTableWidgetItem(str(r[4])))
            self.time_table.setItem(i, 5,
                                    QTableWidgetItem(str(r[5])))
            self.time_table.setCellWidget(i, 6, joinButton)
            joinButton.clicked.connect(lambda ch, num=i:
                                       self._change_timetable(num, records[num][6]))
            self.time_table.setCellWidget(i, 7, joinButton1)
            joinButton1.clicked.connect(lambda ch, num=i:
                                       self._delete_record_from_table(records[num][6]))
            self.time_table.resizeRowsToContents()

        self.time_table.setRowCount(len(records) + 1)
        joinButton = QPushButton("Create")
        joinButton1 = QPushButton("Nothing")
        self.time_table.setCellWidget(len(records), 6, joinButton)
        joinButton.clicked.connect(lambda ch, num=len(records):
                                   self._create_day_for_timetable(num))
        self.time_table.setCellWidget(len(records), 7, joinButton1)

    def _update_subjects(self):
        self.cursor.execute('SELECT subject_name FROM subject')
        records = list(self.cursor.fetchall())
        self.subject_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            joinButton1 = QPushButton("Delete")
            self.subject_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.subject_table.setCellWidget(i, 1, joinButton)
            joinButton.clicked.connect(lambda ch, num=i:
                                       self._change_subject(num, records[num][0]))
            self.subject_table.setCellWidget(i, 2, joinButton1)
            joinButton1.clicked.connect(lambda ch, num=i:
                                       self._delete_subject(records[num][0]))
            self.subject_table.resizeRowsToContents()
        self.subject_table.setRowCount(len(records) + 1)
        joinButton = QPushButton("Create")
        joinButton1 = QPushButton("Nothing")
        self.subject_table.setCellWidget(len(records), 1, joinButton)
        joinButton.clicked.connect(lambda ch, num=len(records):
                                   self._create_subject(num))
        self.subject_table.setCellWidget(len(records), 2, joinButton1)

    def _update_teachers(self):
        self.cursor.execute('SELECT full_name, subject, id FROM teacher')
        records = list(self.cursor.fetchall())
        self.teacher_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Delete")
            joinButton1 = QPushButton("Join")
            self.teacher_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.teacher_table.setCellWidget(i, 2, joinButton1)
            joinButton1.clicked.connect(lambda ch, num=i:
                                        self._change_teacher(num, records[num][2]))
            self.teacher_table.setCellWidget(i, 3, joinButton)
            joinButton.clicked.connect(lambda ch, num=i:
                                       self._delete_teacher(records[num][2]))
            self.teacher_table.resizeRowsToContents()
        self.teacher_table.setRowCount(len(records) + 1)
        joinButton = QPushButton("Create")
        joinButton1 = QPushButton("Nothing")
        self.teacher_table.setCellWidget(len(records), 2, joinButton)
        joinButton.clicked.connect(lambda ch, num=len(records):
                                   self._create_teacher(num))
        self.teacher_table.setCellWidget(len(records), 3, joinButton1)

    def _create_day_for_timetable(self, rowNum):
        row = self.readtext_from_time_table(rowNum)
        nomer = self.nomer(row[5])
        self.cursor.execute(
            'INSERT INTO timetable (week, day, nomer, subject, room_numb, start_time) VALUES (%s, %s, %s, %s, %s, %s)',
            (row[0], row[1], nomer, row[3], row[4], row[5]))
        self.conn.commit()

    def _create_day_from_table(self, rowNum, day):
        row = self.readtext(rowNum, day)
        wk = self.current_week()
        print(wk)
        nomer = self.nomer(row[1])
        print(nomer)
        print(row[0], row[1], row[2])
        self.cursor.execute('INSERT INTO timetable (week, day, nomer, subject, room_numb, start_time) VALUES (%s, %s, %s, %s, %s, %s)',
                            (wk, day, nomer, row[0], row[2], row[1]))
        self.conn.commit()

    def _create_subject(self, rowNum):
        row = self.read_subject(rowNum)
        self.cursor.execute('INSERT INTO subject VALUES (%s)', (row[0],))
        self.conn.commit()


    def _create_teacher(self, rowNum):
        row = self.read_teacher(rowNum)
        self.cursor.execute('INSERT INTO teacher(full_name, subject) VALUES (%s, %s)', (row[0], row[1]))
        self.conn.commit()
    def _change_day_from_table(self, rowNum, day, idx):
        row = self.readtext(rowNum, day)
        nomer = self.nomer(row[1])
        self.cursor.execute(
            """UPDATE timetable SET subject = %s, start_time = %s, room_numb = %s, nomer = %s
            WHERE id = %s""",
            (row[0], row[1], row[2], nomer, idx))
        self.conn.commit()

    def _change_timetable(self, rowNum, id):
        row = self.readtext_from_time_table(rowNum)
        nomer = self.nomer(row[5])
        self.cursor.execute(
            """UPDATE timetable SET week = %s, day = %s, nomer = %s, subject =%s, room_numb = %s, start_time = %s
            WHERE id = %s""",
            (row[0], row[1], nomer, row[3], row[4], row[5], id))
        self.conn.commit()


    def _change_subject(self, rowNum, subject):
        row = self.read_subject(rowNum)
        self.cursor.execute('UPDATE timetable SET subject = %s WHERE subject = %s', (row[0], subject))
        self.cursor.execute('UPDATE teacher SET subject = %s WHERE subject = %s', (row[0], subject))
        self.cursor.execute('UPDATE subject SET subject_name = %s WHERE subject_name = %s', (row[0], subject))
        self.conn.commit()


    def _change_teacher(self, rowNum, id):
        row = self.read_teacher(rowNum)
        self.cursor.execute('UPDATE teacher SET full_name = %s, subject = %s WHERE id = %s', (row[0], row[1], id))
        self.conn.commit()


    def _delete_record_from_table(self, id):
        self.cursor.execute('DELETE FROM timetable WHERE id = %s', (id,))
        self.conn.commit()

    def _delete_subject(self, subject):
        print(subject)
        self.cursor.execute('DELETE FROM timetable WHERE subject = %s', (subject,))
        self.cursor.execute('DELETE FROM teacher WHERE subject = %s', (subject,))
        self.cursor.execute('DELETE FROM subject WHERE subject_name = %s', (subject,))
        self.conn.commit()


    def _delete_teacher(self, id):
        self.cursor.execute('DELETE FROM teacher WHERE id = %s', (id,))
        self.conn.commit()

    def current_week(self):
        wk = datetime.datetime.now().isocalendar().week
        if wk % 2 == 1:
            wk = 1
        elif wk % 2 == 0:
            wk = 2
        return wk

    def nomer(self, time):
        if time == '09.30 - 11.05':
            return 1
        elif time == '11.20 - 12.55':
            return 2
        elif time == '13.10 - 14.45':
            return 3
        elif time == '15.25 - 17.00':
            return 4
        elif time == '17.15 - 18.50':
            return 5

    def readtext_from_time_table(self, rowNum):
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        times = ['09.30 - 11.05', '11.20 - 12.55', '13.10 - 14.45', '15.25 - 17.00', '17.15 - 18.50']
        self.cursor.execute('SELECT subject_name FROM subject')
        records = self.cursor.fetchall()
        subjects = []
        for i in records:
            subjects.append(i[0])
        row = list()

        try:
            row.append(self.time_table.item(rowNum, 0).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введена неделя")

        try:
            row.append(self.time_table.item(rowNum, 1).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введен день")

        try:
            row.append(self.time_table.item(rowNum, 2).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введен номер")

        try:
            row.append(self.time_table.item(rowNum, 3).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введена предмет")

        try:
            row.append(self.time_table.item(rowNum, 4).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введена комната")

        try:
            row.append(self.time_table.item(rowNum, 5).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введено время")

        if not row[0] != '1' and row[0] != '2':
            QMessageBox.about(self, "Error", "Неправильно введена неделя")
        elif row[1] not in days:
            QMessageBox.about(self, "Error", "Неправильно введен день")
        elif row[3] not in subjects:
            QMessageBox.about(self, "Error", "Неправильно введен предмет")
        elif row[5] not in times:
            QMessageBox.about(self, "Error", "Неправильно введено время")
        else:
            return row

    def readtext(self, rowNum, day):
        times = ['09.30 - 11.05', '11.20 - 12.55', '13.10 - 14.45', '15.25 - 17.00', '17.15 - 18.50']
        self.cursor.execute('SELECT subject_name FROM subject')
        records = self.cursor.fetchall()
        a = []
        for i in records:
            a.append(i[0])
        row = list()
        if day == 'Понедельник':
            for i in range(self.monday_table.columnCount()):
                try:
                    row.append(self.monday_table.item(rowNum, i).text())
                except:
                    row.append(None)

        if day == 'Вторник':
            for i in range(self.tuesday_table.columnCount()):
                try:
                    row.append(self.tuesday_table.item(rowNum, i).text())
                except:
                    row.append(None)

        if day == 'Среда':
            for i in range(self.wednesday_table.columnCount()):
                try:
                    row.append(self.wednesday_table.item(rowNum, i).text())
                except:
                    row.append(None)

        if day == 'Четверг':
            for i in range(self.thursday_table.columnCount()):
                try:
                    row.append(self.thursday_table.item(rowNum, i).text())
                except:
                    row.append(None)

        if day == 'Пятница':
            for i in range(self.friday_table.columnCount()):
                try:
                    row.append(self.friday_table.item(rowNum, i).text())
                except:
                    row.append(None)

        if day == 'Суббота':
            for i in range(self.sunday_table.columnCount()):
                try:
                    row.append(self.sunday_table.item(rowNum, i).text())
                except:
                    row.append(None)

        if row[0] is None or row[0] not in a:
            QMessageBox.about(self, "Error", "Неправильно введено занятие")
        elif row[1] is None or row[1] not in times:
            QMessageBox.about(self, "Error", "Неправильно введено время")
        elif row[2] is None:
            QMessageBox.about(self, "Error", "Неправильно введена аудитория")
        else:
            return row

    def read_subject(self, rowNum):
        row = list()
        self.cursor.execute('SELECT subject_name FROM subject')
        records = self.cursor.fetchall()
        subjects = []
        for i in records:
            subjects.append(i[0])
        print(subjects)

        self.cursor.execute('SELECT full_name FROM teacher')
        records = self.cursor.fetchall()
        teachers = []
        for i in records:
            teachers.append(i[0])
        try:
            row.append(self.subject_table.item(rowNum, 0).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введен предмет")

        if row[1] in subjects:
            QMessageBox.about(self, "Error", "Такой предмет уже есть")
        elif row[0] in teachers:
            QMessageBox.about(self, "Error", "Такой преподаватель уже есть")
        else:
            return row

    def read_teacher(self, rowNum):
        row = list()
        self.cursor.execute('SELECT subject_name FROM subject')
        records = self.cursor.fetchall()
        subjects = []
        for i in records:
            subjects.append(i[0])
        print(subjects)
        try:
            row.append(self.teacher_table.item(rowNum, 0).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введенj имя")
        try:
            row.append(self.teacher_table.item(rowNum, 1).text())
        except:
            QMessageBox.about(self, "Error", "Неправильно введен предмет")

        if row[1] not in subjects:
            QMessageBox.about(self, "Error", "Такого предмета нет")
        else:
            return row

    def _update_shedule(self):
        self._update_table('Понедельник')
        self._update_table('Вторник')
        self._update_table('Среда')
        self._update_table('Четверг')
        self._update_table('Пятница')
        self._update_table('Суббота')
        self._update_teachers()
        self._update_timetable()
        self._update_subjects()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
