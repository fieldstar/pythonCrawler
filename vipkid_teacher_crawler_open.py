# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 10:13:10 2018
@author: Xiaoqing Zeng, CSUST
"""

import urllib.request
import urllib.parse
import http.cookiejar
import re
import http.client

#url="http://www.baidu.com/s?wd="
#keyword="曾小青"
#keyword_code=urllib.request.quote(keyword)
#url_all=url+keyword_code
#print(url_all)

#proxy_addr="120.26.218.22:808"
#proxy=urllib.request.ProxyHandler({'http':proxy_addr})
#opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
#urllib.request.install_opener(opener)

cjar=http.cookiejar.CookieJar()
#opener.add_handler(urllib.request.HTTPCookieProcessor(cjar)) #如果前面已经build了opener，则此时调用add_handler添加handler
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
urllib.request.install_opener(opener)

def getcontent(url,page):
    #以浏览器方式登录，设置request header
    req=urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    req.add_header('Origin','https://www.vipkid.com.cn')
    req.add_header('Referer','https://www.vipkid.com.cn/login/')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header("Authorization","parent xxxxxxxxxxxxxxxxx")

#    response samples
#    resp='"avatar":"https://teacher-media.vipkid.com.cn/teacher/avatar/6615782/avatar_large/image_20170817094416_dbbca49b13674ab4923ce07bf40ea514.png"'
    teacheridpattern='"avatar":"https://teacher-media.vipkid.com.cn/teacher/avatar/(\d{7})/avatar_large'  #teacherid是7位数字
    data=str(opener.open(req).read().decode('utf-8')) 
#    data=str(urllib.request.urlopen(req).read().decode('utf-8')) #另一种读数据方式，是网络爬虫而不是模拟浏览器
 
    teacheridList=re.compile(teacheridpattern).findall(data) #返回teacherid列表
#    print("teacher's id is "+str(teacheridList))
#    teachernamepattern='{"id":\d{7},"name":"(.*?)","showName"'   
 
#    teachernameList=re.compile(teachernamepattern).findall(data) #返回teachername列表
#    print(teachernameList)
    teacherdata=""
    ftdler=open("c:\\tmp\\web\\vipkid_teacher_detail.json","ab+")       #该教师的详细信息
    fscsler=open("c:\\tmp\\web\\vipkid_teacher_stu_comm_stat.json","ab+") #该教师的学生评价统计
    fctcler=open("c:\\tmp\\web\\vipkid_teacher_comm_tag_count.json","ab+") #该教师的标签统计
    
          
    for i in range(0,len(teacheridList)):
#        print('Teacher\'s id is:'+str(teacheridList[i]))
#        print('Teacher\'s name is:'+str(teachernameList[i]))
        try:
    #        teacherdata=getTeachderDetail(teacheridList[i]) #获取该教师的详细信息
    #        ftdler.write(bytes('{beginTeacher}'+str(teacherdata)+'{endTeacher}',encoding='utf-8'))
                
            stuCommStatdata=getStuCommStat(teacheridList[i])    #获取该教师的学生评价统计
            fscsler.write(bytes('{beginTeacher}"teacherid":'+str(teacheridList[i])+',"studentCommentStatistics":'+stuCommStatdata+'{endTeacher}',encoding='utf-8'))
                
            teacherCommTagCountData=getTeacherCommTagCount(teacheridList[i]) #获得该教师的标签统计
            fctcler.write(bytes('{beginTeacher}"teacherid":'+str(teacheridList[i])+',"teacherCommentTagCount":'+teacherCommTagCountData+'{endTeacher}',encoding='utf-8'))

        except http.client.HTTPException as e:
            print('Error occurred in reading info in teacheridList loop')
            continue
        except http.client.IncompleteRead as e:
            print('Error occurred in reading info in teacheridList loop')
            continue
        except urllib.error.URLError as e:
            print('Error occurred in reading info in teacheridList loop')
            continue
        
# 关闭文件，数据存入磁盘      
    ftdler.close()     
    fscsler.close()     
    fctcler.close()

    return data

def getTeachderDetail(teacherid):
    print(teacherid+' is the teacherid')
    teacherDetailURL='https://www.vipkid.com.cn/rest/parentrest/api/pc/teacher/getTeacherDetails?teacherId='+teacherid+'&studentId=xxxxxxxx&t=1516678882941'
    req=urllib.request.Request(teacherDetailURL)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    req.add_header('Origin','https://www.vipkid.com.cn')
    req.add_header('Referer','https://www.vipkid.com.cn/login/')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header("Authorization","parent xxxxxxxxxxxxxxxxx")
    try: 
#    teacherdetail=str(urllib.request.urlopen(req).read().decode('utf-8'))
        teacherdetail=str(opener.open(req).read().decode('utf-8'))
        return teacherdetail
    except http.client.HTTPException as e:
        print('Error occurred in getTeachderDetail')
    except http.client.IncompleteRead as e:
        print('Error occurred in getTeachderDetail')
    except urllib.error.URLError as e:
        print('Error occurred in getTeachderDetail')


def getStuCommStat(teacherid):  #获取该教师的学生评价统计
    stuCommentStatURL='https://www.vipkid.com.cn/rest/parentrest/api/teacherDetail/getStudentCommentStatistics?teacherId='+teacherid+'&studentId=xxxxxxxx&t=1516678882941'
    req=urllib.request.Request(stuCommentStatURL)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    req.add_header('Origin','https://www.vipkid.com.cn')
    req.add_header('Referer','https://www.vipkid.com.cn/login/')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header("Authorization","parent xxxxxxxxxxxxxxxxx")
    try: 
    #    stuCommentStatData=str(urllib.request.urlopen(req).read().decode('utf-8'))
        
        stuCommentStatData=str(opener.open(req).read().decode('utf-8'))  
    ##   读取学生对该教师的评价
    #    countOfCommentByTeacherPattern='"data":{"total":(.*?),"high"'  #匹配字符串
    #    countOfComment=re.compile(countOfCommentByTeacherPattern).findall(stuCommentStatData)
    #    count=int(countOfComment[0]) #该教师的评价数
    ##    print('the count of teacher\'s comments is:'+str(count))
    #    
    #    import math
    #    pagenum=math.ceil(count/15)  #每页显示的学生评价数是15条
    #    fstuCommListler=open("c:\\tmp\\web\\vipkid_stu_comm_list_byTeacher.json","ab+") #该教师的学生评价    #    
    #    fstuCommListler.write(bytes('{beginTeacher}"teacherid":'+str(teacherid)+',"StuCommentByTeacher":',encoding='utf-8'))
    #
    #    for i in range(1,pagenum+1):
    #        try:
    #            fstuCommListData=getCommListByTeacher(teacherid,str(i))   #获取该教师的学生评价
    #            fstuCommListler.write(bytes(fstuCommListData,encoding='utf-8'))
    #        except http.client.HTTPException as e:
    #            continue  
    #        except http.client.IncompleteRead as e:
    #            continue
    #        except urllib.error.URLError as e:
    #            continue
    #
    #    fstuCommListler.write(bytes('{endTeacher}',encoding='utf-8'))
    #
    #    fstuCommListler.close()
        return stuCommentStatData
    
    except http.client.HTTPException as e:
        print('Error occurred in getStuCommStat, the reason is')
    except http.client.IncompleteRead as e:
        print('Error occurred in getStuCommStat, the reason is')
    except urllib.error.URLError as e:
        print('Error occurred in getStuCommStat, the reason is')

def getTeacherCommTagCount(teacherid):  #获得该教师的标签统计
    teacherCommTagCountURL='https://www.vipkid.com.cn/rest/parentrest/api/pc/studentComment/getCommentTagsCount?teacherId='+teacherid
    req=urllib.request.Request(teacherCommTagCountURL)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    req.add_header('Origin','https://www.vipkid.com.cn')
    req.add_header('Referer','https://www.vipkid.com.cn/login/')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header("Authorization","parent xxxxxxxxxxxxxxxxx")
    try:
    #    teacherCommTagCountData=str(urllib.request.urlopen(req).read().decode('utf-8'))
        teacherCommTagCountData=str(opener.open(req).read().decode('utf-8'))  
        return teacherCommTagCountData
    except http.client.HTTPException as e:
        print('Error occurred in getTeacherCommTagCount')
    except http.client.IncompleteRead as e:
        print('Error occurred in getTeacherCommTagCount')
    except urllib.error.URLError as e:
        print('Error occurred in getTeacherCommTagCount')


def getCommListByTeacher(teacherid,pagenum):  #获取该教师的学生评价
    stuCommListByTeacherURL='https://www.vipkid.com.cn/rest/parentrest/api/teacherDetail/getStudentCommentListByTeacherId?teacherId='+teacherid+'&page='+pagenum+'&featured=1&ratingLevel=&t=1516690167554'
    req=urllib.request.Request(stuCommListByTeacherURL)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    req.add_header('Origin','https://www.vipkid.com.cn')
    req.add_header('Referer','https://www.vipkid.com.cn/login/')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header("Authorization","parent xxxxxxxxxxxxxxxxx")
    try:
    #    stuCommListByTeacherData=str(urllib.request.urlopen(req).read().decode('utf-8'))
        stuCommListByTeacherData=str(opener.open(req).read().decode('utf-8')) 
        return stuCommListByTeacherData       
    except http.client.HTTPException as e:
        print('Error occurred in getCommListByTeacher')
    except http.client.IncompleteRead as e:
        print('Error occurred in getCommListByTeacher')
    except urllib.error.URLError as e:
        print('Error occurred in getCommListByTeacher')


#fhandle=open("c:\\tmp\\web\\vipkid_teacherlist1.htm","wb") #新建文件并覆盖写入用"wb"参数，文件追加用"ab"，都是二进制写入
#fhandle.write(data)
#fhandle.close()
data=""
fhandle=open("c:\\tmp\\web\\vipkid_teacher_lists.json","ab+")  #所有教师基本信息写入
for i in range(1,75):
    url="https://www.vipkid.com.cn/rest/parentrest/api/pc/teacher/getTeacherList?keyword=&studentId=xxxxxxxx&page="+str(i)+"&count=500&startTime=09:00&endTime=21:30&gender=BOTH&t=1516514334658"
    
    try:
        data=getcontent(url,i)
    except http.client.HTTPException as e:
        continue  
    except http.client.IncompleteRead as e:
        continue
    except urllib.error.URLError as e:
        continue
#print(data)
    fhandle.write(bytes(data,encoding='utf-8'))
    
fhandle.close()
