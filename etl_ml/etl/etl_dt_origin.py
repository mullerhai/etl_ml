from etl_ml.etl.etl_master import  E_M
import pandas as pd
import numpy as np
from datetime import datetime
import  logging

logger = logging.getLogger(
    name=__name__,
)
class ETL_DT_Origin(E_M):
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logger = logging.getLogger(__name__)
  def __init__(self,sec_name='sec_dt_origin_edit',tmp_pre='tmp_finance_model_data_source_'):
    super().__init__()
    self.raw_col_names=['id', 'gid', 'realname','mobile', 'certid',  'card', 'apply_time',
                  '信贷平台注册详情(如有多条命中,以分号分隔)', '贷款申请详情', '贷款放款详情', '贷款驳回详情', '逾期平台详情',
                  '欠款详情']
    self.sheet_name=self.config_parser.get(sec_name,"sheet_name")
    self.dt_origin_file=self.config_parser.get(sec_name,"dt_origin_file")
    self.date_Filed=self.config_parser.get(sec_name,"date_Filed")
    self.phone_Filed=self.config_parser.get(sec_name,"phone_Filed")
    self.idcard_Filed=self.config_parser.get(sec_name,"idcard_Filed")
    self.client_nmbr=self.config_parser.get(sec_name,"client_nmbr")
    self.batch=self.config_parser.get(sec_name,"batch")
    self.cn_simple_name=self.config_parser.get(sec_name,"cn_simple_name")
    logging.info(msg="各项配置参数已经加载。。。")
    dt=datetime.now()
    self.date_mid=dt.strftime('_%m%d_')
    self.file_extension='.txt'
    self.export_txt_file="../data/"+tmp_pre+self.cn_simple_name+self.date_mid+self.client_nmbr+self.batch+self.file_extension
    self.raw_data=pd.read_excel(self.dt_origin_file, sheet_name=self.sheet_name,
      dtype={self.idcard_Filed: np.str, self.date_Filed: np.str,self.phone_Filed:np.str})
    logging.info(msg="已经 加载文件到pandas 中...")


  def load_dt_origin_excel_file(self):
    raw_data = pd.read_excel(self.dt_origin_file, sheetname=self.sheet_name,
      dtype={'certid': np.str, 'apply_time': np.str, 'mobile': np.str})
    return raw_data

  def re_construct_df(self):
    self.raw_data['id'] = self.raw_data.index
    self.raw_data['apply_time'] = pd.to_datetime(self.raw_data['apply_time'], format='%Y/%m/%d', errors='coerce')
    self.raw_data['apply_time'] = self.raw_data['apply_time'].apply(lambda x: x.strftime('%Y/%m/%d'))
    logging.info(msg="已经将原始文件做了相关的清洗和处理")

  def  save_export_file(self,encoding='utf-8'):
    self.re_construct_df()
    self.new_data = self.raw_data[self.raw_col_names]
    self.new_data.to_csv(self.export_txt_file, sep='\t', header=False, index=False, encoding=encoding)
    logging.info(msg="导出文件成功，文件路径 ： %s "%self.export_txt_file)

  def  dt_origin_send_azkaban(self):
    print("log")

  def  download_dt_origin_from_azkaban(self):
    print("log")


if __name__ == '__main__':
    et=ETL_DT_Origin()
    et.save_export_file()
    # sec='sec_dt_origin_editor'
    # final_col_list='final_columns_list'
    # final_col=et.config_parser.get(sec,final_col_list)
    # ls=list(final_col.strip(',').split(','))
    # for l in ls:
    #   print(l)
    #print(final_col)
