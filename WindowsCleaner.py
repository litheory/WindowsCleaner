#coding:utf-8
#file WindowsCleaner.py

import Tkinter
import tkMessageBox
#"关于"菜单

#系统菜单
class Window:
	def __init__(self):
		self.root = Tkinter.Tk()

		#Create Menu
		menu = Tkinter.Menu(self.root)

		#Create the Cleaner submenu
		submenu = Tkinter.Menu(menu, tearoff=0)
		submenu.add_command(label="扫描垃圾文件", command = self.MenuScanRubbish)
		submenu.add_command(label="删除垃圾文件", command = self.MenuDelRubbish)
		menu.add_cascade(label="清理垃圾", menu=submenu)

		#Create the Search submenu
		submenu = Tkinter.Menu(menu, tearoff=0)
		submenu.add_command(label="搜索大文件", command = self.MenuScanBigFile)
		submenu.add_separator()
		submenu.add_command(label="按名称搜索文件", command = self.MenuSearchFile)
		menu.add_cascade(label="深度清理", menu=submenu)

		#Create the Help submenu
		submenu = Tkinter.Menu(menu, tearoff=0)
		submenu.add_command(label="源码" )
		submenu.add_command(label="用户手册")
		submenu.add_command(label="关于", command = self.MenuAbout)
		submenu.add_command(label="许可")
		submenu.add_separator()
		submenu.add_command(label="退出", command = self.MenuExit)
		menu.add_cascade(label="帮助", menu=submenu)

		self.root.config(menu=menu)

		#创建标签，用于显示状态信息
		self.progress = Tkinter.Label(self.root,
								anchor = Tkinter.W,
								text = '状态',
								bitmap = 'hourglass',
								compound = 'left')
		self.progress.place(x=10, y=370, width = 480, height = 15)

		#创建文本框，显示文件列表
		self.flist = Tkinter.Text(self.root)
		self.flist.place(x=10, y=10, width = 480, height = 350)

		#为文本框添加垂直滚动条
		self.vscroll = Tkinter.Scrollbar(self.flist)
		self.vscroll.pack(side = 'right', fill = 'y')
		self.flist['yscrollcommand'] = self.flist.yview

	def MainLoop(self):
		self.root.title("WindowsCleaner")
		self.root.minsize(500,400)
		self.root.maxsize(500,400)
		self.root.mainloop()

	#"关于"菜单
	def MenuAbout(self):
		tkMessageBox.showinfo("Windows Cleaner",
					"由python编写的Windows系统垃圾清理脚本,\n是用来练习Tkinter编写GUI的练手项目\n\n           Copyright © 2016 乃逸夫\n\t       Version 0.01")
	#”退出“菜单
	def MenuExit(self):
		self.root.quit();
	#"扫描垃圾文件"菜单
	def MenuScanRubbish(self):
		result = tkMessageBox.askquestion("Windows Cleaner","扫描垃圾文件将需要较长时间，是否继续？")
		if result == 'no':
			return
		tkMessageBox.showinfo("Windows Cleaner","马上开始扫描垃圾文件！")
	#"删除垃圾文件"菜单
	def MenuDelRubbish(self):
		result = tkMessageBox.askquestion("Windows Cleaner","删除垃圾文件将需要较长时间，是否继续？")
		if result == 'no':
			return
		tkMessageBox.showinfo("Windows Cleaner","马上开始删除垃圾文件！")
	#"搜索大文件菜单"
	def MenuScanBigFile(self):
		result = tkMessageBox.askquestion("Windows Cleaner","扫描大文件降序要较长时间，是否继续？")
		if result == 'no':
			return
		tkMessageBox.showinfo("Windows Cleaner","马上开始扫描大文件！")
	#"按名称搜索文件"菜单
	def MenuSearchFile(self):
		result = tkMessageBox.askquestion("Windows Cleaner","输入文件名称以搜素")
		if result == 'no':
			return
		tkMessageBox.showinfo("Windows Cleaner","马上开始搜索")


if __name__ == "__main__" :
	window = Window()
	window.MainLoop()
 
