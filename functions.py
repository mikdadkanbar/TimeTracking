import json
import time 
from datetime import date, timedelta
from dateutil import parser
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib

msg='error'

def write (whole_data , file_name) : #re-write our updated dictionary

    with open(file_name, "w") as file:
        
              json.dump(whole_data, file)                 
                    
def  read ( file_name)    : #return a python dict
    
    with open(file_name , 'r') as file:
        if file.read() !='' : 
            file.seek(0)
            return json.loads( file.read()) 
        else : 
            return {}
        
json_file='users.json'              
dicti=read(json_file)          
break_time=5
study_time=5
long=5

  



def send_emails(data, recipients ):
    global msg
    if len(recipients) > 0 :
        for recipient  in  recipients : 
            send_email(data,recipient)
        msg='Emails Sent Successfully'   
    else:
        msg='No Emails found!'  

        
    def send_email   (data, recipient  ):
        global msg
        if type ( data ) == list and len(data) > 2 :
                #converting it to DataFrame , first list would be the header
                data = pd.DataFrame(data[1:], columns = data[0])

        email_sender = 'test.email.group3@gmail.com'
        password = 'ojnertaqnwmklank'
        subject = 'TimeTrackingApp Report'
        body = f'''

        This is a report requested on {current_date()}


        {data}'''

        

        em = EmailMessage()

        em['From'] = email_sender
        em['To'] = recipient
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, password)
                        smtp.sendmail(email_sender, recipient , em.as_string())
        msg='Email Sent Successfully'           
        

    


   
    




def email_spelling_control (email) :
    if email !='' and '@' in email and '.' in email and email.count( '@') ==1 and email[email.index('@'):].count('.')==1 and email[-1]!= '.' and email.count(' ')==0 : 
        return True
    else : 
            return False

def name_spelling_control (name) :
    if name!='' and name[0] !=' ' and name.count(' ') <2 and name[-1] != ' ' :
        return True
    else:
        return False



def signup (email, name) : 
    global msg
    email=email.lower()

    if email_spelling_control(email) and name_spelling_control(name) : 

        if email not in dicti.keys() : 
            new_user_data ={ email : {"name": name, 
                                    "projects": {}  ,
                                    'recipients' : [email] } }
            dicti.update (new_user_data) 
            write(dicti,json_file)
            msg=f'{name} is successfully registered!'
            return True
        else:
            msg= 'Email already registered!'
            return False
    else:
        msg='Email or name format is incorrect!'
  

def login(email):
    global msg
    email=email.lower()
    if email_spelling_control(email) : 
        if email in dicti.keys() : 
            
            global user1
            user1=User(email)
            msg=f'{user1.name} is logged in'
            return True
            
        else : 
            
            user1='Not found'
            msg='Email not registered!'
            return False
    else:
        msg='Email format is incorrect'   


def time_difference(a,b)  : 
    return str(parser.parse(b) - parser.parse(a ))[:-3]

def current_time() :

    t = time.localtime()
    return time.strftime("%H:%M", t)


def current_date():
       today = date.today()
       return  today.strftime("%d/%m/%Y") 


def timer (t) : 
        global msg
        t*=60
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            # msg=f'timer, end="\r"'
            print (timer, end="\r")
           
            time.sleep(1)
            t -= 1
            # print (msg)
        msg='Finished!'      

        
        
        
class User  : 
    def __init__ ( self, email):
        self.data = dicti.get (email)
        self.email=email
        self.name=self.data.get('name')
        self.projects= self.data.get('projects')
        self.recipients=self.data.get('recipients')
        self.history=[]
