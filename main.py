import os.path
import sys
import tkinter
from tkinter import ttk
from tkinter.messagebox import *
import random
import json
import configgui
import tempfile
import threading
import logging
import traceback

temp_dir = tempfile.gettempdir()
VERSION = "1.1.1dev"
VER_NO = 6
CODENAME = "Sonetto"
if os.path.exists("DEBUG"):
    logging.basicConfig(filename='log.log',level=logging.DEBUG,filemode='w')
elif os.path.exists("IDE"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(filename='log.log', level=logging.INFO, filemode='w')

logging.info("⌈晴朗和静谧统治着一切⌋")
class App(tkinter.Tk):
    def __init__(self):
        global allowRepeat,alwaysOnTop,showName,SupportCW,pref,pickNames,pns
        allowRepeat = False
        alwaysOnTop = True
        showName = True
        SupportCW = False
        pickNames = 1
        super().__init__()
        self.geometry("450x200")
        self.iconbitmap("favicon.ico")
        self.loadcfg()
        self.attributes('-topmost',alwaysOnTop)
        self.title("NamePicker - 随机抽选")
        self.resizable(False, False)
        pref = [tkinter.StringVar(), tkinter.StringVar()]
        pns = tkinter.IntVar()
        pns.set(1)
        self.loadname()
        self.createWidget()
        self.report_callback_exception = self.handle_exception
    names = []
    chosen = []
    length = 0
    sexlen = [0,0,0]
    sexl = [[],[],[]]
    numlen = [0,0]
    numl = [[],[]]

    def pick(self):
        global allowRepeat,showName
        self.loadcfg()
        if pref[0].get() != "男女都抽":
            if pref[0].get() == "只抽男":
                le = self.sexlen[0]
                tar = self.sexl[0]
            elif pref[0].get() == "只抽女":
                le = self.sexlen[1]
                tar = self.sexl[1]
            else:
                le = self.sexlen[2]
                tar = self.sexl[2]
        else:
            le = self.length
            tar = self.names[0]

        if pref[1].get() != "单双都抽":
            if pref[1].get() == "只抽双数":
                tar = list(set(tar)&set(self.numl[0]))
                le = len(tar)
            else:
                tar = list(set(tar) & set(self.numl[1]))
                le = len(tar)
        if le != 0:
            chs = random.randint(0, le - 1)
            if not allowRepeat:
                if len(self.chosen)>=le:
                    self.chosen=[]
                    chs = random.randint(0, le-1)
                else:
                    while chs in self.chosen:
                        chs = random.randint(0, le-1)
                self.chosen.append(chs)
                logging.debug(self.chosen)
            logging.info("抽选完成")
            return [tar[chs],self.names[2][self.names[0].index(tar[chs])]]
        else:
            showwarning("警告","没有符合筛选条件的学生")
            logging.warning("没有符合筛选条件的学生")
            return ["尚未抽选","尚未抽选"]

    def pickcb(self):
        global SupportCW,temp_dir,pickNames
        name.delete(*name.get_children())
        if pickNames == 1:
            res = self.pick()
            if SupportCW:
                with open("%s\\unread"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("111")
                with open("%s\\res.txt"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("%s（%s）"%(res[0],res[1]))
                logging.info("写入名单完成")
            else:
                name.insert("","end", values=res)
                logging.info("写入名单完成")
        else:
            res = []
            for i in range(pickNames):
                res.append(self.pick())
            if SupportCW:
                rese = []
                for i in res:
                    rese.append("%s（%s）" % (i[0], i[1]))
                with open("%s\\unread"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("111")
                with open("%s\\res.txt"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("，".join(rese))
                logging.info("写入名单完成")
            else:
                for i in res:
                    name.insert("", "end", values=i)
                logging.info("写入名单完成")


    def opencfg(self):
        cfg = configgui.cfgpage()
        cfg.mainloop()
        logging.info("打开配置菜单")

    def updatenames(self):
        global pickNames,pns
        pickNames = pns.get()
        logging.debug("updatenames被调用")

    def createWidget(self):
        global name
        scroll_v = ttk.Scrollbar(self)
        scroll_v.pack(side="right",fill="y")
        name = ttk.Treeview(self, height=10,columns=["姓名","学号"],show='headings',yscrollcommand=scroll_v.set)
        name.heading('姓名', text='姓名')
        name.heading('学号', text='学号')
        name.column("姓名",width=75)
        name.column("学号", width=75)
        name.place(relx=0,rely=0,anchor="nw")
        scroll_v.config(command=name.yview)
        button = ttk.Button(self, text="点击以抽选", command=self.pickcb)
        button.place(x=250, y=50, anchor="center")
        pn = tkinter.Spinbox(self,textvariable=pns,from_=1,to=len(self.names[2]),width=3,command=self.updatenames)
        pn.place(x=370, y=50, anchor="center")
        confb = ttk.Button(self, text="点击打开配置菜单", command=self.opencfg)
        confb.place(x=300, y=150, anchor="center")
        sexpref = ttk.OptionMenu(self,pref[0],"男女都抽","只抽男","只抽女","只抽非二元","男女都抽")
        sexpref.place(x=250,y=100,anchor="center")
        numpref = ttk.OptionMenu(self, pref[1], "单双都抽", "只抽单数", "只抽双数", "单双都抽")
        numpref.place(x=370, y=100, anchor="center")
        logging.info("组件设置完成")

    def loadname(self):
        try:
            name = {"name": {},"sex": {},"no": {}}
            with open("names.csv","r",encoding="utf-8") as f:
                l = f.readlines()
                ll = []
                for i in range(len(l)):
                    l[i] = l[i].strip("\n")
                    ll = l[i].split(",")
                    if i != 0:
                        name["name"][i] = ll[0]
                        name["sex"][i] = int(ll[1])
                        name["no"][i] = int(ll[2])
            print(name)
            self.names.append(list(name["name"].values()))
            self.names.append(list(name["sex"].values()))
            self.names.append(list(name["no"].values()))
            self.length =len(name["name"])
            self.sexlen[0] = self.names[1].count(0)
            self.sexlen[1] = self.names[1].count(1)
            self.sexlen[2] = self.names[1].count(2)
            for i in self.names[0]:
                if self.names[1][self.names[0].index(i)] == 0:
                    self.sexl[0].append(i)
                elif self.names[1][self.names[0].index(i)] == 1:
                    self.sexl[1].append(i)
                else:
                    self.sexl[2].append(i)

            for i in self.names[0]:
                if self.names[2][self.names[0].index(i)]%2==0:
                    self.numl[0].append(i)
                else:
                    self.numl[1].append(i)
            self.numlen[0] = len(self.numl[0])
            self.numlen[1] = len(self.numl[1])
            logging.info("名单导入完成")
        except FileNotFoundError:
            with open("names.csv","w",encoding="utf-8") as f:
                st  = ["name,sex,no\n","example,0,1"]
                f.writelines(st)
            r = showwarning("警告","检测到names.csv不存在，已为您创建样板文件，请修改")
            logging.warning("names.csv不存在")
            sys.exit(114514)

    def loadcfg(self):
        try:
            global allowRepeat,alwaysOnTop,showName,SupportCW,pickNames
            with open("config.json","r",encoding="utf-8") as f:
                conf = f.read()
            config = json.loads(conf)
            allowRepeat = config["allowRepeat"]
            alwaysOnTop = config["alwaysOnTop"]
            SupportCW = config["SupportCW"]
            if config["VER_NO"] < VER_NO:
                r = showwarning("警告","当前配置文件版本较低，可能会出现一些玄学问题")
                logging.warning("当前配置文件版本较低")
            elif config["VER_NO"] > VER_NO:
                r = showwarning("警告","当前配置文件版本较高，可能会出现一些玄学问题")
                logging.warning("当前配置文件版本较高")
            self.attributes('-topmost',alwaysOnTop)
        except FileNotFoundError:
            cfg = {"VERSION": VERSION,
                   "VER_NO": VER_NO,
                   "CODENAME": CODENAME,
                   "allowRepeat": False,
                   "alwaysOnTop": True,
                   "SupportCW":False}
            conf = json.dumps(cfg)
            with open("config.json", "w", encoding="utf-8") as f:
                f.write(conf)
            logging.warning("没有找到config.json")

    def handle_exception(sel,exception, value, trace):
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    app = App()
    app.mainloop()