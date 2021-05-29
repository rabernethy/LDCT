# slfClean.py
![dashexample](/img/pic2.png)
## Requirements and How to install:

### Installing Git:
Git is a version manager for code development. It is also a useful tool for distributing the latest version of a project. Follow the instructions for your specific system to install.

#### MacOS:
Homebrew is a tool used to install pacakages on your computer, install it to install git.
```shell
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then use Homebrew to install git
```shell
$ brew install git
```

#### Linux
```shell
$ apt-get install git
```

#### Windows
Go to the Git [download](https://git-scm.com/download/win) page and download for your version of windows.

### Installing Firefox:
If you don't already, please go to the [download](https://www.mozilla.org/en-US/firefox/new/) page for Firefox and install the latest version of the browser.

### Installing Python:
Go to the [download](https://www.python.org/downloads/) page for python and follow the install instructions for your system

### Installing Pip:
Pip is a tool for downloading code packages that normally comes preinstalled with most python distributions. If for some reason your version did not come with it already, you'll have to install it as we need a package or 2 for this program to work.

#### MacOS & Linux
```shell
$ python -m ensurepip --upgrade
```

#### Windows
```powershell
C:> py -m ensurepip --upgrade
```

### Installing Dependences:
This project requries external libraries that do not come preinstalled with python. Included in this repository is a requirements.txt file that will help install the required packages. To simplify things, it is recommended to use a virtual enviroment. In a terminal, please run the following(they work on all systems):
```shell
$ virtualenv --no-site-packages venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Installing GeckoDriver:
#### Windows 
To be able to interact with a web browser, we need to download an extra driver. Go to the geckodriver [download](https://github.com/mozilla/geckodriver/releases) page and download the correct version for your system. Once you've downloaded the zipfile, unzip it and copy the .exe file into your python parent directory (e.g. C:\\Python34)
#### MacOS
To be able to interact with a web browser, we need to download an extra driver. Go to the geckodriver [download](https://github.com/mozilla/geckodriver/releases) page and download the correct version for your system. Once you've downloaded the zipfile, unzip it and place the exe somewhere (Downloads is perfectly fine). Now open up terminal and run sudo nano /etc/paths and enter your password. Go to the bottom of this file and type in the path of the exe file (an easy way to get this is to go to finder, make sure the exe is highlighted, then hit option+command+c and the path of the exe will now be copied to your clipboard). Now close nano by pressing control+x, y to save, and return to confirm.

## How to run:
To run the program, the csv you want to clean needs to be in the slfLocateCleaningTool folder. Once you have it in the right place, you can start the program with:

#### MacOS & Linux
```shell
$ python slfClean.py
```

#### Windows
```powershell
C:> py slfClean.py
```

