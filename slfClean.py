# slfClean.py 
# Author: Russell Abernethy
# Date: 05/27/2021


import sys
import tkinter as tk
from tkinter import filedialog
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
import csv
import subprocess

in_data = []
out_data = []
driver = None
seachbox = '//*[@id="searchboxinput"]'
filename = ''

def open_csv(): # opens file explorer to load csv

    global filename

    filename = filedialog.askopenfilename()     # open file explorer
    if filename != '':                          # 
        on_open()
    else:
        print('error opening csv')


def on_open(): # starts cleaner

    global driver
    global filename

    if not driver:
        load_input_csv(filename)                    # load in all the entires from the input csv
        driver = selenium.webdriver.Firefox()       # start webbrowser
        driver.get('https://www.google.com/maps/')  # go to google maps
        next_loc()                                  # load in the first location


def on_close(): #closes program

    global driver

    if driver:
        driver.close()  # close the webbrowser
        produce_csv()   # create csv output files
        quit()          # quit the program


def loc_correct(): # correct location button logic

    global out_data

    if geol.get() != '':                # user entered new cords.
        data = out_data.pop()
        geo = geol.get().split(',')
        lon = geo.pop()
        data.append(geo.pop())
        data.append(lon)
        data.append("")
        out_data.append(data)
        next_loc()

    
def next_loc(): # advances the browser to the next entry.
    
    global in_data
    global out_data
    global driver
    global seachbox

    try: # if there are more locations to check, do so.
        new_loc = in_data.pop()
        out_data.append(new_loc)

    except IndexError: # no more places to check, wrap up the program
        produce_csv()
        on_close()

    # clear seachbox and go to next place to check.
    driver.find_element_by_xpath(seachbox).clear()
    driver.find_element_by_xpath(seachbox).send_keys(str(new_loc) + Keys.ENTER)
    

def produce_csv(): # produces the output csv
    
    global out_data

    # Create csv that contains all the entires and any additions made during anlysis.
    with open(filename[:-4]+'(2).csv','w',newline='') as outcsv:
        headers = ['Business Name', 'Full Address', 'Latitude', 'Longitude', 'NewLatitude', 'NewLongitude', 'Notes']
        writer = csv.DictWriter(outcsv,fieldnames=headers)
        writer.writeheader()
        for data in out_data:   # retrive data from out_data and 
            note = data.pop()   # prepare for csv format
            nlon = data.pop()
            nlat = data.pop()
            lon = data.pop()
            lat = data.pop()
            fulladr = data.pop()
            bisname = data.pop()
            writer.writerow({'Business Name':bisname, 'Full Address': fulladr, 'Latitude':lon, 'Longitude':lat, 'NewLatitude': nlat, 'NewLongitude': nlon, 'Notes': note})

    # Create final csv that only has valid locations included.
    with open(filename[:-4]+'(2).csv','r',newline='') as csv2:
        reader = csv.DictReader(csv2)
        with open(filename[:-4]+'(3).csv','w',newline='') as csv3:
            headers=["Business Name", "Full Address", "Latitude", "Longitude"]
            writer = csv.DictWriter(csv3,fieldnames=headers)
            writer.writeheader()
            for row in reader:
                if row['NewLatitude'] != '':
                    writer.writerow({'Business Name': row['Business Name'], 'Full Address': row['Full Address'], 'Latitude': row['NewLatitude'], 'Longitude': row['NewLongitude']})


def load_input_csv(filename): # reads in csv and places data into a list
    
    global in_data

    with open(filename,'r',newline='\n') as f:
        reader = csv.DictReader(f)
        rowc = 0
        for row in reader:
            if rowc == 0: #skip the header
                rowc = 1
                continue
            in_data.append([row['Business Name'],row['Full Address'], row['Latitude'],row['Longitude']])


def wrongCategory(): # marks entry as wrong category
    
    global out_data

    temp = out_data.pop()
    temp.append("")         #no lat or long
    temp.append("")
    temp.append("{notes}".format(notes='Does_not_fall_within_search_category'))
    out_data.append(temp)
    next_loc()


root  = tk.Tk()                                                                 # Create the widget box
root.title('slfLocate Data Cleaning Tool')
e = tk.Button(root, text='Open csv file', command=open_csv)                     # Open csv button
e.pack()
b = tk.Button(root, text='Quit', command=on_close)                              # Quit Button
b.pack()
b = tk.Button(root, text='Does Not Fall Into Category.', command=wrongCategory) # not in category
b.pack()
b = tk.Button(root, text = 'Location is at: ', command=loc_correct)             # Correct / correct w/ adjustments button
b.pack()
geol = tk.Entry(root)                                                           # Text entry for geo cords
geol.pack()
root.mainloop()
