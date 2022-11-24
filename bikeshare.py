import time
import pandas as pd

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
    # List of available city data
    city_option = ['chicago', 'new york city', 'washington']

    city = str(input('Enter the city you want to investigate (Chicago, New York City or Washington): '))

    # Check if the input is in the list of cities
    while city.lower() not in city_option:
        city = str(input('Please enter one of the follwing cities: Chicago, New York City or Washington '))
    
    print('The city we will be investigating is: {}'.format(city.title()))

    filter_option = ['day', 'month', 'both', 'none']
    filter = str(input('\nWould you like to filter by day, month, both or not at all. Type "none" for not at all: '))

    # Check if the input is in the list of filters
    while filter.lower() not in filter_option:
        filter = str(input('You must enter the correct filter: '))

    print('OK, so you want to filter by {}'.format(filter.title()))   

    day = 'all'
    month = 'all'

    # check filter type
    if filter == 'day':    
        day_option = ['1','2','3','4','5','6','0']
        day = str(input('Enter day number 0-6: '))
    # make sure correct day is entered
        while day not in day_option:
            day = str(input('Enter correct day number 0-6: '))
    # check for month
    elif filter == 'month':
        month_option = ['january', 'february', 'march', 'april', 'may', 'june']
        month = str(input('Enter month January - June: '))
    # make sure correct month is entered
        while month.lower() not in month_option:
            month = str(input('Enter correct month: '))

    elif filter == 'both':
        day_option = ['1','2','3','4','5','6','0']
        day = str(input('Enter day number 0-6: '))
        while day not in day_option:
            day = str(input('Enter correct day number 0-6: '))

        month_option = ['january', 'february', 'march', 'april', 'may', 'june']
        month = str(input('Enter month January - June: '))
        while month.lower() not in month_option:
            month = str(input('Enter correct month: '))
        
    else:
        print('Allright no filters there is')

        print('-'*40)
    print(city, month, day)
   
    return city.lower(), month.lower(), day


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

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month from month_dict
    month_dict = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    common_month = df['month'].mode()[0]
    print('Most common month is {}'.format(month_dict[common_month]))

    day_dict = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4: 'Friday', 5:'Saturday', 6:'Sunday'}
    # display the most common day of week from day_dict
    common_day = df['day_of_week'].mode()[0]
    print('Most common weekday is {}'.format(day_dict[common_day]))

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour is {}'.format(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station is {}'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station is {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    print('Most common trip is to start at {} and end at {}'.format(common_start_station, common_end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    tot_travel_time = df['Trip Duration'].sum()
    tot_travel_time = int(tot_travel_time/3600)
    print('Total travel time is {} hours'.format(tot_travel_time))

    # display mean travel time in minutes
    avg_travel_time = df['Trip Duration'].mean()
    avg_travel_time = int(avg_travel_time/60)
    print('Average travel time is {} minutes'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    count_of_user_type = df.groupby(['User Type'])['User Type'].count()
    print('The number of each type of user can be seen in the table below \n\n{}'.format(count_of_user_type))

    # Display counts of gender
    count_of_gender = df.groupby(['Gender'])['Gender'].count()
    print('\nThe number of each gender can be seen in the table below \n\n{}'.format(count_of_gender))
    # Display earliest, most recent, and most common year of birth
    birth_year_min = int(df['Birth Year'].min())
    
    birth_year_max = int(df['Birth Year'].max())

    common_birth_year = int(df['Birth Year'].mode()[0])
    print('\nThe most common year of birth is {} while the youngest customer is born in {} and the oldest in {}'.format(common_birth_year, birth_year_max, birth_year_min))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    ''' Displays 5 rows of raw data if the user requires '''
    
    raw_data_display = input('\nDo you want to look at the raw data as well, (yes or no)? ')
    n = [0,1,2,3,4] 
    #loop to check if user want to see more data
    while raw_data_display.lower() == 'yes':
        index = 0
        print(df.iloc[n])
    #upate list n to know what rows to show
        while index < len(n) :
            n[index] += 5
            index += 1
        raw_data_display = input('\nDo you want to see another five rows, (yes or no)? ')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        #exclude user stats if city is Washington to avoid error due to lack of data
        if 'Gender' in df: 
            user_stats(df)
        else:
            print('User stats cannot be calculated since the data is missing')
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
