from etl_ml.etl.etl_master import  E_M
import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path
import mimetypes
import email.MIMEImage

class EMail_Client(E_M):
  def __init__(self):
    self.FROM=None
    self.TO=None
    self.SUBJECT=None
    self.Body=None
    self.Host=None
    self.Port=None
    self.pwd=None
    self.Send_File_Name=None
    smtplib.SMTP()
    self.smtp_obj = smtplib.SMTP_SSL()
    self.smtp_obj.connect(host=self.Host, port=self.Port)
    result =self.smtp_obj.login(user=self.FROM, password=self.pwd)

  def send_normal_email(self,text):
    message_content = '\n'.join(['From:%s' % self.FROM, 'To:%s' %self.TO, 'Subject:%s' % self.SUBJECT, '', text])
    try:
      self.smtp_obj.sendmail(from_addr=self.FROM, to_addrs=[self.TO], msg=message_content)
      print("success")
    except Exception as  ex:
      print("failed %s" % ex)
      raise

  def  send_email_with_file(self,text,file_name):
    # 构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = email.MIMEText.MIMEText("this is a test text to text mime")
    main_msg.attach(text_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)

    ## 读入文件内容并格式化
    data = open(file_name, 'rb')
    file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    email.Encoders.encode_base64(file_msg)

    ## 设置附件头
    basename = os.path.basename(file_name)
    file_msg.add_header('Content-Disposition',
      'attachment', filename=basename)
    main_msg.attach(file_msg)
    fullText = main_msg.as_string()

    # 用smtp发送邮件
    try:
      self.smtp_obj.sendmail(self.FROM, self.TO, fullText)
    finally:
      self.smtp_obj.quit()




