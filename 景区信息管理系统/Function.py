# -*-coding:utf-8 -*-

import pymssql

from Graph import Graph
import numpy as np  #邻接矩阵用的  很重要
import os           #判断是不是文件 清屏用
from numpy import matlib
#下面俩画图用的
import networkx as nx
import matplotlib.pyplot as plt

#检查输入命令 返回命令序号
def judge_input(massage):
	ins = 'a'
	while (ins.isdigit() == False):
		ins = input(massage)
	ins = int(ins)
	return ins

class Function():
	def __init__(self):
		self.ga = Graph()

	#名称转化为编号 判断名字或者编号是否合法
	def name_to_id(self):
		massage = '1、按编号\n2、按名称\n'
		ins = judge_input(massage)
		if ins == 1:
			massage = '请输入景区编号'
			id = int(input(massage)) - 1
			if id >= self.ga.n or id < 0:
				input('出无此点，任意键返回主菜单\n')
				return -1
		elif ins == 2:
			massage = '请输入景区名称'
			name = input(massage)
			t = 0
			for i in range(self.ga.n):
				if self.ga.dictionaries[i]['name'] == name:
					id = i
					t = 1
					break
			if t == 0:
				input('出无此点，任意键返回主菜单\n')
				return -1
		else:
			input('指令错误，任意键返回主菜单\n')
			return -1
		return id


	#手写录入无向图
	def m_entry(self):
		n = int(input('请输入景点数\n'))
		m = int (input('请输入道路数\n'))
		massage = '请为景点自然数编号，随意输入可能发生不可预知的错误'
		input(massage + '按任意键继续\n')
		mat = np.zeros((n,n),dtype = float)
		dic = { }
		edge = { }
		for i in range(n):
			features = { }
			name = input('请输入第' + str(i+1) +'个景点的名称')
			if name == '':
				name = '空'
			syn = input('请输入第' + str(i+1) +'个景点简介')
			if syn == '':
				syn = '略'
			features ['name'] = name
			features['syn'] = syn
			dic[i] = features
		
				

		for i in range(m):
			os.system('cls')
			print('\t\t\t路线不重复输入\n\t\t\t不输入自己和自己的道路\n\t\t\t输入错误继续输入，之后在修改中改正')


			print('请输入第' + str(i+1) + '条路')
			start = -1
			while start < 0 or start >= n:
				start = judge_input('请输入起点\n') - 1
			end = -1
			while end < 0 or end >= n or end == start :
				end = judge_input('请输入终点，不与起点相同\n') - 1
			length = judge_input('请输入这条路的长度\n')
			if start in edge.keys():
				edge[start][end] = length
			else:
				lang = { }
				lang[end] = length
				edge[start] = lang
		for i in edge.keys():
			for j in edge[i].keys():
				mat[i][j] = edge[i][j]
				mat[j][i] = edge[i][j]
		self.ga = Graph(n,m,dic,edge,mat)
		return 0


	#文件录入无向图
	def file_entry(self):
		massage = '输入文件路径，目录分隔使用/，请不要用\。\n默认路径请直接回车，返回主菜单输入q\n'
		t = True
		while(t):
			filepath = input(massage)
			if (filepath == 'q' or filepath == 'Q'):
				return 
			elif(filepath == ''):
				filepath = 'D:/Graph.txt'
				t = False
			else:
				if os.path.isfile(filepath):
					t = False
				else:
					print('路径异常，重新输入\n')
		file = open(filepath,'r')
		n = int(file.readline())
		m = int(file.readline())
		dic = eval(file.readline())
		edge = eval(file.readline())
		mat = np.loadtxt(file,)
		self.ga = Graph(n,m,dic,edge,mat)
		file.close()
		massage = '文件读取成功，任意键返回主菜单\n'
		input(massage)


	#查询景点和相邻景点的信息。
	#① 景点名字② 景点介绍③ 相邻景区的名字④ 到达相邻景区的路径长度
	def query(self):
		#name_to_id输入景点名称或者编号，判断是否有效 有效返回编号，无效返回-1
		id = self.name_to_id()
		#无效输入返回主菜单
		if id == -1:
			return 
		#输出景点名称和介绍
		print('景点名称：' + str(self.ga.dictionaries[id]['name']))
		print('景点介绍：' + str(self.ga.dictionaries[id]['syn']))
		print('相邻景点:')
		#挨个遍历邻接矩阵第i行 寻找相邻景点输出
		for i in range(self.ga.n):
			if self.ga.matrix[id][i] > 0:
				print('景点名称：' + str(self.ga.dictionaries[i]['name']))
				print('景点介绍：' + str(self.ga.dictionaries[i]['syn']))
				print('与' + str(self.ga.dictionaries[id]['name']) + '距离' + str(self.ga.matrix[id][i]) + '米' + '\n')
		input('查询完毕，任意键退出返回主菜单\n')


	#使用深度优先搜索(DFS)算法，查询以该景点为起点，无回路游览整个景区的路线。输出：所有符合要求的导航路线。
	#递归前的输出
	def DFS_be(self):
		id = self.name_to_id()
		if id == -1:
			return 
		else:
			#os.system('cls')
			print('游览路线有（若显示空行则为不存在路线）：')
			list_be = [x for x in range(self.ga.n)]
			del list_be[id]
			path = [id]
			self.DFS(list_be,path)
			input('\n路线输出完毕,任意键返回主菜单\n')

	#路径的输出
	def DFS_path(self,path):
		length = 0.0
		for i in path:
			print(self.ga.dictionaries[i]['name'],end = '->')
			if i != path[-1]:
				length += self.ga.matrix[i][path[path.index(i) + 1]]

		print('路线总长' + str(length))
		return 

	#递归找路线 list_be 是还没有遍历的点  path是路径
	def DFS(self,list_be,path):
		#路径最后一个点
		id = path[-1]
		#循环所有点
		for i in range(self.ga.n):
			#id到i有路并且i不在已经走过的路径里
			if (self.ga.matrix[id][i] !=0 and i not in path):
				#创建新的未遍历列表和已走路径
				list_be_new = []
				list_be_new += list_be
				list_be_new.remove(i)
				path_new =path + [i]
				#如果走完了 输出路径  否则递归
				if list_be_new == []:
					self.DFS_path(path_new)
				else:
					self.DFS(list_be_new,path_new)
		return


	#处理：使用迪杰斯特拉(Dijkstra)算法，求得从起始景点到终点之间的最短路径，计算路径总长度。① 最短路线② 路径总长度
	#计算最短长度
	def dijkstra_length(self):
		print('需要输入起点')
		start = self.name_to_id()
		if id == -1:
			return 
		print('还需要终点')
		end = self.name_to_id()
		if end == -1:
			return 
		#book是已经找到最短距离点的列表  INF 表无穷大
		book = []
		INF = 65535
		#dis 起点到每个点最短距离  默认为无穷大
		dis = dict((i,INF) for i in self.ga.dictionaries.keys())
		#加入最小距离点设为起点 距离为0
		min_v = start
		dis[min_v] = 0

		#没有找到全部点前循环
		while len(book) < len(self.ga.dictionaries):
			#已找到列表加入距离最小点
			book.append(min_v)
			#循环所有点 如果起点到距离最小点+最小点到v有路且的距离和小于原来到v的距离 更新v的距离
			for v in self.ga.dictionaries.keys():
				if (self.ga.matrix[min_v][v] != 0 and dis[min_v] + self.ga.matrix[min_v][v] < dis[v]):
					dis[v] = dis[min_v] + self.ga.matrix[min_v][v]

			#寻找新的 距离最小点
			new_length = INF
			for v in dis.keys():
				#已经收集了  跳过
				if v in book :
					continue
				if dis[v] < new_length:
					new_length = dis[v]
					min_v = v
		#os.system('cls')
		print('从' + str(self.ga.dictionaries[start]['name']),end = ' ')
		print('到' + str(self.ga.dictionaries[end]['name']),end = ' ')
		print('最短距离是  ' + str(dis[end]),end = ' ')
		print('路线是')
		list_uncollected = []
		path = []
		list_uncollected += list(self.ga.dictionaries.keys())
		list_uncollected.remove(end)
		path.append(end)
		self.dijkstra_path(start,end,list_uncollected,path,dis[end])
	
	#根据最短长度从终点递归回溯路径
	#start 起点 end 终点，没走过的点列表 路线 终点起点距离
	def dijkstra_path(self,start,end,list_uncollected,path,length):
		#路线最后一个是起点 并且最短路正好边0 找到路 输出
		if (path[-1] == start and length == 0):
			self.print_path(path)
			return True

		#循环没走过点
		for v in list_uncollected:
			#如果终点到这个点有路 并且减去距离后大于零
			if self.ga.matrix[end][v] > 0:
				if length - self.ga.matrix[end][v] >= 0:
					#创建新的列表 递归 新找到的点是终点 起点不变 距离减去刚刚去掉的距离
					list_uncollected_new = []
					list_uncollected_new += list_uncollected
					list_uncollected_new.remove(v)

					path_new = []
					path_new += path
					path_new.append(v)

					length_new = length - self.ga.matrix[end][v]
					self.dijkstra_path(start,v,list_uncollected_new,path_new,length_new)
		return
		

	#输出路径
	def print_path(self,path):
		#列表反过来
		path.reverse()
		for i in path:
			print(self.ga.dictionaries[i]['name'],end = '--->')
		input('到达目的地\n任意键返回主菜单\n')


	#普里姆(Prim)算法构造最小生成树，设计出一套铺设线路最短，但能满足每个景点都能通电的方案。
	#① 需要铺设电路的道路② 每条道路铺设电路的长度③ 铺设电路的总长度
	def prim(self):
		#无穷大
		INF = 65535
		#未收集为空 已手机为全部
		list_collected = []

		list_uncollected = []
		list_uncollected += list(self.ga.dictionaries.keys())

		start = self.name_to_id()
		#去掉/加上 起点
		list_collected.append(start)
		list_uncollected.remove(start)
		#路线总长
		total_length = 0

		#循环寻找最小边<v,u>,v已经收集 u未收集
		#直到没有未收集
		#os.system('cls')

		while list_uncollected:
			max_length = INF
			for v in list_collected:
				for u in list_uncollected:
					if self.ga.matrix[v][u] > 0 and self.ga.matrix[v][u] < max_length :
						max_length = self.ga.matrix[v][u]
						start = v
						end = u
			print(self.ga.dictionaries[start]['name'] + '-->' + self.ga.dictionaries[end]['name'] )
			total_length += self.ga.matrix[start][end]
			list_collected.append(end)
			list_uncollected.remove(end)
		print('路线总长' + str(total_length) + '米')
		input('最短路径输出完毕，任意键退出\n')
		return 0


	#插入、删除、修改顶点、边的信息，注意顶点和边的关系，之后保存文件，重新读取文件建立图的存储结构并显示。
	#重点注意顶点和边的关系，考虑边是否重复？顶点是否存在？……
	def set(self):
		massage = '1、修改景点\n2、修改道路\n3、整体修改【重新录入】'
		ins = judge_input(massage)
		if ins == 3:
			return 0
		elif ins == 1:
			ins = judge_input('1、添加景点\n2、删除景点')
			if ins == 1:
				return self.add_point()
			elif ins == 2:
				return self.del_point()
			else:
				input('输入有误，任意键返回主菜单')
			return -1
		elif ins == 2:
			return self.set_edge()
		else:
			input('输入有误，任意键返回主菜单')
		return -1

	#加点
	def add_point(self):
		os.system('cls')
		print('\t\t增加景点')
		#改景点数
		v = self.ga.n 
		self.ga.n += 1

		#修改矩阵形状 最外面加一行一列  初始化为0
		y = np.zeros((1,v))# 1行v列
		z = np.zeros((v+1,1))#v+1行（因为刚刚加了一行，1列

		#append函数责增加元素，返回增加玩元素的新矩阵
		#第一个参数是基础矩阵，第二个参数是增加的元素，第三个是轴 0是加一行 1是加一列 不写轴参数矩阵会被展开
		#不会改变原矩阵  需要赋值
		self.ga.matrix = np.append(self.ga.matrix,y,axis = 0)
		self.ga.matrix = np.append(self.ga.matrix,z,axis = 1)


		print('新加景点编号为' + str(v+1))
		feat = {}
		name = input('请输入新景点名称\n')
		syn = input('请输入新景点简介\n')
		feat['name'] = name
		feat['syn'] = syn
		self.ga.dictionaries[v] = feat

		massage = '请输入新景点和其他景点连接道路数量\不计算自己与自己\n'
		m = judge_input(massage)
		self.ga.m += m
		for i in range(m):
			massage = '请输入第' + str(i+1) + '条路连接景点编号'
			id = judge_input(massage)
			while(id <= 0 or id > v):
				print('输入有误，重新输入')
				id = judge_input(massage)
			length = judge_input('输入道路长度\n')
			#把新路加到矩阵和边的字典 中
			self.ga.matrix[v][id-1] = length
			self.ga.matrix[id-1][v] = length
			self.ga.edge[id-1][v] = length

		self.ga.edge[v] = { }
		return 1

	#删点
	def del_point(self):
		#os.system('cls')
		print('\t\t删除景点')
		v = self.name_to_id()
		if v == -1:
			return -1
		self.ga.n -= 1

		#字典删除点
		del self.ga.dictionaries[v]

		#边的字典删除点
		for i in range(self.ga.n):
			if i == v:
				del self.ga.edge[v]
				break
		for i in list(self.ga.edge.keys()):
			for j in list(self.ga.edge[i].keys()):
				if i == v:
					del self.ga.edge[i][v]
					break




		#从删除的点后面一个到最后一个 更新编号 也就是字典的key值
		for i in range(v+1,list(self.ga.dictionaries.keys())[-1]+1):
			self.ga.dictionaries[i-1] = self.ga.dictionaries.pop(i)
			self.ga.edge[i-1] = self.ga.edge.pop(i)

		for i in range(self.ga.n):
			for j in list(self.ga.edge[i].keys()):
				if j > v:
					self.ga.edge[i][j-1] = self.ga.edge[i].pop(j)

		#delete返回按要求删除后的新矩阵， 参数  原矩阵，索引，轴，不写轴会展开
		#不改变原来矩阵，需要赋值
		self.ga.matrix = np.delete(self.ga.matrix,v,axis = 0)
		self.ga.matrix = np.delete(self.ga.matrix,v,axis = 1)

		#nonzero 返回矩阵非零元素索引  二维的是两个元组 一个0轴 一个1轴【测试一下更清楚】
		#transpose 把两个元组转换成一个列表
		#求列表长度就是非零元素数量 除以2就是边的数量
		self.ga.m = int(len(np.transpose(np.nonzero(self.ga.matrix))) / 2)


		return 1

	#改线
	def set_edge(self):
		os.system('cls')
		print('\t\t修改道路')
		print('首先输入道路起点')
		start = self.name_to_id()
		if start == -1:
			return -1
		print('接着输入道路终点')
		end = self.name_to_id()
		if end == -1:
			return -1

		massage = '请输入道路长度，删除或者不存在请输入0\n'
		length = judge_input(massage)
		self.ga.matrix[start][end] = abs(length)
		self.ga.matrix[end][start] = abs(length)
		if length == 0:
			if end in self.ga.edge[start].keys():
				del self.ga.edge[start][end]
			if start in self.ga.edge[end].keys():
				del self.ga.edge[end][start]
		else:
			if end in self.ga.edge[start].keys():
				self.ga.edge[start][end] = length
			if start in self.ga.edge[end].keys():
				self.ga.edge[end][start] = length
		return 1


	#图的绘图显示
	def draw(self):
		#穿件一个顶点的列表
		node = []
		for i in range(self.ga.n):
			node.append(self.ga.dictionaries[i]['name'])
		#创建边的列表 每个边是一个三元组 首顶点 尾顶点 权值
		edge = []
		for i in self.ga.edge.keys():
			for j in self.ga.edge[i].keys():
				edge.append((self.ga.dictionaries[i]['name'],self.ga.dictionaries[j]['name'],self.ga.edge[i][j]))
		#空的无向图  然后加入点和边
		G = nx.Graph()
		G.add_nodes_from(node)
		G.add_weighted_edges_from(edge)
		#标题 不支持中文
		plt.title('map')
		#布局方式 不布局每次画的不一样而且有些图会很奇怪 circular_layout布局是顶点分布在一个圆环上 试了下这个最好
		pos = nx.circular_layout(G)
		#draw接受近20个参数  这里写的三个是  需要画的无向图 布局方式 顶点带标签 具体参数可以看
		#https://networkx.github.io/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html#networkx.drawing.nx_pylab.draw_networkx

		nx.draw(G,pos = pos,with_labels = True)
		plt.show()
		#清空图
		G.clear()


	#保存并退出
	def save_exit(self):
		if self.ga.n !=0 :
			filepath = 'D:/输出文件.txt'
			file = open(filepath,'w')
			file.write(str(self.ga.n) + '\n')
			file.write(str(self.ga.m) + '\n')
			file.write(str(self.ga.dictionaries) + '\n')
			file.write(str(self.ga.edge) + '\n')
			#savetxt numpy提供的文件操作函数，参数较多 
			#这里写的参数是 文件【可以输文件对象也可以是路径】 需要获取数据的矩阵 数据格式【和C语言一样】
			np.savetxt(file,self.ga.matrix,fmt = '%.2f')
			file.close()
		os._exit(0)

class SQLSever():
	def __init__(self):
