# clean.py - a tool for verifing location data

# Author: Russell Abernethy
# Date Created: 05/27/2021
# Date Last Modified: 10/28/2021

import sys, selenium, csv
import tkinter as tk
from scripts import pyperclip
from tkinter import filedialog
from selenium.webdriver.common.keys import Keys


start = False
driver,filename = None, None
in_data, out_data = [],[]
entries, progress = 0,0
searchbox = '//*[@id="searchboxinput"]'


def remove_non_ascii(s):
# Cleans output of non ascii characters.
    return "".join(c for c in s if ord(c)<128)


def open_csv(): 
# Opens file explorer to load csv file.
    global filename
# If there is no csv file loaded in, open the file explorer then open the initilize the driver.
    if filename is None:
        filename = filedialog.askopenfilename()
    if filename is not None:
        on_open()
    else:
        print('error opening csv, try again')


def on_open(): 
# Opens webbrowser and starts the cleaning tool.
    global start, driver, filename
    if not driver and not start:
        start = True
        load_input_csv(filename)
# Determine what system the user is using and use the apropriate webdriver.
        if sys.platform.startswith('linux'):
            driver = selenium.webdriver.Chrome('./ChromeDriver/linux/chromedriver')
        elif sys.platform.startswith('win32'):
            driver = selenium.webdriver.Chrome('./ChromeDriver/win32/chromedriver')
        elif sys.platform.startswith('darwin'):
            driver = selenium.webdriver.Chrome('./ChromeDriver/macos/chromedriver')
# Go to google maps and load in the first location to be verified.
        driver.get('https://www.google.com/maps/')
        next_loc()


def on_close(): 
# Closes the program. Only will occur if the webdriver had been created.
# If called before all of the entries have been verified, only one csv will be produced.
    global driver
    if driver:
        driver.close()
# Create output file. 
        produce_csv()


def loc_correct():
# Handles event where the location was correct.
    global out_data
    if geol.get() != '':
        data = out_data.pop()
# If the user entered a new business name or new address, change it for the final output.
        data[0] = data[0] if name_change.get(1.0,tk.END) == '\n' else name_change.get(1.0,tk.END).replace('\n','')
        data[1] = data[1] if adr_change.get(1.0,tk.END) == '\n' else adr_change.get(1.0,tk.END).replace('\n','')
        geo = geol.get().split(',')
        lon = geo.pop()
        data.append(geo.pop())
        data.append(lon)
        data.append("")
        out_data.append(data)
        geol.delete(0,len(geol.get()))
        next_loc()

    
def next_loc():
# Advances the browser to the next entry.
    global in_data, out_data, driver, searchbox, entries, progress
    progress += 1
# Change What is displayed in the progress-bar portion of the GUI
    pbar.delete(1.0,'end')
    pbar.insert(3.0,'Progress : {progress}/{entries}'.format(progress=progress,entries=entries))
    adr_change.delete(1.0,'end')
    name_change.delete(1.0,'end')
# If there are more locations to check, do so.
    try:                                                                        
        new_loc = in_data.pop()
        out_data.append(new_loc)
# No more entires to verify, create output csv files
    except IndexError:
        produce_csv()
# Clear the search box if it can be found, otherwise just 
    try:
        driver.find_element_by_xpath(searchbox).clear()
    except tk.ElementNotInteractableException:
        driver.get('https://www.google.com/maps/')
# Advance to the next entry to be cleaned and update the progress bar in the gui.
    driver.find_element_by_xpath(searchbox).send_keys( remove_non_ascii(new_loc[1]) + Keys.ENTER)
    pbar.insert(1.0,remove_non_ascii(new_loc[0]) + " " + remove_non_ascii(new_loc[1]) + "\n" + remove_non_ascii(new_loc[2]) + " " + remove_non_ascii(new_loc[3])+ "\n")
    

