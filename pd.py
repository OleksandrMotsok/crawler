import pandas as pd
from statistics import mean

df = pd.read_csv('Automobile_data.csv')
print(df)

# first and last five rows
print(df.head(5))
print(df.tail(5))

# Replace all column values which contain ‘?’ and n.a with NaN.
print(df.replace(['?', 'n.a'], 'NaN'))

# Print most expensive car’s company name and price
index = df['price'].argmax()
print(df.loc[[index], ['company', 'price']])
df.reset_index()

# Print All Toyota Cars details
print(df.loc[df['company'] == 'toyota'])
df.reset_index()

# Count total cars per company
print(df['company'].value_counts())

# Find each company’s Highest price car
companies = df['company'].unique()
for company in companies:
    l_price = ["Max for company:", company, str(df.loc[df['company'] == company]['price'].max())]
    print(" ".join(l_price))

df.reset_index()

# Find the average mileage of each car making company
for company in companies:
    l_average = ["Average for company:", company, str(df[df['company'] == company]['price'].mean())]
    print(" ".join(l_average))

# Sort all cars by Price column
df.sort_values(by='price', inplace=True)
print(df)

# Create two data frames using the following two Dicts, Concatenate those two data frames and create a key for each
# data frame:
GermanCars = {'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'], 'Price': [23845, 171995, 135925, 71400]}
JapaneseCars = {'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi '], 'Price': [29995, 23600, 61500, 58900]}

dfGermanCars = pd.DataFrame(data=GermanCars)
dfJapaneseCars = pd.DataFrame(data=JapaneseCars)

dfRes = pd.concat([dfGermanCars, dfJapaneseCars], ignore_index=True)
print(dfRes)

# Create two data frames using the following two Dicts, Merge two data frames, and append second data frame as a new
# column to the first data frame.
Car_Price = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'Price': [23845, 17995, 135925, 71400]}
Car_Horsepower = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'horsepower': [141, 80, 182, 160]}

dfPrice = pd.DataFrame(data=Car_Price)
dfHorsepower = pd.DataFrame(data=Car_Horsepower)
dfResMerge = pd.merge(dfPrice, dfHorsepower, how='inner', on='Company')

print(dfResMerge)