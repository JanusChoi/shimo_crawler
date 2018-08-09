## Crawler for shimo documents

### 1. Running Environment

  - Windows 7 Ultimate SP1
  - Windows PowerShell
  - Chrome V67
  - Python 3.6.0
  - Python Packages
    - selenium ( refer: https://www.seleniumhq.org/docs/index.jsp )
    - urllib
    - bs4

### 2. Purpose

For generating folders & documents indexing file, e.g.

FolderName1 https://shimo.im/folder/abcdef
  FileName1 https://shimo.im/docs/aabbcc
FolderName2 https://shimo.im/folder/cdefgh

### 3. Instructions

To run this source code, you need to:

1. Install python3.6 on your PC

  Download from https://www.python.org/downloads/release/python-360/
  Download webdriver for Chrome via http://chromedriver.chromium.org/downloads
  Set the webdriver path in **./crawler_new.py**:
  ```{python}
  self.browser = webdriver.Chrome('Your chromedriver Here')  #Add path to your Chromedriver
  ```

2. Install required packages
```{cmd}
pip install selenium
pip install bs4
```

3. Set parameters in ./crawler_main.py including:
  - shimo url info
  - username & password for log in
  - link those will be excluded
  - output file path

4. Run py file in PowerShell
```{cmd}
python ./crawler_main.py
```
