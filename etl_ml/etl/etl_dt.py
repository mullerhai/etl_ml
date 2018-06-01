
from  etl_ml.etl.etl_master import E_M
from configparser import ConfigParser
class ETL_DT(E_M):


  def __init__(self,file_path,conf_sec='section_etl_excel_label',config_file='conf/etl.conf'):
    super().__init__()
    self.client_nmbr=None
    self.batch=None
    # self.file_path=file_path
    # self.config_parser = ConfigParser()
    # self.etl_file = config_file
    # self.conf_etl_sec = conf_sec
    # self.config_ftp_sec = 'sec_ftps_login'
    # self.config_parser.read(self.conf_etl_sec, encoding='utf-8-sig')
  def  reconstruct_dt_df(self):
    print("error")

  def send_dt_ftp(self):
    print("log")

  def ftpget_dt_server(self):
    print("log")


  def insert_dt_hive(self):
    print("log")

  def dt_reply_mail(self):
    print("log")


if __name__ == '__main__':
  fp='data/AA99p1_20180530.xlsx'

  etl_dt=ETL_DT(fp)
  sec_remote_host = 'sec_remote_host'
  etl_dt.get_ssh_client(sec_remote_host)
  if etl_dt.ssh_session !=None:
    print("ok")
  else:
    print('error')