#       
      
    def add_recipient (self , email)       :
        global msg
        if email_spelling_control (email): 
                
            if email not in  self.recipients : 
                
                self.recipients.append ( email)
                self.update()
                msg='Recipient Added Successfully!'
            else:
                msg='Recipient Already Existed!'    
        else:
            msg='Email format is incorrect!'
    
    def delete_recipient(self, email) :
        global msg
        if email_spelling_control (email): 
                
            if email  in  self.recipients : 
                
                self.recipients.remove ( email)
                self.update()
                msg='Recipient Deleted Successfully!'
            else:
                msg='Recipient Not Found!!'    
        else:
            msg='Email format is incorrect!'

    

    def project_existed (self, project) : 
        if project  in  self.data.get('projects').keys() : 
            return True
        else:
            return False
    def subject_existed (self, project, subject) : 
        if self.project_existed(project) and subject in self.data.get('projects') .get(project).keys(): 
            return True
        else:
            return False
    
    
    def add_project (self,project) : 
            global msg
            if name_spelling_control(project) : 

                if  not self.project_existed (project) :
                    self.data.get('projects')[project]={}
                    self.update()
                    msg=f'{project} is successfully added !'
                else : 
                    msg= f'{project} is already added before!'
                # print (msg)   
            else :
                msg='Project name format is incorrect!'

    def delete_project (self,project) : 
        global msg
        
        if self.project_existed (project) :
            del self.projects  [ project ]
            self.update()
            msg= f' {project} Deleted Successfully!'
        else: 
                msg='Project Not found!'
        print (msg)
       
    def add_subject(self, project, subject) : 
        global msg
        if name_spelling_control (subject) :
                
            if  self.project_existed ( project ) :
                
                if not self.subject_existed(project, subject)  : 
                    self.data.get('projects') .get(project)[subject] = {}
                    self.add_promodoro ( project, subject)  
                    self.update()
                    msg = f'{subject} added to Project {project}'
                else : 
                    msg='Subject already existed !'
            else :
                msg = 'Project Not existed !'
        else:
            msg='''Format of subject's name is incorrect '''        
        # print (msg)  
        
    def delete_subject(self, project, subject) : 
        global msg
        if  self.project_existed ( project ) :
            
            if  self.subject_existed(project, subject)  : 
                  del user1.data.get('projects') .get(project)[subject] 
                  self.update()
                  msg = f'{subject} Deleted Successfully'
            else : 
                msg='Subject Not Found! !'
        else :
            msg = 'Project Not existed !'
            
        print (msg)  
        
 


        
    def add_promodoro(self, project, subject) :   
        global msg
        if self.project_existed ( project ) :
            if self.subject_existed ( project, subject  ) :
                
                 
                    task='task'
                    Break='break'
            #         #determine last promodoro number : 
                    l=sorted  ( list( self.data.get('projects') .get(project).get (subject).keys()) )
                    print (l)
                    if len(l) == 0 :
                        next_promodoro='1'
                    else :
                        last_promodoro= int (l[-1])
                        print (last_promodoro)
                        next_promodoro = str( last_promodoro +1 )
                        #   [0, Break, 0 , break_time, 'start', 'finish','time consumed' , 'date' ]
                    self.data.get('projects') .get(project).get (subject)[ next_promodoro ] = {
                                  'study1' : [ 0, task, 0 , study_time, '00:00', '00:00','00:00' , 'date' ],
                                  'break1' :  [0, Break, 0 , break_time,'00:00', '00:00','00:00' , 'date' ],
                                  'study2' : [ 0,task, 0 , study_time, '00:00', '00:00','00:00' , 'date' ],
                                  'break2' :  [ 0,Break, 0 , break_time, '00:00', '00:00','00:00' , 'date' ],
                                  'study3' : [ 0,task,0 , study_time, '00:00', '00:00','00:00' , 'date' ],
                                 'break3' : [0, Break, 0 , break_time, '00:00', '00:00','00:00' , 'date' ],
                                  'study4' : [0, task, 0 , study_time, '00:00', '00:00','00:00' , 'date' ],

                                  'long_break' :  [0, Break, 0 , long, '00:00', '00:00','00:00' , 'date' ],
                              }


                    self.update()
                    # msg=f'{next_promodoro} successfully added'
                    # print (msg)
                
                
                
                
            else: 
                msg='Subject Not Found'
            
        else:
            msg='Project Not found !'
            
        print (msg)
        
        
        
       
        
    def delete_promodoro(self, project, subject , promodoro ):
         global msg
         if self.project_existed ( project ) :
            if self.subject_existed ( project, subject  ) :
                if promodoro  in self.data.get('projects').get(project).get(subject)  :
                  del self.data.get('projects').get(project).get(subject)[promodoro] 
                  self.update()
                  msg='Promodoro Deleted Successfully !'
                else:
                    msg='Promodoro Not Found!'
            else: 
                msg='Subject Not Found'
            
         else:
            msg='Project Not found !'
            
         print (msg)
        
        
    def get_promodoros (self, project, subject ) : 
         global msg
         if self.project_existed ( project ) :
            if self.subject_existed ( project, subject  ) :
               list_p= list(self.data.get('projects').get(project).get (subject).keys())
            #    msg='done'  
               return list_p
            else: 
                msg='Subject Not Found'
            
         else:
            msg='Project Not found !'
            
