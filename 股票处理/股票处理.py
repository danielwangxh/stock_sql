# -*- coding: GBK -*-
from tkinter import *
from tkinter import messagebox
import string 
import os
import sys
from datetime import date
import pymysql
from math import sqrt
from math import fabs
import warnings

warnings.simplefilter('ignore')

db=pymysql.connect('localhost','root','GuoXiaoBo960906','data',charset='utf8')
cursor=db.cursor()


def create_new_table(daima):
    dm='a{}'.format(daima)
    sql="create table {0} like a600000".format(dm)
    cursor.execute(sql)
    db.commit()
    dm1='A{}'.format(daima)
    sql="insert into data_list(dm) values ('{0}')".format(dm1)
    cursor.execute(sql)
    db.commit()

class main(object):
    def __init__(self,master):
        self.master=master

        self.mainlabel=Label(master,text='����������ǣ�'+str(date.today()),font=('Alrial,12'),justify=CENTER)
        self.mainlabel.grid(row=0,columnspan=100,rowspan=1)

        self.add_button=Button(master,text='�����Ʊ����',width=30, command=self.add_button_command)
        self.add_button.grid(row=1,column=0)

        self.zg7hp_button=Button(master,text='zghp',command=self.zghp_button_command,width=30)
        self.zg7hp_button.grid(row=2,columnspan=100)

    def add_button_command(self):
        add(self.master)

    def zghp_button_command(self):
        zghp(self.master)


class add(object):
    def __init__(self,master):
        self.add_page=Toplevel(master)

        self.date_label=Label(self.add_page,text='��������ӵ�����')
        self.date_label.grid(row=0,column=0,sticky=W)
        self.date_entry=Entry(self.add_page)
        self.date_entry.grid(row=0,column=1,sticky=E)

        self.index_entry=Label(self.add_page,text='������ָ��')
        self.index_entry.grid(row=1,column=0,sticky=W)
        self.index_entry=Entry(self.add_page)
        self.index_entry.grid(row=1,column=1,sticky=E)

        self.date_button=Button(self.add_page,text='����',command=self.date_button_command,width=40)
        self.date_button.grid(row=2,columnspan=2)


    def date_button_command(self):
        self.date=self.date_entry.get().strip()
        self.index=self.index_entry.get().strip()
        if self.date=='':
            messagebox.showinfo(message='����������')
        if self.index=='':
            messagebox.showinfo(message='����ָ��')
        mysql_add(self.date,self.index)
        self.add_page.destroy()

class zghp(object):
    def __init__(self,master):
        self.zg7hp_page=Toplevel(master)

        self.command_label=Label(self.zg7hp_page,text='������ָ��')
        self.command_label.grid(row=0,column=0,sticky=W)
        self.command_entry=Entry(self.zg7hp_page)
        self.command_entry.grid(row=0,columnspan=4,sticky=E)
        self.command_entry.bind('<Return>',self.command_entry_command)



        self.show_text=Text(self.zg7hp_page,width=50)
        self.show_text.grid(row=2,columnspan=4,rowspan=20)

    def command_entry_command(self,event):
        self.command=self.command_entry.get().strip()
        if self.command=='':
            messagebox.showinfo(message='����������')
        else:
            self.show_text.insert('1.0',zghp_command_show(self.command))
            self.command_entry.delete(0,END)



