import sys
from PyQt5.QtGui import QPixmap,QPalette
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QWidget,QInputDialog,QMainWindow,QDialog,QLabel,QLineEdit,QGridLayout,  QToolTip,QPushButton, QApplication
from jumps.Jump_Tunnel import Jump_Tunnel
from PyQt5.QtCore import Qt
import click
import  time
import  logging
import threading
from configparser import ConfigParser
from etl_ml.etl.etl_master import E_M
import traceback


logger = logging.getLogger('etl_ml-gui')
class JumpTunnel_GUI(QWidget,threading.Thread,E_M):

  def __init__(self):
    self.state_flag = False
    self.ssh_session=None
    self.config_parser=ConfigParser()
    self.config_file='conf/etl.conf'
    self.conf_etl_sec='section_etl_excel_label'
    self.conf_remote_host='sec_remote_host'
    self.config_parser.read(self.etl_file,encoding='utf-8-sig')
    self.Ftps=None
    super().__init__()
    self.my_UI(True)
  def my_UI(self,test=False):
    jhLabel=QLabel("JumpHost:")
    jpLabel=QLabel("JumpPort:")
    juLable=QLabel("JumpUser:")
    jpwdLabel=QLabel("JumpPwd:")
    thLabel=QLabel("TunnelHost:")
    tpLabel=QLabel("TunnelPort:")
    lhLabel=QLabel("LocalHost:")
    lpLabel=QLabel("LocalPort:")
    gitLabel = QLabel("GithubRepo:")
    dtLabel=QLabel("DaemonSecond:")
    if test==True:
      self.jumpHost=QLineEdit("117.48.195.186")
      self.jumpPwd=QLineEdit("Vts^pztbvE339@Rw")
      self.tunnelHost=QLineEdit("172.16.16.32")
    else:
      self.jumpHost = QLineEdit()
      self.jumpPwd = QLineEdit()
      self.tunnelHost = QLineEdit()
    self.jumpPort = QLineEdit("2222")
    self.jumpUser = QLineEdit("dm")
    self.tunnelPort=QLineEdit("10000")
    self.localHost=QLineEdit("127.0.0.1")
    self.localPort=QLineEdit("3560")
    self.daemonSecond=QLineEdit("21600")
    github=QLineEdit("https://github.com/mullerhai/sshjumphive")
    self.btnConn = QPushButton("Trun ON", self)
    self.btnClose=QPushButton("Trun Off",self)
    self.grid=QGridLayout()
    self.grid.setSpacing(10)
    self.grid.addWidget(jhLabel,2,0)
    self.grid.addWidget(self.jumpHost,2,1)
    self.grid.addWidget(jpLabel,2,2)
    self.grid.addWidget(self.jumpPort,2,3)
    self.grid.addWidget(juLable,3,0)
    self.grid.addWidget(self.jumpUser,3,1)
    self.grid.addWidget(jpwdLabel,3,2)
    self.grid.addWidget(self.jumpPwd,3,3)
    self.grid.addWidget(thLabel,5,0)
    self.grid.addWidget(self.tunnelHost,5,1)
    self.grid.addWidget(tpLabel,5,2)
    self.grid.addWidget(self.tunnelPort,5,3)
    self.grid.addWidget(lhLabel,7,0)
    self.grid.addWidget(self.localHost,7,1)
    self.grid.addWidget(lpLabel,7,2)
    self.grid.addWidget(self.localPort,7,3)
    self.grid.addWidget(gitLabel,8,0)
    self.grid.addWidget(github,8,1)
    self.grid.addWidget(dtLabel,8,2)
    self.grid.addWidget(self.daemonSecond,8,3)
    self.grid.addWidget(self.btnConn,9,0)
    self.grid.addWidget(self.btnClose,9,3)
    pixmap = QPixmap("../img/guilogo.jpg")
    pixmap=pixmap.scaledToHeight(80)
    pixmap=pixmap.scaledToWidth(180)
    lbl = QLabel(self)
    lbl.setFixedHeight(80)
    lbl.setFixedWidth(180)
    lbl.setPixmap(pixmap)
    self.grid.addWidget(lbl,10,1)
    pixfox = QPixmap("../img/tunnel.jpg")
    pixfox=pixfox.scaledToHeight(90)
    pixfox=pixfox.scaledToWidth(90)
    lblfox = QLabel(self)
    lblfox.setFixedHeight(90)
    lblfox.setFixedWidth(90)
    lblfox.setPixmap(pixfox)
    self.grid.addWidget(lblfox,10,2)
    self.btnConn.clicked.connect(self.buttonClicked)
    self.btnClose.clicked.connect(self.btnCloseSession)
    self.setLayout(self.grid)
    self.setWindowTitle('SSH-Jump-Hive')
    self.setGeometry(300, 300, 490, 450)
    self.show()

  def btnCloseSession(self):
    # text, ok = QInputDialog.getText(self, 'Turn Off',
    #   'Please Input 1 then Trun off tunnel :')
    # logging.warn(msg="Will kill recently ssh tunnle process")
    # if ok and text=='1':
      self.state_flag=False
      try:
        self.jump_tunnel.client.close()
        logging.info(msg="ssh_tunnel turn off  successfully")
        sucTLabel = QLabel("turn off Success")
        self.grid.addWidget(sucTLabel, 9, 1)
        # text, ok = QInputDialog.getText(self, 'Success',
        #   'ssh_tunnel turn off  successfully close dialog ok')
      except:
        failedTLabel = QLabel("turn off be Failed")
        self.grid.addWidget(failedTLabel, 9, 2)
        # text, ok = QInputDialog.getText(self, 'Failed',
        #   'ssh_tunnel turn off  failed check the config')
        logging.error(msg="ssh_tunnel turn off failed,please try again")
    # else:
    #   failedTLabel = QLabel("turn off Failed")
    #   self.grid.addWidget(failedTLabel, 9, 2)
      # text, ok = QInputDialog.getText(self, 'Failed',
      #   'ssh_tunnel turn off  failed check the config')

  def buttonClicked(self):  # 在buttonClikced()方法中，我们调用sender()方法来判断哪一个按钮是我们按下的
    jumphost=self.jumpHost.text().strip()
    jumpuser=self.jumpUser.text().strip()
    jumppwd=self.jumpPwd.text().strip()
    tunnelhost=self.tunnelHost.text().strip()
    localhost=self.localHost.text().strip()

    logging.info(msg=self.jumpHost.text()+"%%"+self.jumpUser.text()+"%%"+self.jumpPwd.text())
    try:
      jumpport = (int(self.jumpPort.text().strip()) if self.jumpPort.text().strip() != None else 2222)
      tunnelappport = (int(self.tunnelPort.text().strip()) if self.tunnelPort.text().strip() != None else 10000)
      localbindport = (int(self.localPort.text().strip()) if self.localPort.text().strip() != None else 4320)
      daemonsecond = (int(self.daemonSecond.text().strip()) if self.daemonSecond.text().strip() != None else 21600)

      self.jump_tunnel=Jump_Tunnel(jumphost,jumpport,jumpuser,jumppwd,tunnelhost,tunnelappport,localhost,localbindport)
      tunnel_conn=self.jump_tunnel.jump_con_tunnel()
      self.state_flag=True
      while self.state_flag:
        with  tunnel_conn:
        #time.sleep(0.1)
          logging.info(msg="启动成功")
          sucLabel = QLabel("Connect Success")
          self.grid.addWidget(sucLabel, 9, 2)
          print(self.state_flag)
        # pe = QPalette()
        # pe.setColor(QPalette.WindowText, Qt.red)
        #sucLabel.setAutoFillBackground(pe)

        # text, ok = QInputDialog.getText(self, 'Success',
        #   'connect ssh tunnel successfully close dialog ok')
        # time.sleep(daemonsecond)
        #
    except Exception as  err :

      logging.info(msg="启动失败 %s"%err)
      failedLabel=QLabel("Connect Failed")
      self.grid.addWidget(failedLabel, 9, 2)
      # text, ok = QInputDialog.getText(self, 'Failed',
      #   'connect ssh tunnel failed check the config')

    #sender = self.sender()
    # self.showMessage(sender.text() + ' 是发送者')

def main():
  app = QApplication(sys.argv)
  jtGui = JumpTunnel_GUI()
  sys.exit(app.exec_())


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = JumpTunnel_GUI()
  sys.exit(app.exec_())
