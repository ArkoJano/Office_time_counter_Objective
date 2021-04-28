Arkadiusz Janus

Wersja Python'a: 3.8.7
Wersja PyInstaler'a : 4.3
System: Windows 10

--------------------- Zawartosc -----------------------

W folderze glownym znajduja sie:

	- readme
	- input.csv - przykladowy plikiem z danymi ktore 
		      zostaly podane w 'Zadanie.pdf'

	- swi.exe   - plik wykonywalny programu

	- source  -  |
		     | - input.csv - ten sam plik z danymi  
		     |		     co w folderze glownym
		     |
		     | - swi.py  - skrypt Pythona ktory 
		     |   	   zawiera caly kod



	- test_input-| 
		     | - input.csv - plik z wlasnymi danymi
				     na ktorych testowalem
				     dzialanie programu

	- build, 
	__pycache__  - foldery zawierajace pliki dla swi.exe
	

-------------------- Uruchomienie ---------------------

Plik wykonywalny dla systemu z rodziny Windows:

	- swi.exe 	- plik wykonywalny ktory wykona caly program
           	   	  po uruchomieniu go.

Skrypt Python - Preferowany sposob - w przypadku blednych danych 
									 wypisze w  konsoli jaki problem 
									 napotkal
(wymaga zainstalowanego Python 3 
- testowane dla wersji 3.8.7)

	 - swi.py - wymaga uruchomienia w linii komend

	    
Wymogiem dzialania jest to aby plik input.csv
i sam program znajdowaly sie w tym samym folderze.

-------------------- Dzialanie ---------------------

Program 'swi.py'/'swi.exe' po uruchomieniu przeszukuje
folder w poszukiwaniu pliku 'input.csv' ktory zawiera
dane w formacie:

YYYY-MM-DD hh:mm:ss ;Reader [event]; E/[0-3]/KD1/[0-9]-[0-9]

Na podstawie ktorego oblicza czas spedzony danego dnia
w biurze i zapisuje go w pliku wyjsciowym 'result'
(nazwy zapisane sa w stalych na samym poczatku pliku)


-------------------- Obsluga bledow ---------------------

W przypadku niepoprawnych danych w pliku input.csv
zostanie zgloszony blad i program zakonczy swoje dzialanie
poniewaz nie ma mozliwosci wykonac obliczen na 
blednych danych.

Format wprowadzanych danych jest bardzo precyzyjny i 
kazde odstepstwo od niego zakonczy sie bledem, co 
oczywiscie w przypadku innych oczekiwan mozna 
bardzo latwo zmodyfikowac zeby np. byly akceptowane
pewne wyjatki.

Akceptowalna jest dowolna ilosc bialych znakow 
pomiedzy ; (srednikami) dla Event i Gate.

Nie bylem pewien co do sygnalizowania blednych danych wiec w 
przypadku gdy np. mamy sytuacje nastepujaca: 

2021-04-26 14:33:00 ;Reader entry;E/0/KD1/3-8
2021-04-26 13:34:00 ;Reader entry;E/0/KD1/7-8

kiedy godzina wejscia do budynku tego samego dnia jest 
pozniejsza niz poprzednia wpisana, postanowilem trzymac 
sie zalecen i dopisac po prostu flage "i" przy tym dniu 
podczas wpisywania wynikow, zamiast zgloszenia wyjatku 
(co zostawilem zakomentowane).

Zaimplementowalem mozliwosc zliczania roznych
"parti" czasu spedzonego w biurze, czyli gdy np.
pracownik wyjdzie i wroci za jakis czas, rozpocznie
kolejna partie czasu w biurze ktora tez bedzie zliczana.

W kwestii rozszyfrowania kodu bramek przyjalem 
ze druga liczba po (E/) oznacza pietro i tylko
wejscie/wyjscie na parterze oznacza opuszczenie 
budynku.