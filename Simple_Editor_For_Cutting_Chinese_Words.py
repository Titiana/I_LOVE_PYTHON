from tkinter import*
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import jieba

class SimpleEditor(Tk):
    def __init__(self,*args,**kwargs): # 位置定义的参数放前面，keyword定义的参数放后面
        super().__init__(*args,**kwargs)
        self.setup_ui()

    def setup_ui(self):
        self.title('Simple Editor For Cutting Chinese Words')
        frm1 = Frame()
        frm1.grid(row = 0)
        frm2 = Frame(width = 600 ,height = 30 )
        frm2.grid(row = 3,sticky = N+S+W)
        self.contents = ScrolledText()
        self.contents.grid(row = 1,column = 0 )
        self.contents_cut = ScrolledText()
        self.contents_cut.grid(row = 1,column = 1)
        
        self.file_name = StringVar()
        self.filename = ttk.Entry(frm1,textvariable = self.file_name,width = 45) # 输入控件绑定txt

        self.filename.grid(row = 0,column = 0,sticky = E+W)
        self.file_name.set('test.txt')

        ttk.Button(frm1,text = 'Load',command = self.load).grid(row = 0,column = 1)
        ttk.Button(frm1,text = 'Save',command = self.save).grid(row = 0,column = 3)
        ttk.Button(frm1,text = 'Cut Words',command = self.cut).grid(row = 0, column = 2)
        


    def load(self):
        with open(self.file_name.get(),'r',encoding = 'UTF-8') as file:
            self.contents.delete('1.0',END)
            self.contents.insert(INSERT,file.read())
            
        
            
    def save(self):
        with open(self.file_name.get(),'w',encoding = 'UTF-8') as file:
            file.write(self.contents_cut.get('1.0',END))
    
 
    def cut(self):
           
            text = self.contents.get('1.0',END)
            lines = text.split('\n')
            print(lines)
            for line in lines:
                seg_line = jieba.cut(line,cut_all=False)
                self.contents_cut.insert(INSERT,' '.join(seg_line)+'\n')
                
    # designed by Titiana        
            


SimpleEditor().mainloop()       
