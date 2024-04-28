"""
Write your answers in the space between the questions, and commit/push only
this file (homework2.py) and countries.csv to your repo. Note that there can 
be a difference between giving a "minimally" right answer, 
and a really good answer, so it can pay to put thought into your work. 

This is a much longer project than those you've done in class - remember to use
comments to help readers navigate your work!

To answer these questions, you will use the two csv files provided in the repo.
The file named gdp.csv contains the per capita GDP of many countries in and 
around Europe in 2023 US dollars. The file named population.csv contains 
estimates of the population of many countries.
"""
# Name: Penny Shi #
"""
QUESTION 1

Short: Open the data

Long: Load the GDP data into a dataframe. Specify an absolute path using the Python 
os library to join filenames, so that anyone who clones your homework repo 
only needs to update one string for all loading to work.
"""
import os
os.getcwd()
os.chdir(r"/Users/changgeshi/Desktop/Harris-Python")

# Join paths:
base_path = (r"/Users/changgeshi/Desktop/Harris-Python")
path = os.path.join(base_path, "GDP.csv")

# Import csv documents:
import pandas as pd
df_gdp = pd.read_csv(path)
"""
QUESTION 2

Short: Clean the data

Long: There are numerous issues with the data, on account of it having been 
haphazardly assembled from an online table. To start with, the column containing
country names has been labeled TIME. Fix this.

Next, trim this down to only member states of the European Union. To do this, 
find a list of members states (hint: there are 27 as of Apr 2024) and manually 
create your own CSV file with this list. Name this file countries.csv. Load it 
into a dataframe. Merge the two dataframes and keep only those rows with a 
match.

(Hint: This process should also flag the two errors in naming in gdp.csv. One 
 country has a dated name. Another is simply misspelt. Correct these.)
"""
#Rename the column 
df_gdp.rename(columns = {'TIME':'Country'}, inplace = True) 

df_countries = pd.read_csv('countries.csv')

df_new = df_gdp.merge(df_countries, on= 'Country', how = "right") 

#correct the error in country column of the gdp dataframe
df_gdp.at[5, 'Country'] = 'Czech Republic'
df_gdp.at[14, 'Country'] = 'Italy'
df_new = df_gdp.merge(df_countries, on= 'Country', how = "right") 

"""
QUESTION 3

Short: Reshape the data

Long: Convert this wide data into long data with columns named year and gdp.
The year column should contain int datatype objects.

Remember to convert GDP from string to float. (Hint: the data uses ":" instead
of NaN to denote missing values. You will have to fix this first.) 
"""
# Convert the wide data into long data

df_clean = df_new.melt(id_vars="Country", 
                       var_name="Year", 
                       value_name="GDP")

# Turn year into int datatype 
df_clean["Year"] = df_clean["Year"].map(lambda x: int(x.replace("GDP","")))



## Convert each cell to numeric, coercing non-numeric values to NaN
df_clean["GDP"] = df_clean["GDP"].apply(pd.to_numeric, errors='coerce')

## Convert NaN values to integers
df_clean["GDP"] = df_clean["GDP"].fillna(0).astype(int)
"""  
QUESTION 4

Short: Repeat this process for the population data.

Long: Load population.csv into a dataframe. Rename the TIME columns. 
Merge it with the dataframe loaded from countries.csv. Make it long, naming
the resulting columns year and population. Convert population and year into int.
"""
# Rename the column 
df_pop = pd.read_csv('population.csv')
df_pop.rename(columns = {'TIME':'Country'}, inplace = True)


# Merge the data with countries.csv
df_pop_new = df_countries.merge(df_pop, on= 'Country', how = "left") 
df_pop_complete = df_pop_new.melt(
    id_vars ='Country',
    var_name = 'Year',
    value_name = 'Population')

# Convert the population and year iinto int
df_pop_complete['Year'] =df_pop_complete['Year'].astype(int)

df_pop_complete['Population'] =df_pop_complete['Population'].astype(int)
"""
QUESTION 5

Short: Merge the two dataframe, find the total GDP

Long: Merge the two dataframes. Total GDP is per capita GDP times the 
population.
"""
# Merge the data
df_complete = df_clean.merge(df_pop_complete, on= ['Country','Year'], how = 'left')

# Calculate total GDP
df_complete['Total GDP'] = df_complete['GDP'] * df_complete['Population']

"""
QUESTION 6

Short: For each country, find the annual GDP growth rate in percentage points.
Round down to 2 digits.

Long: Sort the data by name, and then year. You can now use a variety of methods
to get the gdp growth rate, and we'll suggest one here: 

1. Use groupby and shift(1) to create a column containing total GDP from the
previous year. We haven't covered shift in class, so you'll need to look
this method up. Using groupby has the benefit of automatically generating a
missing value for 2012; if you don't do this, you'll need to ensure that you
replace all 2012 values with missing values.

2. Use the following arithematic operation to get the growth rate:
gdp_growth = (total_gdp - total_gdp_previous_year) * 100 / total_gdp
"""
df_complete['Total_GDP_Previous_Year'] = df_complete.groupby('Country')['Total GDP'].shift(1)

# Compute the GPD_Growth
df_complete['GDP_Growth'] = (df_complete['Total GDP'] - df_complete['Total_GDP_Previous_Year'] ) * 100 / df_complete['Total GDP']
df_complete['GDP_Growth'] = df_complete['GDP_Growth'].round(2)

"""
QUESTION 7

Short: Which country has the highest total gdp (for the any year) in the EU? 

Long: Do not hardcode your answer! You will have to put the automate putting 
the name of the country into a string called country_name and using the following
format string to display it:

print(f"The largest country in the EU is {country_name}")
"""

# Find the country with the largest total GDP 
country_name = df_complete.loc[df_complete['Total GDP'].idxmax(), "Country"]

print(f"The country with the largest GDP in the EU is: {country_name}")



"""
QUESTION 8

Create a dataframe that consists only of the country you found in Question 7

In which year did this country have the most growth in the period 2012-23?

In which year did this country have the least growth in the peroid 2012-23?

Do not hardcode your answer. You will have to use the following format strings 
to show your answer:

print(f"Their best year was {best_year}")
print(f"Their worst year was {worst_year}")
"""

# Extract the country from the original dataframe to a new dataframe
Germany_country_df = df_complete[df_complete['Country'] == 'Germany']

# Find the best_year and worst_year
best_year = Germany_country_df.loc[Germany_country_df['GDP_Growth'].idxmax(),"Year"]
print(f"Their best year was {best_year}")

worst_year = Germany_country_df.loc[Germany_country_df['GDP_Growth'].idxmin(),"Year"]
print(f"Their worst year was {worst_year}")
