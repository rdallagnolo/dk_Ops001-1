import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

# Read in the dummy dataset
df = pd.read_csv("Ops001-1_data.csv",parse_dates=["Date"])

# Split the dummy dataset by graphs 
# droping 'Grand Total' and Regions
branch = df.drop(labels=[6,13,18,25,27,33,34],axis=0)

# only regions
region = df.iloc[[6,13,18,25,27,33]]

# grand total
total = df.iloc[[34]]

##### The dashboard
st.set_page_config(layout="wide")           # wide layout

with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white '>Area and branch wise daily updates</h1>", unsafe_allow_html=True)

# Adding a side bar with 
st.sidebar.markdown("<h1 style='text-align: center; color: white '>Pick the day</h1>", unsafe_allow_html=True)

d=st.sidebar.date_input(label="",value=datetime.date.today())
#col1, col2  = st.columns(2)



##################################################################
# BY Branch
##################################################################
fig = go.Figure(data=[
    go.Bar(name='# of drop', y=branch['Branch Name'], x=branch['# of drop'],
           orientation='h',text=branch['# of drop'],
           marker_color='rgb(45, 139, 186)'),
    go.Bar(name='# of partial', y=branch['Branch Name'], x=branch['# of partial'],
           orientation='h',text=branch['# of partial'],
           marker_color='rgb(108, 230, 232)'),
    go.Bar(name='Yesterday paid off #', y=branch['Branch Name'], x=branch['Yesterday paid off #'],
           orientation='h',text=branch['Yesterday paid off #'],
           marker_color='rgb(47, 94, 152)'),
    go.Bar(name='Today disbursed #', y=branch['Branch Name'], x=branch['Today disbursed #'],
           orientation='h',text=branch['Today disbursed #'],
           marker_color='rgb(49, 53, 110)'),
    go.Bar(name='# of irregular borrower', y=branch['Branch Name'], x=branch['# of irregular borrower'],
           orientation='h',text=branch['# of irregular borrower'],
           marker_color='rgb(5, 183, 213)'),
    go.Bar(name='Virtual new borrower', y=branch['Branch Name'], x=branch['Virtual new borrower'],
           orientation='h',text=branch['Virtual new borrower'],
           marker_color='rgb(150, 108, 152)'),
    go.Bar(name='Returning', y=branch['Branch Name'], x=branch['Returning'],
           orientation='h',text=branch['Returning'],)
])


# chart layout
fig.update_layout(barmode='stack',height=750, width=750,
                  paper_bgcolor='rgb(38, 39, 48)',
                  plot_bgcolor='rgb(38, 39, 48)',
                  font_color='rgb(199, 208, 216)',
                  margin=dict(l=50, r=20, t=20, b=20,pad=20),
                  xaxis = dict(tickfont = dict(size=15)),
                  yaxis = dict(tickfont = dict(size=15)))

fig.update_xaxes(categoryorder='category ascending', gridcolor='gray')
fig.update_yaxes(autorange="reversed",showline=False)
fig.update_traces(marker_line_width=0, textposition='inside')

# legend
fig.update_layout(legend=dict(
       orientation="h",
       yanchor="bottom",
       y=1.05,
       xanchor="left",
       x=0,
       font_size=15))


##################################################################
# BY REGION
##################################################################
fig2 = go.Figure(data=[
    go.Bar(name='# of drop', x=region['Branch Name'], y=region['# of drop'],
           marker_color='rgb(45, 139, 186)',text=region['# of drop']),
    
    go.Bar(name='# of partial', x=region['Branch Name'], y=region['# of partial'],
           marker_color='rgb(108, 230, 232)',text=region['# of partial']),
    
    go.Bar(name='Yesterday paid off #', x=region['Branch Name'], y=region['Yesterday paid off #'],
           marker_color='rgb(47, 94, 152)',text=region['Yesterday paid off #']),
    
    go.Bar(name='Today disbursed #', x=region['Branch Name'], y=region['Today disbursed #'],
           marker_color='rgb(49, 53, 110)',text=region['Today disbursed #']),
    
    go.Bar(name='# of irregular borrower', x=region['Branch Name'], y=region['# of irregular borrower'],
           marker_color='rgb(5, 183, 213)',text=region['# of irregular borrower']),
    
    go.Bar(name='Virtual new borrower', x=region['Branch Name'], y=region['Virtual new borrower'],
           marker_color='rgb(150, 108, 152)',text=region['Virtual new borrower']),
    
    go.Bar(name='Returning', x=region['Branch Name'], y=region['Returning'],
          text=region['Returning'])
])

# chart layout
fig2.update_layout(barmode='stack',height=750, width=500,
                  paper_bgcolor='rgb(38, 39, 48)',
                  plot_bgcolor='rgb(38, 39, 48)',
                  font_color='#c7d0d8',
                  margin=dict(l=20, r=20, t=20, b=20, pad=20),
                  xaxis = dict(tickfont = dict(size=15),tickangle=45),
                  yaxis = dict(tickfont = dict(size=15)))

fig2.update_yaxes(gridcolor='gray')

# legend
fig2.update_layout(legend=dict(
       orientation="h",
       yanchor="bottom",
       y=1.05,
       xanchor="left",
       x=0.0,
       font_size=15))

# remove line
fig2.update_traces(marker_line_width=0)

##################################################################
# Grand Total 
##################################################################
n_of_drops = total.loc[34,'# of drop']
n_of_partial = total.loc[34,'# of partial']
yesterday_paid = total.loc[34,'Yesterday paid off #']
today_disbursed = total.loc[34,'Today disbursed #']
n_irregulars_borrower = total.loc[34,'# of irregular borrower'] 
virtual_new_borrower = total.loc[34,'Virtual new borrower']
returning = total.loc[34,'Returning']


## PLoting the graphs in the streamlit app
col1, col2, col3, col4, col5, col6, col7 = st.columns(7) 
col1.metric(label='# of drops',value=n_of_drops)
col2.metric(label='# of partial',value=n_of_partial)
col3.metric(label='Yesterday paid off',value=yesterday_paid)
col4.metric(label='Today disbursed',value=today_disbursed)
col5.metric(label='# of irregular borrowes',value=n_irregulars_borrower)
col6.metric(label='virtual new borrowers',value=virtual_new_borrower)
col7.metric(label='Returning',value=returning)
col1.plotly_chart(fig)
col5.plotly_chart(fig2)

df2 = df.drop(["Date","order"],axis=1)

st.table(data=df2)
