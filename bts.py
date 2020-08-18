#mac 환경에서 개발됨
from tkinter import*
from tkinter import messagebox
import tkinter.simpledialog
import random
import time
import sqlite3
from playsound import playsound

## define global variable
#뒷장 빼고 총 16장
fnameList = ["BTS01.png", "ARMY.png","JHOPE01.png", "JHOPE02.png", "JIMIN01.png", "JIMIN02.png", "JIN01.png", "JIN02.png", "JK01.png", "JK02.png", "RM01.png", "RM02.png", "SUGA01.png", "SUGA02.png", "V01.png", "V02.png"]
photoList = [None] * 100
pLabelList = [None] * 100 
cardList = [None] * 100
prevCard = ""
num = 2
prevnum = 100
complete = 0
level = 1
score = 0
score1 = 0
score2 = 0
count = 60
nickname = ""
con, cur = None, None
sql = ""
turn = ""
listName = [None]*5
listLevel = [None]*5
listScore = [None]*5

con = sqlite3.connect("gameDB")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS userTABLE (userName char(15), userLevel int, userScore int)")
#DB 없을시 새로 생성. 사용자 이름, 최종레벨, 최종점수를 저장하는 userTable 생성

class CreateAccount(tkinter.simpledialog.Dialog):     
    def body(self, window):
        tkinter.Label(window, text="닉네임 입력: ", font=("",20)).grid(row=0)
        tkinter.Label(window, text="------------------------------------------", font=("",15)).grid(row=1, columnspan=2)
        tkinter.Label(window, text="LEVEL 1", font=("",30)).grid(row=2, columnspan=2)
        tkinter.Label(window, text="OK를 누르면 게임이 바로 시작됩니다", font=("",15)).grid(row=3, columnspan=2)
        tkinter.Label(window, text="시작후 3초간 전체 카드를 보여드립니다", font=("",15)).grid(row=4, columnspan=2)
        tkinter.Label(window, text="##제한시간 50초!!##", font=("",15)).grid(row=5, columnspan=2)
        tkinter.Label(window, text="##스페셜카드 맞출경우 200점##", font=("",15)).grid(row=6, columnspan=2)
        tkinter.Label(window, text="------------------------------------------", font=("",15)).grid(row=7, columnspan=2)
        self.user_id = tkinter.Entry(window)
        self.user_id.grid(row=0, column=1)        
    def apply(self): # OK button click event
        global nickname
        global level 
        global score
        level = 1 #새로 시작시 닉네임, 레벨, 점수 초기화
        score = 0 
        nickname = ""
        nickname = self.user_id.get()
        play=Singleplay()
        play.in_game(level)

class CreateAccountMulti(tkinter.simpledialog.Dialog):     
    def body(self, window):
        tkinter.Label(window, text="Player1 닉네임 입력: ", font=("",20)).grid(row=0)
        tkinter.Label(window, text="Player2 닉네임 입력: ", font=("",20)).grid(row=1)
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=2, columnspan=2)
        tkinter.Label(window, text="OK를 누르면 게임이 바로 시작됩니다", font=("", 15)).grid(row=3, columnspan=2)
        tkinter.Label(window, text="시작후 3초간 전체 카드를 보여드립니다", font=("", 15)).grid(row=4, columnspan=2)
        tkinter.Label(window, text="처음 시작은 랜덤으로 정해드립니다.", font=("", 15)).grid(row=5, columnspan=2)
        tkinter.Label(window, text="##스페셜카드 맞출경우 200점##", font=("", 15)).grid(row=6, columnspan=2)
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=7, columnspan=2)
        
        self.player1_id = tkinter.Entry(window)
        self.player1_id.grid(row=0, column=1)
        self.player2_id = tkinter.Entry(window)
        self.player2_id.grid(row=1, column=1)
        
    def apply(self):# OK button click event
        global player1
        global player2
        global level 
        global score1
        global score2
        
        player1 = self.player1_id.get()
        player2 = self.player2_id.get()
        score1, score2 = 0, 0
        play=Multiplay()
        play.in_game(4)

