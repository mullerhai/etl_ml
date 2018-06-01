from etl_ml.etl.etl_master import  E_M


class ETL_DT_Origin(E_M):

  def __init__(self):
    super().__init__()

  def load_dt_origin_excel_file(self):
    print("log")
  def re_construct_df(self):
    print("log")


  def  save_export_file(self):
    print("log")

  def  dt_origin_send_azkaban(self):
    print("log")

  def  download_dt_origin_from_azkaban(self):
    print("log")