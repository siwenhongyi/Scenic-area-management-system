# -*-coding:utf-8 -*-

from Function import Function

class Interface():
	def __init__(self):
		self.f = Function()
		self.t = -1

	#命令处理
	def dispose(self,ins):
		if ins.isdigit():
			ins = int(ins)
		if ins == 1:
			self.t = self.create()
		elif ins == 2:
			self.query_v()
		elif ins == 3:
			self.navigation()
		elif ins == 4:
			self.query_e()
		elif ins == 5:
			self.plan()
		elif ins == 6:
			self.set()
		elif ins == 7:
			self.draw()
		elif ins == 8:
			self.save_exit() 
			return False
		else:
			input('输入有误，按任意按键返回主菜单\n')
			return

	#数据录入
	def create(self):
		massage = '请选择录入方式\n' + '1人工输入\n' + '2文件读入\n'
		t = int(input(massage))
		if t == 1:
			self.f.m_entry()
		elif t == 2:
			self.f.file_entry()
		else:
			input('输入有误，按任意按键返回主菜单\n')
		return

	#查询景点
	def query_v(self):
		if self.t == -1:
			input('未录入景区信息，按任意键返回主菜单\n')
			return
		self.f.query()

	#导航遍历路线
	def navigation(self):
		if self.t == -1:
			input('未录入景区信息，按任意键返回主菜单\n')
			return
		self.f.DFS_be()

	#查找最短路线
	def query_e(self):
		if self.t == -1:
			input('未录入景区信息，按任意键返回主菜单\n')
			return
		self.f.dijkstra_length()

	#铺设电路规划
	def plan(self):
		if self.t == -1:
			input('未录入景区信息，按任意键返回主菜单\n')
			return
		self.f.prim()

	#修改景区信息
	def set(self):
		if self.t == -1:
			input('未录入景区信息，按任意键返回主菜单\n')
			return
		t = self.f.set()
		if t == -1:
			return
		elif t == 0:
			self.create()
		else:
			input('修改完成，任意键返回主菜单')
			return

	#画地图
	def draw(self):
		self.f.draw()
	#保存并退出
	def save_exit(self):
		self.f.save_exit()
		return 
