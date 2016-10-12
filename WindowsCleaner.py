#coding:utf-8
#
#file WindowsCleaner.py

import Tkinter
import tkMessageBox,tkSimpleDialog
import os,os.path
import threading

rubbishExt = ['.tmp','.bak','.old','.wbk','.xlk','._mp','.gid','.chk','.syd','.$$$','.@@@','.~*']		#未添加.log文件,对于不需要调试系统的用户可以添加


#遍历某文件夹
#def traverse(pathname):
#	for item in os.listdir(pathname):
#		fullitem = os.path.join(pathname, item)
#		print(fullitem)
#		if os.path.isdir(fullitem):
#			traverse(fullitem)
#
#traverse("D:/Python27")
#
#遍历某文件夹2
#def trav_walk(pathname):
#	for root,dirs,files, in os.walk(pathname):
#		for file in files:
#			filename = os.path.abspath(os.path.join(root, file))
#			print(filename)
#
#trav_walk("D:/Python27")

#获取当前计算机盘符
def GetDrives():
	drives = []
	for i in range(65,91):
		vol = chr(i) + ':/'
		if os.path.isdir(vol):
			drives.append(vol)
	return tuple(drives)

#系统菜单
class Window:
	def __init__(self):
		self.root = Tkinter.Tk()

		#Create Menu
		menu = Tkinter.Menu(self.root)

		#Create the Cleaner submenu
		submenu = Tkinter.Menu(menu, tearoff=0)
		submenu.add_command(label="扫描垃圾", command = self.MenuScanRubbish)
		submenu.add_command(label="删除垃圾", command = self.MenuDelRubbish)
		submenu.add_separator()
		submenu.add_command(label="搜索大文件", command = self.MenuScanBigFile)
		submenu.add_command(label="按名称搜索文件", command = self.MenuSearchFile)
		menu.add_cascade(label="开始", menu=submenu)

		#Create the Search submenu
		submenu = Tkinter.Menu(menu, tearoff=0)
		submenu.add_command(label="添加垃圾类型")
		submenu.add_separator()
		submenu.add_command(label="选择扫描盘符")
		menu.add_cascade(label="自定义", menu=submenu)

		#Create the Help submenu
		submenu = Tkinter.Menu(menu, tearoff=0)
		submenu.add_command(label="关于", command = self.MenuAbout)
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
		self.filelist = Tkinter.Text(self.root)
		self.filelist.place(x=10, y=10, width = 480, height = 350)

		#为文本框添加垂直滚动条
		self.vscroll = Tkinter.Scrollbar(self.filelist)
		self.vscroll.pack(side = 'right', fill = 'y')
		self.filelist['yscrollcommand'] = self.vscroll.set
		self.vscroll['command'] = self.filelist.yview

	def MainLoop(self):
		self.root.title("WindowsCleaner")
		self.root.minsize(500,400)
		self.root.maxsize(500,400)
		self.root.mainloop()

	#"关于"菜单
	def MenuAbout(self):
		tkMessageBox.showinfo("Windows Cleaner",
					"\t\tThe MIT License (MIT)\
\n\
\t            Copyright © 2016 乃逸夫\
\n\
\n\
\nPermission is hereby granted, free of charge, to any person obtaining a copy\
of this software and associated documentation files (the \"Software\"), to deal\
in the Software without restriction, including without limitation the rights\
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\
copies of the Software, and to permit persons to whom the Software is\
furnished to do so, subject to the following conditions:\
\n\
\nThe above copyright notice and this permission notice shall be included in all\
copies or substantial portions of the Software.\
\n\
\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE \
SOFTWARE.")
	#”退出“菜单
	def MenuExit(self):
		result = tkMessageBox.askquestion("Windows Cleaner","确定要退出吗？")
		if result == 'no':
			return
		self.root.quit();
	#"扫描垃圾文件"菜单
	def MenuScanRubbish(self):
		result = tkMessageBox.askquestion("Windows Cleaner","扫描垃圾文件将需要较长时间，是否继续？")
		if result == 'no':
			return
		#tkMessageBox.showinfo("Windows Cleaner","马上开始扫描垃圾文件！")
		#self.ScanRubbish()
		self.drives = GetDrives()
		t = threading.Thread(target=self.ScanRubbish, args=(self.drives,))		#创建线程
		t.start()																#执行线程
	#"删除垃圾文件"菜单
	def MenuDelRubbish(self):
		result = tkMessageBox.askquestion("Windows Cleaner","删除垃圾文件将需要较长时间，是否继续？")
		if result == 'no':
			return
		#tkMessageBox.showinfo("Windows Cleaner","马上开始删除垃圾文件！")
		self.drives = GetDrives()
		t = threading.Thread(target=self.DeleteRubbish, args=(self.drives,))
		t.start()
	#"搜索大文件菜单"
	def MenuScanBigFile(self):
		s = tkSimpleDialog.askinteger('Windows Cleaner','请设置要搜索的文件大小(M)')
		t = threading.Thread(target=self.ScanBigFile,args=(s,))
		t.start()
	#"按名称搜索文件"菜单
	def MenuSearchFile(self):
		s = tkSimpleDialog.askstring('Windows Cleaner', '请输入文件名的部分字符')
		t = threading.Thread(target=self.SearchFile,args=(s,))
		t.start()

	#扫描垃圾文件
	def ScanRubbish(self,scanpath):		#scanpath参数可以接受元组
		global rubbishExt
		total = 0
		filesize = 0
		for drives in scanpath:
			for root,dirs,files in os.walk(drives):
				try:
					for file in files:
						filesplit = os.path.splitext(file)
						if filesplit[1] == '':	#无扩展名
							continue
						filename = os.path.join(os.path.abspath(root),file)
						filesize += os.path.getsize(filename)
						self.progress['text'] = filename
						try:
							if rubbishExt.index(filesplit[1]) >= 0:		#扩展名在垃圾文件扩展名列表中																			
								l = len(filename)
								if l>50:	#文件名过长
									filename = filename[:25] + '...' + filename[l-25:l]
								self.filelist.insert(Tkinter.END, filename + '\n')
								self.filelist.see(Tkinter.END)			#滚动条始终在最底部
								total += 1	#计文件数
						except ValueError:
							pass
				except Exception as e:
					print(e)
					pass
		self.progress['text'] = "找到 %s 个垃圾文件，共占用 %.2f M 磁盘空间" %(total, filesize/1024/1024)
	
	#删除垃圾文件
	def DeleteRubbish(self,scanpath):
		global rubbishExt
		total = 0
		filesize = 0
		for drives in scanpath:
			for root,dirs,files in os.walk(drives):
				try:
					for file in files:
						filesplit = os.path.splitext(file)
						if filesplit[1] == '':	#无扩展名
							continue
						filename = os.path.join(os.path.abspath(root),file)
						filesize += os.path.getsize(filename)
						self.progress['text'] = filename
						try:
							if rubbishExt.index(filesplit[1]) >= 0:		#扩展名在垃圾文件扩展名列表中
								
								try:
									os.remove(filename)			#删除文件
									l = len(filename)
									if l > 50:
										filename = filename[:25] + '...' + filename[l-25:l]
									self.filelist.insert(Tkinter.END, 'Deleted ' + filename + '\n')
									self.filelist.see(Tkinter.END)								
									total += 1
								except:		#不能删除，则跳过
									pass
						except ValueError:
							pass
				except Exception as e:
					print(e)
					pass
		self.progress['text'] = "删除 %s 个垃圾文件，释放 %.2f M 磁盘空间" %(total, filesize/1024/1024)

	#搜索大文件
	def ScanBigFile(self,fsize):
		total = 0
		fsize = fsize * 1024 * 1024
		for drives in GetDrives():
			for root,dirs,files in os.walk(drives):
				for file in files:
					try:
						filename = os.path.abspath(os.path.join(root,file))
						filesize = os.path.getsize(filename)
						self.progress['text'] = filename 	#在状态栏显示每一个遍历的文件
						if filesize >= fsize:
							total += 1
							self.filelist.insert(Tkinter.END, '%s, [%.2f M]\n' %(filename,filesize/1024/1024))
							self.filelist.see(Tkinter.END)
					except:
						pass
		self.progress['text'] = "找到 %s 个超过 %s M 的大文件" %(total, fsize/1024/1024)

	#按名称搜索文件
	def SearchFile(self,filename):
		total = 0
		filename = filename.upper()
		for drives in GetDrives():
			for root,dirs,files in os.walk(drives):
				for file in files:
					try:
						fn = os.path.abspath(os.path.join(root,file))
						self.progress['text'] = fn
						l = len(fn)
						if l > 50:
							fn = fn[:25] + '...' + fn[l-25:l]
						if file.upper().find(filename) >= 0:
							total += 1
							self.filelist.insert(Tkinter.END, fn + '\n')
							self.filelist.see(Tkinter.END)			#滚动条始终在最底部
					except:
						pass
		self.progress['text'] = "找到 %s 个文件" %(total)

if __name__ == "__main__" :
	window = Window()
	window.MainLoop()
 