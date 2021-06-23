# Sprint 3 Assignment: Population Generator
# Andrew Suezaki

# citations:
# modified the examples for reading/writing csv files
#   https://www.programiz.com/python-programming/csv
# modified examples for making requests to census API
#   https://www.geeksforgeeks.org/get-post-requests-using-python/
# API call format
#   https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_api_handbook_2020_ch02.pdf
# method of using lambda operator for tkinter button binding (command=lambda)
#   https://www.delftstack.com/howto/python-tkinter/how-to-pass-arguments-to-tkinter-button-command/


import csv
import sys
import requests
import tkinter as tk
from os.path import isfile
from tkinter import filedialog
import subprocess

# lists for dropdown menus
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
# dict to store state code for each state
state_codes = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}
# list of person generator states
person_states = ["AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NM",
                 "NV", "OR", "UT", "WA", "WY"]
# initializing tkinter GUI window and text box
window = tk.Tk()
window.geometry("600x550")
window.title("Population Generator")
text_box = tk.Text(window, width=250, height=5)


def getreq(year, state):
    """
    Sends a get request to acs1 census API and returns total population for the given
    year and state.
    """
    # gov census api key
    api_key = "d4e67c460f8480323926a362022c258223f8f804"
    baseURL = "https://api.census.gov/data/"
    # creating url for api call
    url = baseURL + str(year) + "/acs/acs1?get=NAME,B01003_001E&for=state:" + state_codes[state] + "&key=" + api_key
    # sends get request and saves response as response object
    res = requests.get(url)
    data = res.json()
    pop = data[1][1]
    return pop


def inputCSV(filename):
    """
    Parses the inputted csv file and creates an output file with the requested information.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # skip header row
        next(reader, None)
        # grab year and state from input file
        for row in reader:
            inyear = row[0]
            instate = row[1].upper()
    # get request to get total population
    pop = getreq(inyear, instate)
    # clear text box
    text_box.delete(1.0, tk.END)
    # print output to GUI
    text_box.insert(tk.END, "The total population for " + instate + " in " + str(inyear) + " was " + str(pop) + ".")
    # handling request file
    if filename == "getpop.csv":
        print("Population Generator: Request from Content Generator received")
    # create CSV file in same directory with requested info
    outputCSV(inyear, instate, pop, filename)


def outputCSV(year, state, pop, filename):
    """
    Creates a csv file in the same directory containing the requested information
    """
    if filename == "getpop.csv":
        outfile = "outpop.csv"
    else:
        outfile = "output.csv"
    # opens or creates output.csv file in the same directory as population-generator.py
    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file)
        # writing header row
        writer.writerow(["input_year", "input_state", "output_population_size"])
        # writing output row
        writer.writerow([str(year), state, str(pop)])
    if outfile == "output.csv":
        # confirmation message that file was created
        text_box.insert(tk.END, "\n\n'output.csv' file created.")
    else:
        # prints confirmation that response was created
        print("Population Generator: Response sent")


def generate(year, state):
    """
    Generate button functionality. Performs a get request on the selected year and state
    and prints the info
    """
    # get requested total population
    pop = getreq(year, state)
    # clear text box
    text_box.delete(1.0, tk.END)
    # print output
    text_box.insert(tk.END, "The total population for " + state + " in " + str(year) + " was " + str(pop) + ".")


def selectCSV():
    """
    Select CSV button functionality. Opens file explorer for user to
    select a csv file, then calls inputCSV() on the selected csv file
    """
    # open file explorer
    targetfile = filedialog.askopenfilename()
    if isfile(targetfile):
        # call inputCSV to parse selected csv file
        inputCSV(targetfile)
    else:
        text_box.insert(tk.END, "\nError: File could not be found.")


def contentreq(state, addresses):
    """
    Calls person generator to make a request with the inputted parameters
    and prints the response to the console
    """
    with open('getperson.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # writing header row
        writer.writerow(["input_state", "input_number_to_generate"])
        # writing output row
        writer.writerow([state.lower() + '.csv', str(addresses)])
    # calls person generator and waits for it to finish
    subprocess.call(['python', 'cs361Project.py', 'getperson.csv'])
    # opens response and prints it to the console
    file = open("gotperson.csv", 'r')
    reader = csv.reader(file)
    print(list(reader))


def runGUI():
    """
    Initializes the GUI
    """
    prompt = tk.Label(window, text='Welcome to Population Generator!\nSelect a target year and state and press Generate'
                                   ' when ready to get the population size.\nResults will be printed to the text box '
                                   'below.\nAlternatively, use the `Select a CSV` '
                                   'button to select a csv file for input (an output.csv file will be generated).'
                                   '\nCSV must follow the format of input_year, input_state with a header row.'
                                   '\nTo run this program from the command line, include a CSV file as an argument.')
    prompt2 = tk.Label(window, text='To request from Person Generator:\nEnter a state and # of addresses to generate'
                                    ' in the boxes below and click `Request Person Generator`.\nGenerated addresses'
                                    ' for the selected state will be printed to the console.')
    # year dropdown menu
    var1 = tk.StringVar(window)
    var1.set(years[0])
    year_menu = tk.OptionMenu(window, var1, *years)
    # state dropdown menu
    var2 = tk.StringVar(window)
    var2.set(states[0])
    state_menu = tk.OptionMenu(window, var2, *states)
    # input fields for Content Generator Requests
    var3 = tk.StringVar(window)
    var3.set(person_states[0])
    person_menu = tk.OptionMenu(window, var3, *person_states)
    var4 = tk.Entry()
    # button to select a csv file
    select_csv = tk.Button(
        text="Select a CSV file",
        width=15,
        height=2,
        command=lambda: selectCSV()
    )
    # button to generate info
    generate_info = tk.Button(
        text="Generate",
        width=25,
        height=3,
        command=lambda: generate(var1.get(), var2.get())
    )
    # button to request from Person Generator
    request_info = tk.Button(
        text="Request Person Generator",
        width=25,
        height=3,
        command=lambda: contentreq(var3.get(), var4.get())
    )
    # button to create output file
    output_csv = tk.Button(
        text="Export to CSV",
        width=25,
        height=3,
        command=lambda: outputCSV(var1.get(), var2.get(), getreq(var1.get(), var2.get()))
    )
    # place prompt
    prompt.pack()
    # pack menus and buttons
    year_menu.pack()
    state_menu.pack()
    select_csv.pack()
    generate_info.pack()
    prompt2.pack()
    person_menu.pack()
    var4.pack()
    request_info.pack()
    text_box.pack()
    output_csv.pack()
    # GUI main loop
    window.mainloop()


# checking if input file was passed in cmd line
if len(sys.argv) > 1:
    # checking if file is valid
    if isfile(sys.argv[1]):
        # skips GUI if a file was inputted
        inputCSV(sys.argv[1])
    else:
        # file input validation error message
        print("Error: file " + sys.argv[1] + " cannot be found")
else:
    # otherwise loads the GUI
    runGUI()