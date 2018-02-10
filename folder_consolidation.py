# -*- coding: utf-8 -*-
_author_ = '$陈吉-一颗小洋葱'

import os
import sys
import hashlib
import time
import shutil

class FolderConsolidation():
    def __init__(self):
        self.fileNum = 0      #文件数目
        self.folderNum = 0    #文件夹数目
        self.backupNum = 0    #创建的旧文件备份的数目
        self.sum = 0          #总数目
    
    # 计算文件的MD5值   
    def get_file_md5(self,filename):     
        if not os.path.isfile(filename):
            return
        filehash = hashlib.md5()
        f = open(filename,'rb')
        while True:
            i = f.read(8096)
            if not i :
                break
            filehash.update(i)
        f.close()
        return filehash.hexdigest()

    # 判断文件是否修改过
    def isModify(self,file1,file2):
        return  self.get_file_md5(file1) != self.get_file_md5(file2)

    # 将时间戳转换成时间显示格式
    def stamp_to_time(self,Stamp):
        timeArray = time.localtime(Stamp)
        newTime = time.strftime("%Y.%m.%d.%H.%M.-old_file_backup", timeArray)
        return newTime

    # 合并两个文件夹
    def consolidation(self,path1,path2):
        pathsB = os.listdir(path2)    # 获取文件夹2中的目录结构
        for fp in os.listdir(path1):   # 遍历文件夹1中的文件或文件夹
            new_path1 = os.path.join(path1,fp)    # 文件夹1中的文件或子文件夹
            new_path2 = os.path.join(path2,fp)    # 文件夹2中的文件或路径，不一定存在
            if os.path.isdir(new_path1):           # 文件夹1中的目录
                if os.path.exists(new_path2):      # 如果在文件夹2中存在
                    self.consolidation(new_path1,new_path2)    # 递归，继续合并下一级文件夹
                else:   # 如果在文件夹2中不存在
                    print ('[目录]\t%s --> %s' %(new_path1,new_path2))
                    shutil.copytree(new_path1,new_path2)   # 完全复制目录到文件夹2
                    self.folderNum += 1
                    
            elif os.path.isfile(new_path1):        # 文件夹1中的文件
                if os.path.exists(new_path2):      # 如果在文件夹2中存在
                    s = os.stat(new_path2)
                    if self.isModify(new_path1,new_path2) == True:  # 如果该文件修改过
                        # 创建备份
                        backup = new_path2.split('.')[-1]  # 得到文件的后缀名
                        # 将文件夹2中原文件创建备份
                        copy_path2 = new_path2[:-len(backup)-1]+"(%s)."%(self.stamp_to_time(s.st_mtime))+backup
                        print ('[备份]\t%s --> %s' %(new_path1,copy_path2))
                        shutil.copy2(new_path2,copy_path2)
                        self.backupNum += 1
                        # 将文件夹1中修改过的文件复制过来
                        print ('[文件]\t%s --> %s' %(new_path1,new_path2))
                        shutil.copy2(new_path1,new_path2)
                        self.fileNum += 1
                    else:  # 如果该文件没有修改过，不复制
                        pass
                    
                else:   # 如果在文件夹2中不存在，将该文件复制过去
                    print ('[文件]\t%s --> %s' %(new_path1,new_path2))
                    shutil.copy2(new_path1,new_path2)
                    self.fileNum += 1
    
    # 显示当前的文件夹合并状态              
    def print_status(self):       
        self.sum = self.folderNum + self.fileNum + self.backupNum
        print ('[合并状态]')
        print('当前已复制文件%d个，子文件夹%d个，创建旧文件备份%d个，总共合并项目%d个' %(self.fileNum,self.folderNum,self.backupNum,self.sum))

    # 清除当前的文件夹合并状态
    def clear_status(self):      
        self.fileNum = 0
        self.folderNum = 0
        self.backupNum = 0
        self.sum = 0
    #首页
    def welcome(self):
        print('                               文件夹合并工具')
        print('     __________________________________________________________________')
        print('     |                                                                |')
        print('     |           欢迎使用文件夹合并工具FolderConsolidation            |')
        print('     |              此程序工具可以将文件夹1合并到文件夹2              |')
        print('     |  即文件夹1 --> 文件夹2将文件夹1中修改的内容在文件夹2中更新合并 |')
        print('     |                  具体的合并规则可以查看帮助文档                |')
        print('     |                                                                |')
        print('     |                         制作人：陈 吉                          |')
        print('     |________________________________________________________________|')
        print('\n键盘敲击任意键进入菜单开始使用！\n')
        os.system('pause');
        os.system('cls');

    #菜单
    def menu(self):
        print('                             文件夹合并工具菜单')
        print('     __________________________________________________________________')
        print('     |                                                                |')
        print('     |                    开始进行文件夹合并请输入：1                 |')
        print('     |                       查看帮助文档请输入：2                    |')
        print('     |                          退出请输入：0                         |')
        print('     |________________________________________________________________|')
        print('\n')

    def do_consolidation(self):
        path1 = input('请输入文件夹1的绝对路径：\n').strip()
        path2 = input('请输入文件夹2的绝对路径：\n').strip()
        if path1 == '':
            print('文件夹1的绝对路径为空，请输入正确的路经！\n')
            input('请按回车键退出！')
            sys.exit(0)
        elif path2 == '':
            print('文件夹2的绝对路径为空，请输入正确的路经！\n')
            input('请按回车键退出！')
            sys.exit(0)
        print('开始合并文件夹1 %s 到文件夹2 %s,%s --> %s' %(path1,path2,path1,path2))
        try:
            print('文件夹合并中......\n')
            self.consolidation(path1,path2)
        except Exception as e:
            print('文件夹合并失败!\n')
            print('失败原因:',e)
            self.clear_status()
        else:
            print('文件夹合并成功！\n')
            self.print_status()
            self.clear_status()
        input('请按回车键退出！')
        sys.exit(0)

    # 显示帮助文档
    def help(self):
        print('                           文件夹合并工具帮助文档\n')
        print('                               制作人：陈 吉\n                           ')     
        print(' 功能：')
        print('     合并两个文件夹。')
        print('     将文件夹1合并到文件夹2，同级目录下，')
        print('     将文件夹1中有，文件夹2中没有的目录完全复制到文件夹2中；')
        print('     将文件夹1中没有，文件夹2中有的目录不做改动；')
        print('     文件夹1和文件夹2中均有的文件，比对两个文件是否有发生过修改，')
        print('     将文件夹1中做了修改的文件，在文件夹2的同级目录下创建旧文件的备份。（并没有覆盖旧文件）')
        print('     文件夹中的子文件夹也采用这种方式进行递归进行合并。')

        print(' 适应需求：')
        print('     1、整理文件夹时合并两个文件夹。')
        print('     2、U盘中是文件夹与本机中的文件夹进行合并：')
        print('         一般文件夹1是从文件夹2复制过来的文件夹，做了修改后，想合并回文件夹2。')
        print('         这样在文件夹1中做的一些改动有时我们就不太清楚了，这个程序可以：')
        print('         将文件夹1中修改的部分在文件夹2中更新。')

        print(' 文件版本：')
        print('     将修改后的文件完全复制过去。')
        print('     旧的文件创建备份，')
        print('     基于文件的MD5值判断文件是否修改过。')

            

if __name__=='__main__':
    fc = FolderConsolidation()
    fc.welcome()
    i = 1
    while(i == 1):
        fc.menu()
        j = input('请选择菜单：\n').strip()
        if j == '1' :
            fc.do_consolidation()
            print('\n继续使用工具进行文件夹合并请输入 1 ，退出请输入0\n')
            k = input().strip()
            if k == '0' :
                del fc
                sys.exit(0)                        
        if j == '2' :
            fc.help()
            print('\n继续使用工具进行文件夹合并请输入 1 ，退出请输入0\n')
            k = input().strip()
            if k == '0' :
                del fc
                sys.exit(0)
        if j == '0' :
            del fc
            sys.exit(0)