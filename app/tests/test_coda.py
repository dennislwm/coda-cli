from coda import clickMain
from click.testing import CliRunner

def test_version():
  runner = CliRunner()
  result = runner.invoke(clickMain)
  assert result.exit_code == 0
  assert "v" in result.output 

def test_list_docs():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-docs'])
  assert result.exit_code == 0
  assert "id" in result.output 

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                M A I N   P R O C E D U R E                               |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
def main():
  test_version()
  test_list_docs()

if __name__ == "__main__":
  main()