"""OADOI lookup via DOI from .csv"""

import json
import csv
from tkinter import Tk, Entry, Label, Button, END
from tkinter.filedialog import askopenfilename
from urllib import request, error

URL = 'https://api.oadoi.org/' #URL for API

class MyGui:
    """The main GUI"""
    def __init__(self, window):
        window.geometry("382x95")
        window.title("oaDOI Miner v0.2 by Asger Hansen")
        window.configure(background="grey")

        self.label1 = Label(window, text='Import from file (.csv):', bg='grey') \
            .grid(row=0, sticky='W')
        self.label2 = Label(window, text='Output to file (.json):', bg='grey') \
            .grid(row=1, sticky='W')
        self.label3 = Label(window, text='Your email:', bg='grey') \
            .grid(row=2, sticky='W')

        self.entry1 = Entry(window)
        self.entry2 = Entry(window)
        self.entry3 = Entry(window)
        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)
        self.entry3.grid(row=2, column=1)

        self.button1 = Button(window, text='BROWSE', width='6', command=self.click1) \
            .grid(row=0, column=2, sticky='E')
        self.button2 = Button(window, text='BROWSE', width='6', command=self.click2) \
                .grid(row=1, column=2, sticky='E')
        self.button3 = Button(window, text='SUBMIT', width='6', command=self.click3) \
            .grid(row=2, column=2, sticky='E')

    def click1(self):
        """Action on button click"""
        self.entry1.delete(0, END) #deletes the current value
        self.entry1.insert(0, askopenfilename()) #inserts new value assigned by 2nd parameter

    def click2(self):
        """Action on button click"""
        self.entry2.delete(0, END) #deletes the current value
        self.entry2.insert(0, askopenfilename()) #inserts new value assigned by 2nd parameter

    def click3(self):
        """Action on button click"""
        self.open_csv()

    def open_csv(self):
        """read DOI from .csv file"""
        mail = '?email=' + str(self.entry3.insert(0, self.entry3.get())) \
        #inserts new value assigned by 2nd parameter
        file_name = self.entry1.get()
        with open(file_name, newline='') as _:
            reader = csv.reader(_, delimiter=';')
            next(_)
            for row in reader:
                self.pull_data_api(URL + row[0] + mail)

    def pull_data_api(self, url):
        """http request and error handeling"""
        json_name = self.entry2.get()
        req = request.Request(url)
        try:
            response = request.urlopen(req)
            data = json.loads(response.read())
            self.write_json2csv(json_name, data)
            print(data)

        except error.HTTPError as _:
            print(_.reason)

    def write_json2csv(self, json_name, data):
        """write json stream from html to file"""
        with open(json_name, mode="a") as file:
            file.write(json.dumps(data))

def main():
    """main"""
    root = Tk()
    gui = MyGui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
