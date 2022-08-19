# Build and test a command and return its output

<!-- TOC -->

- [Build and test a command and return its output](#build-and-test-a-command-and-return-its-output)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Test driven development of a command](#test-driven-development-of-a-command)
- [Create test case](#create-test-case)
- [Configure build](#configure-build)
- [Build the command](#build-the-command)

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
  * List sections `python coda.py list-sections`

* Connection users are taken to
  * `python coda.py list-sections` --> `list_sections()` --> `Coda()` --> `objCoda.list_sections()` --> `pycoda.list_sections()` --> `codaio.list_sections()` --> Dict --> Json --> Stdout

# Test driven development of a command

When you approach coding using a test driven development ["TDD"], you start with a test case and then build your code around the test case. You can have have one or more test cases for each feature.

In our example, we a command that allows users to list sections in a document. There are two cases that we test for:

- Exit code is 0
- Json output contains a string `Section`.

In our first test case, with reference to our connection where users are taken to, this fails if the environment variable `CODA_API_KEY` is not configured, or if the docID is invalid.

The second test case, with reference to our places where users can navigate, this fails if the docID is invalid.

# Create test case

1. Edit the `tests/test_coda.py` file and append the following lines of code:

```py
strDoc='QlIwnjdg3j'

def test_list_sections():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-sections', '--doc', strDoc])
  assert result.exit_code == 0
  assert "page" in result.output 

def main():
  ...
  test_list_sections()
```

# Configure build

1. Install Python packages

Before we can run our app, we need to activate virtual environment and install any dependencies. We use the flag `--dev` to specify that these packages are for development only.

```sh
cd app
pipenv shell
pipenv install --dev pytest=6.2.4
```

# Build the command

With reference to our connection where users are taken to:
* `python coda.py list-sections` --> `list_sections()` --> `Coda()` --> `objCoda.list_sections()` --> `pycoda.list_sections()` --> `codaio.list_sections()` --> Dict --> Json --> Stdout

When a user makes a `list-sections` command, the `coda.py` calls the global function `list_sections()`, that in turn calls the method `list_sections()` of instance `ctx.obj`, which is an object of the `Coda` class. 

This method of instance `ctx.obj` calls your custom wrapper function `list_sections()` of instance `objCoda`, which is an object of the `Pycoda` class. Your custom library calls the function `list_sections` from the package `codaio`, which returns a dictionary. This is parsed by your function and translated to a Json return value.

1. Edit the `coda.py` file in the path `app/`. Modify the following lines of code:

```py
class Coda(object):
  ...
  def list_sections(self, strDocId):
    result = self.objCoda.list_sections(strDocId)
    print ( result )

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
```

2. Edit the `pycoda.py` file in the path `app/`. Add the following lines of code:

```py
class Pycoda():
  ...
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
```
