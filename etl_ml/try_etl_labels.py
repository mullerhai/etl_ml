from etl_ml.etl.etl_label import ETL_Label
from etl_ml.etl.etl_master import E_M
from configparser import  ConfigParser
def etl_label_func():
  etl = ETL_Label()
  df = etl.re_construct_df_by_raw_header_loc_char_dict()
  etl.save_export_files(df, is_export_excel=True, csv_header=False)
  print(df.head())
  etl.put_etlfile_ftp()
  etl.exec_ftp_get_mv_insert_command()


def  send_batch_zip_file_func():

  send_cli=E_M()
  sec_upload_file='sec_upload_batch_zip_file'
  upload_batch_zip_file =send_cli.config_parser.get(sec_upload_file,'upload_batch_zip_file')
  send_cli.push_file_ftp(upload_batch_zip_file)

  send_cli.hive_server_dir_path=send_cli.config_parser.get(sec_upload_file,'hive_server_dir_path')
  send_cli.export_txtfile_path =upload_batch_zip_file
  send_cli.ftp_etl_file=upload_batch_zip_file
  send_cli.ftpget_file_server()


if __name__ == '__main__':
  #etl_label_func()
  send_batch_zip_file_func()