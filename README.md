<div align="center">
<img src="assets\NamePicker.png" alt="icon" width="18%">
<h1>NamePickerXP</h1>
<h3>NamePicker的Windows XP特供版</h3>
</div>

[QQ群（群号2153027375）](https://qm.qq.com/q/fTjhKuAlCU)

> [!caution]
> 
> 此版本专为Windows XP打造，更新速度慢于源仓库，并且可能会缺失一些功能
> 
> 如果您的大脑运作正常，且运行环境使用的系统是Windows 7及以上，请前往[NamePicker](https://github.com/NamePickerOrg/NamePicker)

## 功能清单/大饼
> 由于Tkinter过于原始，迁移至PyQt的计划将会提前

> 概率内定过于缺德，并且实现难度相当高，不会考虑

1. [x] 基础的点名功能
2. [x] 人性化（大嘘）的配置修改界面
3. [x] 从外部读取名单
4. [x] 特殊点名规则
5. [x] 悬浮窗（点击展开主界面）
6. [ ] 软件内更新
7. [x] 支持非二元性别
8. [x] 同时抽选多个
9. [ ] 播报抽选结果
10. [x] 与ClassIsland/Class Widgets联动（联动插件均已上架对应软件的插件商城）（目前已知ClassIsland在进行多次抽选时100%崩溃（真不是我菜在开发环境都没这破事），Class Widgets不受影响）
11. [ ] 手机遥控抽选
12. [ ] 改用PyQt

## 运行指南

### 运行指南（成品程序）
1. Windows：将Release中下载的压缩包解压到某个空文件夹中，随后运行main.exe

### 运行指南（源码）

0. （可选）创建虚拟环境
1. 安装依赖项
`pip install -r requirements.txt`
2. 运行main.py

### 打包可执行文件指南（不使用打包脚本）

0. （可选）创建虚拟环境
1. 安装依赖项
`pip install -r requirements.txt`
2. 在虚拟环境中运行
`nuitka --standalone --onefile --enable-plugin=tk-inter --remove-output --windows-disable-console  main.py`

## FAQ
### Q:怎么配置名单

A:修改names.csv，第一行别改，第二行开始按照"学生名字,性别（0=男，1=女，2=非二元，不符合标准的性别代号理论上会被忽视）,学号"来填写，**务必使用英文符号**

就像这样：
```
name,sex,no
example,0,1
caixukun,2,2
sunxiaochuan,1,3
```
PS:不建议设置重复的学号和姓名，以免在使用时带来困扰

图形化的编辑界面见[NP-NameEditor](https://github.com/NamePickerOrg/NP-NameEditor)

当然，也没人拦着你用Excel或WPS Office编辑，但是请记住 _**务必使用UTF-8编码保存**_ ，否则会导致无法读取名单

### Q:杀毒软件认为这是病毒软件

A:将该软件添加至杀毒软件的白名单/信任区中，本软件保证不含病毒，您可以亲自审查代码，如果还是觉得不放心可以不使用

### Q:打开好慢

A:Python的运行效率不高，慢属于正常现象