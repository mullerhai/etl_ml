from ftplib import FTP
from ftplib import FTP_TLS

class  Ftps_client:
  ##初始化的时候会把登录参数赋值初始化
  def __init__(self,host,user,pwd,port=21):
    self.host=host
    self.port=port
    self.user=user
    self.pwd=pwd
    self.Ftp=None
    #self._old_makepasv=FTP_TLS.makepasv

## ftp 登录项  含有闭包项
  def login(self,debug=2,set_pasv=True):
    _old_makepasv = FTP_TLS.makepasv
    def _new_makepasv(self):
      host, port = _old_makepasv(self)
      host = self.sock.getpeername()[0]
      return host, port
    FTP_TLS.makepasv = _new_makepasv
    self.Ftp = FTP_TLS(self.host)
    self.Ftp.set_debuglevel(debug)
    self.Ftp.auth()
    self.Ftp.login(self.user,self.pwd)
    self.Ftp.makepasv()
    self.Ftp.sendcmd('pbsz 0')
    self.Ftp.set_pasv(set_pasv)
    self.Ftp.prot_p()
    print("您好 您已经登录 ftp： %s 服务器" % self.host)
    self.Ftp.getwelcome()
    return self.Ftp

  #显示  目录下的 文件列表
  def ftplistDir(self,ftps,sever_path):
    self.Ftp.cwd("/")#首先切换得到根目录下，否则会出现问题
    self.Ftp.cwd(sever_path)
    files = ftps.nlst()
    for f in files:
      print(f)

# 下载服务器文件
  def  ftpDownloadSeverFile(self,sever_path,sever_file,new_localfile,buffersize=1024):
    self.Ftp.cwd("/")
    self.Ftp.cwd(sever_path)
    with open(new_localfile , 'wb')as download_file:
      self.Ftp.retrbinary('RETR %s' %sever_file , download_file.write, buffersize)

##上传文件 需要注意 上传文件的  new_severfile 只能是文件名，不能包含带目录 的 文件全路径
  def  ftpUploadLocalFile(self,local_filepath,sever_path,new_severfile,buffersize=1024):
    self.Ftp.cwd("/")
    self.Ftp.cwd(sever_path)
    with open(local_filepath,'rb') as  upload_file:
      self.Ftp.storbinary('STOR ' + new_severfile, upload_file, buffersize)




def test():
  host = 'ftps.baidu.com'
  port = '21'
  user = 'zh****'
  pwd = 'zz****m'
  cli=Ftps_client(host,user,pwd,port)
  fs= cli.login(2,True)
  #fs.makepasv()
  # files = []
  # files = fs.nlst()
  # for f in files:
  #   print(f)
  path='china'
  cli.ftplistDir(fs,path)

##测试使用 通过
if __name__ == '__main__':
  test()