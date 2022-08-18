# Create a single CLI command with Python

<!-- TOC -->

- [Create a single CLI command with Python](#create-a-single-cli-command-with-python)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Create a virtual environment](#create-a-virtual-environment)
- [Install dependencies](#install-dependencies)
- [Create a Makefile](#create-a-makefile)
- [Create a Main Application](#create-a-main-application)

<!-- /TOC -->

# Constraint

Base time: 2 workday (Max: 4)

## Hill chart
```
  .
 . .
.   +
0-1-2
```

# Place, Affordance, Connection

* Affordance users can act
  * App version `python coda.py`
  * List docs `python coda.py list-docs`

* Connection users are taken to
  * `python coda.py` --> `clickMain()` --> `Coda()` --> String --> Stdout
  * `python coda.py list-docs` --> `list_docs()` --> `Coda()` --> `objCoda.list_docs()` --> `pycoda.list_docs()` --> `codaio.list_docs()` --> Dict --> Json --> Stdout

# Create a virtual environment

We will start by navigating to our `app` folder. This is the root folder of our virtual environment.

Then, we will install `pipenv` and create a Python 3 virtual environment for this project.

```sh
cd app
pip3 install --user pipenv
pipenv --python $(which python3)
```

# Install dependencies

1. Workstation

Before we can run our app, we need to activate virtual environment and install any dependencies. Ensure that you are in the `app` folder.

```sh
pipenv shell
```

This command creates both the `Pipfile` and `Pipfile.lock` in your current folder. To add any dependencies under the `[packages]` section, type the following command:

```sh
pipenv install click==8.1.3 codaio==0.6.10
```

To uninstall any dependency.

```sh
pipenv uninstall click
```

To deactivate the virtual environment.

```sh
exit
```

2. Verify the installation

Create a file `hello.py` in the `app` folder. Add the following lines to the file:

```py
from codaio import Coda
import json
import os

if 'CODA_API_KEY' in os.environ:
  strApiKey = os.environ['CODA_API_KEY']

coda = Coda(strApiKey)

list = coda.list_docs(is_owner=True)
strRet=""
for doc in list:
  if doc == "items":
    for obj in list[doc]:
      strRet=strRet+json.dumps(obj)
print(strRet)
```

In the terminal, run the command `python hello.py | jq` and you should see an output similar to the example below. You may delete the `hello.py` file after verification.

```json
{
  "id": "QlIwnjdg3j",
  "type": "doc",
  "href": "https://coda.io/apis/v1/docs/QlIwnjdg3j",
  "browserLink": "https://coda.io/d/_dQlIwnjdg3j",
  "name": "Question Voting and Polling",
  "owner": "<EMAIL>",
  "ownerName": "Dennis Lee",
  "createdAt": "2020-03-21T02:25:17.000Z",
  "updatedAt": "2020-03-21T02:29:14.066Z",
  "icon": {
    "name": "hand-right",
    "type": "image/png",
    "browserLink": "https://cdn.coda.io/icons/png/color/hand-right-128.png"
  },
  "docSize": {
    "totalRowCount": 2,
    "tableAndViewCount": 2,
    "pageCount": 2,
    "overApiSizeLimit": false
  },
  "sourceDoc": {
    "id": "WFmkWSXKJJ",
    "type": "doc",
    "href": "https://coda.io/apis/v1/docs/WFmkWSXKJJ",
    "browserLink": "https://coda.io/d/_dWFmkWSXKJJ"
  },
  "workspaceId": "ws-fADlRmDYsZ",
  "folderId": "fl-uLFmBA1_Aq",
  "workspace": {
    "id": "ws-fADlRmDYsZ",
    "type": "workspace",
    "browserLink": "https://coda.io/docs?workspaceId=ws-fADlRmDYsZ",
    "name": "My Workspace"
  },
  "folder": {
    "id": "fl-uLFmBA1_Aq",
    "type": "folder",
    "browserLink": "https://coda.io/docs?folderId=fl-uLFmBA1_Aq",
    "name": "My docs"
  }
}
```

# Create a Makefile

You can use `make` to automate different parts of developing a Python app, like running tests, cleaning builds, and installing dependencies. To use `make` in your project, you need to have a file named `Makefile` at the root of your project.

1. Create a file `Makefile` in the `app` folder. Add the following lines to the file:

```makefile
.PHONY: default install_freeze install_new install_pipfile run shell shell_clean

default: run

install_freeze:
  pip3 install pipreqs
	pipreqs --ignore tests . --force
	echo "click==8.1.3" >> ./requirements.txt
	echo "codaio==0.6.10" >> ./requirements.txt
	pip3 uninstall -y pipreqs

install_new:
	pipenv install click==8.1.3 codaio==0.6.10
	pipenv install --dev pytest=6.2.4

install_pipfile:
	pipenv install --dev

run:
  python coda.py

shell:
	pipenv shell

shell_clean:
	pipenv --rm
```

Each rule consists of 3 parts: a target, a list of pre-requisities, and a recipe. The follow this format:

```makefile
target: pre-req1 pre-req2 pre-req3
  recipes
```

The `target` represents a file that needs to be created in your build. The pre-requisites list tells `make` what dependencies are required, which can be a file or another target. Finally the recipes are a list of shell commands that will be executed.

The `.PHONY` line declares a target that does not exist. As Python is an interpreted language, there is no build file.

# Create a Main Application

1. Create a file `coda.py` in the `app` folder. Add the following lines to the file:

```py
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
  This script prints coda data
  """
  ctx.obj = Coda(out)

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                M A I N   P R O C E D U R E                               |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
if __name__ == "__main__":
  clickMain()
```

2. Create a file `pycoda.py` in the `app` folder. Add the following lines to the file:

```py
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
```

3. Edit the file `Makefile` and insert a target `run` to the `.PHONY` declaration. Then declare the target `run` with the following lines of code:

```makefile
run:
	python coda.py
```

There are three environment variables used in the `run` command:
* `CODA_API_KEY` sets the CODA API key that you generated in your Coda.io account.

4. Run the make command:

```sh
make run
