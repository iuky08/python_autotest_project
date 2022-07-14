# Python autotests

## Install virtual environment.

Make sure that Python interpeter already installed:

Run in command line:

```
whereis python
```

#### Install virtual environment.

Run in command line from root folder:

```
python-virtualenv
python pip
python -m .venv venv
pip install -r requirements.txt
```

#### Initial Allure results folder.

Run in command line from root folder, this script is running autotests from folder_with_test_scenarios:

```
pytest --alluredir=%allure_result_folder% ./%folder_with_test_scenarios%
```

#### Serve Allure Report results via HTML page.

Run in command line from root folder:

```
allure serve %allure_result_folder%
```

#### Generate Allure Report results via ZIP-file.

Run in command line from root folder:

```
allure generate %allure_result_folder%
```
