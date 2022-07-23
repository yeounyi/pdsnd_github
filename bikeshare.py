import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DICT = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in ['chicago','new york city', 'washington']:
        city = input('Choose a city: ', ).lower()
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while month not in ['all','january', 'february','march','april','may','june']:
        month = input('Choose a month from january to june: ', ).lower()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ['all','monday', 'tuesday', 'wednesday','thursday','friday','saturday','sunday']:
        day = input('Choose a day from monday to sunday: ', ).lower()
    
    # print(city, month,day)

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.day_name().lower())
    
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_DICT[month]
        # filter by month to create the new dataframe
        df = df.query('month==@month')


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.query('day_of_week==@day')
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print(df.head())
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('the most common month: ', df.month.value_counts().idxmax())

    # TO DO: display the most common day of week
    print('the most common day of week: ', df.day_of_week.value_counts().idxmax().title())

    # TO DO: display the most common start hour
    print('the most common start hour: ', df.hour.value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('the most commonly used start station: ', df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('the most commonly used end station: ', df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    # reference: https://stackoverflow.com/questions/63229237/finding-the-most-frequent-combination-in-dataframe
    print('the most frequent combination of start station and end station trip: ', df.groupby('Start Station')['End Station'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('total travel time: ', total_travel_time)

    # TO DO: display mean travel time
    print('mean travel time: ', total_travel_time / df.shape[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('counts of user types: ', df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' not in df.columns:
        print('Gender info is not available')
    else:
        print('counts of gender: ', df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('Birth year info is not available')
    else:
        earliest = df['Birth Year'].min() 
        most_recent = df['Birth Year'].max() 
        most_common = df['Birth Year'].value_counts().idxmax()
        print('earliest year of birth: ', earliest)
        print('most recent year of birth: ', most_recent)
        print('most common year of birth: ', most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if len(df) == 0:
            print('No data')
            print('-'*40)
        
        else:
            # displaying raw data 
            start_row = 0
            check_raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            while check_raw.lower() == 'yes':
                print(df.iloc[start_row:start_row+5,:])
                start_row += 5 
                check_raw = input('\nWould you like to see the next 5 lines of raw data? Enter yes or no.\n')

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()