import time
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

ALL = 13

MONTH_DATA = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec', ALL:'All'}

DAY_DATA = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thurday', 5:'Friday', 6:'Saturday', 7:'Sunday', ALL:'All'}



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
    prompt = '''Select City.
    {}
    Enter a whole number from 1 to 3 corresponding to a city to explore its data.
    1 - Chicago
    2 - New York City
    3 - Washington
    0 - Quit
    --> '''.format('-'*20)
    exitPrompt = '\nThanks for using this app.'
    while True:
        try:
            city = int(input(prompt))
            if city == 0:
                #exit the app
                print(exitPrompt)
                os._exit(0)
            elif city > 3:
                print('xxxx     Invalid city option selected!\n')
                continue
            else:
                break
        except:
            print('xxxx     Not a number!\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    prompt = '''\nSelect Month.
    {}
    Enter a whole number from 1 to 6 corresponding to a month.
    1 - Jan, 2 - Feb, 3 - Mar, 4 - Apr, 5 - May, 6 - Jun, 7 - Jul, 8 - Aug, 9 - Sept, 10 - Oct, 11 - Nov, 12 - Dec, {} - All, 0 - Quit
    --> '''.format('-'*20, ALL)
    while True:
        try:
            month = int(input(prompt))
            if month == 0:
                #exit the app
                print(exitPrompt)
                os._exit(0)
            elif month not in MONTH_DATA:
                print('xxxx     Invalid month option selected!\n')
                continue
            else:
                break
        except:
            print('xxxx     Not a number!\n')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    prompt = '''\nSelect Day.
    {}
    Enter a whole number from 1 to 7 corresponding to a day of the week.
    1 - Mon, 2 - Tues, 3 - Wed, 4 - Thurs, 5 - Fri, 6 - Sat, 7 - Sun, {} - All, 0 - Quit
    --> '''.format('-'*20, ALL)
    while True:
        try:
            day = int(input(prompt))
            if day == 0:
                #exit the app
                print(exitPrompt)
                os._exit(0)
            elif day not in DAY_DATA:
                print('xxxx     Invalid day option selected!')
                continue
            else:
                break
        except:
            print('xxxx     Not a number!')

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
    city_name = ''
    for i, city_names in enumerate(CITY_DATA):
        if i == city - 1:
            city_name = city_names
            break
    try:
        data = pd.read_csv(CITY_DATA[city_name])
        df = pd.DataFrame(data)
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month from the Start Time column to create a month column
        df['month'] = df['Start Time'].dt.month

        # extract day of week from the Start Time column to create a day_of_week column
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # extract hour from the Start Time column to create an start_hour column
        df['start_hour'] = df['Start Time'].dt.hour

        #fill NA for gender with 'Other'
        if 'Gender' in df.columns:
            df['Gender'] = df['Gender'].fillna('Other')

        return df, city_name
    except FileNotFoundError:
        raise FileNotFoundError('File for {} not found.'.format(city_name.title()))

def time_stats(df, city_name, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Selected month:\n \t{}.'.format(MONTH_DATA[month]))
    print('Most common travel month for {}:\n \t{}'.format(city_name, MONTH_DATA[popular_month]))

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Selected day:\n \t{}.'.format(DAY_DATA[day]))
    print('Most common travel day for {} {}:\n \t{}'.format(city_name, 'for ' + MONTH_DATA[month] + ' months' if month == ALL else 'for month ' + MONTH_DATA[month], popular_day_of_week))

    # TO DO: display the most common start hour
    popular_start_hour = df['start_hour'].mode()[0]
    print('Most common travel start hour for {}:\n \t{}'.format(city_name, popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common travel start station:\n \t{}'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common travel end station:\n \t{}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    route = df['Start Station'] + ' to ' + df['End Station']
    popular_route = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('Most common travel route:\n \t{}'.format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:\n \t{}'.format(total_travel_time))


    # TO DO: display mean travel time
    print("\nAverage Trip duration:")
    print('\t', df['Trip Duration'].mean())

    # Population (ddof=0) Standard deviation of Trip duration
    print("\nStandard deviation of Trip duration:")
    print('\t', df['Trip Duration'].std(ddof=0))


    # Population (ddof=0) Average of Trip duration per month
    print("\nAverage and Standard deviation of Trip duration per month:")
    trip_duration_month = df.groupby(['month'])['Trip Duration']
    print('\tMonth\tAverage\t\tStd Dev')
    for month, data in trip_duration_month:
        mean = round(data.mean(),2)
        std =round(data.std(),2)
        print('\t', MONTH_DATA[month], '\t', mean, '\t', std if std == std else '')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Users by type:")
    user_type_count = df.groupby(['User Type'])['User Type']
    for user_type, data in user_type_count:
        print('\t', user_type, ' = ', data.count())

    if 'Gender' in df.columns:
        # TO DO: Display counts of gender
        print("\nUsers by gender:")
        user_gender_count = df.groupby(['Gender'])['Gender']
        for gender, data in user_gender_count:
            print('\t', gender, ' = ', data.count())

        # Average Trip duration by gender
        print("\nAverage Trip duration by gender:")
        travel_time_gender = df.groupby(['Gender'])['Trip Duration']
        for gender, data in travel_time_gender:
            print('\t', gender, ' = ', data.mean())

        # Sample (ddof=1 or ignore) Standard deviation of Trip duration by gender
        print("\nStandard deviation of Trip duration by gender:")
        #travel_time_gender = df.groupby(['Gender'])['Trip Duration']
        for gender, data in travel_time_gender:
            print('\t', gender, ' = ', data.std(ddof=1))

    if 'Birth Year' in df.columns:
        # TO DO: Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth:\n \t{}'.format(int(df['Birth Year'].min())))
        print('Most recent year of birth:\n \t{}'.format(int(df['Birth Year'].max())))
        common_years = df['Birth Year'].mode().values
        print('Most common year of birth:'.format())
        for year in common_years:
            print('\t', int(year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        try:
            df, city_name = load_data(city, month, day)

            time_stats(df, city_name.title(), month, day)

            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except FileNotFoundError as ferr:
            print(ferr)
        restart = input('\nWould you like to restart? Enter yes(y) or no(n).\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
