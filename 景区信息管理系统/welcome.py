# -*-coding:utf-8 -*-

import Interface
import os
def menu():
	print("欢迎来到景区管理系统!")
	print("请按对应编号选择功能")
	print("1.输入景区信息")
	print("2.查询景点")
	print("3.旅游景点导航")
	print("4.路线查询")
	print("5.铺设电路规划")
	print("6.修改景区信息")
	print("7.输出景点图")
	print("8.保存并退出")



if __name__ == '__main__':
	test1 = Interface.Interface()
	t =True
	while t :
		menu()
		instruction=input('请根据相应需求输入对应功能前序号\n')
		test1.dispose(instruction)
		os.system('cls')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
