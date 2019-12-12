from tkinter import *
from tkinter import ttk
from enum import Enum

# enum 实现的是python的枚举类型
class State(Enum):
    calculated = 0 # 计算之后的状态
    in_number1 = 1 # 输入第一个操作数的第一个数字之后的状态
    post_operator = 2 #输入运算符之后的状态
    in_number2 = 3 #输入第二哥操作数的第一个数字之后的状态

class Calculator(Tk):
    def __init__(self,*args,**kwargs):


        super().__init__(*args,**kwargs)
        self.title('Simple Calculator')
        self.geometry('400x600')
        self.result_string = StringVar()
        self.process_string = StringVar()
        self.result_string.set('0')
        self.process_string.set('')
        self.number1 = '0'
        self.number2 = None
        self.record = '' #用于记录运算过程
        self.operator = None
        self.state = State.calculated

        
        process = ttk.Label(self,textvariable = self.process_string,font = ('Arial',10),anchor = E)
        process.pack(side = TOP,expand = True,fill = BOTH)

        # Output
        output = ttk.Label(self,textvariable = self.result_string,font = ('Arial',20,'bold'),anchor = E)
        output.pack(side = TOP,expand = True,fill = BOTH)

        # Row 1
        row = Frame(self)
        row.pack(side = TOP,expand = True,fill = BOTH)
        self.add_button(row, 'CE', self.on_ce_click)
        self.add_button(row, 'C', self.on_c_click)
        self.add_button(row, 'Back', self.on_back_click)
        self.add_button(row, '/', self.on_division_click)

        # Row 2
        row = Frame(self)
        row.pack(side=TOP, expand=True, fill=BOTH)
        self.add_button(row, '7', self.gen_on_number_click('7'))
        self.add_button(row, '8', self.gen_on_number_click('8'))
        self.add_button(row, '9', self.gen_on_number_click('9'))
        self.add_button(row, 'x', self.on_multiply_click)
        
        # row 3 
        row = Frame(self)
        row.pack(side=TOP, expand=True, fill=BOTH)
        self.add_button(row, '4', self.gen_on_number_click('4'))
        self.add_button(row, '5', self.gen_on_number_click('5'))
        self.add_button(row, '6', self.gen_on_number_click('6'))
        self.add_button(row, '-', self.on_minus_click)

        # row 4 
        row = Frame(self)
        row.pack(side=TOP, expand=True, fill=BOTH)
        self.add_button(row, '1', self.gen_on_number_click('1'))
        self.add_button(row, '2', self.gen_on_number_click('2'))
        self.add_button(row, '3', self.gen_on_number_click('3'))
        self.add_button(row, '+', self.on_add_click)

        # row 5 
        row = Frame(self)
        row.pack(side=TOP, expand=True, fill=BOTH)
        self.add_button(row, '+/-', self.on_negative_click)
        self.add_button(row, '0', self.gen_on_number_click('0'))
        self.add_button(row, '.', self.gen_on_number_click('.'))
        self.add_button(row, '=', self.on_equal_click)
        
        # 添加按钮

    def add_button(self, parent, text=None, command=None):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(side=LEFT, expand=True, fill=BOTH)        
    
    # 注意按了CE只是清除当前的状态
    def on_ce_click(self):

        if self.state == State.calculated:
            self.number1 = 0
            self.result_string.set(self.number1)
            self.record =''
            self.process_string.set(self.record)

        elif self.state == State.in_number1:
            self.number1 = 0
            self.result_string.set(self.number1)
            self.record =''
            self.process_string.set(self.record)
            self.state = State.calculated
        elif self.state == State.in_number2:
            self.number2 = 0
            self.record = self.record + '0'
            self.result_string.set(self.number2)
            self.state = State.post_operator
        elif self.state == State.post_operator:
            self.number2 = 0
            self.record = self.record + '0'
            self.result_string.set(self.number2)




    def on_c_click(self):
        self.state = State.calculated
        self.number1 = 0
        self.number2 = 0
        self.record = ''
        self.process_string.set(self.record)
        self.result_string.set(self.number1)
        
    def on_back_click(self):
        
        if self.state == State.in_number1:
            if len(self.number1) == 1:
                self.number1 = 0
                self.record = '0'
            else:
                temp = list(self.number1)
                self.number1 = ''.join(temp[:-1])
                self.record = self.record[:-1]
            self.result_string.set(self.number1)
            
        elif self.state == State.in_number2:
            if len(self.number2) == 1:
                self.number2 = 0
                self.record = self.record[:-1] + '0'
            else:
                temp = list(self.number2)
                self.number2 = ''.join(temp[:-1])
                self.record = self.record[:-1]
            self.result_string.set(self.number2)
        
        elif self.state == State.calculated:
            self.process_string.set('')


        
            
        
    def on_negative_click(self):
        

        if self.state == State.in_number1 or self.state == State.calculated:
            if float(self.number1) > 0:
                self.number1 = '-' + self.number1
                self.record = '-' + self.record
               
            elif float(self.number1) < 0:
                self.number1 = str(float(self.number1)*-1)
                temp = self.record[1:]
                self.record = temp
            
            self.result_string.set(self.number1)
            self.process_string.set(self.record)
        if self.state == State.in_number2:
            if float(self.number2) > 0:
                temp = list()
                for i in range(len(self.record)-len(self.number2)):
                    temp.append(self.record[i])
                temp.extend('-'+self.number2)
                self.record = ''.join(temp)
                self.number2 = '-' + self.number2
                
            elif float(self.number2) < 0:
                temp = list()
                for i in range(len(self.record)-len(self.number2)):
                    temp.append(self.record[i])
                temp.extend('-'+self.number2)
                self.record = ''.join(temp)
                self.number2 = str(float(self.number2)*-1)
              
            self.result_string.set(self.number2)
            self.process_string.set(self.record)
        
    def on_operator(self, operator):

            if self.state == State.calculated:
                self.state = State.post_operator
            elif self.state == State.in_number1:
                self.state = State.post_operator
            elif self.state == State.in_number2:
                self.on_equal_click()
                self.state = State.post_operator
            elif self.state == State.post_operator:
                temp = self.record[:-1]
                self.record = temp
            else: assert(0)        
            
            self.operator = operator
            if self.record == '':
                self.record = '0' + operator
            elif self.record[-1] == '=':
                temp = list(self.record[:-1])
                self.record = ''.join(temp) + operator
            else:
                self.record = self.record + operator
            
            self.process_string.set(self.record)
        
    def on_number(self, ch):
            
            if self.state == State.calculated:
                self.number1 = ch
                self.state = State.in_number1
                self.result_string.set(self.number1)
                self.process_string.set('')
                self.record = ch
            elif self.state == State.in_number1:    
                self.number1 = self.number1 + ch
                self.result_string.set(self.number1)
                self.record = self.record + ch
            elif self.state == State.post_operator:
                self.number2 = ch
                self.state = State.in_number2
                self.result_string.set(self.number2)
                self.record = self.record + ch
            elif self.state == State.in_number2:
                self.number2 = self.number2 + ch
                self.result_string.set(self.number2)
                self.record = self.record + ch
            else: assert(0)
           
            print(self.state)
        # 按了 = 
    def on_equal_click(self):
            
            if self.state == State.post_operator:
                if self.record[-1] == '+':
                    temp = self.record[:-1]
                    self.record = self.record + temp +'='
                    self.process_string.set(self.record)
                    self.number1 = str(float(self.number1)+float(self.number1)) 
                    self.result_string.set(self.number1)
                    self.record = self.number1
                elif self.record[-1] == '-':
                    temp = self.record[:-1]
                    self.record = self.record + temp + '='
                    self.process_string.set(self.record)
                    self.number1 = str(float(self.number1)-float(self.number1)) 
                    self.result_string.set(self.number1)
                    self.record = self.number1
            
                elif self.record[-1] == 'x':
                    temp = self.record[:-1]
                    self.record = self.record + temp + '='
                    self.process_string.set(self.record)
                    self.number1 = str(float(self.number1)*float(self.number1)) 
                    self.result_string.set(self.number1)
                    self.record = self.number1
                
                elif self.record[-1] == '/':
                    try:
                        self.number1 = str(float(self.number1)/float(self.number1)) 
                    except ZeroDivisionError:
                        self.process_string.set(self.record)
                        self.result_string.set('Result Undefined')
                        self.record =''
                    else:
                        temp = self.record[:-1]
                        self.record = self.record + temp + '='
                        self.process_string.set(self.record)
                        self.result_string.set(self.number1)
                        self.record = self.number1
                else:
                    self.state =    State.in_number2
            if self.state == State.in_number2:

                self.record = self.record + '='
                if self.operator == '+':
                    self.number1 = str(float(self.number1) + float(self.number2))
                    self.process_string.set(self.record)
                    self.result_string.set(self.number1)
                    self.record = self.number1
                    #self.state = State.calculated
                elif self.operator == '-':
                    self.number1 = str(float(self.number1) - float(self.number2))
                    self.process_string.set(self.record)
                    self.result_string.set(self.number1)
                    self.record = self.number1
                    #self.state = State.calculated
                elif self.operator == 'x':
                    self.number1 = str(float(self.number1) * float(self.number2))
                    self.process_string.set(self.record)
                    self.result_string.set(self.number1)
                    self.record = self.number1
                    #self.state = State.calculated
                elif self.operator == '/':
                    try:
                        self.number1 = str(float(self.number1) / float(self.number2))
                    except ZeroDivisionError:
                        self.record = self.record[:-2]
                        self.process_string.set(self.record)
                        self.result_string.set('The Divisor Cannot Be Zero')
                        self.record =''
                        #self.state = State.calculated
                    else:
                        self.process_string.set(self.record)
                        self.result_string.set(self.number1)
                        self.record = self.number1
                        #self.state = State.calculated

            self.state = State.calculated

        # 各种运算
    def on_add_click(self):
        self.on_operator('+')


    def on_minus_click(self):
        self.on_operator('-')
        print('minus clicked.')
    
    def on_multiply_click(self):
        self.on_operator('x')
        print('multiply clicked.')
        
    def on_division_click(self):
        self.on_operator('/')
        print('division clicked.')
        


        
        # 按键 0-9
        
    def gen_on_number_click(self,ch):
        return lambda: self.on_number(ch)

        
if __name__ == '__main__':
    app = Calculator()
    app.mainloop()