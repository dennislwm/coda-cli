#-------------------------
# Blasterai/codaio library
from codaio import Coda

#-----------------
# Standard library
import json
import re

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                    M A I N   C L A S S                                   |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
class Pycoda():

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                   C O N S T R U C T O R                                  |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def __init__(self, strApiKey):
    #----------------------------
    # initialize class _CONSTANTS
    assert(strApiKey)
    self._init_meta()

    self.CODA_API_KEY = strApiKey
    self.coda = Coda(strApiKey)

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                C L A S S   R E Q U E S T S                               |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def list_docs(self):
    """ Returns a list of documents """
    try:
      list = self.coda.list_docs(is_owner=True)
    except:
      return "{}"
    return self.json_items(list)

  def list_controls(self, strDocId):
    """ Returns a list of controls in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_controls(strDocId)
    except:
      return "{}"
    return self.json_items(list)

  def list_folders(self, strDocId):
    """ Returns a list of folders in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_folders(strDocId)
    except:
      return "{}"
    return self.json_items(list)

  def list_formulas(self, strDocId):
    """ Returns a list of formulas in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_formulas(strDocId)
    except:
      return "{}"
    return self.json_items(list)

  def list_sections(self, strDocId):
    """ Returns a list of sections in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_sections(strDocId)
    except:
      return "{}"
    return self.json_items(list)

  def list_tables(self, strDocId):
    """ Returns a list of tables in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_tables(strDocId)
    except:
      return "{}"
    return self.json_items(list)

  def list_views(self, strDocId):
    """ Returns a list of views in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_views(strDocId)
    except:
      return "{}"
    return self.json_items(list)

  def list_columns(self, strDocId, strTableId):
    """ Returns a list of columns in TableId """
    assert(strDocId)
    assert(strTableId)
    try:
      list = self.coda.list_columns(strDocId, strTableId)
    except:
      return "{}"
    return self.json_items(list)

  def list_rows(self, strDocId, strTableId):
    """ Returns a list of rows in TableId """
    assert(strDocId)
    assert(strTableId)
    try:
      list = self.coda.list_rows(strDocId, strTableId)
    except:
      return "{}"
    return self.json_items(list)

  def get_doc(self, strDocId):
    """ Returns a document """
    assert(strDocId)
    try:
      val = self.coda.get_doc(strDocId)
    except:
      return "{}"
    return json.dumps(val)

  def get_section(self, strDocId, strSectionId):
    """ Returns a section """
    assert(strDocId)
    assert(strSectionId)
    try:
      val = self.coda.get_section(strDocId, strSectionId)
    except:
      return "{}"
    return json.dumps(val)

  def get_column(self, strDocId, strTableId, strColumnId):
    """ Returns a column """
    assert(strDocId)
    assert(strTableId)
    assert(strColumnId)
    try:
      val = self.coda.get_column(strDocId, strTableId, strColumnId)
    except:
      return "{}"
    return json.dumps(val)

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                 C L A S S   M E T H O D S                                |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def json_items(self, dictItems):
    strRet=""
    for key in dictItems:
      if key == "items":
        for val in dictItems[key]:
          strRet=strRet+json.dumps(val)
    return strRet

  def json_error(self):
    jsnRet = json.dumps({})
    jsnRet['error_code'] = 1
    jsnRet['error_msg'] = 'Failed request'
    return jsnRet

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