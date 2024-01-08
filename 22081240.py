#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter



def format_ticks(value, _):
    """
    Function to Formate the X-ticks and Y-ticks
    Parameters
    ----------
    value : integer
        Value to convert into K or M.
    _ : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        Returnng the String back.

    """
    if value >= 1e6:
        return f'{value / 1e6:.2f}M'
    elif value >= 1e3:
        return f'{value / 1e3:.0f}K'
    else:
        return str(value)
    
# Importing the Data Frames
natural_disasters = pd.read_csv('natural-disasters-decade.csv')
natural_disasters.head()
natural_disasters = natural_disasters[['Country name','Year','Number of deaths from drought','Number of deaths from earthquakes','Number of deaths from floods','Number of deaths from storms','Homelessness rate from drought','Homelessness rate from earthquakes','Homelessness rate from floods','Homelessness rate from storms']]

natural_disasters_deaths = natural_disasters[['Country name','Year','Number of deaths from drought','Number of deaths from earthquakes','Number of deaths from floods','Number of deaths from storms']]
w_natural_disasters_deaths = natural_disasters_deaths[natural_disasters_deaths['Country name']=='World']
w_natural_disasters_deaths = w_natural_disasters_deaths.drop('Country name', axis=1)
w_natural_disasters_deaths.head()

fig, axs = plt.subplots(2, 2, figsize=(20, 10))
# Ploting the Line Graph
s = 1
Types_natural_disasters = list(w_natural_disasters_deaths.columns)[1:]
for i in Types_natural_disasters:
    sns.lineplot(x=w_natural_disasters_deaths['Year'],
                 y=w_natural_disasters_deaths[i],
                 label=i,
                 ax=axs[0,
                        0],
                 linestyle='solid',
                 marker = 's',
                 color=sns.color_palette('tab20')[s])
    s += 1

# Setting Labels legends and their face color.
axs[0, 0].set_ylabel('Deaths Per Decade')
axs[0, 0].set_xlabel('Years')
axs[0, 0].set_facecolor('azure')
axs[0, 0].legend(facecolor='azure')
axs[0, 0].set_title(
    'Global Decadal Fatalities: Floods, Storms, Droughts and Earthquakes (1900-2020)')
axs[0, 0].yaxis.set_major_formatter(FuncFormatter(format_ticks))

Countries_natural_disasters_deaths = natural_disasters_deaths.groupby('Country name').sum().reset_index()
Countries_most_deaths_by_drought = Countries_natural_disasters_deaths[['Country name','Number of deaths from drought']]
Countries_most_deaths_by_drought = Countries_most_deaths_by_drought.sort_values(by='Number of deaths from drought', ascending=False)
Countries_most_deaths_by_drought = Countries_most_deaths_by_drought.head(20)
Countries_most_affected = ['Sudan','Ethiopia','India','China','Mozambique','Indonesia']
Countries_most_deaths_by_drought = Countries_most_deaths_by_drought[Countries_most_deaths_by_drought['Country name'].isin(Countries_most_affected)]
df_sorted = Countries_most_deaths_by_drought.sort_values(by='Number of deaths from drought', ascending=False)
df_sorted['Number of deaths from drought (K)'] = df_sorted['Number of deaths from drought'] / 1000
Countries_natural_disasters_deaths = natural_disasters_deaths[natural_disasters_deaths['Country name'].isin(Countries_most_affected)]
Countries_natural_disasters_deaths = Countries_natural_disasters_deaths.groupby('Country name').sum().reset_index()
Countries_natural_disasters_deaths = Countries_natural_disasters_deaths.drop('Year',axis=1)
Countries_natural_disasters_deaths.head(7)

# Create a horizontal bar chart using Seaborn
barplot = sns.barplot(x='Number of deaths from drought (K)', y='Country name', data=df_sorted, color='skyblue', ax= axs[0,1])

# Display values on the bars
for index, value in enumerate(df_sorted['Number of deaths from drought (K)']):
    barplot.text(value, index, f'{value:.1f}K', ha='left', va='center', color='black', fontweight='bold')
axs[0, 1].set_xlabel('Deaths')
axs[0, 1].set_facecolor('azure')
axs[0, 1].set_title(
    'Countries with Most Number of Deaths From Drought (1900-2020)')

home_less_rate = natural_disasters[['Country name','Year','Homelessness rate from earthquakes','Homelessness rate from floods','Homelessness rate from storms']]
w_home_less_rate = home_less_rate[home_less_rate['Country name']=='World']
w_home_less_rate= w_home_less_rate.drop('Country name', axis=1)

