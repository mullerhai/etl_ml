import smtplib



if __name__ == '__main__':
  HOST = 'smtp.qq.com'

  # QQ邮箱的端口是465

  PORT = '465'

  TO='zhanghaining@geotmt.com'
  pwd='wblrjgvfznnybbje'
  FROM='hai710459649@foxmail.com'
  SUBJECT='welcome to world'
  TEXT='today is friday ,we will get rest for two days '
  smtplib.SMTP()
  smtp_obj = smtplib.SMTP_SSL()
  smtp_obj.connect(host=HOST, port=PORT)
  result = smtp_obj.login(user=FROM, password=pwd)
  print(result)
  message_content ='\n'.join(['From:%s'%FROM,'To:%s'%TO,'Subject:%s'%SUBJECT,'', TEXT])

  try:
    smtp_obj.sendmail(from_addr=FROM,to_addrs=[TO],msg=message_content)
    print("success")
  except Exception as  ex:
    print( "failed %s"%ex)
    raise


