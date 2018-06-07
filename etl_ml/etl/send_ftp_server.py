from etl_ml.etl.etl_master import E_M


class  Send_Ftps_hive_server(E_M):

  def __init__(self,sec='sec_upload_batch_zip_file'):
    super.__init__()
    self.sec_upload_file=sec
    self.upload_batch_zip_file=self.config_parser.get(self.sec_upload_file, 'upload_batch_zip_file')
    self.hive_server_dir_path=self.config_parser.get(self.sec_upload_file, 'hive_server_dir_path')

    #发送文件到 ftp服务器 ，并 从ftp  下载到hive服务器
  def send_batch_zip_file_func(self):
    self.push_file_ftp(self.upload_batch_zip_file)
    self.export_txtfile_path =self.upload_batch_zip_file
    self.ftp_etl_file =self.upload_batch_zip_file
    self.ftpget_file_server()
