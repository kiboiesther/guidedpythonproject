import pandas as pd
df = pd.read_csv('owid-covid-data.csv')

# Filter for countries of interest
countries_of_interest = ['Kenya', 'United States', 'India']
filtered_df = df[df['location'].isin(countries_of_interest)]

# Drop rows with missing dates or critical values (e.g., total_cases, total_deaths)
critical_columns = ['date', 'total_cases', 'total_deaths']
filtered_df = filtered_df.dropna(subset=critical_columns)

# Convert date column to datetime
filtered_df['date'] = pd.to_datetime(filtered_df['date'])

# Handle missing numeric values with fillna() or interpolate()
numeric_cols = filtered_df.select_dtypes(include='number').columns
filtered_df[numeric_cols] = filtered_df[numeric_cols].interpolate().fillna(0)

print(filtered_df.columns)
print(filtered_df.head())
print(filtered_df.isnull().sum())

#line chart of 'cases' and 'deaths' over time for each country
import matplotlib.pyplot as plt
plt.figure(figsize=(14, 8))
for country in countries_of_interest:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=f'{country} - Cases')
    plt.plot(country_data['date'], country_data['total_deaths'], label=f'{country} - Deaths')   
    plt.title(f'COVID-19 Cases and Deaths Over Time in {country}')
    plt.xlabel('Date')  
    plt.ylabel('Count')
    plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Bar chart of 'top countries' by ' total cases'
top_countries = filtered_df.groupby('location')['total_cases'].max().nlargest(10).index
top_data = filtered_df[filtered_df['location'].isin(top_countries)] 
top_data = top_data.groupby('location')['total_cases'].max().reset_index()
plt.figure(figsize=(12, 6))
plt.bar(top_data['location'], top_data['total_cases'], color='skyblue')
plt.title('Top 10 Countries by Total COVID-19 Cases')
plt.xlabel('Country')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# heatmap of 'cases' and 'deaths' correlation
import seaborn as sns
plt.figure(figsize=(10, 6))
correlation_matrix = filtered_df[['total_cases', 'total_deaths']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f') 
plt.title('Correlation Heatmap of Total Cases and Total Deaths')
plt.show()

# Plot cumulative vaccinations over time for selected countries
plt.figure(figsize=(14, 8))
for country in countries_of_interest:
    country_data = filtered_df[filtered_df['location'] == country]
    if 'total_vaccinations' in country_data.columns:
        plt.plot(country_data['date'], country_data['total_vaccinations'], label=f'{country} - Vaccinations')
plt.title('Cumulative COVID-19 Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Compare % vaccinated population (people_fully_vaccinated_per_hundred)
plt.figure(figsize=(10, 6))
for country in countries_of_interest:
    country_data = filtered_df[filtered_df['location'] == country]
    if 'people_fully_vaccinated_per_hundred' in country_data.columns:
        plt.plot(
            country_data['date'],
            country_data['people_fully_vaccinated_per_hundred'],
            label=f'{country}'
        )
plt.title('Percentage of Population Fully Vaccinated Over Time')
plt.xlabel('Date')
plt.ylabel('Fully Vaccinated (% of Population)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
