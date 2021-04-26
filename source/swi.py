from pprint import pprint
import csv
from datetime import datetime, timedelta, date, time
import re 

# nazwy plikow
INPUT = "input.csv"
OUTPUT = "result"
# stale odpowiadajace wartosciom w liscie zebranej z pliku "input.csv"
DATE  = 0   
EVENT = 1    
GATE  = 2 

# stale odpowiadajace indeksom w liscie skladajacej sie z [czasu_wejscia, czasu_wyjscia] (z biura)
ENTRY = 0
EXIT = 1



def read_rows_from_input():

    '''
    funkcja otwiera plik input.csv,
    sprawdza czy istnieje, czy nie jest pusty
    i zwraca wiersze w postaci listy bez naglowka 
    '''

    with open(INPUT, 'r') as input_file:
        
        try:
            input_read = csv.reader(input_file, delimiter=';')
        except ValueError:
            raise ValueError("""Incorrect data format, should be:
                                '%Y-%m-%d %H:%M:%S ;Reader [event]; E/[]/KD1/[]-[]
                                """)
        except FileNotFoundError:
            raise FileNotFoundError(f" Could not open file {INPUT} ", )

        input_list = list(input_read)

        # jesli plik nie jest pusty
        if (len(input_list) == 0):
            raise ValueError("Input file is empty!")
        
        return input_list[1:]

def validation_of_rows(input_list):

    ''' 
    funkcja sprawdzajaca poprawnosc wpisanych danych
    jesli ktorys z wierzy nie bedzie pasowal do okreslonego
    formatu, funkcja zwroci blad
    '''

    for i in range(2):
        for row in input_list:
            
            # jesli mamy pusty wiersz to go usun
            if row == []:
                input_list.remove(row)
            
            else:
                # format DATE
                header_date_pattern = re.compile(r'\s*Date\s*')


                if bool(re.match(header_date_pattern, row[DATE])):
                    input_list.remove(row)
                    continue

                else:
                    try:
                        datetime.strptime(row[DATE], '%Y-%m-%d %H:%M:%S ')
                    except ValueError as err:
                        print(err)

                # format EVENT
                header_event_pattern = re.compile(r'\s*Event\s*')

                if bool(re.match(header_event_pattern, row[EVENT])):
                    input_list.remove(row)
                    continue
                else:

                    pattern_event = re.compile(r'\s*Reader (exit|entry)\s*')
                    matched_event = re.match(pattern_event, row[EVENT])
                    is_matched_event = bool(matched_event)

                    if is_matched_event is False:
                        raise ValueError(f'Event data does not match format: Reader (exit|entry)')

                #format GATE

                header_gate_pattern = re.compile(r'\s*Gate\s*')

                if bool(re.match(header_gate_pattern, row[GATE])):
                    print("usuwany gate")
                    input_list.remove(row)
                    continue
                else:
                    
                    pattern_gate = re.compile(r'\s*E/[0-3]/KD1/[0-9]-[0-9]\s*')
                    matched_gate = re.match( pattern_gate, row[GATE])
                    is_matched_gate = bool(matched_gate)

                    if is_matched_gate is False:
                        raise ValueError(f'Data Gate does not match format: E/[0-3]/KD1/[0-9]-[0-9]')


def get_formated_date(str_date):

    ''' 
    funkcja przyjmuje date jako string w 
    formacie YYYY-MM-DD hh:mm:ss i zwraca
    ja jako obiekt datetime.datetime
    '''

    return datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S ")


def add_all_days_to_collection(input_list, colleciton_of_days):

    '''
    funkcja tworzy obiekt OneDay dla kazdego 
    indywidualnego dnia i dodaje go do klasy 
    kolekcji dni
    '''


    for index in range(len(input_list)):

        batch_obj = BatchOfWork()


        formated_day = get_formated_date(input_list[index][DATE])

        formated_date = formated_day.date()
        
        one_day = OneDay(formated_date)

        if colleciton_of_days.is_date_in_collection(formated_date) is False:
            colleciton_of_days.add_day(one_day)


