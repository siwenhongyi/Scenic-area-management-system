# -*-coding:utf-8 -*-

import numpy as np

class Graph(object):

	def __init__(self ,n = 0 ,m = 0 ,dic = {},dege = { },mat = np.zeros((1,1)) ):
		#顶点数
		self.n = n	
		#边数
		self.m = m		 
		#编号，名称，简介的字典
		self.dictionaries = dic
		#边的权值的字典
		self.edge = dege  
		#邻接矩阵
		self.matrix = mat