import ctypes
from tkinter import *
from tkinter.ttk import *
from typing import Dict
import datetime
from time import strftime
import time
import cl
import matplotlib.pyplot as plt
import datetime
from PIL import Image
import os
import json

# 读取 JSON 文件并解析为 Python 对象
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将 lunch_break_personnel 列表转换为元组
lunch_break_personnel_tuple = tuple(data['lunch_break_personnel'])

def ph():
  path = 'image'  # 图片所在文件夹
  files = os.listdir(path)
  images = []
  for file in files:
      if file.endswith('.jpg'):
          images.append(Image.open(os.path.join(path, file)))

  widths, _ = zip(*(i.size for i in images))
  fix_width = sum(widths) // len(images)
  new_height = int(sum(i.size[1] * fix_width // i.size[0] for i in images))
  new_image = Image.new('RGB', (fix_width, new_height), color=(255, 255, 255))

  y_offset = 0
  for image in images:
      width, height = image.size
      new_width = fix_width
      new_height = int(height * fix_width / width)
      image = image.resize((new_width, new_height))
      new_image.paste(image, (0, y_offset))
      y_offset += new_height

  new_image.save('数据分析.jpg')
  os.startfile( '数据分析.jpg')


# 绘制折线图
def tp(data):
  name=data[0]
  da = data[1:]
  # 设置横坐标
  plt.rcParams['font.sans-serif'] = ['SimHei']
  x = range(len(data))
  # 设置图片大小和分辨率
  plt.figure(figsize=(8, 6), dpi=100)
  # 绘制折线图
  plt.plot(x, data)
  # 添加标题和标签
  plt.title(name)
  plt.xlabel("相对时间(D)")
  plt.ylabel("积分(F)")
  # 保存图片
  plt.savefig('image/'+name+'.jpg')


def tme():#获取当前时间
    now=datetime.datetime.now()
    tme=now.strftime("%Y-%m-%d %H:%M:%S")
    return tme

def zg():#获取分值前三名
    with open('file.txt', 'r', encoding="utf-8") as f:
        scores = {}
        for line in f:
            parts = line.strip().split()
            name = parts[1]
            score = int(parts[0])
            if name in scores:
                scores[name] += score
            else:
                scores[name] = score
        # 排序字典，获取前3名
        sorted_scores = sorted(scores.items(), key=lambda x:x[1], reverse=True)
        top_three = sorted_scores[:3]
        # 输出前3名姓名和分数
        a=''
        b=0
        for name, score in top_three:
            b=b+1
            a=a+'     '+str(b)+'.'+(f"{name}: {score}")
        return a

def dy(a):#获取低于a的人
    with open('file.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    scores_dict = {}      # 用字典来存储每个人的总分数

    for line in lines:
        parts = line.split()
        name = parts[1]
        score = int(parts[0])
        if name in scores_dict:
            scores_dict[name] += score
        else:
            scores_dict[name] = score
    sc=''
    # 遍历字典，选取积分总数小于a的人名，并打印出来
    for name, score in scores_dict.items():
        if score < a:
            sc=sc+' '+(f'{name}: {score}')
    return sc




def wie(a):#写入文件
    with open('file.txt', 'a+', encoding='utf-8') as f:
        # 将文件指针移到文件末尾
        f.seek(0, 2)
        # 写入传入的字符串，并在后面加上换行符
        f.write(a + '\n')
        # 将文件内容保存
        f.flush()



class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_paihangbang"] = self.__tk_label_paihangbang(self)
        self.widget_dic["tk_label_jingshibang"] = self.__tk_label_jingshibang(self)
        self.widget_dic["tk_label_huanying"] = self.__tk_label_huanying(self)
        self.widget_dic["tk_label_date"] = self.__tk_label_date(self)
        self.widget_dic["tk_tabs_xxk"] = self.__tk_tabs_xxk(self)

    def __win(self):
        self.title("午休积分")
        # 设置窗口大小、居中
        width = 700
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        self.configure(bg='#FFFFFF')
        #告诉操作系统使用程序自身的dpi适配
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        #获取屏幕的缩放因子
        ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
        #设置程序缩放
        self.tk.call('tk', 'scaling', ScaleFactor/100)
        self.iconbitmap('icon.ico')

        # 自动隐藏滚动条
    def scrollbar_autohide(self,bar,widget):
        self.__scrollbar_hide(bar,widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
    
    def __scrollbar_show(self,bar,widget):
        bar.lift(widget)

    def __scrollbar_hide(self,bar,widget):
        bar.lower(widget)
        
    def __tk_label_paihangbang(self,parent):
        label = Label(parent,text="积分排行榜："+zg(),anchor="center",font=("Arial", 13))
        label.place(x=0, y=400, width=700, height=35)
        return label

    def __tk_label_jingshibang(self,parent):
        aaaa=int(data['jingshi'])
        label = Label(parent,text="警示榜："+dy(aaaa),anchor="center",font=("Arial", 13))
        label.place(x=0, y=435, width=700, height=35)
        return label

    def __tk_label_huanying(self,parent):
        label = Label(parent,text="欢迎使用积分程序",anchor="center",font=("Arial", 14))
        label.place(x=0, y=470, width=550, height=30)
        return label

    def __tk_label_date(self,parent):
        a=tme()
        label = Label(parent,text=a[:16],anchor="center",font=("Arial", 10))
        label.place(x=550, y=470, width=150, height=30)
        return label

    def __tk_tabs_xxk(self,parent):
        frame = Notebook(parent)

        self.widget_dic["tk_tabs_xxk_0"] = self.__tk_frame_xxk_0(frame)
        frame.add(self.widget_dic["tk_tabs_xxk_0"], text="午休积分-记录")

        self.widget_dic["tk_tabs_xxk_1"] = self.__tk_frame_xxk_1(frame)
        frame.add(self.widget_dic["tk_tabs_xxk_1"], text="午休积分-统计")

        frame.place(x=0, y=0, width=700, height=400)
        return frame

    def __tk_frame_xxk_0(self,parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=700, height=400)

        self.widget_dic["tk_label_bt1"] = self.__tk_label_bt1(frame)
        self.widget_dic["tk_label_llx1"] = self.__tk_label_llx1(frame)
        self.widget_dic["tk_select_box_lx1"] = self.__tk_select_box_lx1(frame)
        self.widget_dic["tk_select_box_ry"] = self.__tk_select_box_ry(frame)
        self.widget_dic["tk_label_lry"] = self.__tk_label_lry(frame)
        self.widget_dic["tk_label_lfz"] = self.__tk_label_lfz(frame)
        self.widget_dic["tk_input_fz"] = self.__tk_input_fz(frame)
        self.widget_dic["tk_label_lyy"] = self.__tk_label_lyy(frame)
        self.widget_dic["tk_input_yy"] = self.__tk_input_yy(frame)
        self.widget_dic["tk_button_bjf"] = self.__tk_button_bjf(frame)
        return frame

    def __tk_label_bt1(self,parent):
        label = Label(parent,text="午休积分-记录",anchor="center",font=("Arial", 27))
        label.place(x=0, y=0, width=700, height=60)
        return label

    def __tk_label_llx1(self,parent):
        label = Label(parent,text="积分类型",anchor="center",font=("Arial", 14))
        label.place(x=40, y=110, width=100, height=30)
        return label

    def __tk_select_box_lx1(self,parent):
        cbq = Combobox(parent, state="readonly")
        cbq['values'] = ("加分","减分")
        cbq.place(x=180, y=110, width=122, height=30)
        return cbq

    def __tk_select_box_ry(self,parent):
        cb = Combobox(parent, state="readonly")
        cb['values'] = lunch_break_personnel_tuple
        cb.place(x=540, y=110, width=120, height=30)
        return cb

    def __tk_label_lry(self,parent):
        label = Label(parent,text="积分人员",anchor="center",font=("Arial", 14))
        label.place(x=400, y=110, width=100, height=30)
        return label

    def __tk_label_lfz(self,parent):
        label = Label(parent,text="积分分值",anchor="center",font=("Arial", 14))
        label.place(x=40, y=200, width=100, height=30)
        return label

    def __tk_input_fz(self,parent):
        ipt = Entry(parent)
        ipt.place(x=180, y=200, width=120, height=30)
        return ipt

    def __tk_label_lyy(self,parent):
        label = Label(parent,text="积分原因",anchor="center",font=("Arial", 14))
        label.place(x=400, y=200, width=100, height=30)
        return label

    def __tk_input_yy(self,parent):
        ipt = Entry(parent)
        ipt.place(x=540, y=200, width=120, height=30)
        return ipt

    def __tk_button_bjf(self,parent):
        btn = Button(parent, text="确认积分")
        btn.place(x=275, y=290, width=150, height=48)
        return btn

    def __tk_frame_xxk_1(self,parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=700, height=400)

        self.widget_dic["tk_label_bt2"] = self.__tk_label_bt2(frame)
        self.widget_dic["tk_label_ltj"] = self.__tk_label_ltj(frame)
        self.widget_dic["tk_label_lqc"] = self.__tk_label_lqc(frame)
        self.widget_dic["tk_progressbar_jindu"] = self.__tk_progressbar_jindu(frame)
        self.widget_dic["tk_label_ljindu"] = self.__tk_label_ljindu(frame)
        self.widget_dic["tk_button_tj"] = self.__tk_button_tj(frame)
        self.widget_dic["tk_button_qc"] = self.__tk_button_qc(frame)
        self.widget_dic["tk_label_lmz"] = self.__tk_label_lmz(frame)
        self.widget_dic["tk_input_mz"] = self.__tk_input_mz(frame)
        
        return frame

    def __tk_label_bt2(self,parent):
        label = Label(parent,text="午休积分-统计",anchor="center",font=("Arial", 27))
        label.place(x=0, y=0, width=700, height=60)
        return label

    def __tk_label_ltj(self,parent):
        label = Label(parent,text="积分统计：对所有积分进行统计",anchor="center",font=("Arial", 14))
        label.place(x=10, y=130, width=400, height=30)
        return label

    def __tk_label_lqc(self,parent):
        label = Label(parent,text="积分清除：备份后清除现有积分",anchor="center",font=("Arial", 14))
        label.place(x=10, y=190, width=400, height=30)
        return label

    def __tk_progressbar_jindu(self,parent):
        progressbar = Progressbar(parent, orient=HORIZONTAL)
        progressbar.place(x=40, y=260, width=615, height=30)
        return progressbar

    def __tk_label_ljindu(self,parent):
        label = Label(parent,text="暂时没有任务",anchor="center",font=("Arial", 13))
        label.place(x=80, y=310, width=500, height=30)
        return label

    def __tk_button_tj(self,parent):
        btn = Button(parent, text="积分统计")
        btn.place(x=420, y=130, width=121, height=30)
        return btn

    def __tk_button_qc(self,parent):
        btn = Button(parent, text="积分清除")
        btn.place(x=420, y=190, width=121, height=30)
        return btn

    def __tk_label_lmz(self,parent):
        label = Label(parent,text="为保障数据安全，请输入密钥:",anchor="center",font=("Arial", 14))
        label.place(x=10, y=80, width=400, height=30)
        return label

    def __tk_input_mz(self,parent):
        ipt = Entry(parent)
        ipt.place(x=420, y=80, width=119, height=30)
        return ipt

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def jf(self,evt):
        lx=self.widget_dic["tk_select_box_lx1"].get()
        if lx=='减分':
            lx='-'
        elif lx=='加分':
            lx='+'
        ry=self.widget_dic["tk_select_box_ry"].get()
        fz=self.widget_dic["tk_input_fz"].get()
        yy=self.widget_dic["tk_input_yy"].get()
        time1=tme()
        if yy=='':
            yy='原因没写'
        gggg=str(lx+fz+' '+ry+" "+yy)
        if lx=='' or fz=='' or ry=='':
            self.widget_dic["tk_label_huanying"].configure(text="积分失败，原因是缺少必填项")
            # 在1000毫秒（即1秒）后，调用lambda表达式更新文本
            self.widget_dic["tk_label_huanying"].after(1500, lambda: self.widget_dic["tk_label_huanying"].configure(text="你好，欢迎使用积分程序"))
        else:
            try:
                 int(fz)
                 ggg=str(gggg+" "+time1)
                 wie(ggg)
                 self.widget_dic["tk_select_box_ry"].set('')
                 self.widget_dic["tk_input_fz"].delete(0, 'end')
                 self.widget_dic["tk_input_yy"].delete(0, 'end')
                 self.widget_dic["tk_select_box_lx1"].set('')
                 self.widget_dic["tk_label_huanying"].configure(text="积分成功！")
                 # 在1000毫秒（即1秒）后，调用lambda表达式更新文本
                 self.widget_dic["tk_label_huanying"].after(1500, lambda: self.widget_dic["tk_label_huanying"].configure(text="你好，欢迎使用积分程序"))    

            except ValueError:
                self.widget_dic["tk_label_huanying"].configure(text="积分失败，原因是积分分值不是整数")
                # 在1000毫秒（即1秒）后，调用lambda表达式更新文本
                self.widget_dic["tk_label_huanying"].after(1500, lambda: self.widget_dic["tk_label_huanying"].configure(text="你好，欢迎使用积分程序"))

    def tj(self,evt):
      mz_input = self.widget_dic["tk_input_mz"]  # 获取名为 'tk_input_mz' 的输入框控件实例
      mz_input_value = mz_input.get()  # 通过 .get() 方法获取文本框内的值
      jindu_bar = self.widget_dic["tk_progressbar_jindu"]  # 获取进度条控件实例
      if mz_input_value ==str(data['statistics_key']):
            print('ok')
            jindu_bar = self.widget_dic["tk_progressbar_jindu"]  # 获取进度条控件实例
            jindu_bar.step(100)
            a1=cl.cl()
            for i in a1:
                tp(i) 
            ph()
            jindu_bar.step(99)
            self.widget_dic["tk_label_huanying"].configure(text="生成成功！")
            # 在1000毫秒（即1秒）后，调用lambda表达式更新文本
            self.widget_dic["tk_label_huanying"].after(1500, lambda: self.widget_dic["tk_label_huanying"].configure(text="你好，欢迎使用积分程序"))
            
      else:
            self.widget_dic["tk_label_huanying"].configure(text="密钥错误，请重新输入")
           # 在1000毫秒（即1秒）后，调用lambda表达式更新文本
            self.widget_dic["tk_label_huanying"].after(1500, lambda: self.widget_dic["tk_label_huanying"].configure(text="你好，欢迎使用积分程序"))

            
        
    def qc(self,evt):
        self.widget_dic["tk_label_huanying"].configure(text="暂不支持，请手动清除")
        # 在1000毫秒（即1秒）后，调用lambda表达式更新文本
        self.widget_dic["tk_label_huanying"].after(1500, lambda: self.widget_dic["tk_label_huanying"].configure(text="你好，欢迎使用积分程序"))

        
    def __event_bind(self):
        self.widget_dic["tk_button_bjf"].bind('<Button>',self.jf)
        self.widget_dic["tk_button_tj"].bind('<Button>',self.tj)
        self.widget_dic["tk_button_qc"].bind('<Button>',self.qc)
        
if __name__ == "__main__":
    win = Win()
    win.mainloop()
