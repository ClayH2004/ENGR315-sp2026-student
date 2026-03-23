import sys


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """
    #Approach:  The data set contains rows of COVID data.  Each row includes the date, county, state, FIPS code, number of cases, and deaths.
    #In order to find the first positive case in both locations, I loop through the data until I find the first row where the number of cases is atleast 1.  
    # Since the data is ordered by date, the first time this condition is met must be the first reported case.
    
    #Loop through every row in the data set
    for (date, county, state, fips, cases, deaths) in data:

        #Check if the row is for Rockingham, Virginia, & if the number of cases is atleast 1
        if cases >= 1 and county == "Rockingham" and state == "Virginia":

            #If this condition is true, print the date
            #Represents the first reported case in Rockingham Virginia
            print("The first positive COVID case in Rockingham County was on", date)
            
            #Stops the loop once the first case is found
            #This ensures the code does not keep searching through the rest of the data
            break
    
    #Same process is used for Harrisonburg
    for (date, county, state, fips, cases, deaths) in data:
        if cases >= 1 and county == "Harrisonburg city" and state == "Virginia":
            print("The first positive COVID case in Harrisonburg was on", date)
            break
    return
    


def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases `recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """
    # your code here
    #Approach: The data set provides the total number of COVID cases for each day.
    #To find the greatest number of new daily cases, I first need to calculate the number of new cases reported each day.
    #This is done by subtracting the previous day's total cases from the current day's total cases.
    #I loop through the data set and only look at rows that correspond to Harrisonburg and Rockingham.
    #I then compare the number of new cases to the current maximum of new cases.
    #If the new value is greater than the current maximum, I update the maximum value and store the corresponding date.
    #After all of the data is looped through, the maximum cases and corresponding date should be stored and printed.
    
    #Placeholder variables
    prev_hburg = None    #Stores the previous day's total cases
    max_hburg = 0        #Stores the maximum number of new cases found so far
    hburg_date = ''      #Stores the date when the maximum number of new cases occurred

   
   #Loops through every row in the data set
    for (date, county, state, fips, cases, deaths) in data:

        #Check if the row corresponds to Harrisonburg, Virginia
        if county == "Harrisonburg city" and state == "Virginia":
            cases = int(cases)    #converts numbers and strings in the cases column into integers

           #Skip the first row to create a previous value used for calculations
            if prev_hburg is not None:

                #Calculate new daily cases by subtracting the previous day's total from the current day's total
                new_cases = cases - prev_hburg

                #Check if this value is larger than the current max
                if new_cases > max_hburg:

                    #Updates the maximum number of new cases
                    max_hburg = new_cases

                    #Stores the date when a new maximum occurs
                    hburg_date = date
        
            #Updates the previous day's case count for the next loop
            prev_hburg = cases
    
    #Print the result
    print("the greatest number of new daily cases recorded in Harrisonburg happened on", hburg_date)

   #Same process is used for Rockingham, Virginia
    prev_rock = None
    max_rock = 0
    rock_date = '' 

    for (date, county, state, fips, cases, deaths) in data:
        if county == "Rockingham" and state == "Virginia":
            cases = int(cases)

            if prev_rock is not None:
                new_cases = cases - prev_rock

                if new_cases > max_rock:
                    max_rock = new_cases
                    rock_date = date
        
            prev_rock = cases
    print("the greatest number of new daily cases recorded in Rockingham happened on", rock_date)

    return

def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    
    # your code here
    #Approach:  To determine the worst 7-day period for new cases, I first calculate the number of new cases reported each day just like I did in the previous question.
    #I store these new case values and their corresponding dates in lists so I can keep track of when each value occurred.
    #I then use a loop to examine every possible 7-day window in the list.
    #I calculate the sum of the next 7 days of cases for each position in the list.
    #If the total is greater than the current max, the maximum value is updated.
    #The date where the 7-day period begins is then stored.

    
    prev_rock = None   #Stores the previous day's case total
    rock_cases = []    #List that stores new daily case counts
    rock_dates = []    #List that stores the corresponding dates to the daily case counts

    for (date, county, state, fips, cases, deaths) in data:
        if county == "Rockingham" and state == "Virginia":
            cases = int(cases)

            if prev_rock is not None:
                new_cases = cases - prev_rock
                
                #Add the daily new cases to the end of the list
                rock_cases.append(new_cases)

                #Add the date associated to the end of the list
                rock_dates.append(date)
            prev_rock = cases
 
    max_rock = 0          #Stores the largest 7-day case count
    max_rock_date = ''    #Stores the start date of the worst 7-day period

    #Loop through the list of daily cases
    #I purposefully subtract 6 so I can add a total of 7 case counts together
    for i in range(len(rock_cases)-6):

        #Sums the case totals over a 7-day window
        total_cases = sum(rock_cases[i:i+7])

        #Check if the total is larger than the current maximum
        if total_cases>max_rock:

            #Update the maximum total
            max_rock = total_cases

            #Stores the starting date of the 7-day period
            max_rock_date = rock_dates[i]

    #Print the result
    print("The worst 7-day period in Rockingham, Virginia started on", max_rock_date)

    return

if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

   ## for (date,county, state, fips, cases, deaths) in data:
  ##      print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)


    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What was the worst seven day period in Harrisonburg for new COVID cases (in terms of absolute number of cases)?
    # What was the worst seven day period in Rockingham County for new COVID cases (in terms of absolute number of cases)?
    third_question(data)


