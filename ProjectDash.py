import os
from turtle import title
from dash import Dash, html, dcc, callback, Input, Output,State
import plotly.express as px
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
import plotly.graph_objects as go

app = Dash(__name__)
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
path = 'globalUsers' 
jibStore_file = os.path.join(path, 'superStore.csv')

jibStore_df = pd.read_csv(jibStore_file) 
#CATEGORY ANALYSIS
category_info = jibStore_df.groupby(['Category'])[['Sales', 'profit_merging']].sum()
category_info1= category_info.sort_values(by=['profit_merging'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
fig = px.bar(category_info1,x=category_info1.index,y=[category_info1.profit_merging,category_info1.Sales], title= "Bar graph for the Best selling and more profitable Category",barmode='group')

#SUB-CATEGORY ANALYSIS
subcategory1 = jibStore_df.groupby(['Sub_Category'])[['Sales', 'profit_merging']].sum()
subcategory_sales = subcategory1.sort_values(by=['profit_merging'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
fig1 = px.bar( subcategory_sales,x=subcategory_sales.index,y=[subcategory_sales.profit_merging,subcategory_sales.Sales], title= "Bar graph for the Best selling and more profitable Sub-Category",barmode='group')

subcategory = jibStore_df.groupby(['Sub_Category'])[['Quantity']].sum()#.sort_values('Quantity',ascending=False)
fig2 = px.bar(subcategory,x=subcategory.index,y=subcategory.Quantity, title= "Bar graph for the top selling Sub-Category",color=subcategory.index)

#SEGMENT ANALYSIS
segment_profit = jibStore_df.groupby(['Segment'])[['profit_merging']].sum()
fig3 = px.bar(segment_profit,x=segment_profit.index,y=segment_profit.profit_merging, title= "Bar graph for the Most Profitable Segment",color=segment_profit.index)

#SHIPMODE ANALYSIS
shipmode=jibStore_df.groupby(['Ship_Mode'])['Sales'].sum().reset_index(name="counts")
fig4 = px.bar(shipmode,x=shipmode.Ship_Mode,y=shipmode.counts, title= "Bar graph for the Most Prefered Ship mode",color=shipmode.Ship_Mode)

#REGIONAL ANALYSIS
region_profit = jibStore_df.groupby(['Region'])['profit_merging'].sum().reset_index()
fig5 = px.bar(region_profit,x=region_profit.Region,y=region_profit.profit_merging, title= "Bar graph for the Most Profitable Region",color=region_profit.Region)

#CITY ANALYSIS
city_sales = jibStore_df.groupby(['City'])['Sales', 'Quantity'].sum().sort_values('Quantity',ascending=False)
city_sales1 = city_sales[:10]
fig6 = px.bar(city_sales1,x=city_sales1.index,y=city_sales1.Quantity, title= "Bar graph for the top 10 selling City",color=city_sales1.index)


app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children="BEST SELLING AND MOST PROFITABLE CATEGORY", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph9',
                figure=fig
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children="BEST SELLING AND MOST PROFITABLE SUB-CATEGORY", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph1',
                figure=fig1
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children="TOP SELLING SUB-CATEGORY", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph2',
                figure=fig2
            ),  
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children="MOST PROFITABLE CUSTOMER SEGMENT", style={'textAlign': 'center'}),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),  
    ], className='row'),
    html.Div([
            html.H1(children="MOST PREFERED SHIP MODE", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph4',
                figure=fig4
            ),  
        ], className='six columns'),
        html.Div([
        html.H1(children="MOST PROFITABLE REGION", style={'textAlign': 'center'}),

        dcc.Graph(
            id='graph5',
            figure=fig5
        ),  
    ], className='row'),
    html.Div([
            html.H1(children="HIGHEST SELLING CITIES", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph6',
                figure=fig6
            ),  
        ], className='six columns'),
    
])
    
    

if __name__ == '__main__':
    app.run_server(debug=True)  