# v0.0.
# This is a working prototype written by a Python newbie. Use at your own risk.
# Licence: GPL 3.0 https://www.gnu.org/licenses/gpl-3.0.html

# Get number of files
numfiles = input("Specify the number of files: ")
try:
    numfiles = int(numfiles)
except:
    print("Invalid input.")
    exit()

#Open files
try:
    files = [open("test_data%d.csv" % i) for i in range(1, numfiles+1)]
except:
    print("Invalid input.")
    exit()
#print(files)

print("Working...")

#make empty dictionary
evals = dict()

#Read files
fcount = 0
for f in files:                 #pick file
    firstline = True            #reset to first line
    for line in f:              #read lines
        if firstline is True:
            firstline = False
            continue            #skip header row
        cells = line.rstrip().split("|") #split based on "|" delimiter
        s = cells[0]            #set current student to bannerid; we ignore student names i.e. cells[1]
        q1 = float(cells[2])    #get answers to questions
        q2 = float(cells[3])
        q3 = float(cells[4])
        q4 = float(cells[5])
        c1 = cells[6]
        c2 = cells[7]
        if s not in evals:
            evals[s] = [(q1,q2,q3,q4,c1,c2)]
        else:
            evals[s].append((q1,q2,q3,q4,c1,c2))
#print(evals)

#dictionary structure
#{ "studentID1":[(1,2,3,4,a,b),(1,2,3,4,a,b),...],
#  "studentID2":[(1,2,3,4,a,b),(1,2,3,4,a,b),...], ... }

#calculate averages and concatenate comments
output = dict() #create new empty dictionary for output
for s in evals:
    enum = len(evals[s]) #get number of evals for this student
    q1tot = 0.0            #set variables to starting values
    q2tot = 0.0
    q3tot = 0.0
    q4tot = 0.0
    c1con = ""
    c2con = ""
    for e in evals[s]:  #iterate through tuples to create totals and concats
        q1tot += e[0]
        q2tot += e[1]
        q3tot += e[2]
        q4tot += e[3]
        if c1con == "": #concatenation with '; ' to separate comments
            c1con = e[4]
        else:
            c1con = "; ".join((c1con,e[4]))
        if c2con == "":
            c2con = e[5]
        else:
            c2con = "; ".join((c2con,e[5]))
    output[s] = (str(q1tot/enum),str(q2tot/enum),str(q3tot/enum),str(q4tot/enum),c1con,c2con) #write avgs and concats to output dict
#print(output)

#To output final calculations:
#   loop through tuples to compute averages and concatenate comments
#   write these to a new file

fout = open("evals_out.csv", "w") #create new file
for s in output:                  #write a line for each student's results
    fout.write(s + "|")           #start line with studentid
    for t in output[s]:           #start by grabbing the items in each tuple
        fout.write(t + "|")       #write each value, separated by '|'
    fout.write("\n")              #end line
fout.close() #save file

print("Done. Check 'evals_out.csv' for your data.")
# The final output is a pipe-delimited csv.
