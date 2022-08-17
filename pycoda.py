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
    list = self.coda.list_docs(is_owner=True)
    strRet=""
    for doc in list:
      if doc == "items":
        for obj in list[doc]:
          strRet=strRet+json.dumps(obj)
    return strRet

  def list_sections(self, strDocId):
    """ Returns a list of sections in DocId """
    assert(strDocId)
    list = self.coda.list_sections(strDocId)
    strRet=""
    for doc in list:
      if doc == "items":
        for obj in list[doc]:
          strRet=strRet+json.dumps(obj)
    return strRet

  def list_tables(self, strDocId):
    """ Returns a list of tables in DocId """
    assert(strDocId)
    list = self.coda.list_tables(strDocId)
    strRet=""
    for doc in list:
      if doc == "items":
        for obj in list[doc]:
          strRet=strRet+json.dumps(obj)
    return strRet

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                 C L A S S   M E T H O D S                                |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
  def json_error():
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