class NextLevel(tkinter.simpledialog.Dialog): #레벨 완료시 뜨는 Dialog
    global level    
    def body(self, window):
        tkinter.Label(window, text="------------------------------------------", font=("",15)).grid(row=0, columnspan=2)
        tkinter.Label(window, text="Level Clear!", font=("",30)).grid(row=1,columnspan=2)
        tkinter.Label(window, text="OK를 누르면 다음 레벨이 바로 시작됩니다.", font=("", 15)).grid(row=2, columnspan=2)
        tkinter.Label(window, text="시작후 3초간 전체 카드를 보여드립니다", font=("", 15)).grid(row=3, columnspan=2)
        tkinter.Label(window, text="제한시간 50초!!", font=("", 15)).grid(row=4, columnspan=2)
        tkinter.Label(window, text="##스페셜카드 맞출경우 200점##", font=("", 15)).grid(row=5, columnspan=2)
        tkinter.Label(window, text="LEVEL"+str(level), font=("", 30)).grid(row=6, columnspan=2)
        tkinter.Label(window, text="------------------------------------------", font=("",15)).grid(row=7, columnspan=2)
       
    def apply(self):# OK button click event
        play=Singleplay()
        play.in_game(level) #다음 레벨 게임 진행

class Gameover(tkinter.simpledialog.Dialog): #시간이 초과되어 게임이 끝났을 때 뜨는 Dialog   
    global level
    global score
    global nickname
    global sql
    def body(self, window):
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=0, columnspan=2)
        tkinter.Label(window, text="LEVEL" + str(level) +" Game Over!", font=("",25)).grid(row=1,columnspan=2)
        tkinter.Label(window, text= nickname +"님 최종점수: "+ str(score) + "점", font=("", 25)).grid(row=2, columnspan=2)
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=3, columnspan=2)
    def apply(self):# OK button click event
        sql = "INSERT INTO userTable VALUES('"+nickname+"',"+str(level)+","+str(score)+")" #사용자의 닉네임, 레벨, 점수를 DB에 추가
        cur.execute(sql)
        con.commit()
        con.execute("SELECT * FROM userTable")
        print(nickname, level, score)        
        quit

class MultiEnd(tkinter.simpledialog.Dialog): #멀티플레이가 종료되었을 때 뜨는 Dialog. player별 점수와 최종 승리자를 알려줌. 
    global score1
    global score2
    global player1
    global player2
    
    def body(self, window):
        tkinter.Label(window, text="게임종료", font=("",30)).grid(row=0, columnspan=2)
        tkinter.Label(window, text=player1 + " : " + str(score1) + "점", font=("",20)).grid(row=1, columnspan=2)
        tkinter.Label(window, text=player2 + " : " + str(score2) + "점", font=("",20)).grid(row=2, columnspan=2)
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=3, columnspan=2)
        if score1 > score2:
            tkinter.Label(window, text=player1 + "승리!", font=("",25)).grid(row=4, columnspan=2)
        elif score1 == score2:
            tkinter.Label(window, text="무승부!", font=("",20)).grid(row=4, columnspan=2)
        else:
            tkinter.Label(window, text=player2 + " 승리!", font=("",30)).grid(row=4, columnspan=2)
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=5, columnspan=2)
        tkinter.Label(window, text="다시하시겠습니까?", font=("",20)).grid(row=6, columnspan=2)
            
    def apply(self):# OK button click event
        global score1
        global score2
        score1=0
        score2=0
        play=Multiplay()
        play.in_game(4) #OK 버튼 클릭시 기존 player 정보 유지한 채 새로운 게임 시작. score 리셋됨. 