def substract_datetime(start, end):

    '''
    funkcja odejmujaca od siebie dwie podane godziny,
    zwraca obiekt timedelta
    '''

    tmp_date = date(1,1,1)
    start = datetime.combine( tmp_date, start )
    end = datetime.combine( tmp_date, end )

    return end - start

def timedelta_to_HMS(time_delta_data):

    '''
    funkcja konwertujaca obiekt 'timedelta' (ktory automatycznie wyswiela
    podany czas w optymalnej postaci, tj. jesli jest wiecej niz 24h to
    zaczyna dopisywac dni) w zmienne odpowiadajace konkretnym danym
    czasowym ktore sa umieszczane w formie zwyklego stringa
    ''' 

    w_data = list()     # lista ktora bedzie przechowywac dane o:
    w_hours = 0         # - godzinach
    w_min = 0           # - minutach
    w_sec = 0           # - sekundach
                         

    if time_delta_data.seconds == 0 and time_delta_data.days == 0:
        return "00:00:00"

    if time_delta_data.days == 0 or time_delta_data.days == 1:
        
        w_hours += time_delta_data // timedelta(hours=1)
        w_min += (time_delta_data - timedelta(hours=w_hours)) // timedelta(minutes=1)
        w_sec += (time_delta_data - timedelta(hours=w_hours, minutes=w_min)) // timedelta(seconds=1)


    elif time_delta_data.days > 1:
        for i in range(time_delta_data.days - 1):
            w_hours += time_delta_data // timedelta(hours=1)
            w_min += (time_delta_data - timedelta(hours=w_hours)) // timedelta(minutes=1)
            w_sec += (time_delta_data - timedelta(hours=w_hours, minutes=w_min)) // timedelta(seconds=1)
        
    # wymuszamy format zawsze dwoch cyfr (00:00:00 zamiast 0:0:0)
    f_HMS = f"{w_hours:02}:{w_min:02}:{w_sec:02}"


    return f_HMS




class BatchOfWork:

    """
        klasa dla obiektu kontrolujacego ilosc "parti"
        czasu spedzonego w biurze
    """

    def __init__(self, value=1):
        self.value = value

    def increment(self):
        self.value += 1
    
    def decrement(self):
        self.value -= 1

    def set_value(self, value=1):
        self.value = value

    def get_value(self):
        return self.value

class OneDay:

    def __init__(self, date):
        self.date = date
        self.batches_of_time_in = {}
        self.sum_of_work = timedelta(seconds=0)
        self.flags = {
                'weekend':"",
                'overtime':"", 
                'undertime':"", 
                'inconclusive':"",
                'inconclusive_nv':0,    #non_valid for funcion: 
                                        #           is_this_correct_time
        }
        self.out_of_office = 1
        self.batch_obj = BatchOfWork()


    def set_flag(self, flag):
        if flag == 'weekend':
            self.flags['weekend'] = "w "
        if flag == 'overtime':
                self.flags['overtime'] = "ot "
        if flag == 'undertime':
                self.flags['undertime'] = "ut "
        if flag == 'inconclusive':
                self.flags['inconclusive'] = "i "
        if flag == 'inconclusive_nv':
            self.flags['inconclusive_nv'] += 1 
            
    def unset_flag(self, flag):
        if flag == 'inconclusive_nv':
            self.flags['inconclusive_nv'] -= 1 
        else:
            self.flags[flag] = ""

    def value_of_flag(self, flag):
        return self.flags[flag]
        

    def get_date(self):
        print(self.date)

    def print_data(self):
        print("Data: ", self.date)
        print("Batches: ", self.batches_of_time_in)
        print("Sum of work: ", self.sum_of_work)
        print("Flags: ", self.flags)
        print("Out of office: ", self.out_of_office)
        print("Batch value: ", self.batch_obj.get_value())


