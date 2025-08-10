#--------------------------
# Create a command line app
import click
#---------------
# Custom library
from common.pycoda import Pycoda
from common.template_exporter import TemplateExporter
from common.template_registry import TemplateRegistry
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
  def resolve_doc_id(self, strDocId):
    """Resolve template name to document ID if registered, otherwise return original ID
    
    Args:
        strDocId: Either a template name or direct document ID
        
    Returns:
        str: Resolved document ID
    """
    try:
      from common.template_registry import TemplateRegistry
      registry = TemplateRegistry()
      if registry.is_template_registered(strDocId):
        return registry.get_template_doc_id(strDocId)
    except Exception:
      # If any registry error occurs, use original doc ID (backward compatibility)
      pass
    return strDocId
  def get_column(self, strDocId, strTableId, strColumnId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.get_column(strDocId, strTableId, strColumnId)
    print ( result )

  def get_doc(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.get_doc(strDocId)
    print ( result )

  def get_section(self, strDocId, strSectionId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.get_section(strDocId, strSectionId)
    print ( result )

  def list_docs(self):
    result = self.objCoda.list_docs()
    print( result )

  def list_controls(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_controls(strDocId)
    print ( result )

  def list_folders(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_folders(strDocId)
    print ( result )

  def list_formulas(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_formulas(strDocId)
    print ( result )

  def list_sections(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_sections(strDocId)
    print ( result )

  def list_tables(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_tables(strDocId)
    print ( result )

  def list_views(self, strDocId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_views(strDocId)
    print ( result )

  def list_columns(self, strDocId, strTableId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_columns(strDocId, strTableId)
    print ( result )

  def list_rows(self, strDocId, strTableId):
    strDocId = self.resolve_doc_id(strDocId)
    result = self.objCoda.list_rows(strDocId, strTableId)
    print ( result )

  def export_template(self, strDocId, strOutputFile=None):
    """Export document as YAML template using TemplateExporter"""
    strDocId = self.resolve_doc_id(strDocId)
    # Create TemplateExporter instance
    exporter = TemplateExporter(self.objCoda)
    
    # Extract document structure
    doc_structure = exporter.extract_document_structure(strDocId)
    
    # Detect template variables
    variables = exporter.detect_variables(doc_structure)
    
    # Generate YAML template
    yaml_template = exporter.generate_yaml_template(doc_structure, variables)
    
    if strOutputFile:
      # Write to file
      with open(strOutputFile, "w") as f:
        f.write(yaml_template)
      print(f"Template exported to {strOutputFile}")
    else:
      # Print to stdout
      print(yaml_template)

  def import_template(self, strTemplateFile, strVariables=None):
    """Import YAML template and create new document using TemplateImporter"""
    from common.template_importer import TemplateImporter
    import os
    
    try:
      # Check if template file exists
      if not os.path.exists(strTemplateFile):
        raise click.ClickException(f"Template file '{strTemplateFile}' not found")
      
      # Read YAML template from file
      with open(strTemplateFile, "r") as f:
        yaml_content = f.read()
      
      # Parse variables from command line format: "VAR1=value1 VAR2=value2"
      # Handle quoted values with spaces: 'VAR1=My Project Name VAR2=value2'
      variables = {}
      if strVariables:
        import shlex
        # Use shlex to handle quoted arguments properly
        try:
          # Split respecting quotes: "DOC_NAME=My CLI Test Project" becomes one argument
          args = shlex.split(strVariables)
          for var_pair in args:
            if "=" in var_pair:
              key, value = var_pair.split("=", 1)
              variables[key] = value
        except Exception:
          # Fallback to simple split if shlex fails
          for var_pair in strVariables.split():
            if "=" in var_pair:
              key, value = var_pair.split("=", 1)
              variables[key] = value
      
      # Create TemplateImporter instance and import template
      importer = TemplateImporter()
      result = importer.create_document_from_template(yaml_content, variables, self.objCoda)
      
      # Display success message
      print(f"Document created successfully: ID={result['id']}, Name='{result['name']}'")
      
    except click.ClickException:
      # Re-raise Click exceptions (they handle exit codes properly)
      raise
    except Exception as e:
      # Convert other exceptions to Click exceptions with proper exit codes
      raise click.ClickException(f"Import failed: {str(e)}")

  def export_table(self, strDocId, strTableId, strOutputFile=None):
    """Export table data as CSV with comprehensive error handling"""
    try:
      from common.table_data_exporter import TableDataExporter

      # Resolve template name to document ID if registered
      strDocId = self.resolve_doc_id(strDocId)
      
      # Create TableDataExporter instance
      exporter = TableDataExporter(self.objCoda)
      
      # Export table data to CSV
      csv_content = exporter.export_table_csv(strDocId, strTableId)
      
      if not csv_content.strip():
        print("Warning: No data found for the specified table")
        return
        
      if strOutputFile:
        # Write to file with error handling
        try:
          with open(strOutputFile, "w", encoding="utf-8") as f:
            f.write(csv_content)
          print(f"Table data exported to {strOutputFile}")
        except PermissionError:
          raise click.ClickException(f"Permission denied: Cannot write to {strOutputFile}")
        except Exception as e:
          raise click.ClickException(f"File error: {str(e)}")
      else:
        # Print to stdout
        print(csv_content)
        
    except click.ClickException:
      # Re-raise Click exceptions (they handle exit codes properly)
      raise
    except Exception as e:
      # Convert other exceptions to Click exceptions with proper exit codes
      raise click.ClickException(f"Export failed: {str(e)}")

  def register_template(self, strName, strDocId, strDescription=None):
    """Register a template with given name and document ID using TemplateRegistry"""
    try:
      # Create TemplateRegistry instance
      registry = TemplateRegistry()
      
      # Register template
      registry.register_template(strName, strDocId)
      
      # Display success message
      success_message = f"Template '{strName}' registered successfully with document ID: {strDocId}"
      if strDescription:
        success_message += f"\nDescription: {strDescription}"
      
      print(success_message)
      
    except Exception as e:
      # Convert exceptions to Click exceptions with proper exit codes
      raise click.ClickException(f"Registration failed: {str(e)}")
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
|                            G E T _ C O L U M N   C O M M A N D                           |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.option('--column', required=True)
@click.pass_obj
#---------
# Function 
def get_column(objCoda, doc, table, column):
  """ Returns a column """
  objCoda.get_column(doc, table, column)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                               G E T _ D O C   C O M M A N D                              |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.pass_obj
#---------
# Function 
def get_doc(objCoda, doc):
  """ Returns a document """
  objCoda.get_doc(doc)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                           G E T _ S E C T I O N   C O M M A N D                          |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.option('--section', required=True)
@click.pass_obj
#---------
# Function 
def get_section(objCoda, doc, section):
  """ Returns a section """
  objCoda.get_section(doc, section)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                        E X P O R T _ T E M P L A T E   C O M M A N D                     |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True)
@click.option('--output', '-o', help='Output file path (optional)')
@click.pass_obj
#---------
# Function 
def export_template(objCoda, doc, output):
  """ Export document as YAML template """
  objCoda.export_template(doc, output)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                        I M P O R T _ T E M P L A T E   C O M M A N D                     |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--file', required=True, help='YAML template file path')
@click.option('--variables', help='Template variables in format: VAR1=value1 VAR2=value2')
@click.pass_obj
#---------
# Function 
def import_template(objCoda, file, variables):
  """ Import YAML template and create new document """
  objCoda.import_template(file, variables)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                        E X P O R T _ T A B L E   C O M M A N D                           |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--doc', required=True, help='Document ID')
@click.option('--table', required=True, help='Table ID')
@click.option('--output', '-o', help='Output CSV file path (optional)')
@click.pass_obj
#---------
# Function 
def export_table(objCoda, doc, table, output):
  """ Export table data as CSV """
  objCoda.export_table(doc, table, output)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                      R E G I S T E R _ T E M P L A T E   C O M M A N D                   |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
@clickMain.command()
@click.option('--name', required=True, help='Template name')
@click.option('--doc', required=True, help='Document ID')
@click.option('--description', help='Template description (optional)')
@click.pass_obj
#---------
# Function 
def register_template(objCoda, name, doc, description):
  """ Register a document as a template """
  objCoda.register_template(name, doc, description)
"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                M A I N   P R O C E D U R E                               |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
if __name__ == "__main__":
  clickMain()