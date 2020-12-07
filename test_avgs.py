# Takes a classlist and D2L/BS survey "summary reports" and outputs a csv with
# the average score achieved for each student

import csv

# Get classlist
clistfn = input("Enter the name of the classlist file (enter 'q' to quit): ")
if clistfn == "q" :
    quit()
elif clistfn == "" :
    clistfn = "classlist.csv" # Default
try : # Test to see if file exists
    clistfile = open(clistfn)
    clistfile.close()
except :
    print("Error: invalid file")
    quit()

# Build dictionary of students
sdict = dict()
firstline = True
with open(clistfn, newline="") as clistfile :
    clreader = csv.reader(clistfile, delimiter=",")
    for row in clreader :
        if firstline == True :
            firstline = False
            continue
    # {"StudentID": "Firstname Lastname", "Team"}
        sID, sname, steam, smail = (row[0], " ".join((row[2],row[1])), row[4], row[3])
        sdict[sID] = [sname, steam, smail, ""]
# Dictionary structure:
#    {"StudentID": "Firstname Lastname", "Group ID", "email", placeholder string for grade}


# Get survey report files
# for later: make a while loop to enter multiple files, try/except to ignore
# bad filenames, "c" to confirm and continue (prompt y/n to check the list),
# "q" to quit

# Later: make something that exports individual questions for mail merging to students
# And a prompt to switch between a csv to import and a spreadsheet to mail merge

reportsl = list()
while True:
    creport = input("Enter the name of a report file (Enter '' to continue or 'q' to quit): ")
    if creport == "q" : quit()
    elif creport == "" : break
    else:
        try :
            r = open(creport)
            r.close()
            reportsl.append(creport)
        except :
            print("Invalid file; please re-enter.")
            continue


#reportfn = input("Enter the name of the report file: ")
#try :
#    if reportfn == "" : reportfn = "Team1_test.csv"
#except :
#    print("Test report not found.")
#    quit()
#try :
#    reportfile = open(reportfn)
#    reportfile.close()
#except :
#    print("Error: Invalid file.")
#    quit()

# Below calculates summary grades only (average across all Likert questions)
# Add grades to dictionary entries
for f in reportsl :
    for s in sdict :
        numrespond = 0.0
        scoretot = 0.0
        reportfile = open(f)
        for line in reportfile :
            line = line.rstrip().split(",")
            if line[4].find(sdict[s][0]) == -1 :
                continue
            else :
                if line[2] == "MC" :
                    numrespond += float(line[9])
                    scoretot += float(line[7][0]) * float(line[9])
        reportfile.close()
        if numrespond != 0.0 :
            finalscore = scoretot / numrespond
            sdict[s][3] = str(finalscore)

# Export into a useable spreadsheet
out = open("marks_out.csv", "w") #create file
for s in sdict :
    out.write(",".join((s,sdict[s][3],"\n")))
out.close()
