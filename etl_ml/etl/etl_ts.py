from etl_ml.etl.etl_master import E_M


class ETL_TS(E_M):

  def __init__(self):
    super().__init__()
    self.model_code=None
    self.client_nmbr=None
    self.batch

  def  reconstruct_ts_df(self):
    print("error")

  def send_ts_ftp(self):
    print("log")

  def ftpget_ts_server(self):
    print("log")


  def insert_ts_hive(self):
    print("log")

  def ts_reply_mail(self):
    print("log")
