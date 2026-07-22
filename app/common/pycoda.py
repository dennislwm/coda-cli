from codaio import Coda
import json


class Pycoda():

  def __init__(self, strApiKey):
    assert(strApiKey)
    self.CODA_API_KEY = strApiKey
    self.coda = Coda(strApiKey)

  # --- requests ---

  def verify_auth(self):
    """ Returns account info for the configured API key """
    try:
      result = self.coda.account()
      return json.dumps(result)
    except Exception as e:
      return json.dumps({"error": str(e)})

  def list_docs(self):
    """ Returns a list of documents """
    try:
      list = self.coda.list_docs(is_owner=True)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def list_docs_raw(self):
    """ Returns the raw items list of documents, for programmatic use (e.g. sync) """
    return self.coda.list_docs(is_owner=True)["items"]

  def list_controls(self, strDocId):
    """ Returns a list of controls in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_controls(strDocId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def list_formulas(self, strDocId):
    """ Returns a list of formulas in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_formulas(strDocId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def list_sections(self, strDocId):
    """ Returns a list of sections in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_sections(strDocId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def list_tables(self, strDocId):
    """ Returns a list of tables in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_tables(strDocId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def list_tables_raw(self, strDocId):
    """ Returns the raw items list of tables in DocId, for programmatic use (e.g. sync) """
    assert(strDocId)
    return self.coda.list_tables(strDocId)["items"]

  def list_views(self, strDocId):
    """ Returns a list of views in DocId """
    assert(strDocId)
    try:
      list = self.coda.list_views(strDocId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def list_columns(self, strDocId, strTableId):
    """ Returns a list of columns in TableId """
    assert(strDocId)
    assert(strTableId)
    try:
      list = self.coda.list_columns(strDocId, strTableId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def list_rows(self, strDocId, strTableId):
    """ Returns a list of rows in TableId """
    assert(strDocId)
    assert(strTableId)
    try:
      list = self.coda.list_rows(strDocId, strTableId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return self.json_items(list)

  def get_doc(self, strDocId):
    """ Returns a document """
    assert(strDocId)
    try:
      val = self.coda.get_doc(strDocId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return json.dumps(val)

  def get_section(self, strDocId, strSectionId):
    """ Returns a section """
    assert(strDocId)
    assert(strSectionId)
    try:
      val = self.coda.get_section(strDocId, strSectionId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return json.dumps(val)

  def get_column(self, strDocId, strTableId, strColumnId):
    """ Returns a column """
    assert(strDocId)
    assert(strTableId)
    assert(strColumnId)
    try:
      val = self.coda.get_column(strDocId, strTableId, strColumnId)
    except Exception as e:
      return json.dumps({"error": str(e)})
    return json.dumps(val)

  def update_row(self, strDocId, strTableId, strRowId, dictCells):
    """ Updates an existing row in TableId """
    assert(strDocId)
    assert(strTableId)
    assert(strRowId)
    assert(dictCells)
    try:
      cells = [{"column": k, "value": v} for k, v in dictCells.items()]
      data = {"row": {"cells": cells}}
      result = self.coda.update_row(strDocId, strTableId, strRowId, data)
      return json.dumps(result)
    except Exception as e:
      return json.dumps({"error": str(e)})

  def upsert_row(self, strDocId, strTableId, dictCells, lstKeyColumns=None):
    """ Inserts or updates a row in TableId matched by key columns """
    assert(strDocId)
    assert(strTableId)
    assert(dictCells)
    try:
      cells = [{"column": k, "value": v} for k, v in dictCells.items()]
      data = {"rows": [{"cells": cells}]}
      if lstKeyColumns:
        data["keyColumns"] = lstKeyColumns
      result = self.coda.upsert_row(strDocId, strTableId, data)
      return json.dumps(result)
    except Exception as e:
      return json.dumps({"error": str(e)})

  def mutation_status(self, strRequestId):
    """ Returns whether a queued write (the requestId in a 202 body) has been applied (ADR-09) """
    assert(strRequestId)
    try:
      val = self.coda.get(f"/mutationStatus/{strRequestId}")
    except Exception as e:
      return json.dumps({"error": str(e)})
    return json.dumps(val)

  def create_document(self, name):
    """ Create a new document """
    assert(name)
    try:
      result = self.coda.create_doc(name)
      return json.dumps({"id": result["id"], "name": result["name"]})
    except Exception as e:
      return json.dumps({"error": str(e)})

  def add_section(self, doc_id, section_name, section_type, content):
    """ Add a section to a document """
    assert(doc_id)
    assert(section_name)
    assert(section_type)
    try:
      if section_type == "canvas":
        result = self.coda.create_section(doc_id, section_name, content)
      else:
        result = self.coda.create_section(doc_id, section_name)
      return json.dumps({"id": result["id"], "name": result["name"]})
    except Exception as e:
      return json.dumps({"error": str(e)})

  # --- helpers ---

  def json_items(self, dictItems):
    strRet = ""
    for key in dictItems:
      if key == "items":
        for val in dictItems[key]:
          strRet = strRet + json.dumps(val)
    return strRet
