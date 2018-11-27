import time
import statistics
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('Would you like to see data from Chicago, New York City, or Washington?\n')
        if city.lower() in ['chicago','new york city','washington']:
            print('\nLooks like you want to hear about {}! If this is not true, restart the program now!\n'.format(city.title()))
            break
        # get user input for month (all, january, february, ... , june)
    while True:
        month=input('Would you like to filter data by month? You can say january,february,march,april,may or june. Type "all" for no month filter:\n')
        if month.lower() in ['january','february','march','april','may','june']:
            print('\nLet\'s look at data in {}!\n'.format(month.title()))
            break
        elif month.lower()=='all':
            print('\nOK! Month filter will not be applied.\n')
            break
        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Would you like to filter data by day? Type "all" for no day filter:\n')
        if day.lower() in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            print('\nLet\'s look at data on {}s!\n'.format(day.title()))
            break
        elif day.lower()=='all':
            print('\nOK! Day filter will not be applied.\n')
            break
    city=city.lower()
    month=month.lower()
    day=day.lower()
    print('-'*40)
    return city,month,day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    filename=CITY_DATA.get(city)
    df =pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month=statistics.mode(df['month'])
    months=['January','February','March','April','May','June']
    print('\nThe most common month: ',months[most_common_month-1])

    # display the most common day of week
    most_common_day=statistics.mode(df['day_of_week'])
    print('\nThe most common day of week: ',most_common_day)

    # display the most common start hour
    most_common_hour=statistics.mode(df['Start Time'].dt.hour)
    print('\nThe most common start hour: ',most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start=statistics.mode(df['Start Station'])
    print('\nThe most popular start station: ',most_popular_start)

    # display most commonly used end station
    most_popular_end=statistics.mode(df['End Station'])
    print('\nThe most popular end station: ',most_popular_end)

    # display most frequent combination of start station and end station trip
    most_popular_trip=df.groupby(['Start Station','End Station'])['End Station'].count().sort_values().tail(1)

    print('\nThe most popular trip\n',most_popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('\nTotal travel time: ',total_travel_time)
    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('\nMean travel time: ',mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type=df['User Type'].value_counts()
    print('\nUser Types\n',user_type)
    # Display counts of gender
    try:
        user_gender=df['Gender'].value_counts()
        print('\nGender of users\n',user_gender)
    except KeyError:
        print('\nSorry, no data on \"Gender of Users\"  available.\n')
    # Display earliest, most recent, and most common year of birth
    try:
        earlist_birth=df['Birth Year'].min()
        most_recent_birth=df['Birth Year'].max()
        most_common_birth=df['Birth Year'].mode()
        print('\nThe earliest year of birth: {}\nThe most recent year of birth: {}\nThe most common year of birth: {}'.format(int(earlist_birth),int(most_recent_birth),int(most_common_birth[0])))
    except KeyError:
        print('\nSorry, no data on \"Birth Year of Users\" available.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    #Ask the user if they want to see the 5 lines of raw dataself.
    #Prompt the user if they want to see 5 lines of raw data, display that data if the answer is 'yes', and continue these prompts and displays until the user says 'no'.

def view_rawdata(df):
    while True:
        answer=input('\n Would you like to see the first 5 lines of raw data? Enter yes or no.\n')
        if answer.lower()=='no':
            break
        elif answer.lower()=='yes':
            print (df.iloc[0:5])
            count=6
            while True:
                answer=input('\n Would you like to see another 5 lines of raw data? Enter yes or no.\n')
                if answer.lower()=='no':
                    break
                elif answer.lower()=='yes':
                    print (df.iloc[count:count+5])
                    count=count+6

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
