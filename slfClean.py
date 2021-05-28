""" 
    slfClean.py 
    Author: Russell Abernethy
    Date: 05/27/2021
"""

"""
PROGRAM DESCRIPTION:
    This program takes in a csv file that contains location information about a
    certin type of business and helps the user process out undesired entries.
    Once all of the entries have been processed, the program will output 2 csvs:    
    one will be a csv with a few additional columns (newLat, newLong, changes, 
    errors, & notes). The other outputed csv will have the same headers as the 
    inputed csv, the difference is that it has all of the invalid rows removed
    and all of the latitudes and longitudes with corrections have been adjusted.

"""

"""
usage: 
    
    python3 slfClean.py 'name of csv you want to clean'
"""


import sys
import tkinter as tk
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
import csv


in_data = []
out_data = []
driver = None
seachbox = '//*[@id="searchboxinput"]'
filename = sys.argv[1]


def on_open(): # starts cleaner

    global driver

    if not driver:
        driver = selenium.webdriver.Firefox()
        driver.get('https://www.google.com/maps/')
        next_loc()


def on_close(): #closes program

    global driver

    if driver:
        driver.close()
        driver = None

        produce_csv()
        quit()


def loc_correct(): # correct location button logic

    global out_data

    if geol.get() != '': # user entered new cords.
        temp = out_data.pop()
        geo = geol.get().split(',')
        lon = geo.pop()
        temp.append(geo.pop())
        temp.append(lon)
        temp.append("")
        out_data.append(temp)
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
    
    headers = ['Business Name', 'Full Address', 'Latitude', 'Longitude', 'NewLatitude', 'NewLongitude', 'Notes']
    global out_data

    # Create csv that contains all the entires and any additions made during anlysis.
    with open(filename[:-4]+'(2).csv','w',newline='') as outcsv:
        writer = csv.DictWriter(outcsv,fieldnames=headers)
        writer.writeheader()
        for data in out_data:
            note = data.pop()
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
    rowc = 0

    with open(filename,'r',newline='\n') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if rowc == 0: #skip the header
                rowc = 1
                continue
            in_data.append([row['Business Name'],row['Full Address'], row['Latitude'],row['Longitude']])


def wrongCategory(): # marks entry as wrong category
    
    global out_data

    temp = out_data.pop()
    #no lat or long
    temp.append("")
    temp.append("")
    #add note for why not included
    temp.append("{notes}".format(notes='Does_not_fall_within_search_category'))
    out_data.append(temp)
    next_loc()

# Load in all the entires from the input csv
load_input_csv(filename)
# Create the widget box
root  = tk.Tk()
# Website to go to
e = tk.Entry(root)
e.pack()
e.insert('end', 'https://www.google.com/maps/')
# Start Button
b = tk.Button(root, text='Start', command=on_open)
b.pack()
# Quit Button
b = tk.Button(root, text='Quit', command=on_close)
b.pack()
# Correct / correct w/ adjustments button
b = tk.Button(root, text = 'Location is at: ', command=loc_correct)
b.pack()
# Text entry for geo cords
geol = tk.Entry(root)
geol.pack()
# not in category
b = tk.Button(root, text='Does Not Fall Into Category.', command=wrongCategory)
b.pack()

root.mainloop()
