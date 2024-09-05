import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('supermarket_sales.csv', parse_dates=['Date'])

# Create additional columns for analysis
df['Month'] = df['Date'].dt.to_period('M')
df['DayOfWeek'] = df['Date'].dt.day_name()
df['Hour'] = df['Time'].str.split(':').str[0].astype(int)

# Set the style of seaborn
sns.set(style="whitegrid")

# Create a 3x3 grid of subplots
fig, axes = plt.subplots(3, 3, figsize=(20, 18), constrained_layout=True)

# 1. Total Sales Over Time with Rolling Average
daily_sales = df.groupby('Date')['Total'].sum()
rolling_avg = daily_sales.rolling(window=7).mean()

axes[0, 0].plot(daily_sales.index, daily_sales, label='Total Sales', color='blue')
axes[0, 0].plot(rolling_avg.index, rolling_avg, label='7-Day Rolling Average', color='red')
axes[0, 0].set_title('Total Sales Over Time with Rolling Average')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Total Sales ($)')
axes[0, 0].legend()
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Sales by Category
category_stats = df.groupby('Category').agg({'Total': ['sum', 'mean', 'count']})
category_stats.columns = ['Total Sales', 'Average Sales per Transaction', 'Number of Transactions']
category_stats['Percentage Share'] = (category_stats['Total Sales'] / category_stats['Total Sales'].sum()) * 100

sns.barplot(x=category_stats.index, y='Total Sales', data=category_stats, palette='Set2', ax=axes[0, 1])
axes[0, 1].set_title('Total Sales by Product Category')
axes[0, 1].set_xlabel('Product Category')
axes[0, 1].set_ylabel('Total Sales ($)')

# 3. Percentage Share by Category
sns.barplot(x=category_stats.index, y='Percentage Share', data=category_stats, palette='Set2', ax=axes[0, 2])
axes[0, 2].set_title('Percentage Share by Product Category')
axes[0, 2].set_xlabel('Product Category')
axes[0, 2].set_ylabel('Percentage Share (%)')

# 4. Sales by Region and Day of the Week
sns.barplot(x='DayOfWeek', y='Total', data=df, estimator=sum, ci=None, hue='StoreLocation', palette='Set1', ax=axes[1, 0])
axes[1, 0].set_title('Total Sales by Store Location and Day of the Week')
axes[1, 0].set_xlabel('Day of the Week')
axes[1, 0].set_ylabel('Total Sales ($)')

# 5. Sales by Payment Method
payment_stats = df.groupby('PaymentMethod').agg({'Total': ['sum', 'mean']})
payment_stats.columns = ['Total Sales', 'Average Transaction Size']

sns.barplot(x=payment_stats.index, y='Total Sales', data=payment_stats, palette='Set3', ax=axes[1, 1])
axes[1, 1].set_title('Total Sales by Payment Method')
axes[1, 1].set_xlabel('Payment Method')
axes[1, 1].set_ylabel('Total Sales ($)')

# 6. Average Transaction Size by Payment Method
sns.barplot(x=payment_stats.index, y='Average Transaction Size', data=payment_stats, palette='Set3', ax=axes[1, 2])
axes[1, 2].set_title('Average Transaction Size by Payment Method')
axes[1, 2].set_xlabel('Payment Method')
axes[1, 2].set_ylabel('Average Transaction Size ($)')

# 7. Quantity Sold vs. Total Sales with Regression Line
sns.scatterplot(x='Quantity', y='Total', hue='Category', data=df, palette='Set1', alpha=0.7, ax=axes[2, 0])
sns.regplot(x='Quantity', y='Total', data=df, scatter=False, color='black', line_kws={'linewidth': 2}, ax=axes[2, 0])
axes[2, 0].set_title('Quantity Sold vs. Total Sales with Regression Line')
axes[2, 0].set_xlabel('Quantity Sold')
axes[2, 0].set_ylabel('Total Sales ($)')

# 8. Sales Heatmap by Store Location and Date
pivot_table = df.pivot_table(values='Total', index='Date', columns='StoreLocation', aggfunc='sum')
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='.0f', ax=axes[2, 1])
axes[2, 1].set_title('Sales Heatmap by Store Location and Date')
axes[2, 1].set_xlabel('Store Location')
axes[2, 1].set_ylabel('Date')

# 9. Monthly Sales Patterns by Store Location
monthly_pivot_table = df.pivot_table(values='Total', index='Month', columns='StoreLocation', aggfunc='sum')
sns.heatmap(monthly_pivot_table, cmap='YlGnBu', annot=True, fmt='.0f', ax=axes[2, 2])
axes[2, 2].set_title('Monthly Sales Patterns by Store Location')
axes[2, 2].set_xlabel('Store Location')
axes[2, 2].set_ylabel('Month')

# Additional heatmap: Sales by Hour of the Day
hourly_pivot_table = df.pivot_table(values='Total', index='Hour', columns='StoreLocation', aggfunc='sum')
plt.figure(figsize=(14, 10))
sns.heatmap(hourly_pivot_table, cmap='YlGnBu', annot=True, fmt='.0f')
plt.title('Sales by Hour of the Day and Store Location')
plt.xlabel('Store Location')
plt.ylabel('Hour of Day')
plt.show()

plt.show()
