#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf-8
"""
ssh-jump-hive 主程序
"""
# import argparse
# import gettext
import io
# import json
import logging

from jumps.Jump_Tunnel import Jump_Tunnel
import click
import time

import codecs
import os
import importlib
import sys

# input = 'Input here'
# in_stream = io.BytesIO(input.encode('utf-8'))
# sys.stdin = io.TextIOWrapper(in_stream, encoding='utf-8')
# out_stream = io.BytesIO()
# sys.stdout = io.TextIOWrapper(out_stream, encoding='utf-8')


importlib.reload(sys)
click.disable_unicode_literals_warning = True

import locale

print(locale.getpreferredencoding())
print(codecs.lookup(locale.getpreferredencoding()).name)

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
print(locale.getpreferredencoding())
APP_DESC = """

    #########  ####### #                            ###                 ###        ### 
    #             #    #                            ####               ####        ###
    #             #    #                            # ####           ## # #        ###      
    #########     #    #        ##############      # #   ##        ##  # #        ###   
    #             #    #                            # #    ##     ##    # #        ###     
    #             #    #                            # #      # # #      # #        ###     
    #########     #    #########  CODE BY MULLER    # #        #        # #        ############### 

                        ---- A Terminal Tools For ETL  Dirty Data  Feature Project 
                        ---- For Send File to Ftps  Server, ftpget file to hive server
                        ---- insert data to hive  load hive data for  ML model train send email

    @author Muller Helen (https://github.com/mullerhai/sshjumphive)
                                    last_update 2018-06-1 15:50:59
"""

logger = logging.getLogger('ETL-shell')
Process_HoldOn_DaemonSecond = 21600  # 六小时  six hours


def check_setting_and_env():
  logger.info("程序正在启动,检查环境配置")
  if sys.version_info < (3, 2):
    raise RuntimeError("at least Python 3.3 is required!!")
  logger.info("开始配置环境")


@click.command()
# @click.argument('jhost',default="117.48.195.186", required=True)
@click.option('-jh', '--jumphost', default="117.48.195.186",
  help='Jump Gateway Server host 跳板机ssh 主机名, 默认117.48.195.186')
@click.option('-jp', '--jumpport', default=2222, help='Jump Gateway Server port跳板机ssh登录端口号, 默认2222')
@click.option('-ju', '--jumpuser', default='dm', help='Jump Gateway Server login user 跳板机 ssh登录用户名')
@click.option('-jpd', '--jumppwd', default="Vts^pztbvE339@Rw", help='Jump Gateway Server login user password 跳板机登录用户密码')
@click.option('-th', '--tunnelhost', default='172.16.16.32', help='ssh-tunnel 隧道 host ')
@click.option('-tp', '--tunnelappport', default=10000, help='ssh-tunnel Application port隧道 目标程序的端口号 默认为 hive 10000 ')
@click.option('-lh', '--localhost', default='127.0.0.1', help='localhost本机 host ,默认127.0.0.1 ')
@click.option('-lp', '--localbindport', default="4230", help='localbindport 本机 被绑定的端口号')
@click.option('-dt', '--daemonsecond', default="21600",
  help='ssh_tunnel_daemon_session_hold_on_second six hours, ssh 隧道 后台线程 保持时间 默认为六小时')
def parse_command(jumphost, jumpport, jumpuser, jumppwd, tunnelhost, tunnelappport, localhost, localbindport,
                  daemonsecond):
  logger.info("正在检查环境")
  check_setting_and_env()
  if jumphost == "117.48.195.186":
    logger.info(
      msg="jumphost: %s, jumpport: %s,  tunnelhost: %s, tunnelAppPort: %s, localhost: %s, localBindport: %s," % (
        jumphost, jumpport, tunnelhost, tunnelappport, localhost, localbindport))
  else:
    logger.info(
      msg="jumphost: %s, jumpport: %s, jumpuser: %s, jumppwd: %s, tunnelhost: %s, tunnelAppPort: %s, localhost: %s, localBindport: %s," % (
        jumphost, jumpport, jumpuser, jumppwd, tunnelhost, tunnelappport, localhost, localbindport))

  logger.info("环境检查完毕,正在开启 start ssh_tunnel for you(请等待15s~30s)")
  start_jump_tunnel_client(jumphost, int(jumpport), jumpuser, jumppwd, tunnelhost, int(tunnelappport), localhost,
    int(localbindport), int(daemonsecond))


def start_jump_tunnel_client(jumphost, jumpport, jumpuser, jumppwd, tunnelhost, tunnelAPPport, localhost, localbindport,
                             daemonsecond):
  jump_tunnel = Jump_Tunnel(jumphost.strip(), jumpport, jumpuser.strip(), jumppwd.strip(), tunnelhost.strip(),
    tunnelAPPport, localhost.strip(), localbindport)
  tunnel = jump_tunnel.jump_con_tunnel()
  try:
    with  tunnel:
      # jump_tunnel.jump_con_tunnel().start()
      logger.info("ssh tunnel start successfully")
      logger.info("please  hold on the shell ,do not turn off it ! or  you can turn it like daemon process")
      logger.info("please make sure the  ssh_tunnel daemon_session default hold on six hours , ")
      logger.info("if you want to change it   please set the config param -dt")
      logger.info("if you want to close the ssh_tunnel_session just close the shell !")
      time.sleep(daemonsecond)
  except:
    logger.error("ssh tunnel start failed,please check the config param or maybe localport has been used  change it!")


def main():
  print(APP_DESC)
  time.sleep(0.02)
  parse_command()


if __name__ == "__main__":
  main()
