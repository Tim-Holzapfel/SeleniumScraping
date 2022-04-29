# SeleniumScraping

[![Python package](https://github.com/Tim-Lukas-H/SeleniumScraping/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/Tim-Lukas-H/SeleniumScraping/actions/workflows/python-package.yml) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Build Status](https://app.travis-ci.com/Tim-Lukas-H/SeleniumScraping.svg?token=u7sfyunhV25PXdqaPt8C&branch=main)](https://app.travis-ci.com/Tim-Lukas-H/SeleniumScraping)

## Table of Contents

- [SeleniumScraping](#seleniumscraping)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Modules](#modules)
    - [Profile](#profile)
    - [Webdriver](#webdriver)
    - [Account](#account)
    - [Webscraping](#webscraping)
    - [Concatenation](#concatenation)

## Requirements

<a name="requirements">
</a>

The software listed below is necessary to run SeleniumScraper. SeleniumScraper was tested with the versions specified but should also work with more recent versions.

* [Tor Browser 10.5.4](https://www.torproject.org/download/)
* [Firefox 90.0.2](https://www.mozilla.org/en-US/firefox/new/)
* [Python 3.7.9](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64-webinstall.exe)
* [pip](src/SeleniumScraping/utils/get-pip.py)

Note: TheThis step assumes that python is installed and on the system path. To check whether pyhton is on the system path you can open a command prompt (Windows key + cmd) and type `where python` . If python is on the system path the command should return the python directory path.

## Installation

<a name="installation">
</a>

The compressed package can be downloaded from here [here](https://github.com/Tim-Lukas-H/SeleniumScraping/releases/latest). To install the package you first need to open a command prompt or powershell in the folder where the package was downloaded to. This can be achieved by typing `cmd` in the address bar of the folder containing the package. The address bar of a folder can be focused by pressing `CTRL+L` while the folder is open.

The package can be installed by typing following command in the command prompt described previously:

```cmd
python -m pip install SeleniumScraping-1.0.0.tar.gz
```

Should the package manager *pip* currently not be installed on your system then you can install it by simply downloading the file [get-pip.py](https://github.com/Tim-Lukas-H/SeleniumScraping/blob/afd5ffe635d78ac1616f30fef0f0736762dedbb2/SeleniumScraping/utils/get-pip.py). After having downloaded it, you can simply open a command prompt in the folder where you have downloaded the file and executing the following code:

```cmd
python get-pip.py
```

[This guide](https://pip.pypa.io/en/stable/installation/) talks in greater detail about *pip* and its installation.

## Usage

<a name="usage">
</a>

The following section describes how to use the package.

### Modules

<a name="modules">
</a>

First the necessary modules need to be loaded:

```python
from SeleniumScraping import start_scraping, generate_account
```

### Profile

<a name="profile">
</a>

The Firefox profile is being generated implicitly by the modules `start_scraping` and `generate_account` .

```Python
profile = get_profile(blank_profile=False)
```

### Webdriver

<a name="webdriver">
</a>

Next the remote webdriver or driver in short needs to be generated. The driver can be generated by using `generate_tor(profile=profile, headless_mode=False)` . The first argument `profile` is simply the Firefox profile from before. The second argument `headless` determines whether the driver has a graphical user interface (GUI).

```Python
driver = generate_tor(profile=profile, headless_mode=False)
```

### Account

<a name="account">
</a>

For the scraping, we need to create an account that can be used to log into familysearch.org. For that we are going to need a "spoof" phone number. A website where such a number can be obtained is for example: https://quackr.io/temporary-numbers.

An account can be created by using the following code, but first the arguments `phone_number` and `country` need to be replaced.

```Python
generate_account(driver=driver, phone_number="123456789", country_name="Country")
```

The `generate_account` function will create a text file on the User desktop containing all relevant information about the newly created account like password and username.

### Webscraping

<a name="webscraping">
</a>

Now that the account has been created the data collection can begin! The data collection can be initiliazed for example for Mexico by using the following code:

```Python
start_scraping(driver=driver, death_like_place="Mexico")
```

The function will create an excel sheet for each search page. The function will stop once it has reached the last available page.

### Concatenation

<a name="concatenation">
</a>

Finally, the individual pages can be concatenated into one single Excel-sheet by using the following function:

```Python
append_excel(excel_file_name="filename.xlsx")
```
