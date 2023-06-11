import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from plotly.subplots import *
from datetime import *
import time as t
import pandas as pd

st.set_page_config (page_title='Covid App',page_icon='covid-19.png',layout="wide",initial_sidebar_state="expanded")

#data in csv file
data=pd.read_csv('covid_19_india.csv',index_col=0)
V_data=pd.read_csv('covid_vaccine_statewise.csv',index_col=0)

#Adding a new column
data['Active_Cases']= data['Confirmed']-(data['Cured']+data['Deaths'])

#States affected by Covid_19
top_10 = data.groupby(by='State/UnionTerritory').max()[['Active_Cases', 'Date']].sort_values(['Active_Cases'], ascending=False).reset_index()
fig = px.bar(top_10.iloc[:10], x='State/UnionTerritory', y='Active_Cases', labels={'State/UnionTerritory': 'States', 'Active_Cases': 'Active Cases'})
fig.update_layout(title="Top 10 States Affected by COVID-19", xaxis_title="States", yaxis_title="Active Cases")


#States with Highest Deaths Due To Covid_19
top_1 = data.groupby(by='State/UnionTerritory').max()[['Deaths', 'Date']].sort_values(['Deaths'], ascending=False).reset_index()

fig1 = plt.figure(figsize=(16, 9))
plt.title("Top 12 States with Highest Deaths due to COVID-19")
df1 = sns.barplot(data=top_1.iloc[:12], y='Deaths', x="State/UnionTerritory", linewidth=2, edgecolor='white')
plt.xlabel("States")
plt.ylabel("Deaths")

#linechart of Deaths
fig2=plt.figure(figsize=(12,6))
df=sns.lineplot(data = data[data['State/UnionTerritory'].isin(['Telangana','Karnataka','Kerala'])], x = data['Date'], y = 'Active_Cases',hue = 'State/UnionTerritory')
df.set_title('line plot' ,size=16)

#Data for Vaccination

#changing the column Name
V_data.rename(columns = {'Updated On' : 'Vaccine_date'} ,inplace=True)
V_data.rename(columns={'Total Individuals Vaccinated':'Total'},inplace=True)

#pie chart for males and females vaccinated
male=V_data["Male(Individuals Vaccinated)"].sum()
female=V_data["Female(Individuals Vaccinated)"].sum()
others=V_data["Transgender (Doses Administered)"].sum()
fig3=px.pie(names=["Male(Individuals Vaccinated)","Female(Individuals Vaccinated)","Transgender (Doses Administered)"],values=[male,female,others],title="males and females vaccinated")


#deleting the india row snice we are visualizing the vaccinated States and Sorted value to 5 indexes.  
V_data=V_data[V_data.State!='India']
vac=V_data.groupby('State')['Total'].sum().to_frame('Total')
vac=vac.sort_values('Total',ascending=False)[:5]

#Most vaccinated States in India.
fig4 = plt.figure(figsize=(10, 4))
plt.title("Most Vaccinated States")
V_data = sns.barplot(data=vac[:5], y=vac['Total'], x=vac.index, linewidth=2, edgecolor='white')
plt.xlabel("States")
plt.ylabel("Vaccinated")





st.markdown("<h1 style='text-align: center; color:white;'>Covid_19 Data Visualization App</h1>"
            "<h6 style='text-align: center; color: white;'>Data collected from the <a href=https://www.kaggle.com/datasets>[kaggle]</a></h6>"
            "<h6 style='text-align: center; color: white;'>1.Covid_Cases Visualization</h6>"
            "<h6 style='text-align: center; color: white;'>2.Covid_Vaccines Visualization</h6>"
            "<h6 style='text-align: center; color: white;'>3.Covid_Deaths Visualization</h6>"
, unsafe_allow_html=True)

'---'




#creating the sidebar for Covid-19
st.sidebar.markdown('''# :center[Covid_19 Data Visualization]''')
opt=st.sidebar.selectbox('****',options=('Covid_Cases','Covid_Vaccines','Covid_Deaths'))
st.sidebar.markdown('''# :black[Data visualization On Covid_19]
To display the number of deaths happened, the number of people Vaccinated, and current active cases in India.''')

if opt=='Covid_Cases':
    with st.spinner('Loading'):
       t.sleep(0.3)
    st.balloons()
    st.markdown(opt)
    st.info('''States affected by Covid-19''',icon='📌')
    st.plotly_chart(fig)
    st.success('Success!')

elif opt=="Covid_Vaccines":
    with st.spinner('Loading'):
       t.sleep(0.3)
  
    st.write(opt)
    st.info('''Vaccinated Individuals''',icon='👉')
    st.plotly_chart(fig3)
    st.info('''Most Vaccinated States''',icon='👉')
    st.pyplot(fig4)
    st.success('Success!')
    
elif opt=="Covid_Deaths":
     with st.spinner('Loading'):
       t.sleep(0.3)
     st.balloons()
     st.markdown(opt)
     st.info('''States  With Highest Deaths Due To Covid-19''',icon='🪄')
     st.pyplot(fig1)
     st.info('''States  With Highest Deaths Due To Covid-19 using Line Plot''',icon='🪄')
     st.pyplot(fig2)
     st.success('Success!')

else:
    pass