def produce_csv(): 
# Produces the output csv
    global out_data, driver
    counter = 0
    with open(filename[:-4]+'(2).csv','w',newline='') as outcsv:               
        headers = ['Business Name', 'Full Address', 'Latitude', 'Longitude', 'NewLatitude', 'NewLongitude', 'Notes']
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
# Create final csv with only confirmed locations included.
    with open(filename[:-4]+'(2).csv','r',newline='') as csv2:
        reader = csv.DictReader(csv2)
        with open(filename[:-4]+'(3).csv','w',newline='') as csv3:
            headers=["Business Name", "Full Address", "Latitude", "Longitude"]
            writer = csv.DictWriter(csv3,fieldnames=headers)
            writer.writeheader()
            for row in reader:
                if row['NewLatitude'] != '':
                    counter+=1
                    writer.writerow({'Business Name': row['Business Name'].replace('"',""), 'Full Address': row['Full Address'].replace('"',""), 'Latitude': row['NewLatitude'].replace('"',""), 'Longitude': row['NewLongitude'].replace('"',"")})
    driver.close()
    print("Cleaned from: {start} --> {end}".format(start = entries, end = counter))
    exit()

def load_input_csv(filename): 
# Reads in csv and places data into a list.
    global in_data, progress, entries
    with open(filename,'r',newline='\n',encoding='utf8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            entries += 1
            in_data.append([remove_non_ascii(row['Business Name']),remove_non_ascii(row['Full Address']),remove_non_ascii(row['Latitude']),remove_non_ascii(row['Longitude'])])

def wrong_category(): 
# Handles the event where location is not in the right category.
    global out_data
    if geol.get() == '':
        temp = out_data.pop()
        # Latitude and Longitude left blank for sorting later!
        temp.append("")
        temp.append("")
        temp.append("{notes}".format(notes='Does_not_fall_within_search_category'))
        out_data.append(temp)
        next_loc()                                          


def paste():
# Button for pasting from the clipboard.
    if pyperclip.paste() != '':
        geol.insert(0,pyperclip.paste())


# Widget Creation
root  = tk.Tk()                                                                 # Create the widget box.
root.title('slfLocate Data Cleaning Tool')
top=tk.Frame(root)
top.pack()

e = tk.Button(top, text='Open csv file', command=open_csv)                      # Open csv button.
e.pack(side=tk.LEFT)

b = tk.Button(top, text='Quit', command=on_close)                               # Quit button.
b.pack(side=tk.LEFT)

b = tk.Button(root, text='Does Not Fall Into Category', command=wrong_category, bg = 'red') 
b.pack()                                                                        # Not in category button.

b = tk.Button(root, text = 'Location is at: ', bg='green',command=loc_correct)  # Correct button.
b.pack()

search = tk.Frame(root)                                                         # Search Window Frame
search.pack()

geol = tk.Entry(search)                                                         # Text entry for geo cords.
geol.pack(side=tk.LEFT)

p = tk.Button(search, text='Paste',command=paste)                               # Paste Button
p.pack(side=tk.LEFT)

change_header = tk.Frame(root)                                                  # Change Window Frame
change_header.pack()

adr_text = tk.Text(change_header,height=1)                                      # Address Change Text
adr_text.insert(tk.INSERT,"Change Address:")
adr_text.pack(side=tk.RIGHT)

name_text = tk.Text(change_header,height=1)                                     # Business Name Change Text
name_text.insert(tk.INSERT,"Change Business Name:")
name_text.pack(side=tk.LEFT)

change = tk.Frame(root)                                                         # Change Input Window Frame
change.pack()

adr_change = tk.Text(change,height=3)                                           # Address Change Input
adr_change.pack(side=tk.RIGHT)

name_change = tk.Text(change,height=3)                                          # Business Name Change Input
name_change.pack(side=tk.LEFT)

pbar = tk.Text(root)                                                            # Progress bar text.
pbar.pack()

root.mainloop()
