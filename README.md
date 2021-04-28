# Office_time_counter_Objective

-------------------- Functioning of the program ---------------------

The program 'swi.py'/'swi.exe' after being started searches
folder for the file 'input.csv', which contains data in format:

Date; Event; Gate
YYYY-MM-DD hh:mm:ss ;Reader [event]; E/[0-3]/KD1/[0-9]-[0-9]


Based on this, it calculates the time spent in the office that
day and writes it in the output file 'result'.
(names are stored in constants at the beginning of the file)

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

	swi.exe - file that will execute the entire program

Python script (requires Python3 installed - tested for version 3.8.7)

	source/swi.py - requires command line execution

	    
It is required that the input.csv file
file and the program itself must be located in the same folder.




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
