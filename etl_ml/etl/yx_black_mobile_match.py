# shell
# #先合并所有的历史数据
# cd  /民生历史
# wc -l  ./*
# cat. / * | uniq > all.txt


import pandas  as  pd
import numpy  as  np

#加载数据到 pandas 的 dataframe中
path='/Users/geo/Downloads/民生/GEO--5.30.xlsx'
raw_star=pd.read_excel(path,header=0,sheetname='Sheet1')
raw_p=pd.DataFrame()
raw_p['ph_star']=raw_star['手机号码']

history_data_path='/Users/geo/Downloads/民生/民生历史/all.txt'
history_data = pd.read_csv(history_data_path,dtypes={'ph':np.str}, header=None, names=['ph'], sep='\t')
history_data['ph_star']=history_data['ph'].apply(lambda row:str(row)[0:3]+'****'+str(row)[-4:])

moblie_path = '/Users/geo/Downloads/民生/Mobile.csv'
mobile_data=pd.read_csv(moblie_path,header=None,names=['in','ph_pre','province','city','dx','quhao','post']
  ,dtypes={'ph_pre':np.str},sep=',',encoding='utf-8')




# 将 dataframe 转换为 列表
raw_p_list=list(raw_p['ph_star'])

#从历史库中找到 对应的 手机号
origin_phone=list()
for  raw in  raw_p_list:
  if raw=='ph_star':continue
  print(raw)
  try:
    data=history_data[history_data.ph_star==raw]['ph'].iloc[0]
    origin_phone.append(str(data))
    print(str(data))
  except Exception as ex:
    continue

#从 电话-地区映射表中找到 对应手机号对应的城市
city_list=list()
for  raw in  origin_phone:
  if raw=='ph_star':continue
  strs=str(raw)[0:7]
  print(strs)
  try:
    data=mobile_data[mobile_data.ph_pre==strs]['city'].iloc[0]
    city_list.append(str(data))
    print(str(data))
  except Exception as ex:
    continue

#从 电话-地区映射表中找到 对应手机号对应的省份
pro_list=list()

for  raw in  origin_phone:
  if raw=='ph_star':continue
  strs=str(raw)[0:7]
  print(strs)
  try:
    data=mobile_data[mobile_data.ph_pre==strs]['province'].iloc[0]
    pro_list.append(str(data))
    print(str(data))
  except Exception as ex:
    continue

