from etl_ml.etl.etl_master import E_M



class ETL_TH(E_M):

  def __init__(self):
    super().__init__()
    self.model_code=None
    self.client_nmbr=None
    self.batch=None

  def  reconstruct_dt_df(self):
    print("error")

  def send_th_ftp(self):
    print("log")

  def ftpget_th_server(self):
    print("log")


  def insert_th_hive(self):
    print("log")

  def th_reply_mail(self):
    print("log")