s = 1
Types_natural_disasters = list(w_home_less_rate.columns)[1:]
for i in Types_natural_disasters:
    sns.lineplot(x=w_home_less_rate['Year'],
                 y=w_home_less_rate[i],
                 label=i,
                 ax=axs[1,
                        0],
                 linestyle='solid',
                 marker = 's',
                 color=sns.color_palette('tab20')[s])
    s += 1
# Setting Labels legends and their face color.
axs[1, 0].set_ylabel('Percentage Home Less Rate')
axs[1, 0].set_xlabel('Years')
axs[1, 0].set_facecolor('azure')
axs[1, 0].legend(facecolor='azure')
axs[1, 0].set_title(
    'Global Home Less Rates Beacause of Floods, Storms and Earthquakes (1900-2020)')
axs[1, 0].yaxis.set_major_formatter(FuncFormatter(format_ticks))
deaths_by_earthquakes = natural_disasters[['Country name','Year','Number of deaths from earthquakes']]
deaths_by_earthquakes = deaths_by_earthquakes[deaths_by_earthquakes['Year']>1970]
deaths_by_earthquakes = deaths_by_earthquakes.groupby('Country name').sum().reset_index()
deaths_by_earthquakes = deaths_by_earthquakes.sort_values(by='Number of deaths from earthquakes', ascending=False)
Countries_most_affected = ['Haiti','Indonesia','Pakistan','Turkey','China','Iran','India']
world = deaths_by_earthquakes['Number of deaths from earthquakes'][deaths_by_earthquakes['Country name']=='World']
deaths_by_earthquakes = deaths_by_earthquakes[deaths_by_earthquakes['Country name'].isin(Countries_most_affected)]
deaths_by_earthquakes = deaths_by_earthquakes.drop('Year', axis=1)
world = 103115.3
total_deaths = deaths_by_earthquakes['Number of deaths from earthquakes'].sum()
total_deaths
others = world - total_deaths
others
new_value_col1 = 'others'
new_value_col2 = others
deaths_by_earthquakes.at[0, 'Country name'] = new_value_col1
deaths_by_earthquakes.at[0, 'Number of deaths from earthquakes'] = new_value_col2
deaths_by_earthquakes['Ratio by World']=(deaths_by_earthquakes['Number of deaths from earthquakes'] / world)*100
label = list(deaths_by_earthquakes['Country name'])
values = list(deaths_by_earthquakes['Ratio by World'])
explode = (0, 0, 0.0, 0.0, 0.0,0,0,0)
axs[1, 1].pie(values, labels=label, autopct='%1.1f%%',
              startangle=90, colors=sns.color_palette('tab20'), explode=explode)
# Add a circle in the center to make it look like a donut chart (optional)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
axs[1, 1].set_facecolor('azure')
axs[1, 1].legend(facecolor='azure')
fig.gca().add_artist(centre_circle)

# Set aspect ratio to be equal to ensure a circular pie chart
axs[1, 1].axis('equal')

# Add a title
axs[1, 1].set_title(
    'Ratio of Deaths By Earthquakes Percentage Distribution among Countries since 1990')

fig.patch.set_facecolor('azure')
# Adding the Title to Infographic
plt.suptitle(
    'Global Natural Disasters Impact: Deaths, Decadal Fatalities, Homelessness, and Earthquake Patterns (1900-2020)',
    fontsize=24,
    weight='bold')
sns.despine(left=True, right=True, top=True, bottom=True)
plt.gcf().text(0.5, 0.93, 'Usama Saif - 22081240', ha='center', fontsize=16)
# adding the Text to the Graphics
description_text = (
    "The analysis of 'Global Decadal Fatalities: Floods, Storms,  "
    "Droughts, and Earthquakes (1900-2020)' reveals a historical shift in natural disaster impacts.\n"
    "Droughts and earthquakes claimed numerous lives in the 20th century "
    "while floods and storms surged in the 21st century beacuse of climate change linked to industrialization\n"
    "India, China, and Ethiopia witnessed the highest deaths from drought. "
    "Homelessness peaked due to floods and storms, affecting 80% and 40% of the global population from 1980 to 2000,\n"
    "The pie chart highlights Haiti, Indonesia, and Turkey as earthquake-affected "
    "hotspots, representing 22%, 18%, and 14% of global seismic impacts\n")

fig.text(0.5, -0.11, description_text, ha="center", va="center", fontsize=16,
         bbox=dict(facecolor='azure', edgecolor='white',
                   boxstyle='round,pad=0.5'))
# Saving the Picture of the graphics
plt.savefig('22081240.png', bbox_inches='tight', pad_inches=0.5, dpi=300)
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[180]:





# In[ ]:





# In[186]:





# In[ ]:





# In[ ]:





# In[134]:





# In[115]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




