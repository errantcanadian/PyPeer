# v0.0.
# This is a working prototype written by a Python newbie. Use at your own risk.
# Licence: GPL 3.0 https://www.gnu.org/licenses/gpl-3.0.html

# Takes a classlist with group numbers exported from Brightspace as csv.
# Builds a dictionary of students with this structure:
#     {"ID": ("Firstname Lastname", "Team Number")}
# Exports .csv files that can be imported to Brightspace surveys
# to produce one survey per team, with student names autofilled.

# The classlist file to be imported is exported from the "Enter Grades" module
# in D2L/Brightspace, with the following configuration:
#     OrgDefinedID,Last Name,First Name,Email,Group Membership,End-of-Line Indicator
classlist = open("classlist.csv")

# Build dictionary
sdict = dict()
firstline = True
for line in classlist:
    # Skip the header row
    if firstline == True:
        firstline = False
        continue
    line = line.rstrip("#").split(",") # removes D2L's end of line indicator
    # "StudentID": "Firstname Lastname", "Team"
    sID, sname, steam = (line[0], line[2] + " " + line[1], line[4])
    sdict[sID] = ( sID, sname, steam )

#Get number of teams
tl = list()
for s in sdict:
    if sdict[s][2] in tl: continue
    tl.append(sdict[s][2])
tnum = len(tl)

# Write questions for each student in a new file for each team
for t in tl:
    cteam = int(t[5:]) # Group names are all in the form "Team %d"
    sout = open("survey%d.csv" % cteam, "w")
    for s in sdict:
        if sdict[s][2] != "Team %d" % cteam: continue
        # Write D2L/BS new question identifier
        sout.write("NewQuestion,MC\nID,\nTitle,\n")
        # Write Q1 subbing in student name
        sout.write("QuestionText,How well was " + sdict[s][1] + " prepared for each team meeting or assignment?\n")
        # Write misc nonsense that BS wants but isn't useful to us
        sout.write("Points,\nDifficulty,\nImage,\n")
        # Now write the actual options
        sout.write("Option,0,5 (Excellent)\nOption,0,4 (Good)\nOption,0,3 (Satisfactory)\nOption,0,2 (Needs improvement)\nOption,0,1 (Poor)\nOption,0,0 (No-show)\n")
        # Final line of D2L clutter
        sout.write("Hint,\nFeedback,\n\n\n")
        # Repeat for Q2
        sout.write("NewQuestion,MC\nID,\nTitle,\n")
        sout.write("QuestionText,How well did " + sdict[s][1] + " communicate with the team?\n")
        sout.write("Points,\nDifficulty,\nImage,\n")
        sout.write("Option,0,5 (Excellent)\nOption,0,4 (Good)\nOption,0,3 (Satisfactory)\nOption,0,2 (Needs improvement)\nOption,0,1 (Poor)\nOption,0,0 (No-show)\n")
        sout.write("Hint,\nFeedback,\n\n\n")
        # Repeat for Q3
        sout.write("NewQuestion,MC\nID,\nTitle,\n")
        sout.write("QuestionText,To what extent did " + sdict[s][1] + " do their fair share of the work?\n")
        sout.write("Points,\nDifficulty,\nImage,\n")
        sout.write("Option,0,5 (Excellent)\nOption,0,4 (Good)\nOption,0,3 (Satisfactory)\nOption,0,2 (Needs improvement)\nOption,0,1 (Poor)\nOption,0,0 (No-show)\n")
        sout.write("Hint,\nFeedback,\n\n\n")
        # Repeat for Q4
        sout.write("NewQuestion,MC\nID,\nTitle,\n")
        sout.write("QuestionText,\"In your opinion, to what extent did " + sdict[s][1] + "\'s contributions to the team improve in response to the midterm peer evaluations?\"\n")
        sout.write("Points,\nDifficulty,\nImage,\n")
        sout.write("Option,0,5 (Excellent)\nOption,0,4 (Good)\nOption,0,3 (Satisfactory)\nOption,0,2 (Needs improvement)\nOption,0,1 (Poor)\nOption,0,0 (No-show)\n")
        sout.write("Hint,\nFeedback,\n\n\n")
        # Compliment feedback question
        sout.write("NewQuestion,WR\nID,\nTitle,\n")
        sout.write("QuestionText,What is one thing you think " + sdict[s][1] + " did particularly well in your team activities?\n")
        sout.write("Points,\nDifficulty,\nImage,\nInitialText,\nAnswerKey,\nHint,\nFeedback\n\n\n")
        # Constructive criticism question
        sout.write("NewQuestion,WR\nID,\nTitle,\n")
        sout.write("QuestionText,What is one thing you think " + sdict[s][1] + " could improve in future team assignments (at school or at work)?\n")
        sout.write("Points,\nDifficulty,\nImage,\nInitialText,\nAnswerKey,\nHint,\nFeedback\n\n\n")
    #save current file
    sout.close()
