####----Dependencies---####

#tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

#custom

from supporting_scripts.device import device_info
from supporting_scripts.delimit_csv import extract_ids

#common
import pandas as pd
import time
import math

#####----Setting root page layout----#####
root = Tk()
root.title('Device App')
root.iconbitmap('images/cognosos.ico')
root.geometry("400x300")


################----Login Window----######################

def submit_login():

    import requests
    from requests.auth import HTTPBasicAuth

    global username 
    global password

    username = user_entry.get()
    password = pw_entry.get()

    api_response = requests.get("https://api.cognosos.net/device/findByDeviceID?device_id=" + str(200123), auth=HTTPBasicAuth(username, password))
    
    if api_response.status_code == 200:
        success_lbl = Label(top, text="Success!").grid(row=5, column=0, padx=100, columnspan=2)
        top.update_idletasks()
        time.sleep(1)
        top.destroy()

    else:
        error_lbl = Label(top, text='Incorrect Login').grid(row=5, column=0, columnspan=2)
        pw_entry.delete(0, END)


## Login page
top = Toplevel()
top.iconbitmap('images/lock.ico')
top.title('Login')

user_lbl = Label(top, text="username")
user_lbl.grid(row=0,column=0)
user_entry = Entry(top, width=20, borderwidth=5)
user_entry.grid(row=1,column=0)
user_entry.insert(0, 'device_user')

pw_lbl = Label(top, text="password")
pw_lbl.grid(row=0,column=1)
pw_entry = Entry(top, show="*", width=20, borderwidth=5)
pw_entry.grid(row=1,column=1)

submit_button = Button(top, padx=107, text="SUBMIT", command=submit_login).grid(row=4, column=0, columnspan=2)



#############-------Inputs------################

#Manual Entry Section
label_1 = Label(root, text="Enter Device IDs (separated by commas):")
label_1.grid(row=0, column=0)

e_1 = Entry(root, width=20, borderwidth=5)
e_1.grid(row=1,column=0, padx=10, pady=10)

label_2 = Label(root, text="Choose CSV File:")
label_2.grid(row=0,column=1)

#Automated Entry w/ File Selection
def pickfile():

    #clear contents
    e_1.delete(0, END)

    #choose file dialog box
    root.filename = filedialog.askopenfilename(initialdir="C:/Desktop", title="Select a File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    
    label_2 = Label(root, text="File submitted")
    label_2.grid(row=1,column=1)

    my_ids = extract_ids(root.filename)
    
    message = ""
    for item in my_ids[:-1]: 
        message = message + str(item) + ", "
    
    message = message + str(my_ids[-1])

    e_1.insert(0, message)

browse_button = Button(root, padx=50, pady=10, text="Browse", command=pickfile)
browse_button.grid(row=2, column=1)




########-----Outputs-----######

#What happens when "Get Info" is clicked
def get_device_info():

    #initialize progress bar
    progress_bar['value'] = 0

    #delimit entry by commas
    my_dev = e_1.get()
    dev_list = my_dev.split(", ")

    #columns in output csv
    devices = []
    status = []
    customer = []
    application = []
    GPS_time = []

    #initialize loop and time
    t0 = time.time()
    count = 0

    #pull info for each column
    for device in dev_list: 
        
        #using login info from login page
        my_info = device_info(device, username, password)

        devices.append(my_info[0])
        status.append(my_info[1])
        customer.append(my_info[2])
        application.append(my_info[3])
        GPS_time.append(my_info[4])

        #create output message
        message = "Device: " + str(my_info[0]) + " | Status: " + str(my_info[1]) + " | Customer: " + str(my_info[2]) + " | Application: " + str(my_info[3]) + " | GPS Time: " + str(my_info[4]) 

        #print to terminal
        print(message)

        #update progress bar
        progress_bar['value'] += 100*(1/(len(dev_list)))
        
        ###--Time Remaining--###
        #find average time elapsed per device so far
        count += 1
        t1 = time.time()
        time_passed = t1-t0
        per_device = time_passed/count

        #use this to extrapolate time remaining
        remaining_devices = len(dev_list)-count
        time_left = round(remaining_devices*per_device,0)

        #Create output message
        message = "Time remaining: " + str(math.floor(time_left/60)) + " minutes" + " " + str(time_left%60) + " seconds"
        label_5 = Label(root, text=message)
        label_5.grid_remove()
        label_5.grid(row=7, column=0, columnspan=2)

        #!#!-Always remember to use this when iterating or app will freeze until loop has ended-#!#!
        root.update_idletasks()

    ##-Exporting Data to CSV-##
    my_df = pd.DataFrame({
        'Device ID': devices,
        'Status': status,
        'Customer': customer,
        'Application': application,
        'GPS_Time (seconds)': GPS_time
    })

    #Output message "Done"
    label_5.grid_remove()
    label_5 = Label(root, padx=200, text="Done")
    label_5.grid(row=7, column=0, columnspan=2)

    #resize root window
    root.geometry('450x350')

    def export():
        my_df.to_csv('~/Desktop/device_output.csv')

    export_button = Button(root, padx=50, pady=10, text='Export CSV to Desktop?', command=export)
    export_button.grid(row=6,column=0, columnspan=2)


####---Root Layout---####

#Get Info Button
button_1 = Button(root, padx=50, pady=20, text="Get Info", command=get_device_info)
button_1.grid(row=2, column=0, columnspan=1)

#Progress Bar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress_bar.grid(row=5, column=0, columnspan=2)

#Exit Button
exit_button = Button(root, padx = 50, pady=20, text="Exit Program", command=root.quit)
exit_button.grid(row=8, column=0, columnspan=2)

#Spacing
label_3 = Label(root, text = '')
label_3.grid(row=4, column=0, columnspan=2)

label_4 = Label(root, text = '')
label_4.grid(row=6, column=0, columnspan=2)

root.mainloop()