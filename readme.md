# slfClean.py
![dashexample](/img/screen3.png)
## Requirements and How to install:

### Installing Git:
Git is a version manager for code development. It is also a useful tool for distributing the latest version of a project. Follow the instructions for your specific system to install.

#### **MacOS:**
Homebrew is a tool used to install pacakages on your computer, install it to install git.
Open up terminal and enter:
```shell
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then use Homebrew to install git
```shell
$ brew install git
```

#### **Linux**
```shell
$ apt-get install git
```

#### **Windows**
Go to the Git [download](https://git-scm.com/download/win) page and download for your version of windows.

### Installing Firefox:
If you don't already, please go to the [download](https://www.mozilla.org/en-US/firefox/new/) page for Firefox and install the latest version of the browser.

### Installing Python:
Go to the [download](https://www.python.org/downloads/) page for python and follow the install instructions for your system

### Installing Pip:
Pip is a tool for downloading code packages that normally comes preinstalled with most python distributions. If for some reason your version did not come with it already, you'll have to install it as we need a package or 2 for this program to work.

#### **MacOS & Linux**
```shell
$ python3 -m ensurepip --upgrade
```

#### **Windows**
Open up the cmd promt and enter:
```powershell
C:> py -m ensurepip --upgrade
```

### Installing Dependences:
First, you need to download the entire project from github. This can be done by entering the following in terminal:
```shell
$ git clone https://github.com/rabernethy/slfLocateCleaningTool.git
```
Then navigate to that folder and open a terminal there and download the dependencies by running the following command:
```shell
$ cd slfLocateCleaningTool/
$ pip3 install -r requirements.txt
```

### Installing GeckoDriver:
#### Windows 
To be able to interact with a web browser, we need to download an extra driver. Go to the geckodriver [download](https://github.com/mozilla/geckodriver/releases) page and download the correct version for your system. Once you've downloaded the zipfile, unzip it and copy the .exe file into your python parent directory (e.g. C:\\Python39). The best way I've found to get here is to open file explorer and search for Python39 in your C drive and wait until it finds it.
#### **MacOS**
To be able to interact with a web browser, we need to download an extra driver. Go to the geckodriver [download](https://github.com/mozilla/geckodriver/releases) page and download the correct version for your system. Once you've downloaded the zipfile, unzip it and place the exe somewhere (Downloads is perfectly fine). Now open up terminal and run sudo nano /etc/paths and enter your password. Go to the bottom of this file and type in the path of the exe file (an easy way to get this is to go to finder, make sure the exe is highlighted, then hit option+command+c and the path of the exe will now be copied to your clipboard). Now close nano by pressing control+x, y to save, and return to confirm.

## How to run:
#### **MacOS & Linux**
Open terminal at the slfLocateCleaningTool folder(right click and select New Terminal at Folder) and enter
``` shell
$ python3 slfClean.py
```

#### **Windows**
Double click on the slfClean file to run.

## Downloading Updates:
The plan is to keep this program is to add requested features. This means that new versions of the code will be pushed out that you should download. How this is done is using git. To downoald updates, run:
```shell
$ git fetch https://github.com/rabernethy/slfLocateCleaningTool.git
```
I would suggest doing this every week until changes are finished being made.