class Ranking(tkinter.simpledialog.Dialog): #싱글플레이 랭킹 확인용 Dialog
    global listName
    global listLevel
    global listScore
    i = 0
    j = 0
    def body(self, window):
        tkinter.Label(window, text="Single Play 랭킹", font=("",40)).grid(row=0, columnspan = 3)
        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=1, columnspan=3)
        for i in range(5):  #점수에 따라 상위 5명의 정보만 가져옴
            tkinter.Label(window, text=str(i+1)+"위    " + listName[i], font=("",30)).grid(row=i+2, column = 0, sticky="w")
            tkinter.Label(window, text="    LEVEL" + str(listLevel[i])+ "    ", font=("",30)).grid(row=i+2, column = 1, sticky="w")
            tkinter.Label(window, text=str(listScore[i])+"점", font=("",30)).grid(row=i+2, column = 2, sticky="e")

        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=7, columnspan=3)
        
    def apply(self):
        quit
        
    
class Singleplay():
    randList = []
    pLabelList = []
    column_card = 1
    row_card = 4
    num_card = 0
    choice_card=0
    list_set = 0
    i, j, k = 0, 0, 0
    
    def in_game(self, level):
        
        def make_card(self, level): #카드를 섞어 배열하는 함수, 레벨별로 카드 수가 달라짐
            global cardList
            global pLabelList
            global complete
            
            self.column_card = 1 + level #배열될 카드의 열은 level보다 1이 크다. level 1이 2x4임.
            self.row_card = 4 #카드의 행은 4로 유지됨.
            self.num_card = (self.column_card * self.row_card) #카드의 수는 행x열로 계산
            self.choice_card = int(self.num_card / 2) #카드의 수를 반으로 나눠서, 쌍 갯수를 따로 저장
            self.list_set = 0
            complete = self.choice_card #쌍 갯수 세어서 저장, 추후 clickcard에서 쓰일 예정 모든 짝을 맞추면 게임이 완료되는 변수

            self.randList = random.sample(range(0,15), self.choice_card) #지정한 범위 내에서 choice_card(카드쌍) 수만큼 번호를 뽑아 리스트에 저장. choice_card 수는 레벨별로 달라져야함. 2레벨:4개, 3레벨:6개...
            self.randList += self.randList  #뽑은 리스트를 복제해서 이어붙임 최종적으로 같은 카드가 두개씩 생성됨.
            random.shuffle(self.randList) #전체 카드를 섞는다.
            
            i, j, k = 0, 0, 0

            photoList = [None] * self.num_card #사진을 저장할 리스트를 카드 수만큼 생성
            pLabelList = [None] * self.num_card #화면에 배치하여 보여줄 라벨 리스트를 카드 수만큼 생성 
            cardList = [None] * self.num_card #해당하는 사진의 이름을 저장할 리스트를 카드 수만큼 생숭
            
            for i in range(1, self.column_card+1): #row_card가 행, column_card가 열로 level 1 에서 2x4 카드로 그리드 형식으로 보여주려함. level n이면 (n+1)x4 형식
                for j in range(1, self.row_card+1):
                    photoList[self.list_set] = PhotoImage(file = "image/" + fnameList[self.randList[self.list_set]])
                    pLabelList[self.list_set] = Label(self.ingame, image=photoList[self.list_set], borderwidth=0) #보여지는 동안 사용자가 선택하지 못하게 Label로 설정
                    pLabelList[self.list_set].grid(row=i, column=j)
                    pLabelList[self.list_set].configure(image=photoList[self.list_set])
                    pLabelList[self.list_set].image = photoList[self.list_set]
                    cardList[k] = fnameList[self.randList[self.list_set]] #나중에 카드 뒷면으로 덮으면 라벨 리스트의 사진들도 초기화되기 때문에 사진 이름을 리스트에 따로 저장
                    k += 1                   
                    self.list_set += 1

                    
        def hide_card(self): #make_card함수로 생성 및 배열된 카드를 동일한 이미지(뒷면)으로 바꾸는 함수
            global pLabelList
            global count
            self.list_set=0
            for i in range(1, self.column_card+1): 
                for j in range(1, self.row_card+1):
                    photoList[self.list_set] = PhotoImage(file = "image/BTS.png")                    
                    pLabelList[self.list_set] = Button(self.ingame, image=photoList[self.list_set], borderwidth=0, command = lambda k=self.list_set: click_card(k))
                    #람다식을 활용하여 해당 버튼 클릭시 click_card 함수 호출. 
                    pLabelList[self.list_set].grid(row=i, column=j, sticky = "nesw")
                    pLabelList[self.list_set].configure(image=photoList[self.list_set])
                    pLabelList[self.list_set].image = photoList[self.list_set]
                    self.list_set += 1

            count = 50 #제한시간 50초로 설정
        
            if count >= 0: #제한시간이 0이 될때까지 counter함수를 호출하여 제한시간을 라벨을 통해 보여줌
                counter(self)
            
                

        
        def counter(self): #제한시간을 보여주는 함수. 50초에서 1초씩 줄어든다.
            global count
            count -= 1
            self.timer_label = Label(self.ingame, text=str(count)+"초", font =("", 15)).grid(row=0, column= 4, columnspan=2)
            self.ingame.after(1000, counter, self) 
            if count == 0: #제한시간이 0이 되면 게임 종료
                self.ingame.destroy() 
                Gameover(window) #Gameover 클래스 실행
            
                    
     
               
        def click_card(k): #뒤집혀있는 카드를 클릭할 시 발생하는 함수
            global num #전역변수 num은 2로 초기화되어 있다. 두 개를 뒤집으면 서로 비교하게 하기 위함. 카드를 한번에 두개 초과해서 클릭할 수 없음.
            global prevCard
            global prevnum
            global complete
            global level
            global score

            if k == prevnum: #이전에 눌렀던 카드를 또 선택한 경우 횟수 차감되지 않게함.
                num = 1
            else : #카드 클릭시 기존의 이미지를 보여주고, num을 1 차감함.      
                photoList[k] = PhotoImage(file = "image/" + cardList[k])
                pLabelList[k].image = photoList[k]
                pLabelList[k].configure(image=photoList[k])
                pLabelList[k].image=photoList[k]
                pLabelList[k].update()
                num -= 1
  
            if num == 0: #카드 두개를 선택하여 num이 0이 되면, 이전의 카드와 현재 카드를 비교함 
                if prevCard == cardList[k]: #만약 이전 카드와 현재 카드가 같다면 이미지를 그대로 유지하고, num을 2로 초기화함.
                    pLabelList[k].config(state='disabled') #맞춘 카드를 다시 뒤집지 못하게 Button 상태를 disabled로 설정함.
                    pLabelList[prevnum].config(state='disabled')
                    num = 2
                    complete -= 1 #총 맞춰야 할 카드쌍의 수에서 1을 차감.
                    score += 100
                    if cardList[k] == "ARMY.png": #스페셜 카드를 뒤집을 경우 100점 추가 점수 부여
                        score += 100
                    elif cardList[k] == "BTS01.png": #스페셜 카드를 뒤집을 경우 100점 추가 점수 부여
                        score += 100
                    self.score_label = Label(self.ingame, text="SCORE: " + str(score), font=("",15)).grid(row=0, column = 0, columnspan=2)
                    #변경된 점수를 label로 나타냄
                                              
                else: #선택한 두 카드가 다르다면                   
                    time.sleep(0.2) # 0.2초 해당 카드를 확인한 후 
                    photoList[k] = PhotoImage(file = "image/BTS.png") #다시 카드 뒷면으로 뒤집는다. 
                    pLabelList[k].image = photoList[k]
                    pLabelList[k].configure(image=photoList[k])
                    pLabelList[k].image=photoList[k]
                    pLabelList[k].update()

                    photoList[prevnum] = PhotoImage(file = "image/BTS.png") #이전에 선택한 카드도 동일하게 뒤집는다.
                    pLabelList[prevnum].image = photoList[prevnum]
                    pLabelList[prevnum].configure(image=photoList[prevnum])
                    pLabelList[prevnum].image=photoList[prevnum]
                    pLabelList[prevnum].update()
                    num = 2 #num도 2로 초기화하여 다시 두개를 선택할 수 있게끔 한다. 
                    
            prevnum = k #한 번 클릭 이벤트가 발생할 때, 클릭 함수가 끝나기 전 현재 클릭한 카드의 순서를 prevnum에 저장하여 다음 카드 클릭시 비교한다. 
            prevCard = cardList[k] #현재 클릭한 카드의 정보를 prevCard에 저장한다. 

            if complete == 0: #모든 쌍을 다 맞추면 complete가 0이되고 다음레벨로 이동
                level += 1
                self.ingame.destroy() #현재 레벨의 게임 창은 destroy를 통해 없앤다.
                NextLevel(window) #다음 레벨로 가기 위해 NextLevel 클래스 호출하여 dialog창 띄움.
           
        self.ingame=Toplevel() #외부 윈도우를 생성하여 싱글플레이를 할 수 있는 새 창을 띄움.
        self.ingame.geometry("600x1000")
        self.ingame.title("LEVEL"+str(level))
        self.ingame.resizable(width=FALSE, height=FALSE)

        self.score_label = Label(self.ingame, text="SCORE: " + str(score), font = ("",15)).grid(row=0, column = 0, columnspan=2) #왼쪽 상단에 점수 라벨 배치
        self.level_label = Label(self.ingame, text="LEVEL" + str(level), font=("", 20)).grid(row=0, column = 1, columnspan=4) #중앙 상단에 현재 Level 라벨 배치 
        
        make_card(self, level) #카드 생성 및 배열 함수 호출
        self.ingame.after(3000, hide_card, self) #3초 뒤 모든 카드 숨기는 함수 호출


