# PyPeer
Tools for computing student peer evaluations, written in Python3.<br>
<br>
This repository serves two purposes:<br>
(1) I'm teaching myself Python3 and how to use GitHub.<br>
(2) I'm trying to make it easier to collect and grade student peer evaluations.<br><br>
The current state of the project is a prototype peer evaluation grader, which has a number of limitations. Read carefully before using, caveat emptor, et cetera.<br>

## Files
<strong>test_peers.py</strong> is a first attempt at a program to auto-grade peer evaluations. It takes data as a pipe-delimited .csv in the following configuration:<br><br>
StudentID|Student Name|Q1|Q2|Q3|Q4|C1|C2<br><br>
Where Q1–Q4 are numerical scores on some evaluation criterion, and C1–C2 are qualitative feedback (intent is C1 is a compliment, C2 is constructive criticism).<br>
When run from Terminal, the program prompts for a number of files. This must be supplied as a positive integer that matches the number of evaluation files in the directory.<br>
<br>
<strong>test_data1.csv</strong> and <strong>test_data2.csv</strong> are sample data files. At present <strong>test_peers.py</strong> only takes inputs with filenames that match this pattern, i.e., "test_data%d.csv".

## Output
<strong>test_peers.py</strong> outputs a pipe-delimited .csv (with all averages computed and comments concatenated) as <strong>evals_out.csv</strong><br>
The result can be read easily into LibreOffice Calc for reference by grading spreadsheets.
