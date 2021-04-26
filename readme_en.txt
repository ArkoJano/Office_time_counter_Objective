Python version: 3.8.7
PyInstaler version : 4.3
System: Windows 10

--------------------- Content ---------------------

In the main folder you can find:

	- readme
	- input.csv - an example file with the data that 
		          given in 'Zadanie.pdf'

	- swi.exe - an executable program file

	- source - |
		       | - input.csv - the same file as in 
		       |               in the main folder
		       |
		       | - swi.py - a Python script that 
		       |            contains all the code



	- test_input-| 
		         | - input.csv - file with data on which 
                                 I tested the program

	- build, 
	__pycache__ - files created during the creation of the
		   		  executable file by PyInstaler
	

-------------------- Launching ---------------------

Executable file for the Windows system:

	- swi.exe - file that will execute the entire program

Python script (requires Python3 installed - tested for version 3.8.7)

	 - source/swi.py - requires command line execution

	    
It is required that the input.csv file
file and the program itself must be located in the same folder.

-------------------- Functioning of the program ---------------------

The program 'swi.py'/'swi.exe' after being started searches
folder for the file 'input.csv', which contains data in format:

YYYY-MM-DD hh:mm:ss ;Reader [event]; E/[0-3]/KD1/[0-9]-[0-9]

Based on this, it calculates the time spent in the office that
day and writes it in the output file 'result'.
(names are stored in constants at the beginning of the file)


-------------------- Error handling ---------------------

In case of incorrect data in the input.csv file
an error will be reported and the program will terminate
because it is not possible to perform calculations on 
invalid data.

The format of the input data is very precise and 
any deviation from it will result in an error, which 
Of course, if you have other expectations, you can 
can be very easily modified to, for example, accept
certain deviations.

Any number of whitespace characters 
between the ; (semicolons) for Event and Gate is acceptable.

I was not sure about signaling wrong data so in case 
so if for example we have the following situation: 

2021-04-26 14:33:00 ;Reader entry;E/0/KD1/3-8
2021-04-26 13:34:00 ;Reader entry;E/0/KD1/7-8

When the building entry time on the same day is 
later than the previous entry, I decided to follow 
recommendations and simply add an "i" flag for that day 
when entering the results, instead of reporting an exception 
(which I left commented).

I have implemented the ability to count different
"batches" of time spent in the office, i.e. when
employee goes out and comes back in a while, he starts
another batch of time in the office, which will also be counted.

As far as the decoding of the gate code is concerned, I assumed 
that the second number after (E/) means the floor and only
entry/exit on the first floor means leaving building.


