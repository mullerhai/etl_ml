from etl_ml.etl.etl_label import ETL_Label

def etl_label_func():
  etl = ETL_Label()
  df = etl.re_construct_df_by_raw_header_loc_char_dict()
  etl.save_export_files(df, is_export_excel=True, csv_header=False)
  print(df.head())
  etl.put_etlfile_ftp()
  etl.exec_ftp_get_mv_insert_command()


if __name__ == '__main__':
  etl_label_func()