#          print (msg)
         
        
    
    
        
        
    def get_sessions (self, project, subject, promodoro)   : 
         global msg
         if self.project_existed ( project ) :
            if self.subject_existed ( project, subject  ) :
                if promodoro in  self.data.get('projects').get(project).get (subject).keys() :
                    list_sessions =   list(self.data.get('projects').get(project).get (subject).get(promodoro).keys())
                    # msg='list of sessions returned successfully'
#                     print (msg)
                    return list_sessions
                else: 
                        
                        msg='Promodoro Not existed!'
            else: 
                msg='Subject Not Found'
            
         else:
            msg='Project Not found !'

    def get_subjects (self, project): 
     
     if  self.project_existed ( project ) :
        subjects_list = list(self.data.get('projects').get(project).keys())
        if len( subjects_list ) > 0 : 
            return     subjects_list
        else:
            return ['...' ]
           
     else :
            msg = 'Project Not existed !'
            return ['...']
            
    def get_projects(self)   : 
        projects_list = list(self.data.get('projects').keys())
        if len( projects_list ) > 0 : 

            return     projects_list
        else :
            return ['...'    ]
        
         
    def get_history (self, project, subject,before_days) :
    # this should return all sessions for a subject , as lists , each for a session (rows)
    #all  sessions must satisfy the date condition (should be after the date passed)
    #first : list all sessions , then we will return only those which satisfy the date
        all_sessions =[]
        current_list=[]
        date_point=0
        if before_days!='All' :
         
        

            before_days=int(before_days)
            #creating a new date point : by subtracting this number of days from current date
            date_point = parser.parse (current_date()) - timedelta(days=before_days)

        if self. project_existed(project) and self. subject_existed (project ,subject):
            #1- get promodoros : 2-get sessions for each promodoro
            for p in self.get_promodoros(project, subject) :
                # print (p)
                for session2  in self.get_sessions(project, subject,p):
                    
                    current_list = (self.data.get('projects') .get(project).get (subject).get(p).get(session2))
                    current_list = [session2] + current_list
                    #  current_list.insert(0,session2)
                    # print (f'{session2}  : {current_list}')
                    #now, before adding : let's filter it : 

                    if  (date_point ==0 ) or (current_list[-1] !='date' and parser.parse  (current_list[-1]) > date_point )   :
                        if  current_list[1]!=0  : 
                         all_sessions.append(current_list)
                    
                
            #filtering all sessions : 
            self.history=all_sessions.copy()
            header = [ 'Name of session', 'Session Done', 'Task','Task Done' , 'Normal Time', 'Start Time', 'Finish Time','Time Consumed' , 'Date' ]
            self.history.insert(0, header)
            return  all_sessions


         
 
    
    def get_next_session (self , project, subject  ) : 
        #list all promodoros : 
        global msg
        next_s='all sessions done > create new promodoro'
        if self.project_existed(project) and self.subject_existed (project, subject) : 
            last_p=self.get_promodoros ( project, subject) [-1]
    #        get sesisons inside it : 
            # msg=f'last P is : {last_p} '
            lastP_sessions= self.data.get('projects').get(project).get (subject).get(last_p) 
            for _session in  lastP_sessions.keys() : 
                if lastP_sessions.get(_session)[0]==0 :
                    next_s=_session
                    break
            print (next_s)
            if next_s=='all sessions done > create new promodoro' :
                self.add_promodoro(project, subject )
                print ('New Promodoro Created!')
                self.get_next_session(project, subject )
            # creating a  current object + passing all found info to it :
            if next_s!='all sessions done > create new promodoro' :
                global current
                current = Current( project, subject , last_p , next_s )
                print (current.__dict__)
            return True    
        return False
    #     [ 0, task, 0 , study_time, 'start', 'finish','finish-start' , 'date' ]


    def start_timing_session ( self,current )    : 
        global skipped
        skipped= False
        if isinstance (current, Current) : 
            current.session[4]=current_time()  #start at
            
            # timer(current.session[3]) #start timing
            
            #here : there's a chance of a skip :
            
            if not skipped : 
                current.session[0]=1 #done
                current.session[5]=current_time() #finish
                current.session[6]= time_difference( current.session[4] ,current.session[5]) 
                current.session[-1]= current_date()  #date
                current.update_in_user()
            