def mysql_add(date,index):
    cursor.execute("truncate table zg6hp_temp")
    cursor.execute("truncate table zg7hp_temp")
    sql="truncate table add_temp"
    cursor.execute(sql)
    db.commit()
    sql="LOAD DATA INFILE 'd:/{}.txt' REPLACE INTO TABLE add_temp CHARACTER SET gb2312 FIELDS TERMINATED BY '	' ENCLOSED BY ''".format(date)
    cursor.execute(sql)
    db.commit()
    sql='select * from add_temp'
    cursor.execute(sql)
    re=cursor.fetchall()

    list=[]
    cursor.execute('select * from data_list')
    data_list=cursor.fetchall()
    for daima in data_list:
        list.append(daima[0][1:7])

    for row in re:
            if row[0][2:8] not in list:
                create_new_table(row[0][2:8])

    cursor.execute('select * from astock_index where ����={0}'.format(date))
    results=cursor.fetchall()
    if len(results)==1:
        cursor.execute('delete from astock_index where ����>={0}'.format(date))
        sql='select * from add_temp'
        cursor.execute(sql)
        results=cursor.fetchall()
        for row in list:
            cursor.execute("delete from a{0} where ����>='{1}'".format(row,date))
        cursor.execute("delete from zg6hp where ����>='{0}'".format(date))
        cursor.execute("delete from zg7hp where ����>='{0}'".format(date))
        cursor.execute("delete from zg8hp where ����>='{0}'".format(date))

        db.commit()
        print('success')
    sql='insert into astock_index(����,s2,ָ��) values({0},"��ָ֤��",{1})'.format(date,index)
    cursor.execute(sql)
    db.commit()

    for row in re:
        print(row[0])
        if row[16]>0:
            mgjz=float(row[4])/float(row[16])#ÿ�ɾ�ֵ=�ɼ�/�о���
        else:
            mgjz=0
        if row[15]>0:
            mgsy=float(row[4])/float(row[15])#ÿ������=�ɼ�/��ӯ��
        else:
            mgsy=0
        if float(row[5])*float(row[21])>0:
            gs=row[5]/row[21]*0.000001#����=����/������*0.00001
        else:
            gs=0
        index6=0
        index6=sqrt(row[15]*row[16]/3)
        dm='a'+row[0][2:8]
        if row[4]==0:
            xj=row[6]
        else:
            xj=row[4]
        sql="insert into a{0} (����,����,����,����,���,���,�ּ�,������,���,rsi,����,����,ÿ������,ÿ�ɼ�ֵ,��ҵ,ϵ��6) values ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','0','{10}','{11}','{12}','{13}','{14}','{15}')".format(row[0][2:8],date,dm,row[1],row[7],row[8],row[9],xj,row[21],row[20],row[5],gs,mgsy,mgjz,row[14],index6)
        cursor.execute(sql)
        cursor.execute("insert into zg6hp_temp select * from a{0} where ����='{1}'".format(row[0][2:8],date))
    db.commit()

    for row in re:
        print(row[0])
        cursor.execute('select �ּ�,��ҵ from a{} order by ���� desc limit 20'.format(row[0][2:8]))
        temp_20=cursor.fetchall()

        if len(temp_20)>=20:
            average_20=0
            mark=0
            for row_temp in temp_20:
                average_20=average_20+row_temp[0]
                hy=row_temp[1]
            average_20=average_20/20#20�վ���

            if average_20!=0:
                gll20=100*(row[4]-average_20)/average_20#20�չ�����

            sql="update a{0} set ����20='{1}',������20='{2}' where ����='{3}'".format(row[0][2:8],average_20,gll20,date)
            cursor.execute(sql)
        if hy!='':
            dm='a'+row[0][2:8]
            cursor.execute("update {0} set ��ҵ='{1}' where ����='{2}'".format(dm,hy,date))
            cursor.execute("update zg6hp_temp set ��ҵ='{0}' where ����='{1}'".format(hy,dm))
    db.commit()

    for row in re:
        print(row[0])
        mgsy=0
        mgjz=0
        mark=0
        cursor.execute('select ���,������20,ÿ������,ÿ�ɼ�ֵ from a{} order by ���� desc limit 750'.format(row[0][2:8]))
        temp_750=cursor.fetchall()
        if len(temp_750)>=750:
            zf750=0
            bdl=0
            for row_temp in temp_750:
                zf750=zf750+fabs(row_temp[0])
                bdl=bdl+fabs(row_temp[1])
                if mark==0:
                    mgsy=row_temp[2]
                    mgjz=row_temp[3]
                    mark=1
            zf750=zf750/750#���750
            bdl=bdl/750#������
            index7=0
            if mgsy*mgjz*bdl*zf750>0:
                index7=sqrt(float(row[4])*float(row[4])/(mgjz*mgsy*sqrt(bdl*zf750)))
            sql="update a{0} set ���750='{1}',������='{2}',ϵ��7='{3}' where ����='{4}'".format(row[0][2:8],zf750,bdl,index7,date)
            cursor.execute(sql)
            if index7!=0:
                sql1="insert into zg7hp_temp select * from a{0} where ����={1}".format(row[0][2:8],date)
                cursor.execute(sql1)        
    db.commit()

    cursor.execute("select ����,����,ϵ��6 from zg6hp_temp where ϵ��6!=0 order by ϵ��6" )
    results=cursor.fetchall()
    if len(results)!=0:
        i=1
        min=0
        mark=0
        for row in results:
            if mark==0:
                min=float(row[2])
                mark=1
            cz=float(row[2])-min
            sql="update {0} set λ��6='{1}',ϵ����ֵ6='{2}' where ����='{3}'".format(row[1],i,cz,row[0])
            i=i+1
            cursor.execute(sql)

    cursor.execute("select ����,����,�ּ�,ÿ������,ÿ�ɼ�ֵ,��ҵ,ϵ��6 from zg6hp_temp where ϵ��6!=0 order by ϵ��6 ")
    temp=cursor.fetchall()
    i=1
    cursor.execute("insert into zg6hp (����) values('{0}') ".format(date))
    for temp_temp in temp:
        content=temp_temp[0]+'/'+temp_temp[1]+'/'+str(temp_temp[2])+'/'+str(temp_temp[3])+'/'+str(temp_temp[4])+'/'+temp_temp[5]+'/'+str(temp_temp[6])
        if i<=30:
            cursor.execute("update zg6hp set dim{0}='{1}' where ����={2}".format(i,content,date))
            i=i+1
        else:
            break
    print("zg6hp success")

    cursor.execute("select ����,����,ϵ��7 from zg7hp_temp order by ϵ��7 " )
    results=cursor.fetchall()
    if len(results)!=0:
        i=1
        min=0
        mark=0
        for row in results:
            if mark==0:
                min=float(row[2])
                mark=1
            cz=float(row[2])-min
            sql="update {0} set λ��7='{1}',ϵ����ֵ7='{2}' where ����='{3}'".format(row[1],i,cz,row[0])
            i=i+1
            cursor.execute(sql)
            cursor.execute("update {0} set ϵ����ֵ8='{1}' where ����='{2}'".format(row[1],cz,row[0]))

    cursor.execute("select ����,����,�ּ�,ÿ������,ÿ�ɼ�ֵ,��ҵ,ϵ��7 from zg7hp_temp order by ϵ��7 ")
    temp=cursor.fetchall()
    i=1
    j=1
    cursor.execute("insert into zg7hp (����) values('{0}') ".format(date))
    cursor.execute("insert into zg8hp (����) values('{0}') ".format(date))
    for temp_temp in temp:
        content=temp_temp[0]+'/'+temp_temp[1]+'/'+str(temp_temp[2])+'/'+str(temp_temp[3])+'/'+str(temp_temp[4])+'/'+temp_temp[5]+'/'+str(temp_temp[6])
        if i<=30:
            cursor.execute("update zg8hp set dim{0}='{1}' where ����={2}".format(i,content,date))
            i=i+1
        if temp_temp[1].find('T')==-1:
            if j<=30:
                cursor.execute("update zg7hp set dim{0}='{1}' where ����={2}".format(j,content,date))
                cursor.execute("update {0} set λ��8='{1}' where ����='{2}'".format(temp_temp[0],j,date))
                j=j+1
            else:
                break
    print('zg7hp success')
    print('finish')
    db.commit()


def zghp_command_show(command):
    number=command.split(' ')[-1]
    command=command.rstrip(number)
    command=command.lstrip('select *')
    i=1
    list=['select','����']
    temp=''
    while i<=int(number):
        list.append(",dim{0}".format(i))
        i=i+1
    command=" ".join(list)+" "+" ".join(command.split(' '))
    cursor.execute("{0}".format(command))
    results=cursor.fetchall()
    if len(results)==0:
        return ('û������')
    else:
        str=''
        for row in results:
            str=str+'\n'.join(row) +'\n'
        return (str) 



root=Tk()
root.title('��Ʊ����')
app=main(root)
root.mainloop()