class Multiplay():

    randList = []
    pLabelList = []
    column_card = 1
    row_card = 4
    num_card = 0
    choice_card=0
    list_set = 0
    i, j, k = 0, 0, 0
    turn = ""
    score1=0
    score2=0
    
    
    def in_game(self, level):
        
        def make_card(self, level): #카드를 생성하고 배열하는 방법은 Singleplay와 동일함. 레벨은 4로 지정해놓은 상태.
            global cardList
            global pLabelList
            global complete
            self.column_card = 1 + level
            self.row_card = 4
            self.num_card = (self.column_card * self.row_card)
            self.choice_card = int(self.num_card / 2)
            self.list_set = 0
            complete = self.choice_card #쌍 갯수 세어서 저장, 추후 clickcard에서 쓰일 예정

            self.randList = random.sample(range(0,15), self.choice_card) #지정한 범위 내에서 choice_card 수만큼 번호를 뽑아 리스트에 저장. choice_card 수는 레벨별로 달라져야함. 2레펠:4개, 3레벨:6개...
            self.randList += self.randList  #뽑은 리스트를 복제해서 이어붙임
            random.shuffle(self.randList) #리스트를 섞는다. 
            
            i, j, k = 0, 0, 0

            photoList = [None] * self.num_card
            pLabelList = [None] * self.num_card
            cardList = [None] * self.num_card
            
            for i in range(1, self.column_card+1): #row_card가 행, column_card가 열로 level 1 에서 2*4 카드로 그리드 형식으로 보여주려함.
                for j in range(1, self.row_card+1):
                    photoList[self.list_set] = PhotoImage(file = "image/" + fnameList[self.randList[self.list_set]])
                    pLabelList[self.list_set] = Label(self.ingame, image=photoList[self.list_set], borderwidth=0)
                    pLabelList[self.list_set].grid(row=i, column=j)
                    pLabelList[self.list_set].configure(image=photoList[self.list_set])
                    pLabelList[self.list_set].image = photoList[self.list_set]
                    cardList[k] = fnameList[self.randList[self.list_set]]
                    k += 1
                    self.list_set += 1

                    
        def hide_card(self):#전체 카드를 보여준 후 3초 뒤 뒤집음.
            global pLabelList
            global count
            global player1
            global player2
            global turn
            
            self.list_set=0
                
            player = [player1, player2]
            turn = random.choice(player) #플레이어의 시작 순서를 랜덤으로 정해준다.
            
            for i in range(1, self.column_card+1):
                for j in range(1, self.row_card+1):
                    photoList[self.list_set] = PhotoImage(file = "image/BTS.png")                    
                    pLabelList[self.list_set] = Button(self.ingame, image=photoList[self.list_set], borderwidth=0, command = lambda k=self.list_set: click_card(k))
                    pLabelList[self.list_set].grid(row=i, column=j, sticky = "nesw")
                    pLabelList[self.list_set].configure(image=photoList[self.list_set])
                    pLabelList[self.list_set].image = photoList[self.list_set]
                    self.list_set += 1

            self.turn_label['text'] = turn + "'s turn" #화면 상단에 누구의 턴인지 알려줌.
            self.turn_label.update()
            
        def click_card(k):
            global num, prevCard, prevnum, complete, level, player1, player2, score1, score2, turn

            if k == prevnum: #이전과 같은 버튼을 눌렀을 경우 횟수 차감되지 않게함.
                num = 1
            else :   
                photoList[k] = PhotoImage(file = "image/" + cardList[k])
                pLabelList[k].image = photoList[k]
                pLabelList[k].configure(image=photoList[k])
                pLabelList[k].image=photoList[k]
                pLabelList[k].update()
                num -= 1
                    
            if num == 0: #카드 두개를 선택했을 경우
                if prevCard == cardList[k]: #만약 이전 카드와 현재 카드가 같다면 이미지를 그대로 유지하고, num을 2로 초기화함.
                    pLabelList[k].config(state='disabled') #맞춘 카드를 다시 뒤집지 못하게 Button 상태를 disabled로 설정함.
                    pLabelList[prevnum].config(state='disabled')
                    num = 2
                    complete -= 1
                    if turn == player1: #player1의 turn일 경우 player1에게 점수 부여
                        score1 += 100
                        if cardList[k] == "ARMY.png": #스페셜카드 짝 맞출시 100점 추가 부여
                            score1 += 100
                        elif cardList[k] == "BTS01.png": #스페셜카드 짝 맞출시 100점 추가 부여
                            score1 += 100
                    elif turn == player2: #player2의 turn일 경우 player2에게 점수 부여
                        score2 += 100
                        if cardList[k] == "ARMY.png": #스페셜카드 짝 맞출시 100점 추가 부여
                            score2 += 100
                        elif cardList[k] == "BTS01.png": #스페셜카드 짝 맞출시 100점 추가 부여
                            score2 += 100
                    self.score_label1 = Label(self.ingame, text=player1 + "의 SCORE: " + str(score1), font=("",15)).grid(row=0, column = 0, columnspan=2)
                    self.score_label2 = Label(self.ingame, text=player2 + "의 SCORE: " + str(score2), font=("",15)).grid(row=0, column = 4, columnspan=2)
                    #반영된 점수를 상단 라벨로 보여줌
                else: #선택한 두 카드가 틀리다면                    
                    time.sleep(0.2) #카드를 0.2초간 보여준 후 다시 뒷면으로 뒤집음. 
                    photoList[k] = PhotoImage(file = "image/BTS.png")
                    pLabelList[k].image = photoList[k]
                    pLabelList[k].configure(image=photoList[k])
                    pLabelList[k].image=photoList[k]
                    pLabelList[k].update()
                    photoList[prevnum] = PhotoImage(file = "image/BTS.png")
                    pLabelList[prevnum].image = photoList[prevnum]
                    pLabelList[prevnum].configure(image=photoList[prevnum])
                    pLabelList[prevnum].image=photoList[prevnum]
                    pLabelList[prevnum].update()
                    num = 2
                    if turn == player1: #player1의 turn이었을 경우 player2에게 turn을 넘김. 
                        turn = player2
                        tkinter.messagebox.showinfo("Who's Turn?", player2 + "의 차례") #메시지박스를 띄워 turn이 바꼈음을 알려줌
                        self.turn_label['text'] = player2 + "'s turn"
                        self.turn_label.update() 
                    else:
                        turn = player1 #player2의 turn이었을 경우 player1에게 turn을 넘김. 
                        tkinter.messagebox.showinfo("Who's Turn?", player1 + "의 차례") #메시지박스를 띄워 turn이 바꼈음을 알려줌 
                        self.turn_label['text'] = player1 + "'s turn"
                        self.turn_label.update()    
            prevnum = k
            prevCard = cardList[k]
            if complete == 0: #모든 쌍을 다 맞춰서 0이되면 게임 종료
                self.ingame.destroy() #진행하던 게임 창을 destroy
                MultiEnd(window) 
           
        self.ingame=Toplevel() #외부 윈도우를 생성하여 멀티플레이를 할 수 있는 새 창을 띄움
        self.ingame.geometry("650x800")
        self.ingame.title("Multi Play")
        self.ingame.resizable(width=FALSE, height=FALSE)
        
        self.score_label1 = Label(self.ingame, text=player1 + "의 SCORE: " + str(score1), font=("",15)).grid(row=0, column = 0, columnspan=2)
        #왼쪽 상단에 player1의 닉네임과 점수 라벨 배치
        self.score_label2 = Label(self.ingame, text=player2 + "의 SCORE: " + str(score2), font=("",15)).grid(row=0, column = 4, columnspan=2)
        #오른쪽 상단에 player2의 닉네임과 점수 라벨 배치
        self.turn_label = Label(self.ingame, text="Who's Turn?", font=("", 20))
        self.turn_label.grid(row=0, column = 2, columnspan=2)
                
        make_card(self, level)
        self.ingame.after(3000, hide_card, self)



