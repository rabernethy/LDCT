# slfClean.py 
# Author: Russell Abernethy
# Date: 05/27/2021

import pyperclip, sys, selenium, csv
import tkinter as tk
from tkinter import filedialog
from selenium.webdriver.common.keys import Keys


start = False
driver,filename = None, None
in_data, out_data = [],[]
entries, progress = 0,0
searchbox = '//*[@id="searchboxinput"]'


def remove_non_ascii(s):
    return "".join(c for c in s if ord(c)<128)


def open_csv(): 
# Opens file explorer to load csv file.
    global filename
    if filename is None:
        filename = filedialog.askopenfilename()                                 # Open file explorer.
    if filename is not None:                                                    # If a file was selected start open it and 
        on_open()                                                               # the browser.
    else:                                                                       # Otherwise print an error to screen.
        print('error opening csv, try again')


def on_open(): 
# Opens webbrowser and starts the cleaning tool.
    global start, driver, filename
    if not driver and not start:
        start = True
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
        data[0] = data[0] if name_change.get(1.0,tk.END) == '\n' else name_change.get(1.0,tk.END).replace('\n','')
        data[1] = data[1] if adr_change.get(1.0,tk.END) == '\n' else adr_change.get(1.0,tk.END).replace('\n','')
    
        geo = geol.get().split(',')                                             # ░▄▄▄▄░
        lon = geo.pop()                                                         # ▀▀▄██►
        data.append(geo.pop())                                                  # ▀▀███►
        data.append(lon)                                                        # ░▀███►░█►
        data.append("")                                                         # ▒▄████▀▀
        print(data)
        out_data.append(data)                                                   # This is Frank the dino, he likes hot sause and doing
        geol.delete(0,len(geol.get()))
        next_loc()                                                              # crossword puzzles in red ink (he's crazy!)

    
def next_loc():
# Advances the browser to the next entry.
    global in_data, out_data, driver, searchbox, entries, progress
    progress += 1
    pbar.delete(1.0,'end')
    pbar.insert(3.0,'Progress : {progress}/{entries}'.format(progress=progress,entries=entries))
    adr_change.delete(1.0,'end')
    name_change.delete(1.0,'end')
    try:                                                                        # If there are more locations to check, do so.
        new_loc = in_data.pop()
        out_data.append(new_loc) 
    except IndexError:                                                          # No more places to check, wrap up the program.
        produce_csv()                                                           # Create 2 csvs.
        on_close()                                                              # Call in the cleanup team.
    
    try:                                                                        # If the search box cannot be clicked, go back to a place where there is.
        driver.find_element_by_xpath(searchbox).clear()                         # Clear seachbox and go to next place to check.
    except tk.ElementNotInteractableException:
        driver.get('https://www.google.com/maps/')
    driver.find_element_by_xpath(searchbox).send_keys( remove_non_ascii(new_loc[1]) + Keys.ENTER)
    pbar.insert(1.0,remove_non_ascii(new_loc[0]) + " " + remove_non_ascii(new_loc[1]) + "\n" + remove_non_ascii(new_loc[2]) + " " + remove_non_ascii(new_loc[3])+ "\n")
    

def produce_csv(): 
# Produces the output csv
    global out_data, driver
    counter = 0
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
                    counter+=1
                    writer.writerow({'Business Name': row['Business Name'], 'Full Address': row['Full Address'], 'Latitude': row['NewLatitude'], 'Longitude': row['NewLongitude']})
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
        temp.append("")                                                          # No lat or long included since we don't really care
        temp.append("")                                                          # if it's there or not.
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

b = tk.Button(root, text='Does Not Fall Into Category.', command=wrong_category, bg = 'red') 
b.pack()                                                                        # Not in category button.

b = tk.Button(root, text = 'Location is at: ', bg='green',command=loc_correct)  # Correct button.
b.pack()

search = tk.Frame(root)
search.pack()

geol = tk.Entry(search)                                                         # Text entry for geo cords.
geol.pack(side=tk.LEFT)

p = tk.Button(search, text='Paste',command=paste)
p.pack(side=tk.LEFT)

change_header = tk.Frame(root)
change_header.pack()

adr_text = tk.Text(change_header,height=1)
adr_text.insert(tk.INSERT,"Change Address:")
adr_text.pack(side=tk.RIGHT)

name_text = tk.Text(change_header,height=1)
name_text.insert(tk.INSERT,"Change Business Name:")
name_text.pack(side=tk.LEFT)

change = tk.Frame(root)
change.pack()

adr_change = tk.Text(change,height=3)
adr_change.pack(side=tk.RIGHT)

name_change = tk.Text(change,height=3)
name_change.pack(side=tk.LEFT)

pbar = tk.Text(root)                                                            # Progress bar text.
pbar.pack()

root.mainloop()
