import click
from common.pycoda import Pycoda
from common.template_exporter import TemplateExporter
from common.template_registry import TemplateRegistry
import json
import os


class Coda(object):

  def __init__(self, out):
    self.load_config()
    self.out = out
    self.objCoda = Pycoda(self.API_KEY)

  # --- helpers ---

  def resolve_doc_id(self, strDocId):
    """Resolve template name to document ID if registered, otherwise return original ID"""
    try:
      from common.template_registry import TemplateRegistry
      registry = TemplateRegistry()
      if registry.is_template_registered(strDocId):
        return registry.get_template_doc_id(strDocId)
    except Exception:
      pass
    return strDocId

  def resolve_table_id(self, strDocId, strTableId):
    """Resolve table name to table ID if registered under the doc, otherwise return original ID"""
    try:
      from common.template_registry import TemplateRegistry
      registry = TemplateRegistry()
      strTableName = registry.get_table_id(strDocId, strTableId)
      if strTableName is not None:
        return strTableName
    except Exception:
      pass
    return strTableId

  def print_result(self, result):
    """Print a Pycoda result, or abort non-zero if it is a CON-01 error object.

    ponytail: lives in coda.py despite CON-03's "thin dispatcher" rule because
    CON-01 forbids Pycoda from raising; move it if CON-01 ever changes.
    """
    if isinstance(result, str) and result.lstrip().startswith('{"error"'):
      raise click.ClickException(f"Coda API error: {result}")
    print(result)

  # --- commands ---

  def verify_auth(self):
    result = self.objCoda.verify_auth()
    self.print_result(result)

  def get_column(self, strDocId, strTableId, strColumnId):
    strTableId = self.resolve_table_id(strDocId, strTableId)
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.get_column(strDocId, strTableId, strColumnId)
    self.print_result(result)

  def get_doc(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.get_doc(strDocId)
    self.print_result(result)

  def get_section(self, strDocId, strSectionId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.get_section(strDocId, strSectionId)
    self.print_result(result)

  def list_docs(self):
    result = self.objCoda.list_docs()
    self.print_result(result)

  def list_controls(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_controls(strDocId)
    self.print_result(result)

  def list_formulas(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_formulas(strDocId)
    self.print_result(result)

  def list_sections(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_sections(strDocId)
    self.print_result(result)

  def list_tables(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_tables(strDocId)
    self.print_result(result)

  def list_views(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_views(strDocId)
    self.print_result(result)

  def list_columns(self, strDocId, strTableId):
    strTableId = self.resolve_table_id(strDocId, strTableId)
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_columns(strDocId, strTableId)
    self.print_result(result)

  def list_rows(self, strDocId, strTableId):
    strTableId = self.resolve_table_id(strDocId, strTableId)
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_rows(strDocId, strTableId)
    self.print_result(result)

  def update_row(self, strDocId, strTableId, strRowId, dictCells):
    strTableId = self.resolve_table_id(strDocId, strTableId)
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.update_row(strDocId, strTableId, strRowId, dictCells)
    self.print_result(result)

  def upsert_row(self, strDocId, strTableId, dictCells, lstKeyColumns=None):
    strTableId = self.resolve_table_id(strDocId, strTableId)
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.upsert_row(strDocId, strTableId, dictCells, lstKeyColumns)
    self.print_result(result)

  def export_template(self, strDocId, strOutputFile=None):
    """Export document as YAML template using TemplateExporter"""
    strDocId = self.resolve_doc_id(strDocId)
    exporter = TemplateExporter(self.objCoda)
    exporter.export_with_cli_output(strDocId, strOutputFile)

  def import_template(self, strTemplateFile, strVariables=None):
    """Import YAML template and create new document using TemplateImporter"""
    from common.template_importer import TemplateImporter
    importer = TemplateImporter()
    importer.import_with_cli_output(strTemplateFile, strVariables, self.objCoda)

  def export_table(self, strDocId, strTableId, strOutputFile=None):
    """Export table data as CSV with comprehensive error handling"""
    from common.table_data_exporter import TableDataExporter
    strTableId = self.resolve_table_id(strDocId, strTableId)
    strDocId = self.resolve_doc_id(strDocId)
    exporter = TableDataExporter(self.objCoda)
    exporter.export_with_cli_output(strDocId, strTableId, strOutputFile)

  def register_template(self, strName, strDocId, strDescription=None):
    """Register a template with given name and document ID using TemplateRegistry"""
    registry = TemplateRegistry()
    registry.register_template_cli(strName, strDocId, strDescription)

  def list_templates(self):
    """List all registered templates"""
    registry = TemplateRegistry()
    registry.list_templates_cli()

  def sync(self):
    """Sync all docs and tables from the Coda account into the registry as nested entries (REQ-013)"""
    registry = TemplateRegistry()
    docs = self.objCoda.list_docs_raw()
    synced_names = set()
    for doc in docs:
      tables = {t["name"]: t["id"] for t in self.objCoda.list_tables_raw(doc["id"])}
      registry.register_doc(doc["name"], doc["id"], tables)
      synced_names.add(doc["name"])
    pruned = registry.prune_synced(synced_names)
    print(f"Synced {len(docs)} docs" + (f", pruned {pruned} stale" if pruned else ""))

  def backup(self, strOutputDir, strDocName=None):
    """Export every registered table to <output>/<date>/<doc>/<table>.csv, skipping empties (REQ-016/ADR-07)"""
    from common.table_data_exporter import TableDataExporter
    from common.template_registry import TemplateRegistry
    from datetime import date
    registry = TemplateRegistry()
    exporter = TableDataExporter(self.objCoda)
    strDateDir = os.path.join(strOutputDir, date.today().isoformat())
    intDocs = intTables = intSkipped = 0
    lstFailures = []
    for strName, dictEntry in registry.list_templates().items():
      if strDocName and strName != strDocName:
        continue
      if not isinstance(dictEntry, dict) or "tables" not in dictEntry:
        continue  # skip flat/legacy entries -- only nested {id, tables} entries are backupable
      for strTableName, strTableId in dictEntry["tables"].items():
        try:
          strCsv = exporter.export_table_csv(dictEntry["id"], strTableId)
        except Exception as e:
          # ponytail: a backup keeps capturing reachable tables; one failure never aborts the rest
          lstFailures.append(f"{strName}/{strTableName}: {e}")
          continue
        if not strCsv.strip():
          intSkipped += 1
          continue
        strPath = os.path.join(strDateDir, strName, strTableName + ".csv")
        os.makedirs(os.path.dirname(strPath), exist_ok=True)
        with open(strPath, "w", encoding="utf-8") as f:
          f.write(strCsv)
        intTables += 1
      intDocs += 1
    print(f"Backed up {intDocs} doc(s): {intTables} exported, {intSkipped} skipped, {len(lstFailures)} failed -> {strDateDir}")
    if lstFailures:
      raise click.ClickException("Backup incomplete:\n  " + "\n  ".join(lstFailures))

  def remove_template(self, strName):
    """Remove a template from the registry"""
    registry = TemplateRegistry()
    registry.remove_template_cli(strName)

  # --- config ---

  def load_config(self):
    self.API_KEY = ""
    if 'CODA_API_KEY' in os.environ:
      self.API_KEY = os.environ['CODA_API_KEY']
    if os.path.exists("config.json"):
      with open("config.json", 'r') as f:
        config = json.load(f)
        if 'CODA_API_KEY' in config:
          self.API_KEY = config['CODA_API_KEY']


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option("v0.1")
@click.option('--out', '-o', default='text',
  type=click.Choice(['csv', 'json', 'markdown', 'text']),
  help='Output type, default=text')
@click.pass_context
def clickMain(ctx, out):
  """
  This script prints coda data
  """
  ctx.obj = Coda(out)


@clickMain.command()
@click.pass_obj
def verify_auth(objCoda):
  """ Verifies the configured API key against the Coda /whoami endpoint """
  objCoda.verify_auth()


@clickMain.command()
@click.pass_obj
def list_docs(objCoda):
  """ Returns the list of documents in Coda """
  objCoda.list_docs()


@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
def list_controls(objCoda, doc):
  """ Returns the list of controls in a doc """
  objCoda.list_controls(doc)


@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
def list_formulas(objCoda, doc):
  """ Returns the list of formulas in a doc """
  objCoda.list_formulas(doc)


@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
def list_sections(objCoda, doc):
  """ Returns the list of sections in a doc """
  objCoda.list_sections(doc)


@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
def list_tables(objCoda, doc):
  """ Returns the list of tables in a doc """
  objCoda.list_tables(doc)


@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
def list_views(objCoda, doc):
  """ Returns the list of views in a doc """
  objCoda.list_views(doc)


@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.pass_obj
def list_columns(objCoda, doc, table):
  """ Returns the list of columns in a table """
  objCoda.list_columns(doc, table)


@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.pass_obj
def list_rows(objCoda, doc, table):
  """ Returns the list of rows in a table """
  objCoda.list_rows(doc, table)


@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.option('--row', required=True, help='Row ID')
@click.option('--cells', required=True, help='Comma-separated col-id=value pairs')
@click.pass_obj
def update_row(objCoda, doc, table, row, cells):
  """ Updates an existing row in a table """
  dictCells = dict(pair.split('=', 1) for pair in cells.split(','))
  objCoda.update_row(doc, table, row, dictCells)


@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.option('--cells', required=True, help='Comma-separated col-id=value pairs')
@click.option('--key-columns', help='Comma-separated column IDs to match on (optional)')
@click.pass_obj
def upsert_row(objCoda, doc, table, cells, key_columns):
  """ Inserts or updates a row in a table """
  dictCells = dict(pair.split('=', 1) for pair in cells.split(','))
  lstKeyColumns = key_columns.split(',') if key_columns else None
  objCoda.upsert_row(doc, table, dictCells, lstKeyColumns)


@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.option('--column', required=True)
@click.pass_obj
def get_column(objCoda, doc, table, column):
  """ Returns a column """
  objCoda.get_column(doc, table, column)


@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
def get_doc(objCoda, doc):
  """ Returns a document """
  objCoda.get_doc(doc)


@clickMain.command()
@click.option('--doc', required=True)
@click.option('--section', required=True)
@click.pass_obj
def get_section(objCoda, doc, section):
  """ Returns a section """
  objCoda.get_section(doc, section)


@clickMain.command()
@click.option('--doc', required=True)
@click.option('--output', '-o', help='Output file path (optional)')
@click.pass_obj
def export_template(objCoda, doc, output):
  """ Export document as YAML template """
  objCoda.export_template(doc, output)


@clickMain.command()
@click.option('--file', required=True, help='YAML template file path')
@click.option('--variables', help='Template variables in format: VAR1=value1 VAR2=value2')
@click.pass_obj
def import_template(objCoda, file, variables):
  """ Import YAML template and create new document """
  objCoda.import_template(file, variables)


@clickMain.command()
@click.option('--doc', required=True, help='Document ID')
@click.option('--table', required=True, help='Table ID')
@click.option('--output', '-o', help='Output CSV file path (optional)')
@click.pass_obj
def export_table(objCoda, doc, table, output):
  """ Export table data as CSV """
  objCoda.export_table(doc, table, output)


@clickMain.command()
@click.option('--name', required=True, help='Template name')
@click.option('--doc', required=True, help='Document ID')
@click.option('--description', help='Template description (optional)')
@click.pass_obj
def register_template(objCoda, name, doc, description):
  """ Register a document as a template """
  objCoda.register_template(name, doc, description)


@clickMain.command()
@click.pass_obj
def list_templates(objCoda):
  """ List all registered templates """
  objCoda.list_templates()


@clickMain.command()
@click.pass_obj
def sync(objCoda):
  """ Sync all docs and tables from the Coda account into the registry """
  objCoda.sync()


@clickMain.command()
@click.option('--output', '-o', required=True, help='Backup output directory')
@click.option('--doc', help='Limit to a single registered doc name (optional)')
@click.pass_obj
def backup(objCoda, output, doc):
  """ Export every registered table to CSV under <output>/<date>/<doc>/<table>.csv """
  objCoda.backup(output, doc)


@clickMain.command()
@click.option('--name', required=True, help='Template name to remove')
@click.pass_obj
def remove_template(objCoda, name):
  """ Remove a registered template """
  objCoda.remove_template(name)


if __name__ == "__main__":
  clickMain()
