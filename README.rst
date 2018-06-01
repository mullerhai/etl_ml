DSTL
====

https://github.com/mullerhai/etl_ml

Note: this repo is not supported. License is MIT.


..

    image:: etl_ml.jpg
.. image:: https://github.com/mullerhai/etl_ml/blob/master/img/logo.jpeg

.. contents::

Install [sorry Mircosoft Windows  System  cannot use it]
------------

: pip  install -U etl_ml[Now Version is 0.0.1]

    - python Version >= 3.5
    - sasl>=0.2.1
    - thrift>=0.11.0
    - thrift-sasl>=0.3.0
    - paramiko>=2.4.1
    - selectors>=0.0.14



Use in Unix System Terminal[centos macos  ubuntu]
------------

: jumps
    - default param
: parameter:
    - @click.option('-jh', '--jumphost', default="***", help='Jump Gateway Server host 跳板机ssh 主机名, 默认117.48.195.186')
    -  @click.option('-jp', '--jumpport', default=2222, help='Jump Gateway Server port跳板机ssh登录端口号, 默认2222')
    -   @click.option('-ju', '--jumpuser', default='dm', help='Jump Gateway Server login user 跳板机 ssh登录用户名')
    -   @click.option('-jpd', '--jumppwd', default="***",  help='Jump Gateway Server login user password 跳板机登录用户密码')
    -   @click.option('-th', '--tunnelhost', default='172.16.16.32', help='ssh-tunnel 隧道 host ')
    -   @click.option('-tp', '--tunnelappport', default=10000, help='ssh-tunnel Application port隧道 目标程序的端口号 默认为 hive 10000 ')
    -   @click.option('-lh', '--localhost', default='127.0.0.1', help='localhost本机 host ,默认127.0.0.1 ')
    -   @click.option('-lp', '--localbindport', default="4230", help='localbindport 本机 被绑定的端口号')
    -   @click.option('-dt', '--daemonsecond', default="21600", help='ssh_tunnel_daemon_session_hold_on_second six hours, ssh 隧道 后台线程 保持时间 默认为六小时')

.. image:: https://github.com/mullerhai/sshjumphive/blob/master/img/runshell.jpeg


Use in Unix System Terminal Run GUI[centos macos  ubuntu]
------------
: jumpgui
    - you will see the  GUI like this
.. image:: https://github.com/mullerhai/sshjumphive/blob/master/img/rungui.jpg


If you Buy the  SSH_Tunnel for mac [maybe feel Expensive]
------------

.. image:: https://github.com/mullerhai/sshjumphive/blob/master/img/SSH_Tunnel_mac.jpg

Object types
------------

Note that ssh_jump_hive  is an tools can  jump the jump machine  to connect hive get hive data to pandas dataframe:

- 0: hive_client  for  simple connect hive server  with  no jump server
- 1: Jump_Tunnel just  for  connect hive server with  jump server separete
- 2: SSH_Tunnel  for  get ssh tunnel channel


General approach
----------------

if  you want to use it ,you need  to know some things
for example these parameters [ jumphost,jumpport,jumpuser,jumppwd,tunnelhost,tunnelAPPport,localhost,localbindport]
for hive server  you also need to know params [localhost, hiveusername, hivepassword, localbindport,database, auth]
for query hive data you need to know params [ table, query_fileds_list, partions_param_dict, query_limit]

if your hive server has  jump server separete， you need do  like this
[
::
    from ssh_jump_hive import Jump_Tunnel_HIVE
    import pandas as pd
    ## get hive_tunnel_client_session
    def gethive():
      jumphost = '117.*****.176'
      jumpport = 2222
      jumpuser = 'dm'
      jumppwd = '&&&&&&'
      tunnelhost = '172.**.16.32'
      tunnelhiveport = 10000
      localhost = '127.0.0.1'
      localbindport = 4800
      username = 'muller'
      auth = 'LDAP'
      password = "abc123."
      database = 'fkdb'
      table = 'tab_client_label'
      partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
      query_fileds_list = ['gid', 'realname', 'card']
      querylimit = 1000
      jump = Jump_Tunnel_HIVE(jumphost, jumpport, jumpuser, jumppwd, tunnelhost, tunnelhiveport, localhost, localbindport,
        username, password)
      return jump

 ## query some fileds by table name and  partitions params
 def demo1():
        table = 'tab_client_label'
        partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
        query_fileds_list = ['gid', 'realname', 'card']
        querylimit = 1000
        jump=gethive()
        df2=jump.get_JumpTunnel_df(table,partions_param_dict,query_fileds_list,querylimit)
        return df2
    ## query all fileds by table name and partitions params
    def demo2():
      table = 'tab_client_label'
      partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
      jump =gethive()
      df2 = jump.get_JumpTunnel_table_partitions_df(table,partions_param_dict,1000)
      return df2
    ## use  hsql to query data
    def demo3():
      jump = gethive()
      hsql="select * from fkdb.tab_client_label where  client_nmbr= 'AA75' and batch= 'p1' limit 500"
      df2=jump.get_JumpTunnel_hsql_df(hsql)
      return df2
    ## initail the instance to query
    df3=demo2()
    print(df3.shape)
    print(df3.columns)
    print(df3.head(100))
]


UNet network with batch-normalization added, training with Adam optimizer with
a loss that is a sum of 0.1 cross-entropy and 0.9 dice loss.
Input for UNet was a 116 by 116 pixel patch, output was 64 by 64 pixels,
so there were 16 additional pixels on each side that just provided context for
the prediction.
Batch size was 128, learning rate was set to 0.0001
(but loss was multiplied by the batch size).
Learning rate was divided by 5 on the 25-th epoch
and then again by 5 on the 50-th epoch,
most models were trained for 70-100 epochs.
Patches that formed a batch were selected completely randomly across all images.
During one epoch, network saw patches that covered about one half
of the whole training set area. Best results for individual classes
were achieved when training on related classes, for example buildings
and structures, roads and tracks, two kinds of vehicles.

Augmentations included small rotations for some classes
(±10-25 degrees for houses, structures and both vehicle classes),
full rotations and vertical/horizontal flips
for other classes. Small amount of dropout (0.1) was used in some cases.
Alignment between channels was fixed with the help of
``cv2.findTransformECC``, and lower-resolution layers were upscaled to
match RGB size. In most cases, 12 channels were used (RGB, P, M),
while in some cases just RGB and P or all 20 channels made results
slightly better.


Validation
----------

Validation was very hard, especially for both water and both vehicle
classes. In most cases, validation was performed on 5 images
(6140_3_1, 6110_1_2, 6160_2_1, 6170_0_4, 6100_2_2), while other 20 were used
for training. Re-training the model with the same parameters on all 25 images
improved LB score.