#         if current.session_name=='long_break'  : 
#             print ('yes it is long break')
#             self.add_promodoro (current.project, current.subject, current.task)
    
    def skip  (self):
                skipped=True
        #first let's update the current session : make it -1 instead of 0 :
                current.session[0]=-1 #skipped
                current.session[5]=current_time() #finish
                #if start date is not alreay there : add it : 
                if current.session[4] =='00:00' :
                    current.session[4] =current_time() 
                current.session[6]= time_difference( current.session[4] ,current.session[5]) 
                current.session[-1]= current_date()  #date
                #if start is not yet registered > he skipped immediately
                current.session[4]=current_time()
                current.update_in_user()
        #now : remove the current timer and return to the prev screen
        
    def label_not_finished (self) :   
        global msg
        if  current.session_name not in ['break1', 'break2', 'break3','long_break'] and current.session[1] !='task' and current.session[0] !=0: 

            
                 current.session[2]= -1 #task not done
                 current.update_in_user()
                 msg='Task labeled unfinished'
        else:
            msg='you need to either to start the session , or to add a task!'


    def label_finished (self)     :
        
        global msg
        if  current.session_name not in ['break1', 'break2', 'break3','long_break'] and current.session[1] !='task' and current.session[0] !=0:

                 current.session[2]=1 #task done!
                 current.session[5]=current_time() #finish time 
                 current.session[6]= time_difference( current.session[4] ,current.session[5])  #time consumed
                 current.session[-1]= current_date() 
                 current.update_in_user()
                 msg='Task labeled finished!'
        else:
            msg='you need to add a task!'

        
    def update(self) : 

        dicti.update ({self.email : { 'name' : self.name , 'projects' : self.projects , 'recipients': self.recipients }})
        self.data =  dicti.get (self.email)  
        write(dicti,json_file)    #Re write          
    
class Current():
    def __init__(self, project, subject ,   promodoro , session ) : 
        self.project = project
        self.subject = subject
         
        self.promodoro =   promodoro
        self.session_name = session
        self.session = user1.data.get('projects').get(project).get (subject).get(promodoro).get(session) 
    def update_in_user (self) : 
        user1.data.get('projects').get(self.project).get (self.subject).get(self.promodoro)[self.session_name]= self.session
        user1.update()
        print ('updated')
        
# login('m@gmail.com')
# user1.add_recipient('ddf@.com')
# print (user1.recipients)
# print (msg)
# # print (user1.data)
# print ( user1.get_projects())       
# user1.delete_project('Mathtt')
# print ( user1.get_projects()) 
# user1.add_project('Mathtt')
# print ( user1.get_subjects('Mathtt'))  
# print (user1.history)

# user1.get_history('Math', 'Stat')
# print (user1.history)
# # print(user1.data)