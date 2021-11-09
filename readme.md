# LDCT - Location Data Cleaning Tool

## Written By Russell Abernethy

## Purpose

This tool is intended to take csv's of scraped location data and uses google maps to allow the user to 

### Requirements

* Chrome v95
* Python3

### Installing

NOTE: At any point during the install process, if you install something & it installs and then when you try to run the application it tells you that it was never installed, try restarting your computer.

Make sure that pip was installed when you installed python. You can check this by running the command below. If it is not installed, got to the [pip documentation](https://pip.pypa.io/en/stable/installation/) and follow the instructions for ensurepip / get-pip.py.

(Windows) Open up cmd and type:

``` cmd
C:\Users\tui\LDCT> py -m pip --version
```

(Mac & UNIX) Open up your prefered shell and type:

``` bash
> pip3 --version
```


Now that pip has been installed, all that's left is installing the required python modules:

(Windows) In cmd, type:

``` cmd
C:\Users\tui\LDCT> py -m pip install -r requirements.txt
```

(Mac & UNIX) Open up your prefered shell and type:

``` bash
> pip3 install -r requirements.txt
```

# Running:

On Windows, assuming everything has been installed correctly, you can either double click the clean.py script to start the application or you can enter the following in cmd:

(Windows)

``` cmd
C:\Users\tui\LDCT> py clean.py
```

(Mac & Unux)

``` bash
> python3 clean.py
```
