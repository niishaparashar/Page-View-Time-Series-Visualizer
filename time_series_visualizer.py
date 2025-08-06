import pandas as pd

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data: filter out top and bottom 2.5% of page views
low = df['value'].quantile(0.025)
high = df['value'].quantile(0.975)
df_clean = df[(df['value'] >= low) & (df['value'] <= high)]


import matplotlib.pyplot as plt

def draw_line_plot():
    df_line = df_clean.copy()
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.tight_layout()
    # plt.savefig('path/to/image.png')  # for saving the image
    return fig


def draw_bar_plot():
    # Prepare data for bar plot
    df_bar = df_clean.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    fig = df_grouped.plot(kind='bar', figsize=(12,8)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()
    return fig


import seaborn as sns

def draw_box_plot():
    df_box = df_clean.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    fig, axes = plt.subplots(1, 2, figsize=(18,6))

    # Year-wise boxplot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise boxplot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()
    return fig
