#--------------------------
# Create a command line app
import click
#---------------
# Custom library
from pycoda import Pycoda
#-----------------
# Standard library
import json
import os

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                    M A I N   C L A S S                                   |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
class Coda(object):

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                   C O N S T R U C T O R                                  |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def __init__(self, out):
    #----------------------------
    # initialize class _CONSTANTS
    self._init_meta()

    #----------------
    # Class variables
    self.load_config()

    #-------------------------
    # Initialize click objects
    self.out = out
    self.objCoda = Pycoda(self.API_KEY)

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                        E X T E R N A L   C L A S S   M E T H O D S                       |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def list_docs(self):
    result = self.objCoda.list_docs()
    print( result )

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                        I N T E R N A L   C L A S S   M E T H O D S                       |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def load_config(self):
    self.API_KEY = ""

    #---------------------------
    # Load environment variables
    if 'CODA_API_KEY' in os.environ:
      self.API_KEY = os.environ['CODA_API_KEY']

    #--------------------------------------
    # A JSON file supercedes os environment
    if os.path.exists("config.json"):
        with open("config.json", 'r') as f:
            config = json.load(f)
            if 'CODA_API_KEY' in config:
              self.API_KEY = config['CODA_API_KEY']

  def print_result(self, result):
    if self.out == 'text':
      strText = json.dumps(result, indent=4, separators=(',', ': '))
      strText = strText.replace('[', '')
      strText = strText.replace(']', '')
      strText = strText.replace('{', '')
      strText = strText.replace('}', '')
      strText = strText.replace(',', '')
      strText = strText.replace('\"', '')
      strText = strText.replace('    \n', '')
      strText = strText.replace('    ', '')
      print(strText)

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                C L A S S   M E T A D A T A                               |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def _init_meta(self):
      """
      | _strMETACLASS, _strMETAVERSION, _strMETAFILE used to save() and load() members
      """
      self._strMETACLASS = str(self.__class__).split('.')[1][:-2]
      self._strMETAVERSION = "0.1"
      """
      | Filename "_Class_Version_"
      """
      self._strMETAFILE = "_" + self._strMETACLASS + "_" + self._strMETAVERSION + "_"

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                  M A I N   C O M M A N D                                 |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@click.group( context_settings=dict(help_option_names=['-h', '--help']) )
#---------------
# Choice options
@click.option('--out', '-o', default='text', 
  type=click.Choice([
    'csv',
    'json',
    'markdown',
    'text'
  ]),
  help='Output type, default=text')
@click.pass_context
#--------------
# Main function
def clickMain(ctx, out):
  """
  This script prints bible data
  """
  ctx.obj = Coda(out)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                             L I S T _ D O C S   C O M M A N D                            |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.pass_obj
#---------
# Function 
def list_docs(objBiblia):
  """ Returns the table of contents of a bible """
  objBiblia.list_docs()

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                M A I N   P R O C E D U R E                               |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
if __name__ == "__main__":
  clickMain()