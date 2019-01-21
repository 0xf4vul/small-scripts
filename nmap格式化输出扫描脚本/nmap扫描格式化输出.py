# -*- coding:utf-8 -*-
import re
from bs4 import BeautifulSoup
import xlwt
import os

#将普通扫描结果整理成IP对应端口的形式。  针对xml文件  
def adjust_result(file):
    workbook = xlwt.Workbook(encoding = 'utf-8') # 创建一个workbook 设置编码
    worksheet = workbook.add_sheet('result') # 创建一个worksheet,sheet页名称
    worksheet.write(0,0, label ='Sequence number')
    worksheet.write(0,1, label ='IP:PORT')
    worksheet.write(0,2, label ='Reason')
    worksheet.write(0,3, label ='State')
    worksheet.write(0,4, label ='Service')
    w = 1
    fopen = open(file, "r")
    soup = BeautifulSoup(fopen,"lxml")
    for x in range(0,len(soup.find_all('host'))):
        if soup.find_all('host')[x].find_all('status')[0].attrs['state'] == 'up':
            for y in range(0,len(soup.find_all('host')[x].find_all('port'))):
                worksheet.write(w,0, label =w)
                #获取IP及其对应的端口
                IP_PORT = re.findall('<address addr="(.*?)"',str(soup.find_all('host')[x].find_all('address')[0]),flags=0)[0]+':'+re.findall('<port portid="(.*?)" protocol="tcp"><s',str(soup.find_all('host')[x].find_all('port')[y]),flags=0)[0]
                worksheet.write(w,1, label =re.findall('<address addr="(.*?)"',str(soup.find_all('host')[x].find_all('address')[0]),flags=0)[0]+':'+re.findall('<port portid="(.*?)" protocol="tcp"><s',str(soup.find_all('host')[x].find_all('port')[y]),flags=0)[0])
                #获取连接状态
                reason = soup.find_all('host')[x].find_all('port')[y].find_all('state')[0].attrs['reason']
                worksheet.write(w,2, label =soup.find_all('host')[x].find_all('port')[y].find_all('state')[0].attrs['reason'])
                #获取端口开放情况
                state = soup.find_all('host')[x].find_all('port')[y].find_all('state')[0].attrs['state']
                worksheet.write(w,3, label =soup.find_all('host')[x].find_all('port')[y].find_all('state')[0].attrs['state'])
                #获取端口服务
                service = soup.find_all('host')[x].find_all('port')[y].find_all('service')[0].attrs['name']
                worksheet.write(w,4, label =soup.find_all('host')[x].find_all('port')[y].find_all('service')[0].attrs['name'])
                print(IP_PORT,reason,state,service)
                w = w +1
    workbook.save('result.xls')
    print('创建文件完成！')

#主机端口扫描
def nmap_port_os(IP,PORT):
    os.system(f'nmap -sS -n -Pn -T4 -v --min-hostgroup 1024 {PORT} --initial-rtt-timeout 5s --host-timeout 3600s {IP} -oX result_port.xml')
    adjust_result('result_port.xml')
    os.remove('result_port.xml')

if __name__ == "__main__":
    nmap_port_os('-p 80,8080,443,7001,8000,22','-iL Live_IP.txt') #以nmap格式输入端口，地址两个参数
