# Takes a classlist and D2L/BS survey "summary reports" and outputs a csv with either
# the average score achieved for each student, or the comments entered for each
# student (separated by semicolons)

import csv

# Get classlist
clistfn = input("Enter the name of the classlist file (enter 'q' to quit): ")
if clistfn == "q" : quit()
try :
    if clistfn == "" :
        clistfn = "classlist.csv"
except :
    print("Error: Classlist not found.")
    quit()
try :
    clistfile = open(clistfn)
except :
    print("Error: Invalid file.")
    quit()

print("Working...")

# Build dictionary of students
sdict = dict()
firstline = True
for line in clistfile :
    # Skip the header row
    if firstline == True:
        firstline = False
        continue
    line = line.rstrip("#").split(",") # removes D2L's end of line indicator & splits on comma delimiter
    # {"StudentID": "Firstname Lastname", "Team"}
    sID, sname, steam, smail = (line[0], line[2] + " " + line[1], line[4], line[3])
    sdict[sID] = [sname, steam, smail, 0.0, 0.0, 0.0, 0.0, "", "", 0]
# Dictionary structure:
#    {"StudentID": ["Firstname Lastname", "Group ID", "email", "Q1", "Q2", "Q3", "Q4", "C1", "C2", numreports]}
# Q1–4 are stored as floats because they are averages
# C1-2 are stored as strings because they are text



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

for i in reportsl:
    for s in sdict :
        numq1, numq2, numq3, numq4, sumq1, sumq2, sumq3, sumq4 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        c1, c2 = "", ""
        with open(i, newline="") as r :
            csvreader = csv.reader(r, delimiter=",")
            for row in csvreader :
                if row[4].find(sdict[s][0]) == -1 or sdict[s][9] > 0:
                    continue
                q1avg, q2avg, q3avg, q4avg = 0.0,0.0,0.0,0.0
                if row[4].startswith("How well was"): # Q1 Test
                    numq1 += float(row[9])
                    sumq1 += float(row[7][0]) * float(row[9])
                elif row[4].startswith("How well did"): # Q2 Test
                    numq2 += float(row[9])
                    sumq2 += float(row[7][0]) * float(row[9])
                elif row[4].startswith("To what extent"): # Q3 Test
                    numq3 += float(row[9])
                    sumq3 += float(row[7][0]) * float(row[9])
                elif row[4].startswith("In your opinion"): # Q4 Test
                    numq4 += float(row[9])
                    sumq4 += float(row[7][0]) * float(row[9])
                elif row[4].endswith("activities?"): # C1 Test
                    if c1 == "" : c1 = row[7]
                    else : c1 = "; ".join((c1,row[7]))
                elif row[4].endswith("work)?"):
                    if c2 == "" : c2 = row[7]
                    else : c2 = "; ".join((c2,row[7]))
                else : continue
        # calculate averages & add to student entry in dictionary
        if numq1 != 0.0 :
            q1avg = sumq1 / numq1
            sdict[s][3] = q1avg
        if numq2 != 0.0 :
            q2avg = sumq2 / numq2
            sdict[s][4] = q2avg
        if numq3 != 0.0 :
            sdict[s][5] = q3avg
            q3avg = sumq3 / numq3
        if numq4 != 0.0 :
            q4avg = sumq4 / numq4
            sdict[s][6] = q4avg
        if c1 != "" :
            sdict[s][7] = c1
        if c2 != "" :
            sdict[s][8] = c2
        if numq1 != 0 or numq2 !=0 or numq3 != 0 or numq4 != 0 :
            sdict[s][9] = sum((numq1,numq2,numq3,numq4))

# Write to output file
with open("comments_out.csv", "w", newline="") as out :
    writer = csv.writer(out, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
    for s in sdict :
        s_out = [s]
        for i in range(len(sdict[s]) - 1):
            s_out.append(sdict[s][i]) # Make list to write
        writer.writerow(s_out)
print("Complete. Open comments_out.csv for your data.")

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
#for f in reportsl :
#    for s in sdict :
#        numrespond = 0.0
#        scoretot = 0.0
#        reportfile = open(f)
#        for line in reportfile :
#            line = line.rstrip().split(",")
#            if line[4].find(sdict[s][0]) == -1 :
#                continue
#            else :
#                    numrespond += float(line[9])
#                    scoretot += float(line[7][0]) * float(line[9])
#        reportfile.close()
#        if numrespond != 0.0 :
#            finalscore = scoretot / numrespond
#            sdict[s].append(str(finalscore))

# Export into a useable spreadsheet
#out = open("marks_out.csv", "w") #create file
#for s in sdict :
#    out.write(s + ",")
#    for v in sdict[s] :
#        out.write(v + ",")
#    out.write("\n")
#out.close()
