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

  def list_controls(self, strDocId):
    result = self.objCoda.list_controls(strDocId)
    print ( result )

  def list_folders(self, strDocId):
    result = self.objCoda.list_folders(strDocId)
    print ( result )

  def list_formulas(self, strDocId):
    result = self.objCoda.list_formulas(strDocId)
    print ( result )

  def list_sections(self, strDocId):
    result = self.objCoda.list_sections(strDocId)
    print ( result )

  def list_tables(self, strDocId):
    result = self.objCoda.list_tables(strDocId)
    print ( result )

  def list_views(self, strDocId):
    result = self.objCoda.list_views(strDocId)
    print ( result )

  def list_columns(self, strDocId, strTableId):
    result = self.objCoda.list_columns(strDocId, strTableId)
    print ( result )

  def list_rows(self, strDocId, strTableId):
    result = self.objCoda.list_rows(strDocId, strTableId)
    print ( result )

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
@click.version_option("v0.1")
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
  This script prints coda data
  """
  ctx.obj = Coda(out)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                             L I S T _ D O C S   C O M M A N D                            |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.pass_obj
#---------
# Function 
def list_docs(objCoda):
  """ Returns the list of documents in Coda """
  objCoda.list_docs()

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                         L I S T _ C O N T R O L S   C O M M A N D                        |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
#---------
# Function 
def list_controls(objCoda, doc):
  """ Returns the list of controls in a doc """
  objCoda.list_controls(doc)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                          L I S T _ F O L D E R S   C O M M A N D                         |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
#---------
# Function 
def list_folders(objCoda, doc):
  """ Returns the list of folders in a doc """
  objCoda.list_folders(doc)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                         L I S T _ F O R M U L A S   C O M M A N D                        |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
#---------
# Function 
def list_formulas(objCoda, doc):
  """ Returns the list of formulas in a doc """
  objCoda.list_formulas(doc)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                         L I S T _ S E C T I O N S   C O M M A N D                        |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
#---------
# Function 
def list_sections(objCoda, doc):
  """ Returns the list of sections in a doc """
  objCoda.list_sections(doc)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                           L I S T _ T A B L E S   C O M M A N D                          |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
#---------
# Function 
def list_tables(objCoda, doc):
  """ Returns the list of tables in a doc """
  objCoda.list_tables(doc)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                            L I S T _ V I E W S   C O M M A N D                           |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
#---------
# Function 
def list_views(objCoda, doc):
  """ Returns the list of views in a doc """
  objCoda.list_views(doc)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                          L I S T _ C O L U M N S   C O M M A N D                         |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.pass_obj
#---------
# Function 
def list_columns(objCoda, doc, table):
  """ Returns the list of columns in a table """
  objCoda.list_columns(doc, table)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                             L I S T _ R O W S   C O M M A N D                            |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.pass_obj
#---------
# Function 
def list_rows(objCoda, doc, table):
  """ Returns the list of rows in a table """
  objCoda.list_rows(doc, table)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                M A I N   P R O C E D U R E                               |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
if __name__ == "__main__":
  clickMain()