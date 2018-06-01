
************Geo 风控 样本 自动化 ETL 上传ftp  插入到hive 脚本************

本脚本目录含有文件 列表
----readme.txt 
----etl.conf  
----try_etl_labels.py  
----etl_label.py  
----ftps_client.py     
----/data/    
----AA100p2_20180531.xlsx[测试样本]


1.需要确认本地安装的python包和注意事项
python 3.*版本
pandas
numpy
paramiko
ast
smtplib #暂时可以先不安装 ，如果安装出错的话

需要注意的是：
		由于windows 和mac 的 目录间隔符不同，Windows的是 \ ,mac的是 /, 所以可能会造成 etl处理好的文件，在Windows上无法上传到ftp服务器，修改 try_etl_labels.py 中 etl_label_func()的
		etl.put_etlfile_ftp() 改为 etl.put_etlfile_ftp(dir_sep='\\')


2.添加要处理的样本 excel 文件，放入该文件夹 或者 该文件夹的 data 目录中，data目录一定要预先创建好，否则脚本无法顺利执行，注意创建data目录权限问题 造成的影响


3.打开 excel 文件，观察excel的字段结构和类型，找出需要的字段列号和header名，根据 要求

		***修改 etl.conf配置文件的 [section_etl_excel_label] 片段 的字段值****

建议 把上一次的[section_etl_excel_label] 片段 保留在 一个 新的 section [section_etl_excel_label_*]片段,防止以后复用


	配置文件 相关字段解释：
	encoding ：excel 文件的 编码 ，默认 gbk ，如果因为编码导致读取文件失败 可以修改
	header=： excel 文件 是否包含业务字段名的行 ，默认包含 并在首行
	file_path = excel 文件的路径 例如：AA100p2_20180531.xlsx 放在脚本data目录就是:data/AA100p2_20180531.xlsx

	sheet_name = excel 样本所在的 sheet 名称
	sense_code =  样本的 业务场景
	date_Filed = 样本 字段 apply_time 对应 excel 文件中 实际的 时间的 字段名
	phone_Filed = 样本 字段 mobile 对应  excel 文件中 实际的 时间的 字段名
	client_nmbr = 样本的 客户编号  例如AA100
	batch = 样本的 批次号 例如 p_test4
	raw_header_loc_char_dict  hive 样本表中的11一个字段 对应excel 表中的实际字段所对应的 excel 单元格列号，是一个字典 对应关系



4.打开命令行 进入该 脚本主目录 ，

			*******执行 [ python try_etl_labels.py ]*****

不出意外，会顺利执行从excel 预处理到上传到ftp 并执行到hive 入库 一条龙的操作，注意观察 console log 输出 ，其中每一步出错都会有 错误信息的打印输出，在最后hive入库阶段会等待入库执行结果 停留两三分钟，
直到输出【exec third command insert  data to hive database  successfully】 表示入库成功。






