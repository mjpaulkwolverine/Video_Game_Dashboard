##this cell is the python script I will save to be able to run in streamlit##

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd


##first, grab the dataset and transform it to our final state it was being used in
gamesf = pd.read_csv('Video_Games_Sales.csv')
platform_maker_dict = {
    'Wii': 'Nintendo',
    'WiiU': 'Nintendo',
    'DS': 'Nintendo',
    '3DS': 'Nintendo',
    'Switch': 'Nintendo',
    'NES': 'Nintendo',
    'GB': 'Nintendo',
    'SNES': 'Nintendo',
    'GBA': 'Nintendo',
    'N64': 'Nintendo',
    'GC': 'Nintendo',
    
    
    'PS3': 'Sony',
    'PS4': 'Sony',
    'PS2': 'Sony',
    'PS': 'Sony',
    'PSP': 'Sony',
    'PSV': 'Sony',
    
    'X360': 'Microsoft',
    'XB': 'Microsoft',
    'XOne': 'Microsoft',
    
    'PC': 'PC',
    '2600': 'Atari',
    'GEN': 'Sega',
    'DC': 'Sega',
    'SCD': 'Sega',
    'SAT': 'Sega',
    'GG': 'Sega',
    'WS': 'Other',
    'NG': 'Other',
    'TG16': 'Other',
    '3DO': 'Other',
    'PCFX': 'Other'
}

gamesf['Platform_Maker']= gamesf['Platform'].map(platform_maker_dict)


gamesf['Count']= 1
gamesf['User_Score_Comp']= pd.to_numeric(gamesf['User_Score'], errors = 'coerce')*10
gamesf['Rating_avg']= (pd.to_numeric(gamesf['Critic_Score'], errors= 'coerce') + gamesf['User_Score_Comp'])/2
gamesf.rename(columns={'Year_of_Release': 'Year', 'Name': 'Game'}, inplace = True)
gamesf.head(5)

######Now we'll pop in our create dashboard function#########--------------------------------------------------------------------------------------------------------
def top_N_color(df, column, value, color, N=5):
    ##first, do a groupby to grab the top5 from the target column values
    data = df.groupby(column)[value].sum().reset_index()
    top_N = data.sort_values(by= value, ascending=False).reset_index().head(N)

    ##now filter the original input df to just rows with values from top N columns
    data1 = df[df[column].isin(top_N[column])]
    

    ##then create the groupby that has both the column, color, and value
    data2 = data1.groupby([column, color])[value].sum().reset_index()
    top = data2.sort_values(by= value, ascending=False).reset_index()
    #return top.head(25)
    
    fig = px.bar(
    top,
    x= column,
    y= value,
    color = color,    
    title = f'Top {N} {column} by {value} with {color}'    
)
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig
    #return data2.reset_index().head(5)
    
 
#top_N_color(games4, 'Game', 'Global_Sales', 'Genre',N=10)

def top_N(df, column, value, N=5):
    ##first, do a groupby to grab the top5 from the target column values
    data = df.groupby(column)[value].sum().reset_index()
    top_N = data.sort_values(by= value, ascending=False).reset_index().head(N)

        
    fig = px.bar(
    top_N,
    x= column,
    y= value,
    title = f'Top {N} {column} by {value}'    
)
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig





def create_dashboard(df):
    scatter_x = 'Rating_avg'
    scatter_y = 'Global_Sales'
    scatter_color = 'Genre'
    histo_col = 'Rating_avg'
    box_x = 'Genre'
    box_y = 'Global_Sales'

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=("Sales vs. Rating", "Avg Rating Buckets", "Top 5 Games by Sales","Sales by Genre", "Region Sales Donut", "Top 5 Publishers" ),
        specs=[[{}, {},{}], [{}, {"type": "domain"},{}]]        
    )

    # Scatter Plot creation
    scatter = px.scatter(df, x=scatter_x, y=scatter_y, color=scatter_color)
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=1)

    # hist creation
    hist = px.histogram(df, x=histo_col, nbins=20)
    for trace in hist.data:
        fig.add_trace(trace, row=1, col=2)

    # Box creation
    box = px.box(df, x=box_x, y=box_y, points='suspectedoutliers', notched = True)
    for trace in box.data:
        fig.add_trace(trace, row=2, col=1)

    #  Donut 
    region_df = df[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().reset_index()
    region_df.columns = ['Region', 'Sales']
    donut = px.pie(region_df, names='Region', values='Sales', hole=0.4)
    for trace in donut.data:
        fig.add_trace(trace, row=2, col=2)
    #Top games
    game_bar = top_N_color(df, 'Game', 'Global_Sales', 'Genre',N=5)
    for trace in game_bar.data:
        fig.add_trace(trace, row=1, col=3)
    
    #top publishers
    pub_bar = top_N(df, 'Publisher', 'Count', N=5)
    for trace in pub_bar.data:
        fig.add_trace(trace, row=2, col=3)
    
    ##now lets ad some axis labels
    fig.update_xaxes(title_text="Avg_Rating", row=1, col=1)
    fig.update_yaxes(title_text="Sales", row=1, col=1)
    fig.update_xaxes(title_text="Avg_Rating", row=1, col=2)
    fig.update_yaxes(title_text="Count_of_Games", row=1, col=2)
    fig.update_xaxes(title_text="Game",categoryorder='total descending', row=1, col=3)
    fig.update_yaxes(title_text="Sales", row=1, col=3)
    
    fig.update_xaxes(title_text="Genre", row=2, col=1)
    fig.update_yaxes(title_text="Sales", row=2, col=1)
    
    fig.update_yaxes(title_text="Sales % by Region", row=2, col=2)
    
    fig.update_xaxes(title_text="Publisher", row=2, col=3)
    fig.update_yaxes(title_text="Count of Games", categoryorder='total descending', row=2, col=3)


    
    fig.update_layout(
        height = 1500,
        width = 1500,
        title_text= "Games Sales Dashboard",
        showlegend = True,
        barmode = 'stack'
    )
    ##i think we really only want the legend for the donut chart
    for i, trace in enumerate(fig.data):
        if trace.type != 'pie':
            trace.showlegend = False
    
    fig.update_layout(
    legend=dict(
        orientation="h",
        x=.5,
        y=0.0,
        title="Region")
    )
    
    fig.show()



########  Now we'll add the interactive streamlit pieces #####  --------------------------------------------------------------
platform_options = gamesf['Platform_Maker'].dropna().unique()
platform_choice = st.selectbox("Choose Platform Maker",platform_options)

min_year = int(gamesf['Year'].min())
max_year = int('2014')
year_range = st.slider("Select Year Range", min_value = min_year, max_value = max_year, value=(min_year, max_year))

filtered_df = gamesf[
    (gamesf['Year']>= year_range[0]) &
    (gamesf['Year']<= year_range[1]) &
    (gamesf['Platform_Maker']== platform_choice)
]

create_dashboard(filtered_df)

