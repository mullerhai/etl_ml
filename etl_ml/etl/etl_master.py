import pandas  as pd
import  numpy  as  np
from etl_ml.utils.ftps_client import Ftps_client
import  hashlib
import os
from  configparser import  ConfigParser
import  ast
import traceback
import logging
import paramiko

logger = logging.getLogger(
    name=__name__,
)
class E_M:
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logger = logging.getLogger(__name__)
  def  __init__(self,conf_sec='section_etl_excel_label',config_file='/Users/geo/Documents/etl_ml/etl_ml/conf/etl.conf',header=0,encoding='gbk',is_csv=False,csv_sep='\t'):
    # 标准的 入库 列名 顺序  section_etl_excel_label_AA100_p1
    self.std_filed_list = (
    "gid", "realname", "certid", "mobile", "card", "apply_time", "y_label", "apply_amount", "apply_period",
    "overdus_day", "sense_code")
    col_index = (f for f in range(0, 11))
    # 标准的 入库 列名加索引字典
    self.std_filed_dict = dict(zip(col_index, self.std_filed_list))
    # excel sheet表格 列单元 索引顺序对应的默认字母
    self.sheet_char_index = (
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T')

    self.ssh_session=None
    self.config_parser=ConfigParser()
    self.etl_file=config_file
    self.conf_etl_sec=conf_sec
    self.config_parser.read(self.etl_file,encoding='utf-8-sig')
    self.Ftps=None
    self.header=header
    self.encoding = encoding
    self.is_csv=is_csv
    self.csv_sep=csv_sep
    self.file_path = self.config_parser.get(conf_sec, 'file_path')
    l_c_dict_str=self.config_parser.get(conf_sec, 'raw_header_loc_char_dict')
    # 标准的 入库 列名 与 excel sheet表格 列单元 索引顺序对应的默认字母 的对应字典，不存在用 * 星号 表示
    self.raw_header_loc_char_dict = ast.literal_eval(l_c_dict_str)
    # 获取当前执行路径
    self.raw_dataframe=None
    self.ftp_file_dir = None



  def  config_read_filed(self,conf_sec,conf_filed):
    filed =self.config_parser.get(conf_sec, conf_filed)
    return filed

  def load_csv_file(self,date_filed='',num_filed='',header=0,encoding='utf-8',sep='\t'):
    self.raw_dataframe= pd.read_csv(self.file_path, header=header, encoding=encoding, sep=sep, parse_dates=[date_filed],
      dtype={num_filed: np.str})
    return self.raw_dataframe
  def load_excel_file(self,date_filed='',num_filed='',header=0,encoding='utf-8',sep='\t'):
    self.raw_dataframe = pd.read_excel(self.file_path, header=header, encoding=encoding, parse_dates=[date_filed],
      dtype={num_filed: np.str})
    return self.raw_dataframe

    # 生成最终的 txt 文件  保存在磁盘
  def save_export_csv_file(self, df, export_txtfile_path,base_dir = os.getcwd(), csv_header=False, encoding='utf-8', sep='\t', index=False):
      ex_file=base_dir+'/'+export_txtfile_path
      df.to_csv(ex_file, encoding=encoding, header=csv_header, sep=sep, index=index)
      logger.info(msg="导出最终txt  文件成功，txt路径 ：%s" % export_txtfile_path)

      # 生成最终的 excel 文件  保存在磁盘
  def save_export_excel_file(self, df, export_etl_xlsx_file,base_dir = os.getcwd(), encoding='utf-8', index=False):
      ex_file = base_dir + '/' + export_etl_xlsx_file
      df.to_excel(ex_file, encoding=encoding, index=index)
      logger.info(msg="导出最终excel 文件成功，excel 路径： %s" % export_etl_xlsx_file)



  def get_ftps_client(self,config_ftp_sec='sec_ftps_login'):
    self.host = self.config_parser.get(config_ftp_sec, 'ftp_host')
    self.user = self.config_parser.get(config_ftp_sec, 'ftp_user')
    self.pwd = self.config_parser.get(config_ftp_sec, 'ftp_pwd')
    self.port = self.config_parser.get(config_ftp_sec, 'ftp_port')
    try:
      cli = Ftps_client(self.host, self.user, self.pwd, self.port)
      cli.login(2, True)
      self.Ftps = cli
      self.config_ftp_sec=config_ftp_sec
    except Exception as ex:
      logger.info(msg="登录ftp服务器失败 请检查 ,error %s" % ex)
      traceback.print_exc()

  def  push_file_ftp(self,upload_etl_file,config_ftp_sec='sec_ftps_login',dir_sep='/'):
    self.get_ftps_client(config_ftp_sec)
    server_path = self.config_parser.get(self.config_ftp_sec, 'ftp_server_path')
    server_file_name=str(upload_etl_file).split(dir_sep)[-1]
    logger.info(msg="server_file_name : %s host: %s , user : %s ,pwd: %s ,port : %s ,server_path : %s "%(server_file_name,self.host,self.user,self.pwd,self.port,server_path))
    try:
      logger.info(msg="开始准备上传 %s 到 ftp 服务器" %upload_etl_file)
      self.Ftps.ftpUploadLocalFile(upload_etl_file,server_path,server_file_name)
      logger.info(msg="文件%s 上传成功"%upload_etl_file)
    except Exception as ex :
      logger.info(msg="上传失败请检查 ,error %s"%ex)
      traceback.print_exc()


  def  get_ssh_client(self,sec_remote_host = 'sec_remote_host'):
    self.ssh_session = paramiko.SSHClient()
    self.ssh_session.set_missing_host_key_policy(
      paramiko.AutoAddPolicy(),
    )
    try:
      self.ssh_session.connect(
        hostname=self.config_parser.get(sec_remote_host, 'jump_host'),
        port=self.config_parser.get(sec_remote_host, 'jump_port'),
        username=self.config_parser.get(sec_remote_host, 'jump_user'),
        password=self.config_parser.get(sec_remote_host, 'jump_pwd')
      )
      if self.ssh_session != None:
        logger.info(msg="ssh_session get successfully")
      else:
        logger.error(msg="failed to get ssh_session ")
    except Exception as ex:
      logger.error(msg="failed to get ssh_session by error %s " % ex)
      raise

  def  exec_ssh_command(self,hive_host,cmd_str,is_jump=True):
    if self.ssh_session != None:
      logging.info(msg="server host %s will exec__command  %s" % (hive_host, cmd_str))
      if is_jump==True:
        final_cmd_str = 'ssh  %s -t %s' % (hive_host, cmd_str)
      else:
        final_cmd_str =cmd_str
      stdin, stdout, stderr = self.ssh_session.exec_command(final_cmd_str)
      channel = stdout.channel
      status = channel.recv_exit_status()
      if status == 0:
        logging.info(msg="exec__command %s successfully" % cmd_str)
        return status
      else:
        logging.error(msg="failed to  exec_command %s " % cmd_str)
        return 1


  def  ftpget_file_server(self,sec_remote_host='sec_remote_host',dir_sep='/'):
    self.get_ssh_client(sec_remote_host)
    self.hivehost = self.config_parser.get(sec_remote_host, 'hive_host')
    if self.hive_server_dir_path ==None:
      self.hive_server_dir_path = self.config_parser.get(sec_remote_host, 'hive_server_dir_path')
    self.ftpget_login = self.config_parser.get(sec_remote_host, 'ftpget_login')

    self.ftp_file_dir = self.config_parser.get(sec_remote_host, 'ftp_file_dir')
    if self.ftp_etl_file ==None:
      self.ftp_etl_file = str(self.export_txtfile_path).split(dir_sep)[-1]
    else:
      self.ftp_etl_file = str(self.ftp_etl_file).split(dir_sep)[-1]
    try:
      ftp_get_cmd='%s/%s/%s'%(self.ftpget_login,self.ftp_file_dir,self.ftp_etl_file)
      mv_file_cmd = 'mv  %s  %s ' % (self.ftp_etl_file, self.hive_server_dir_path)
      logger.info(msg=ftp_get_cmd)
      #ftp_get_cmd ='ssh 172.16.16.31
      status=self.exec_ssh_command(self.hivehost,ftp_get_cmd)
      if  status==int(0):
        logger.info(msg=mv_file_cmd)
        mv_status=self.exec_ssh_command(self.hivehost,mv_file_cmd)
        logger.info(msg="exec second command  mv file command:  success " )
        return mv_status
      else :
        logging.warning(msg="first command is failed")
        return status
    except Exception as ex:
      logging.error(msg=ex)
      return 1

  def  script_insert_hive(self,script_param_str='',sec_remote_host='sec_remote_host',script_name='load_label.sh',dir_sep='/'):
    hivehost = self.config_parser.get(sec_remote_host, 'hive_host')
    hive_server_dir_path = self.config_parser.get(sec_remote_host, 'hive_server_dir_path')
    ftp_etl_file = str(self.export_txtfile_path).split(dir_sep)[-1]
    #exec_hive_cmd = 'sh   %s/load_label.sh  %s  %s  %s' % (hive_server_dir_path, ftp_etl_file, self.client_nmbr, self.batch)
    exec_hive_cmd = 'sh   %s/%s  %s  %s  ' % (hive_server_dir_path,script_name, ftp_etl_file, script_param_str)

    try:
     insert_status=self.exec_ssh_command(hivehost, exec_hive_cmd)
     if insert_status==int(0):
       logger.info(msg="exec  insert  data to hive database  successfully")
     else:
       logger.error(msg="failed insert data to hive database ,please check !!!")
    except Exception as ex:
        logger.error(msg="failed insert  data to hive database ,please check the error %s !!!" % ex)
        raise

def  e_m_test():
    print("error")


if __name__ == '__main__':

   e_m_test()


