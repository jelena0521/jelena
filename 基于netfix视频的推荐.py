#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:28:20 2019

@author: liujun
"""



import os 
import random
import operator  
import numpy
import math

#获取文件夹
def getfile(path):
    files=[]
    for f in os.listdir(path):
        files.append(os.path.join(path,f))
        files.sort()
    return files


#获取每个moive的评论数
def num_recs(path):
    files=getfile(path)
    count = -1
    num_recs_list=[]
    for i in range(len(files)):
            for count,line in enumerate(open(files[i])):
                pass
            count += 1
            num_recs_list.append(count-1)    
    return num_recs_list


#排序1：电影按评论数排序
def hot_rate(path):
    num_recs_list=num_recs(path)
    rec_list=[]
    for index,value in enumerate(num_recs_list):
        rec_list.append({'rec_num':value,'moviesid':index+1})      
    rec_list_sorted=sorted(rec_list, key=operator.itemgetter('rec_num'), reverse=True)
    return rec_list_sorted


#整理数据，使其成为[userid,rate,time,moiveid]样式
def proprecess_data(path):
    datas=[]
    files=getfile(path)
    i=0
    while i <len(files):
        with open(files[i],'r') as f:
            for line in f:
                if line.strip().endswith(":"):
                    continue
                userid,rate,time=line.strip().split(",")
                datas.append([userid,int(rate),time,i+1])
        i=i+1            
    return datas


#排序2:按评分排序  计算每部电影的平均得分=评分总和/评分人数
def favorable_rate(path):
    datas=proprecess_data(path)
    num_recs_list=num_recs(path)
    rec_list=[]
    fav_list=[]
    for data in datas:
        rec_list.append(data[1])
    for i in range(len(num_recs_list)):
        if i==0:
            avg_rate=sum(rec_list[:num_recs_list[0]])/num_recs_list[0]
        else:
            avg_rate=sum(rec_list[sum(num_recs_list[:i]):sum(num_recs_list[:i+1])])/num_recs_list[i]
        fav_list.append({'fav_score':avg_rate,'moviesid':i+1})
        fav_list_sorted=sorted(fav_list, key=operator.itemgetter('fav_score'), reverse=True)
    return fav_list_sorted



#排序3：按用户相关度排序  使用pearson相关系数  
def pearson(x_group,y_group):
    x_sum=0
    y_sum=0
    x_power_sum=0
    y_power_sum=0
    x_y_sum=0
    num=0
    for key in x_group.keys():
        if key in y_group.keys():
            num=num+1
            x=x_group[key]
            y=y_group[key]
            x_sum=x_sum+x
            y_sum=y_sum+y
            x_power_sum= x_power_sum+x*x
            y_power_sum= y_power_sum+y*y
            x_y_sum=x_y_sum+x*y
    if num==0:
        return 0
    denominator=math.sqrt(x_power_sum-x_sum*x_sum/num)*math.sqrt(y_power_sum-y_sum*y_sum/num)
    if denominator==0:
        return 0
    else:
        return (x_y_sum-x_sum*y_sum/num)/denominator
            
#将数据整理为[USERID,{movieid1:rate1,movieid2:rate2}]
def fit_data(path):
    datas=proprecess_data(path)
    user_dict={}
    for data in datas:
        user_dict.setdefault(data[0],{})[data[-1]]=data[1] #自动合并了相同的key
    return user_dict
        
def rec(userid,path):
    user_dict=fit_data(path)
    fav_list_sorted=favorable_rate(path)
    neighbor_score=[]
    rec_list=[]
    if userid not in user_dict.keys():
        rec_list.append(fav_list_sorted[0]['moviesid'])
    else:
        for userID in user_dict.keys():
            if userid !=userID:
                r=pearson(user_dict[userid],user_dict[userID])
                neighbor_score.append({'userID':userID,'r':r})
    neighbor_sorted=sorted(neighbor_score, key=operator.itemgetter('r'), reverse=True)#找出最相近的user
    print(neighbor_sorted[0])
    
    #如果相近客户对其他电影的评分超过2分，则推荐该电影，否则好评的电影
    #如果相近用户也没看过其他电影，则推荐好评电影
    uesrID_rate_dict=user_dict[neighbor_sorted[0]['userID']]
    userid_rate_dict=user_dict[userid]
    rec_list=[]
    for key in uesrID_rate_dict.keys():
        if key not in userid_rate_dict.keys():
            rate=uesrID_rate_dict[key]
            if rate >2:
                rec_list.append(key)
            else:
                rec_list.append(fav_list_sorted[0]['moviesid'])
    if rec_list==[]:
        rec_list.append(fav_list_sorted[0]['moviesid'])
    return rec_list



rec_list=rec('573537','./data')  
print(rec_list)  

        
            

