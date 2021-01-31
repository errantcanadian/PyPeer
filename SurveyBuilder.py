# Part of PyPeer, a project by Trystan Goetze.
# Follow the project at github.com/errantcanadian
# Licensed under the GPL 3.0 https://www.gnu.org/licenses/gpl-3.0.html
# If you use this code or want to give feedback, please email me at contact@trystangoetze.ca

# This script takes a classlist as a CSV in the format exported by Brightspace
# then prompts you to enter the questions you wish to have in your peer evaluations.
# Two types of questions are supported: Lickert (i.e. n-point scales) and
# written response questions.
# The export data is a set of CSVs that can be imported into the Question Library
# in Brightspace, where they can be used to create surveys for each team in your class.

import csv

# Get classlist
clistfn = input("Enter the name of the classlist file\n(hit return/enter to default to 'classlist.csv'):\n")
if clistfn == "" : clistfn = "classlist.csv"
try :
    testopen = open(clistfn)
    testopen.close()
except :
    print("Error: Invalid file.")
    quit()

# Build students dictionary
sdict = dict() ## sdict structure: {"sID": ["surname", "firstname", "email", "team"]}
## Open the file
with open(clistfn, newline="") as clist :
    clistreader = csv.reader(clist)
    firstline = True
    for line in clistreader :
        ### Ignore header row
        if firstline == True :
            firstline = False
            continue
        sdict[line[0]] = [line[1], line[2], line[3], line[4]]

# Build Teams Dictionary
tdict = dict() ## tdict structure: {"Team ID": [("sID", "Full name"), (sID, "Full name 2", etc.)]}
with open(clistfn, newline="") as clist :
    clistreader = csv.reader(clist)
    firstline = True
    for line in clistreader :
        if firstline == True :
            firstline = False
            continue
        if line[4] in tdict.keys() :
            tdict[line[4]].append((line[0], line[2] + " " + line[1]))
        else :
            tdict[line[4]] = [(line[0], line[2] + " " + line[1])]

# Build questions
Lickert = False
Written = False
Lscale = 0

## Set Lickert scale
if input("Will your surveys have Lickert questions?\n(e.g. 'Rate the student on a scale of 1 to 5')? (y/n)\n") == "y" :
    Lickert = True
    while True :
        try :
            Lscale = int(input("Enter the scale of your Lickert questions\nFor example: '3' = 3-point, '5' = 5-point, '7' = 7-point, etc.:\n"))
            if Lscale < 1 :
                print("Error: Scale must be a positive integer.")
                if input("Try again? (y/n)\n") == "y" :
                    continue
                else :
                    Lickert = False
                    break
        except :
            print("Error: Scale must be a positive integer.")
            if input("Try again? (y/n)\n") == "y" :
                continue
            else :
                Lickert = False
                break

print("Lickert scale set to %d-point scale." % Lscale)

### Set Lickert labels
if Lickert == True :
    Llabels = list()
    for i in range(Lscale) :
        Llabels.append(input("Enter the label for level %d on your Lickert scale.\n(e.g. 'Poor', 'Good', 'Excellent', etc.)\n" % (i + 1)))
Llabels.reverse()

## Check for Written responses
if input("Will your surveys have written response questions?\n(e.g. 'Describe how the student made a positive contribution to the group.')? (y/n)\n") == "y" : Written = True

## Create question list
qlist = list()

### Create Questions
qnum = 0
while True :
    if input("Create a new question? (y/n)\n") == "y" :
        qnum += 1
        #### Get question type
        if Lickert == True and Written == True :
            qtype = input("Question type? \n L = Lickert, W = Written Response\n")
        elif Lickert == False and Written == True :
            qtype = "W"
        elif Written == False and Lickert == True :
            qtype = "L"
        else :
            print("Error: No question types specified.")
            quit()
        ##### Catch bad input
        if qtype != "L" and qtype != "W" :
            print("Error: Invalid question type.")
            continue
        #### Get question text
        qtext = input("Enter question #%d:\n" % qnum)
        #### Write to list
        qlist.append((qnum, qtype, qtext))
    else : break

print("Working...")

# Build surveys
    ## One csv per team
for t in tdict :
    with open(t + ".csv", "w", newline="") as outputfile :
        out = csv.writer(outputfile, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
    ### For each student in the team...
        for s in tdict[t] :
        #### Loop through all questions
            for q in qlist :
                if q[1] == "L" :
                    out.writerow(["NewQuestion", "MC"])
                    out.writerow(["ID"])
                    out.writerow(["Title"])
                    out.writerow(["QuestionText", "Regarding %s: " % s[1] + " " + q[2]])
                    out.writerow(["Points"])
                    out.writerow(["Difficulty"])
                    out.writerow(["Image"])
                ##### Add rows for each level of the Lickert scale
                    curlvl = Lscale
                    for level in Llabels:
                        out.writerow(["Option", 0, str(curlvl) + " (%s)" % level])
                        curlvl -= 1
                    out.writerow(["Hint"])
                    out.writerow(["Feedback"])
                elif q[1] == "W" :
                    out.writerow(["NewQuestion", "WR"])
                    out.writerow(["ID"])
                    out.writerow(["Title"])
                    out.writerow(["QuestionText", "Regarding %s: " % s[1] + q[2]])
                    out.writerow(["Points"])
                    out.writerow(["Difficulty"])
                    out.writerow(["Image"])
                    out.writerow(["InitialText"])
                    out.writerow(["AnswerKey"])
                    out.writerow(["Hint"])
                    out.writerow(["Feedback"])
# Confirmation
print("Complete. View the directory to check your files.\n Your questions can now be imported to the Brightspace question library for use in surveys.")
