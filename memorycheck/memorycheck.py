from tkinter import filedialog
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import END
from tkinter import messagebox
import numpy as np
import re
import win32api,win32con
import random


#构建单个存储器检查类
class drawfigure(object):
    #通过传入参数进行三种存储器分别处理
    def __init__(self, int):
        type = int
        if type == 0:
            self.memorytype = 0
        elif type == 1:
            self.memorytype = 1
        else:
            self.memorytype = 2

    def __main__(self):
        #单个存储器检查主窗口
        self.mainform = tk.Tk()
        if self.memorytype == 0:
            self.mainform.title('eeprom1')
        elif self.memorytype == 1:
            self.mainform.title('eeprom2')
        elif self.memorytype == 2:
            self.mainform.title('flash')
        else:
            return
        #获取屏幕最大分辨率
        self.screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        #定义空字典用于存放存储器的空间分配
        self.eeprom1 = {}
        self.eeprom2 = {}
        #定义坐标范围
        self.array1x = np.arange(0, pow(2, 23), 1, dtype=np.int)
        self.array1y = np.arange(0, pow(2, 23), 1, dtype=np.int)
        #初始化
        self.array1y[0:-1] = 0
        self.array1y[-1] = 0
        #初始化画布大小为屏幕最大尺寸的5/6
        self.fig = plt.figure(dpi = 100,figsize=(self.screen_x/120, self.screen_y/120))
        #只画一个图
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        # 标签
        self.text0 = plt.text(self.array1x[-1], self.array1y[-1],'(' + str(self.array1x[-1]) + ',' + str(self.array1y[-1]) + ')' , fontsize=10)
        #按键 选择文件
        self.btn_selfile = tk.Button(self.mainform, text='导入')
        self.btn_selfile.pack()
        #按键 开始处理
        self.btn_proc = tk.Button(self.mainform, text='处理')
        self.btn_proc.pack()
        #lable 存放文件路径
        self.lb_file = tk.Label(self.mainform)
        self.lb_file.pack()
        self.btn_selfile.config(command=lambda: self.selfile())
        self.btn_proc.config(command=lambda: self.procdata())


        #事件关联
        self.fig.canvas.mpl_connect('button_press_event',self.signqstart)
        self.fig.canvas.mpl_connect('button_release_event', self.signqend)
        self.fig.canvas.mpl_connect('motion_notify_event', self.motion)
        self.fig.canvas.mpl_connect('scroll_event', self.scroll)
        self.fig.canvas.mpl_connect('key_press_event',self.movemouse)

        #选择坐标范围
        self.txt_xstart = tk.Entry(self.mainform,width = 10 )
        self.txt_xstart.pack()
        self.txt_xend = tk.Entry(self.mainform,width = 10 )
        self.txt_xend.pack()
        self.txt_xend.bind('<Return>',self.changerange)
        self.txt_xstart.bind('<Return>', self.changerange)

        #存储空间分配输入框
        self.areatxt = tk.Text(self.mainform,width = 10,height = 20)
        self.areatxt.pack()

        self.mainform.mainloop()

    #定义函数用于改变坐标范围
    def changerange(self,event):
        x_min1 = int(self.txt_xstart.get())
        x_max1 = int(self.txt_xend.get())
        self.ax1.set_xlim(x_min1, x_max1)
        # ymaxid,ymaxval = self.array1y[x_min1 - fanwei_x:x_max1 + fanwei_x]
        # yminid, yminval = self.array1y[x_min1 - fanwei_x:x_max1 + fanwei_x]
        # event.inaxes.set(ylim = (yminval,ymaxval))
        self.fig.canvas.draw_idle()

    #定义选择文件函数
    def selfile(self):
        filename = filedialog.askopenfilename()
        self.lb_file.config(text=filename)

    #定义处理函数
    def procdata(self):
        self.eeprom1 = {}
        self.eeprom2 = {}
        try:
            areas = self.areatxt.get('1.0',END)
            index = 0
            key = ''
            val1 = 0
            val2 = 0
            slist = re.findall('[A-Za-z0-9]+',areas)
            if len(slist)%3 != 0:
                messagebox.showerror('错误','输入区间信息错误')
                return
            for line in slist:
                line = re.match('[A-Za-z0-9]{1,10}', line)
                line = line.group(0)
                if index == 0:
                    key = line
                    index = 1
                    continue
                elif index == 1:
                    val1 = int(line)
                    index = 2
                    continue
                elif index == 2:
                    val2 = int(line)
                    index = 0
                else:
                    messagebox.showerror('错误','输入区间信息错误')
                    return
                if self.memorytype == 0:
                    self.eeprom1.setdefault(key, []).append(val1)
                    self.eeprom1.setdefault(key, []).append(val2)
                elif self.memorytype == 1:
                    self.eeprom2.setdefault(key, []).append(val1)
                    self.eeprom2.setdefault(key, []).append(val2)
                else:
                    return
        except:
            messagebox.showerror('错误','输入区间信息错误')
            return
        self.array1y[0:-1] = 0
        self.array1y[-1] = 0
        filepath = self.lb_file.cget('text')
        index = filepath.rfind('.txt', 0, len(filepath))
        if index == -1:
            messagebox.showerror('错误', '文件格式错误')
            return
        file = open(filepath, 'r')
        filelines = file.readlines()  # 获取text文件的行数
        if self.memorytype == 0:
            self.ax1.set_title('eeprom1')
            id = 10
        elif self.memorytype == 1:
            self.ax1.set_title('eeprom2')
            id = 11
        elif self.memorytype == 2:
            self.ax1.set_title('flash')
            id = 12
        else:
            return

        maxXlim = 0
        index = 0
        fromvalue = 0
        linenum = 0
        while linenum < len(filelines):
            try:
                line = filelines[linenum]
                linenum = linenum + 1
                line = re.match('[0-9]{1,8}',line)
                value = int(line.group(0))
                if index == 0:
                    if value == id:
                        index = 1
                    else:
                        linenum = linenum + 2
                        index = 0
                    continue
                if index == 1:
                    index = 2
                    fromvalue = value
                    continue
                if index == 2:
                    index = 0
                    tovalue = fromvalue + value
                    if maxXlim < tovalue:
                        maxXlim = tovalue
                    for i in range(fromvalue, tovalue):
                        self.array1y[i] = self.array1y[i] + 1
                    continue
                else:
                    continue
            except:
                print(linenum)

        plt.ion()
        self.ax1.plot(self.array1x, self.array1y, color='blue')
        self.ax1.set_xlim(0, maxXlim+10)
        plt.show()

        maxy = max(self.array1y)
        for key in self.eeprom1.keys():
            self.ax1.set_xlim(self.eeprom1[key][0], self.eeprom1[key][1])
            self.fig.canvas.draw_idle()
            valuey = 0

            cnt = 0
            for i in range(self.eeprom1[key][0], self.eeprom1[key][1]):
                if valuey != self.array1y[int(i)]:
                    valuey = self.array1y[int(i)]
                    stri = '(' + str(int(i)) + ',' + str(valuey) + ')'
                    cnt = (cnt+1)%10
                    self.ax1.annotate(stri,xy=(i, valuey), xytext=(i, min(valuey+cnt,maxy)), xycoords='data')
            plt.savefig('./{}.jpg'.format(key))

    #滚轮缩放
    def scroll(self, event):
        x_min, x_max = event.inaxes.get_xlim()
        fanwei_x = (x_max - x_min)/10
        if event.button == 'up':
            event.inaxes.set(xlim=(x_min + fanwei_x, x_max - fanwei_x))
        elif event.button == 'down':
            event.inaxes.set(xlim=(x_min - fanwei_x, x_max + fanwei_x))
        # arrtmp = self.array1y[(10):(10000)]
        # ymaxid,ymaxval = np.max(arrtmp)
        # yminid, yminval = np.min(arrtmp)
        # event.inaxes.set(ylim = (yminval,ymaxval))
        self.fig.canvas.draw_idle()

    # 实时更新图片的显示内容
    def motion(self, event):
        try:
            temp = self.array1y[int(np.round(event.xdata))]
            self.text0.set_position((event.xdata, event.ydata))
            self.text0.set_text('(' + str(int(np.round(event.xdata))) + ',' + str(temp) + ')')
            self.fig.canvas.draw_idle()
        except:
            pass

    #标注开始
    def signqstart(self, event):
        if event.key == 'shift':
            self.x_start, self.start_y = self.text0.get_position()
            self.start_y = self.array1y[int(self.x_start)]
            self.signstr = '(' + str(int(self.x_start)) + ',' + str(self.start_y ) + ')'

    #标注结束
    def signqend(self, event):
        if event.key == 'shift':
            x, y = self.text0.get_position()
            self.ax1.annotate(self.signstr,
                              xy=(self.x_start, self.start_y), xytext=(x, y),   xycoords='data',
                         arrowprops=dict(width = 1,headwidth=3,facecolor='black', shrink=0.05)
                              )
    #左右键移动标注点位置
    def movemouse(self,event):
        x,y = self.text0.get_position()
        if event.key == 'right':
            x =x + 1
        elif event.key == 'left':
            x = x - 1
        temp = self.array1y[int(x)]
        self.text0.set_position((x, y))
        self.text0.set_text('(' + str(int(x)) + ',' + str(temp) + ')')

        self.fig.canvas.draw_idle()

class MainForm:
    def __init__(self):
        self.MainFormApp = tk.Tk()

        self.btn_ProcE21 = tk.Button(self.MainFormApp, text = 'ProcE21')
        self.btn_ProcE21.pack()
        self.btn_ProcE22 = tk.Button(self.MainFormApp, text = 'ProcE22')
        self.btn_ProcE22.pack()
        self.btn_ProcFlash = tk.Button(self.MainFormApp, text = 'ProcFlash')
        self.btn_ProcFlash.pack()

        self.ProcE21 = drawfigure(0)
        self.ProcE22 = drawfigure(1)
        self.ProcFlash = drawfigure(2)

    def __main__(self):
        self.btn_ProcE21.config(command = lambda: self.ProcE21.__main__())
        self.btn_ProcE22.config(command=lambda: self.ProcE22.__main__())
        self.btn_ProcFlash.config(command=lambda: self.ProcFlash.__main__())
        self.MainFormApp.mainloop()


mainapp = MainForm()
mainapp.__main__()
