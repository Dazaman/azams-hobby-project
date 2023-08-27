# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from matplotlib import cm

def extract_data_from_webpage(url) -> pd.DataFrame:
    # Create object page
    page = requests.get(url)

    # parser-lxml = Change html to Python friendly format
    # Obtain page's information
    soup = BeautifulSoup(page.text, 'lxml')

    # What to do if more than one table? Couldn't find table with id
    table1 = soup.find("table")

    headers = []
    for i in table1.find_all("th"):
        title = i.text.rstrip()
        headers.append(title)
    
    mydata = pd.DataFrame(columns = headers)

    # Create a for loop to fill mydata
    for j in table1.find_all("tr")[1:]:
        row_data = j.find_all("td")
        row = [i.text.strip().rstrip() for i in row_data]
        length = len(mydata)
        mydata.loc[length] = row

    return mydata

# @st.cache(allow_output_mutation=True)
# def make_radar_chart(norm_df, n_clusters):
    fig = go.Figure()
    cmap = cm.get_cmap('tab20b')
    angles = list(norm_df.columns[5:])
    angles.append(angles[0])
    
    for i in range(n_clusters):
        subset = norm_df[norm_df['cluster'] == i]
        data = [np.mean(subset[col]) for col in angles[:-1]]
        data.append(data[0])
        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=angles,
            # fill='toself',
            # fillcolor = 'rgba' + str(cmap(i/n_clusters)),
            mode='lines',
            line_color='rgba' + str(cmap(i/n_clusters)),
            name="Cluster " + str(i)))
        
    fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1])
                ),
            showlegend=True
    )
    fig.update_traces()
    return fig

def make_radar(df, hero):
    fig = go.Figure(data=go.Scatterpolar(
    theta=["STR","AGI","INT","DMG(MAX)","RG"],
    result = df.loc[[hero],["STR","AGI","INT","DMG(MAX)","RG"]],
    fill='toself'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True
        ),
    ),
    showlegend=False
    )

def main():
    url = 'https://dota2.fandom.com/wiki/Table_of_hero_attributes'
    data = extract_data_from_webpage(url)
    
    # data.set_index("HERO", inplace = True)

    # attr = ["STR","AGI","INT","DMG(MAX)","RG"]
    # hero = "Anti-Mage"

    # result = data.loc[[hero],["STR","AGI","INT","DMG(MAX)","RG"]]

    fig = go.Figure(data=go.Scatterpolar(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost','mechanical properties','chemical stability', 'thermal stability',
            'device integration'],
    fill='toself'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True
        ),
    ),
    showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__": main()