def clickSingle():
    CreateAccount(window)
    level=1
    quit
    
    

def clickMulti():
    global score1
    global score2
    CreateAccountMulti(window)
    score1 = 0
    score2 = 0
    quit



def clickRank():
    global listName
    global listLevel
    global listScore
    i=0
    sql = "SELECT * FROM userTable" #사용자의 게임 기록이 저장된 DB 조회
    cur.execute(sql)
    rank = cur.fetchall() #userTable의 모든 정보를 2차원 배열로 rank 배열에 저장. [('nickname', level, score), ... ] 이런식으로 저장됨
    rank.sort(key=lambda x:-x[2]) #세번째 요소인 score의 내림차순에 따라 재정렬. 
    for i in range (5): #점수 상위 5명의 정보를 각각 배열에 저장
        listName[i] = rank[i][0]
        listLevel[i] = rank[i][1]
        listScore[i] = rank[i][2]

    Ranking(window) 
    
    
window = Tk() 
window.geometry("1500x920") 
window.title("BTS 카드 짝맞추기 게임")
window.resizable(width=FALSE, height = FALSE)

playsound('boywithluv.mp3', 0) #노래 실행 *파일 경로에 한글 있으면 오류남

mainphoto = PhotoImage(file = "image/main.png")
pLabel = Label(window, image=mainphoto)
pLabel.configure(image = mainphoto)
pLabel.image = mainphoto

btnSingle = Button(window, text = "싱글플레이", font=("", 20), width=40, command = clickSingle)
btnMulti = Button(window, text = "멀티플레이", font=("", 20), width=40, command = clickMulti)
btnRank = Button(window, text = "랭킹", font=("", 20), width=40, command = clickRank)
btnQuit = Button(window, text="게임종료", font=("", 20), width=40, command=window.destroy)
space = Label(window, text="", width=40)

space.pack(side=BOTTOM)
btnQuit.pack(side = BOTTOM, padx=10, pady=15, ipady=30)
btnRank.pack(side = BOTTOM, padx=10, pady=15, ipady=30)
btnMulti.pack(side = BOTTOM, padx=10, pady=15, ipady=30)
btnSingle.pack(side = BOTTOM, padx=10, pady=15, ipady=30)
pLabel.pack(side = BOTTOM, pady=15, ipady=15)

window.mainloop()
