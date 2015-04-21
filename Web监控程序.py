# coding=utf-8
from smtplib import SMTP
from email import MIMEText
from email import Header
from datetime import datetime
import httplib
#通过列表来添加需要检测的web网站
web_servers = [('wap.busditu.com', 80, 'index.aspx'),('v.busditu.com', 80, 'index.aspx'),('r.zciti.com',80,'index.aspx'),('gg.busditu.com',80,'index.aspx'),
              ]
print web_servers
#定义主机 帐号 密码 收件人 邮件主题
smtpserver = 'smtp.qq.com'
sender = 'mlc@zciti.com'
password = '*******'
receiver = ('gcg@zciti.com','yy@zciti.com','zxd@zciti.com') #通过组添加多个邮箱
subject = u'WEB服务器告警邮件'
From = u'Web服务器'
To = u'服务器管理员'
#定义日志文件位置
error_log = '/Users/dzero/Desktop/web_server_status.txt'   #报错路径
def send_mail(context):
    '''发送邮件'''
                                
    #定义邮件的头部信息
    header = Header.Header
    msg = MIMEText.MIMEText(context,'plain','utf-8')
    msg['From'] = header(From)
    msg['To'] = header(To)
    msg['Subject'] = header(subject + '\n')
    #连接SMTP服务器，然后发送信息
    smtp = SMTP(smtpserver)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.close()
def get_now_date_time():
    '''获取当前的日期'''
    now = datetime.now()
    print
    return str(now.year) + "-" + str(now.month) + "-" \
           + str(now.day) + " " + str(now.hour) + ":" \
           + str(now.minute) + ":" + str(now.second)
def check_webserver(host, port, resource):
    '''检测WEB服务器状态'''
    if not resource.startswith('/'):
        resource = '/' + resource
    try:
        try :
            connection = httplib.HTTPConnection(host, port)
            connection.request('GET', resource)
            response = connection.getresponse()
            status = response.status
            content_length = response.length
        except :
            return  False
    finally :
        connection.close()
    if status in [200,301] and content_length != 0:
        return True
    else:
        return False
if __name__ == '__main__':
    logfile = open(error_log,'a')
    problem_server_list = []
    for host in web_servers:
        host_url = host[0]
        check = check_webserver(host_url, host[1], host[2])
        if not check:
            temp_string = 'The Server [%s] may appear problem at %s\n' % (host_url,get_now_date_time())
            print >> logfile, temp_string
            problem_server_list.append(temp_string)
    logfile.close()
    #如果problem_server_list不为空，就说明服务器有问题，那就发送邮件
    if problem_server_list:
        send_mail(''.join(problem_server_list))