class CollectionOfDays():
    
    def __init__(self):
        self.dict_of_all_days = dict()


    def add_day(self, day):
        date = day.date
        self.dict_of_all_days[date] = day
    
    def is_date_in_collection(self, date):
        self.date = date
        if self.date in self.dict_of_all_days.keys():
            return True
        else:
            return False

    def is_this_correct_time(self, now, before):

        '''
        metoda sprawdza poprawnosc wprowadzonych godzin
        w pliku wejsciowym, jesli rozpatrywana godzina
        bedzie "mniejsza" niz poprzednia tego samego dnia
        ustawi flage 'inconclusive'
        '''

        

        now_date = now.date()
        before_date = before.date()

        # czy sa to te same dni
        if now_date == before_date:
            now_time = now.time()
            before_time = before.time()

            # konwersja na typ timedela aby moc porownac aktualnie 
            # rozpatrywana godzine z ostantio rozpatrywana godzine
            
            # formated_time_timedelta
            now_td = timedelta(hours=now_time.hour, minutes=now_time.minute, seconds= now_time.second)
            # last_timedelta
            before_td = timedelta(hours=before_time.hour, minutes=before_time.minute, seconds= before_time.second)
            
            # jesli nie to ustaw flage "inconclusive"
            if now_td < before_td:
                self.dict_of_all_days[now_date].set_flag('inconclusive_nv')
                #raise ValueError(f"Time of day {now_date} - {now_td} is earlier than the previous one : {before_td}")


    def add_entry_hour(self, formated_day):
        '''
        metoda dodaje do konkretnego obiektu OneDay (odpowiadajacego
        rozpatrywanemu dniu) godzine wejsca do biura
        '''
        
        # ograniczenie daty tylko do YYYY-MM-DD
        formated_date = formated_day.date()
        
        # ograniczenie daty tylko do hh:mm:ss
        formated_time = formated_day.time()

        # rozpatrywany dzien, skrocenie zapisu
        day = self.dict_of_all_days[formated_date]

        # indywidualny numer "partii" czasu kazdego dnia
        batch_obj = self.dict_of_all_days[formated_date].batch_obj
        batch_value = batch_obj.get_value()


        #jesli nie ma jeszcze daty na liscie
        if day.batches_of_time_in == {}:
            # obiekt ktorego wartosc oznacza "partie" czasu spedzonego 
            # w biurze zaczynamy od 1 partii, jesli wyjdzie z biura, 
            # zwiekszamy ja o jeden
            batch_obj.set_value(1)
            day.batches_of_time_in[batch_value] = list()
        
        if batch_value in list(day.batches_of_time_in.keys()):
            
            # dodaj ja jako pierwsza
            if day.batches_of_time_in[batch_value] == list():
                

                day.batches_of_time_in[batch_value].append(formated_time)
                day.batches_of_time_in[batch_value].append(formated_time)

                # flaga na 0 - czyli jest w biurze
                day.out_of_office = 0


            # na miejsce czasu WYJŚCIA tymczasowo zapisywany jest 
            # ostatni czas WEJŚCIA, gdyby nie znaleziono zadnego 
            # innego czasu wyjscia to ten zostanie za niego uznany
            else: 
                # ustatawiamy flage 'inconclusive'
                day.set_flag('inconclusive')
                day.batches_of_time_in[batch_value][EXIT] = formated_time
       
        # utworzenie nowej parti godzin spedzonych w biurze
        else:

            day.batches_of_time_in[batch_value] = list()
            
            day.batches_of_time_in[batch_value].append(formated_time)
            day.batches_of_time_in[batch_value].append(formated_time)

            # flaga na 0 - czyli jest w biurze
            day.out_of_office = 0


    def add_exit_hour(self, formated_day, floor_number):
        '''
        metoda dodaje do konkretnego obiektu OneDay (odpowiadajacego
        rozpatrywanemu dniu) godzine wyjscia z biura
        
        '''        
        

        # ograniczenie daty tylko do YYYY-MM-DD
        formated_date = formated_day.date()
            
        # ograniczenie daty tylko do hh:mm:ss
        formated_time = formated_day.time()

        # rozpatrywany dzien, skrocenie zapisu
        day = self.dict_of_all_days[formated_date]

        # indywidualny numer "partii" kazdego dnia
        batch_obj = day.batch_obj
        batch_value = batch_obj.get_value()


        # jesli ta partia czasu znajduje sie w kluczach
        if batch_value in list(day.batches_of_time_in.keys()):
            # jesli lista godzin tej partii nie jest pusta, czyli juz wszedl
            if len(day.batches_of_time_in[batch_value]) != 0:
                # jesli na miejscu godziny wejscia jest odpowiedni typ <datatime.time>
                if type(day.batches_of_time_in[batch_value][ENTRY]) == type(formated_time):

                    
                    # jesli przechodzi przez bramke na parterze
                    if floor_number == str(0):
                        # jesli znajduje sie w biurze
                        if day.out_of_office == 0:
                            
                            # dodaj pierwsza godzine WYJSCIA 
                            day.batches_of_time_in[batch_value][1] = formated_time

                            # po tym wyjsciu z biura, jesli do niego wroci
                            # utworzymy kolejna partie czasu
                            batch_obj.increment()

                            # wyszedl z biura wiec ustawiamy flage na 1
                            day.out_of_office = 1

                            # znaleziono czasy wyjscia wiec mozemy usunac flage
                            # jest to konieczne poniewaz w warunku wyzej profilaktycznie
                            # ja ustawiamy na wypadek gdyby nie byl podany zaden z 
                            # czasow WYJSCIA
                            day.unset_flag('inconclusive')

                else:
                    day.set_flag('inconclusive')
            else:
                day.set_flag('inconclusive')
                #raise ValueError("Nie mozesz wyjsc jak jeszcze nie weszles")
            
        # jesli nie byloby godziny WEJSCIA tego dnia, ale byly WYJSCIA
        else:
            # ustaw flage 'inconclusive'
            day.set_flag('inconclusive')

            batch_obj.set_value(1)

            #stworz nowa liste ktora bedzie przechowywala [czas_rozpoczacia, czas_zakonczenia]
            day.batches_of_time_in[batch_value] = list()
            
            # wypelnij liste najpierw godzina WEJSCIA rowna 00:00:00
            day.batches_of_time_in[batch_value].append(time(second=0))
            # i na drugiej pozycji - faktyczna godzina WYJSCIA 
            day.batches_of_time_in[batch_value].append(formated_time)

            # flaga na 1 - czyli jest poza biurem
            day.out_of_office = 1


    def fill_days_with_worktime(self, input_list):

        '''
        metoda wypelnia wszystkie obiekty OneDay dodane do
        kolekcji godzinami wejscia i wyjscia do/z biura
        podzielonej odpowiednimi partiami
        '''
        
        for row in input_list:

            # konwersja daty z str na datetime.datetime
            formated_day = get_formated_date(row[DATE])
            

            # test czy nastepna godzina tego samego dnia 
            # nie jest "wczesniejsza" od poprzednich
            try:
                self.is_this_correct_time(formated_day, last_day)
            except NameError:
                pass
            
            last_day = formated_day
            

            #jesli jest to godzina WEJSCIA
            if "entry" in row[EVENT]:
                self.add_entry_hour(formated_day)


            # jesli jest to godzina WYJSCIA
            elif "exit" in row[EVENT]:

                # numer pietra na ktorym znajduje sie bramka 
                floor_number = row[GATE][2] 
                self.add_exit_hour(formated_day, floor_number)

    def get_sum_of_time(self):

        '''
        metoda przypisuje atrybutowi sum_of_work rozpatrywanego
        obiektu sume calego czasu spedzonego w biurze tego dnia
        '''

        for day in self.dict_of_all_days.values():
            

            # zmienna odpowiedzialna za przechowanie sumy czasu
            # wszystkich partii pracy
            sum_of_all_batch = timedelta(seconds=0)
            
            # ilosc "partii" w ktorych przebywal w biurze
            number_of_batches = len(list(day.batches_of_time_in.keys()))


            # jesli tego dnia nie przebywal w biurze 
            if number_of_batches == 0:
                day.set_flag('inconclusive')
                day.sum_of_work =  timedelta(seconds = 0)

            # jesli tego dnia przebywal w biurze
            else:
                # wykonaj dla kazdej parti pracy
                for index in range(1,number_of_batches+1):
                    
                    # przypisujemy do zmiennych konkretne godzinowe wartosci wejscia
                    # i wyjscia do/z budynku
                    start_work = day.batches_of_time_in[index][ENTRY]
                    end_work = day.batches_of_time_in[index][EXIT]
                        
                    # suma jednej partii
                    sum_of_one_batch = substract_datetime(start_work, end_work)
                    sum_of_all_batch += sum_of_one_batch

                # zapisujemy w atrybucie sum_of_work konkretnego dnia ilosc czasu spedzonego w biurze
                day.sum_of_work =  timedelta(seconds = sum_of_all_batch.seconds)

    def get_last_days(self):

        '''
        funkcja obliczajaca ktore dni w podanych danych 
        sa ostatnimi dniami danego tygodnia 
        '''

        # Keys: tydzien, Values: ostatni przepracowany 
        #                        dzien w tym tygodniu
        self.dict_of_last_days = dict() 

        # zapisujemy w zmiennej pierwszy rozpatrywany dzien
        last_day = list(self.dict_of_all_days.keys())[0] 

        # zapisujemy numer tygodnia w skali rocznej tego dnia
        week_of_last_day = last_day.isocalendar()[1]

        self.dict_of_last_days[week_of_last_day] = last_day

        for day in self.dict_of_all_days:

            # tydzien w ktorym znajduje sie ostatnio rozpatrywany dzien
            week_of_last_day = last_day.isocalendar()[1] 
            # tydzien w ktorym znajduje sie akutalnie rozpatrywany dzien
            week_of_this_day = day.isocalendar()[1]      

            # jesli rok jest ten sam i jesli tydzien jest ten sam
            if day.year == last_day.year and week_of_last_day ==  week_of_this_day :
                    
                #numer dnia w tygodniu danego dnia jest wiekszy od "ostatniego", np: czwartek > wtorku
                if day.weekday() >= self.dict_of_last_days[week_of_last_day].weekday():
                    # zamien ostatni dzien na aktualnie rozpatrywany pod tym kluczem 
                    self.dict_of_last_days[week_of_last_day] = day
                    # i zmienna last_day ustaw na rozpatrywany dzien
                    last_day = day
                
            else:
                #jesli sa z roznych lat lub roznych tygodni 
                # to stworz nowy klucz z tym dniem
                self.dict_of_last_days[week_of_this_day] = day
                # i przypisz do zmiennej last_day
                last_day = day

    def get_weekly_time_of_work(self, day):

        '''
        metoda obliczajaca ilosc przepracowanego czasu w 
        calym tygodniu od dnia podanego w 'day', ze 
        wszystkich podanych mu dni zapisanych w 
        dict_of_all_days zliczy przepracowany czas od 
        poczatku danego tygodnia pracy (niekoniecznie
        poniedzialku, dowolnie) do konca (rowniez dowolnie)
        '''
    
        counter_of_working_days = 0             

        # zmienna przechowujaca przepracowany 
        # czas w sekundach ustawiona na zero
        self.weekly_time_of_work = timedelta(seconds=0)  
        
        # zmienna wskazuje od jakiego dnia tygodnia 
        # zaczynamy sprawdzac ilosc dni
        days_to_first_working_day = day.weekday()       
        
        # "iterator" po dniach tygodnia
        next_day = timedelta(days=1)

        # rozpatrywany dzien, ustawiony na 
        week_day = day - timedelta(days=days_to_first_working_day)   

        while week_day != (day+next_day):
            
            if week_day in self.dict_of_all_days.keys():

                # zmienna przechowuje ilosc pracy 
                # danego dnia w sekndach
                sum_of_work = self.dict_of_all_days[week_day].sum_of_work 
                
                self.weekly_time_of_work += sum_of_work 

                counter_of_working_days += 1

            week_day = week_day + next_day 

        self.normal_time_of_work = 8 * counter_of_working_days


        
    def setting_flags(self, day):

        '''
        metoda ustawia odpowiednie flagi
        '''

        day = self.dict_of_all_days[day]


        if (day.date.weekday() == 5 or day.date.weekday() == 6):    # jesli dany dzien byl  
            day.set_flag('weekend')                                 # weekendem - dodaj flage 'w'
                                             
        
        if (day.sum_of_work > timedelta(hours=9)):   # jesli przepracowal ponad 9h 
            day.set_flag('overtime')                   # dodaj flage 'ot'
            

        if (day.sum_of_work < timedelta(hours=6)):   # jesli przepracowal mniej niz
            day.set_flag('undertime')                # 6h - dodaj flage 'ut'
            

        if day.flags['inconclusive_nv'] > 0:    # jesli godziny nie byly zapisane
            day.set_flag('inconclusive')        # w pliku "chronologicznie"
            

    def calculate_under_over_time(self):
 
        '''
        metoda oblicza ilosc czasu 
        nadgodzin/niewyrobienia normy 
        przez caly tydzien
        '''

        self.time_under_over = ""

        time_1 = self.weekly_time_of_work        # czas przepracowany

        time_2 = timedelta(hours=self.normal_time_of_work)   # czas ktory powinien byc przepracowany

        if(time_1 == time_2):   # jesli nie przepracowano przepracowano         
            pass                # co do sekundydokladnie tyle ile powinno
                                                    
        # jesli nie przepracowan nawet sekundy (np. blad systemu)
        elif time_1.seconds == 0:
            self.time_under_over = timedelta_to_HMS(time_2)
            self.time_under_over = f"-{self.time_under_over}"


        # jesli sa wyrobione nadgodziny                            
        elif time_1 > time_2:               
            self.time_under_over = time_1 - time_2
            self.time_under_over = timedelta_to_HMS(self.time_under_over)

        # jesli nie wyrobiono normy
        elif time_1 < time_2:               
            self.time_under_over = time_2 - time_1
            self.time_under_over = timedelta_to_HMS(self.time_under_over)
            self.time_under_over = f"-{self.time_under_over}"

    def write_data_to_result(self):

        '''
        metoda otwiera/tworzy plik "result"
        i zapisuje w nim wszystkie obliczone 
        dane wraz z flagami
        '''
        
        with open(OUTPUT, 'w') as result:

            for day in self.dict_of_all_days:
                
                
                # suma pracy calego dnia przekonwertowana z 'timedelta' do formatu: hours:min:sec
                time_of_work = timedelta_to_HMS(self.dict_of_all_days[day].sum_of_work)

                #-----Flagi----
                self.weekly_time_of_work = ""        # puste zmienne-flagi ktore beda wypelnione
                self.normal_time_of_work = ""        # odpowiednimi wartosciami jesli 
                self.time_under_over = ""            # spelnia warunki 

                # Ustawienie odpowiednich wartosci flagom
                self.setting_flags(day)    

                # Przypisanie odpowiednich wartosci zmiennym flag
                weekend = self.dict_of_all_days[day].value_of_flag('weekend')
                overtime = self.dict_of_all_days[day].value_of_flag('overtime')
                undertime = self.dict_of_all_days[day].value_of_flag('undertime')
                inconclusive = self.dict_of_all_days[day].value_of_flag('inconclusive')


                
                
                # Utworzenie slownika z ostantimi dniami tygodnia
                self.get_last_days()

                
                # jesli dzien jest ostatnim dniem tygodnia to zlicz caly przepracowany w nim czas
                if day in self.dict_of_last_days.values():
                    
                    # obliczenie tygodniowego czasu pracy i ilosci godzin ktore powinien przepracowac
                    self.get_weekly_time_of_work(day)
                    
                    # obliczenie czasu nadgodzin/niewyrobienia normy
                    self.calculate_under_over_time()

                    # konwersja z timedelta na string w odpowiednim formacie (bez dni, >24h)
                    self.weekly_time_of_work = timedelta_to_HMS(self.weekly_time_of_work)


                result.write(f"Day {day} Work {time_of_work} {weekend}{overtime}{undertime}{inconclusive} {self.weekly_time_of_work} {self.time_under_over}\n")


    def print_collection(self):
        for obj in self.dict_of_all_days.values():
            obj.print_data()
            print("-"*20)







# -------------------- Koniec funkcji -------------------------



# utworzenie listy elementow
input_list = read_rows_from_input()  


# sprawdzenie poprawnosci wpisanych danych
# np. eliminacja naglowka
validation_of_rows(input_list)  

colleciton_of_days = CollectionOfDays()

add_all_days_to_collection(input_list, colleciton_of_days)

colleciton_of_days.fill_days_with_worktime(input_list) 

colleciton_of_days.get_sum_of_time()

colleciton_of_days.get_last_days()

colleciton_of_days.write_data_to_result()


    