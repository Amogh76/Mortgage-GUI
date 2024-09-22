import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import csv

fields = ('Loan Amount', 'Interest Rate %', 'Loan Term (Years)',\
           'Monthly Payment', 'Total Paid')

#Name: msgBox
#gives the error messeage if needed
#@param msgText
#@return a warning

def msgBox(msgText):
    msg.showwarning('Error invalid input', msgText)

#Name: mortgage
#calculates mortgage with the given info
#@param loanAmount, interestRate, loanTerm
#@return monthlyPayment, totalPayment
    
def mortgage(entries):
   try:
    loanAmount = float(entries['Loan Amount'].get())
    interestRate = float(entries ['Interest Rate %'].get())
    loanTerm = float(entries['Loan Term (Years)'].get())
    
    if loanAmount < 0 or interestRate < 0 or loanTerm < 0 :
        msgBox ("Must be positive number > 0")

    else:
       monthlyRate = (interestRate / 100) / 12
       numPayments = loanTerm * 12
       monthlyPayment = loanAmount * monthlyRate \
           * pow((1 + monthlyRate), numPayments)\
           / (pow((1 + monthlyRate),numPayments) - 1)
       totalPayment = monthlyPayment * (loanTerm * 12)

       ents ['Monthly Payment'].configure(state='normal')
       ents ['Total Paid'].configure(state='normal')

       totalPaymentText = ('${:,.2f}'.format(totalPayment))
       entries ['Total Paid'].delete(0,END)
       entries['Total Paid'].insert(0, totalPaymentText )

       monthlyPaymentText = ('${:,.2f}'.format(monthlyPayment))
       entries['Monthly Payment'].delete(0,END)
       entries['Monthly Payment'].insert(0, monthlyPaymentText )

       entries ['Monthly Payment'].configure(state='disabled')
       entries ['Total Paid'].configure(state='disabled')      
 
   except:
      msg.showwarning('Error: Invalid Input', 'Must be positive number > 0')
      
Axlist = []
Aylist = []
with open('mortgageRate.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        Axlist.append(int(row[0]))
        Aylist.append(float(row[1]))
plt.plot(Axlist,Aylist, label='Mortgage Rate')
ax = plt.gca() 
plt.xticks(rotation=90, fontsize=8) 
for label in ax.get_xaxis().get_ticklabels()[::7]:
    label.set_visible(False)

#Name: annotationLabel
#annotates points in the chart
#@param xlist, ylist
#@return annotations

def annatationLabel(xlist, ylist):
    count = 0 
    for x,y in zip(xlist,ylist):        
        if (count == 3):  
            label = "{:4f}%".format(y)
            plt.annotate(label, 
                         (x,y), 
                         textcoords="offset points", 
                         xytext=(0,10), 
                         rotation=360,
                         fontsize=10,
                         ha='center') 
            count = 0
        else:
            count = count + 1
            
#Name: Chart
#displays a chart
#@param none
#@return the chart

def Chart():
    plt.xlabel('Year', fontsize=8)
    plt.ylabel('Rate %')
    plt.title('Historical Mortgage Rate')
    annatationLabel(Axlist, Aylist)
    plt.legend()
    plt.show()


#Name: makeform
#forms the GUI
#@param root, fields
#@return open entries

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries

#Name: print_info
#prints name, lab and time
#@param none
#@return none

def printMeFirst(name):
    currentTime = datetime.now()
    msg = name + '\n' + str(currentTime)
    return msg


if __name__ == '__main__':

    labMessage = printMeFirst('Amogh Arora - CNET 142')
    root = Tk()
    root.title("Mortgage Calculator")
    root.configure(background="light green")
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e = ents: fetch(e)))
    ents ['Monthly Payment'].configure(state='readonly', \
                                       font=("Arial", 14, "bold", "italic"))
    ents ['Total Paid'].configure(state='readonly', \
                                       font=("Arial", 14, "bold", "italic"))

    b1 = Button(root, bg = "light blue", text = 'Calculate', \
                command = (lambda e = ents: mortgage(e)))
    b1.pack(side = LEFT, padx = 5, pady = 5)

    NUM_YEARS = 30

    b2 = Button(root, text='Chart', \
                command = (lambda e = ents: Chart()))
    b2.pack(side = LEFT, padx = 5, pady = 5)

    b3 = Button(root, text = 'Quit', command = root.destroy)
    b3.pack(side = LEFT, padx = 5, pady = 5)

    tbox = tk.Text(root, height=2, width=30)
    tbox.pack()
    tbox.insert(tk.END, labMessage)
    tbox.configure(state='disabled')

    root.mainloop()



 
