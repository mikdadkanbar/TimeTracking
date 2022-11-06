from time import time
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QDialog, QApplication ,QLabel
from PyQt5.uic import loadUi

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import  functions  
import time
from PyQt5.QtGui import QColorConstants
from PyQt5.QtCore import Qt 
Email=''
logged=False







class First(QDialog):
    def __init__(self):
        super(First,self).__init__()
        loadUi("first.ui",self)

        self.email_input. setText ('m@gmail.com')
        self.login_button.clicked.connect(self.login_press)
        self.signup_button.clicked.connect(self.signup_press)
       
        
        self.goToMain.clicked.connect(self.go_to_main)
       
    
    def login_press(self) :
       global logged
       #take value of the email input :
       #call login function from 
       email=self.email_input.text()
       
       logged = functions.login(email)
       self.error_msg.setText(functions.msg) 
       print (logged)
    
       global Email
       Email=email
       self.go_to_main()

    def signup_press(self) :
        #get text values :
        email=self.email_input2.text()
        name=self.name_input.text() 
       
            #now sign up : 
        functions.signup(email,name)
        self.error_msg.setText(functions.msg) 
         


    

    def go_to_main(self):
        if logged : 
            main = Main()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex()+1)

class Promodoro(QDialog):
    def __init__(self):
        super(Promodoro,self).__init__()
        loadUi("promodoro.ui",self)

        
        self.add_task_Button.clicked.connect(self.add_task)
        self.go_to_main_Button.clicked.connect(self.go_to_main)
        self.start_Button.clicked.connect(self.start)
        self.skip_Button.clicked.connect(self.skip)
        self.unfinished_Button.clicked.connect(self.unfinished)
        self.finished_Button.clicked.connect(self.finished)
          
        self.msg_label.setText( f'{functions.current.session_name} : {functions.current.session [3] }'  )
    
    def finished (self) : 
        if functions.current.session[0]!= 0 and  functions.current.session_name not in ['break1', 'break2', 'break3','long_break'] : 
            functions.user1.label_finished()    
            self.go_to_main()
            self.msg_label.setText(functions.msg)

    def timer (self,t) : 
        
        while t:
            mins, secs = divmod(t, 60)
            timer2 = '{:02d}:{:02d}'.format(mins, secs)
            # msg=f'timer, end="\r"'
            # print (timer, end="\r")
           
            time.sleep(0.5)
            t -= 1
            
            # self.lcdNumber.display(timer)
            self.msg_label.setText(timer2  )
            QApplication.processEvents()

        self.msg_label.setText('Finished!'  )


    def add_task (self) : 
                    task = self.task_input.text()
                    #changing task only if it is not a break
                    if  task !='' and task != ' ' and  functions.current.session_name not in ['break1', 'break2', 'break3','long_break']:
                        functions.current.session[1]=task
                        functions.current.update_in_user()
                        self.msg_label.setText('Task added!')
                        self.task_label.setText(task)
                    else:
                        functions.msg=''
                    # self.start()

    def unfinished (self) : 
        # if main2.current.session_name not in ['break1', 'break2', 'break3','long_break']:
            # main2.current.session[2]=-1
            # main2.current.update_in_user()
            functions.user1. label_not_finished ()
            self.msg_label.setText(functions.msg)



    def go_to_main (self) : 
                    main = Main()
                    widget.addWidget(main)
                    widget.setCurrentIndex(widget.currentIndex()+1)

    def start(self) : 
                    
                    functions.user1.start_timing_session (functions.current)
                    self.timer(functions.current.session[3])
                    # self.go_to_main()
                    
    def update_label (self, s) :
        pass


                
    def skip (self):
        #if msg_label.Text != 'finished!' : ??
        functions.user1.skip()     
        self.go_to_main()
        # msg_label
        
        # skip_Button

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__()
        loadUi("main.ui",self)
        # main2.login(Email)
        self.msgLabel.setText(functions.msg)
        # self.comboProject.addItems(main2.user1.get_projects())
        # self.comboProject2.addItems(main2.user1.get_projects())
        self.update_combos()

         
         
        self.comboProject.activated.connect(self.load_items  )
        self.showHistoryButton.clicked.connect(self.show_history_press )

        self.backButton.clicked.connect(self.go_first )
        self.addProjectButton.clicked.connect(self.add_project )
        self.addSubjecttButton.clicked.connect(self.add_subject )
        self.start_promodoro_Button.clicked.connect(self.start_promodoro )
        self.delete_subject_Button.clicked.connect(self.delete_subject )
        self.delete_project_Button.clicked.connect(self.delete_project )

        self.add_r_Button.clicked.connect(self.add_recipient )
        self.delete_r_Button.clicked.connect(self.delete_recipient)

        self.delete_project_Button.clicked.connect(self.delete_project )
        
        self.email_history_Button.clicked.connect(self.email_history)

    def email_history (self):
        functions.send_email(functions.user1.history , functions.user1.recipients[0])
        self.msgLabel.setText(functions.msg)

    def add_recipient  (self) : 
            recipient =self.recipient_input.text()
            functions.user1.add_recipient(recipient)
            self.msgLabel.setText(functions.msg)
            self.update_combos()
            

    def delete_recipient(self) : 

            recipient =self.emails_combo.currentText()
            functions.user1.delete_recipient(recipient)
            self.msgLabel.setText(functions.msg)
            self.update_combos()


    def delete_project  (self) :
        
        project =self.comboProject.currentText()
        functions.user1.delete_project(project)
        self.msgLabel.setText(functions.msg)
        self.update_combos()


    def delete_subject  (self) :   
        subject =self.comboSubject.currentText()
        project =self.comboProject.currentText()
        functions.user1.delete_subject(project , subject)
        self.msgLabel.setText(functions.msg)
        self.update_combos()

    def     start_promodoro (self):
        # del main2.user1
        # main2.login(Email)
        #1-get next session for the selected proj & subj
        subject3=self.comboSubject.currentText()
        project3=self.comboProject.currentText()
        if functions.user1.get_next_session(project3,subject3 ) : 
        #2-go to another screen
            self.go_promodoro ()
        #3- you can access all about current session info from main2.current
        

        # going to Promodoro screen : 
        


    def go_promodoro (self )    :
            promodoro = Promodoro()
            widget.addWidget(promodoro)
            widget.setCurrentIndex(widget.currentIndex()+1)


        
        
    def add_project (self) : 
        project  = self.projectText.text()
        functions.user1.add_project(project)
        self.msgLabel.setText(functions.msg)
        self.update_combos()
        # self.comboProject2.clear()
        # self.comboProject.clear()

        # self.comboProject2.addItems(main2.user1.get_projects())
        # self.comboProject.addItems(main2.user1.get_projects())


    def add_subject (self) : 
        subject  = self.subjectText.text() 
        project = self.comboProject2.currentText()
        functions.user1.add_subject(project , subject)
        self.msgLabel.setText(functions.msg)
        # self.comboSubject.clear()
        self.update_combos()

    def update_combos (self):
        self.comboProject2.clear()
        self.comboProject.clear()
        self.comboSubject.clear()
        self.emails_combo.clear()

        self.comboProject2.addItems(functions.user1.get_projects())
        self.comboProject.addItems(functions.user1.get_projects())
        self.emails_combo.addItems(functions.user1.recipients)
        self.comboSubject.addItems(functions.user1.get_subjects(self.comboProject.currentText()) )


    def go_first(self):
        
            first = First()
            widget.addWidget(first)
            widget.setCurrentIndex(widget.currentIndex()+1)




    def load_items (self ) :
        self.comboSubject.clear()
        self.comboSubject.addItems(functions.user1.get_subjects(self.comboProject.currentText()) )
        

    def show_history_press (self) :
        # del main2.user1
        # main2.login(Email)
        history_list=[]
        subject=self.comboSubject.currentText()
        project=self.comboProject.currentText()
        before_days=self.before_days.currentText()
        history_list= functions.user1.get_history (project, subject, before_days)

        # del main2.user1
        # main2.login(Email)
        # print  (history_list)
        self.load_data(history_list)

    def load_data(self, lists)  :

        if type (lists)==list : 
            self.tableWidget.setRowCount(len(lists))

            for i in range (len(lists) ) : 
                for j in range( len(lists[i]) ):
                    # print (f'i is {i} and j is {j}')
                    self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str (lists[i][j])) )       

    





app = QApplication(sys.argv)
UI =First() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
#  UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(1800)
widget.setFixedHeight(1600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())