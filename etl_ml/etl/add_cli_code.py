
from etl_ml.etl.etl_master import E_M


class  Add_Cli_Code(E_M):
  def __init__(self,client_name,client_code,sec_cli_code='sec_cli_code'):
    super().__init__(conf_sec=sec_cli_code)
    self.client_name=client_name
    self.client_code=client_code
    self.script_dir_path=None
    self.script_name='load_new_code.sh'
    self.hive_host=None



  def get_cli_ssh_client(self):
    self.get_ssh_client()


  def exec_add_cli_code(self):
    cmd_str=' %s/%s  %s %s '%(self.script_dir_path,self.script_name,self.client_name,self.client_code)
    self.get_cli_ssh_client()
    self.exec_ssh_command(self.hive_host,cmd_str)