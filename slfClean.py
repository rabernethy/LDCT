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
entries = 0
progress = 0

def open_csv(): 
# Opens file explorer to load csv file.
    global filename
    filename = filedialog.askopenfilename()                                     # Open file explorer.
    if filename != '':                                                          # If a file was selected start open it and 
        on_open()                                                               # the browser.
    else:                                                                       # Otherwise print an error to screen.
        print('error opening csv, try again')


def on_open(): 
# Opens webbrowser and starts the cleaning tool.
    global driver
    global filename
    if not driver:
        load_input_csv(filename)                                                # Load in all the entires from the input csv.
        driver = selenium.webdriver.Firefox()                                   # Start the webbrowser.
        driver.get('https://www.google.com/maps/')                              # Go to google maps.
        next_loc()                                                              # Load in the first location.


def on_close(): 
# Closes the program.
    global driver
    if driver:                                                                  # If the program has already started to run:
        driver.close()                                                          # Close the webbrowser.
        produce_csv()                                                           # Create csv output files.



def loc_correct():
# Handles event where the location was correct.
    global out_data
    if geol.get() != '':                                                        # User entered new cords. Save it and go to next location.
        data = out_data.pop()                                                   # No need to explain this code so I'll put ASCII here.
        geo = geol.get().split(',')                                             # ░▄▄▄▄░
        lon = geo.pop()                                                         # ▀▀▄██►
        data.append(geo.pop())                                                  # ▀▀███►
        data.append(lon)                                                        # ░▀███►░█►
        data.append("")                                                         # ▒▄████▀▀
        out_data.append(data)                                                   # This is Frank the dino, he likes hot sause and doing
        geol.delete(0,len(geol.get()))
        next_loc()                                                              # crossword puzzles in red ink (he's crazy!)

    
def next_loc():
# Advances the browser to the next entry.
    global in_data
    global out_data
    global driver
    global seachbox
    global entries
    global progress
    progress += 1
    pbar.delete(1.0,'end')

    pbar.insert(3.0,'Progress : {progress}/{entries}'.format(progress=progress,entries=entries))
    try:                                                                        # If there are more locations to check, do so.
        new_loc = in_data.pop()
        out_data.append(new_loc)
    except IndexError:                                                          # No more places to check, wrap up the program.
        produce_csv()                                                           # Create 2 csvs.
        on_close()                                                              # Call in the cleanup team.
    driver.find_element_by_xpath(seachbox).clear()                              # Clear seachbox and go to next place to check.
    driver.find_element_by_xpath(seachbox).send_keys( new_loc[1] + Keys.ENTER)
    pbar.insert(1.0,new_loc[0] + " " + new_loc[1] + "\n" + new_loc[2] + " " + new_loc[3]+ "\n")
    

def produce_csv(): 
# Produces the output csv
    global out_data
    global driver
    with open(filename[:-4]+'(2).csv','w',newline='') as outcsv:                # Creates detailed report csv. Boring Code.
        headers = ['Business Name', 'Full Address', 'Latitude', 'Longitude', 'NewLatitude', 'NewLongitude', 'Notes']
        writer = csv.DictWriter(outcsv,fieldnames=headers)                      # ──────▄▀▄─────▄▀▄         - Jerry the -
        writer.writeheader()                                                    # ─────▄█░░▀▀▀▀▀░░█▄        watchful cat!
        for data in out_data:                                                   # ─▄▄──█░░░░░░░░░░░█──▄▄
            note = data.pop()                                                   # █▄▄█─█░░▀░░┬░░▀░░█─█▄▄█
            nlon = data.pop()                                                   
            nlat = data.pop()                                                   # ───▄██▄─██▄───▄           - Joe Camel -                                             
            lon = data.pop()                                                    # ─▄██████████▄███▄
            lat = data.pop()                                                    # ─▌████████████▌
            fulladr = data.pop()                                                # ▐▐█░█▌░▀████▀░░
            bisname = data.pop()                                                # ░▐▄▐▄░░░▐▄▐▄░░░░
            writer.writerow({'Business Name':bisname, 'Full Address': fulladr, 'Latitude':lon, 'Longitude':lat, 'NewLatitude': nlat, 'NewLongitude': nlon, 'Notes': note})
    with open(filename[:-4]+'(2).csv','r',newline='') as csv2:                  # Create final csv that only has valid 
        reader = csv.DictReader(csv2)                                           # locations included.
        with open(filename[:-4]+'(3).csv','w',newline='') as csv3:
            headers=["Business Name", "Full Address", "Latitude", "Longitude"]
            writer = csv.DictWriter(csv3,fieldnames=headers)
            writer.writeheader()
            for row in reader:
                if row['NewLatitude'] != '':
                    writer.writerow({'Business Name': row['Business Name'], 'Full Address': row['Full Address'], 'Latitude': row['NewLatitude'], 'Longitude': row['NewLongitude']})
    driver.close()
    exit()

def load_input_csv(filename): 
# Reads in csv and places data into a list.
    global in_data
    global progress
    global entries
    with open(filename,'r',newline='\n') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if entries == 0:                                                       # Skip the header, but read in everyother row to
                entries += 1                                                       # memory so that it can be processed.
                continue
            entries += 1
            in_data.append([row['Business Name'],row['Full Address'], row['Latitude'],row['Longitude']])

def wrong_category(): 
# Handles the event where location is not in the right category.
    global out_data
    if geol.get() == '':
        temp = out_data.pop()
        temp.append("")                                                             # No lat or long included since we don't really care
        temp.append("")                                                             # if it's there or not.
        temp.append("{notes}".format(notes='Does_not_fall_within_search_category'))
        out_data.append(temp)
        next_loc()                                          


root  = tk.Tk()                                                                 # Create the widget box.
root.title('slfLocate Data Cleaning Tool')
e = tk.Button(root, text='Open csv file', command=open_csv)                     # Open csv button.
e.pack()
b = tk.Button(root, text='Quit', command=on_close)                              # Quit button.
b.pack()
b = tk.Button(root, text='Does Not Fall Into Category.', command=wrong_category, bg = 'red') 
b.pack()                                                                        # Not in category button.
b = tk.Button(root, text = 'Location is at: ', bg='green',command=loc_correct)  # Correct button.
b.pack()
geol = tk.Entry(root)                                                           # Text entry for geo cords.
geol.pack()
pbar = tk.Text(root)                                                            # Progress bar text.
pbar.pack()
root.mainloop()
