import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import toml
from PIL import Image
import mysql.connector
import requests


settings=toml.load(f"C:/Users/rdavi/OneDrive/Desktop/phonepe-pulse/config.toml")

#connection to database

connection=mysql.connector.connect(
    host="localhost",
    port='3306',
    username='root',
    password='root',
    database='phonepe_pluse'
    
)
cursor=connection.cursor()

#aggregate transaction

cursor.execute('SELECT * FROM aggregated_transaction')
table_1=cursor.fetchall()
Aggregated_transaction=pd.DataFrame(table_1,columns=('States','Years','Quarter','Transaction_type','Transaction_count','Transaction_ammount'))


#aggregate users

cursor.execute('SELECT * FROM aggregated_users')
table_2=cursor.fetchall()
Aggregated_users=pd.DataFrame(table_2,columns=('States','Years','Quarter','brands','Transaction_count','percentage'))


#map transaction

cursor.execute('SELECT * FROM map_transaction')
table_3=cursor.fetchall()
Map_transactions=pd.DataFrame(table_3,columns=('States','Years','Quarter','districts','Transaction_count','Transaction_amount'))


#map users

cursor.execute('SELECT * FROM map_users')
table_4=cursor.fetchall()
Map_users=pd.DataFrame(table_4,columns=('States','Years','Quarter','districts','registeredUsers','appOpens'))


# top transaction

cursor.execute('SELECT * FROM top_transaction')
table_5=cursor.fetchall()
Top_transaction=pd.DataFrame(table_5,columns=('States','Years','Quarter','pincodes','Transaction_count','Transaction_ammount'))


#top users

cursor.execute('SELECT * FROM top_user')
table_6=cursor.fetchall()
Top_user=pd.DataFrame(table_6,columns=('States','Years','Quarter','pincodes','registeredUsers'))


def Transaction_amount_count_Y(df,year):
    Aggre_transfor_map=df[df['Years']==year]
    Aggre_transfor_map.reset_index(drop=True,inplace=True)

    Aggre_transfor_mapgrping=Aggre_transfor_map.groupby("States")[["Transaction_count","Transaction_ammount"]].sum()
    Aggre_transfor_mapgrping.reset_index(inplace=True)
       
    figure_pie=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_ammount",title=f"{year} TRANSACTION AMMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)
    
    figure_pie_count=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_1=response.json()
    states_name=[]
    for features in data_1['features']:
        states_name.append(features["properties"]['ST_NM'])
    states_name.sort()
    
    #Formap plotting
    india_map=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="temps",
                            range_color=(Aggre_transfor_mapgrping['Transaction_count'].min(),Aggre_transfor_mapgrping['Transaction_count'].max()),
                            hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                            height=650,width=600)
    india_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map)
    india_map_2=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_ammount",color_continuous_scale="turbo",
                            range_color=(Aggre_transfor_mapgrping['Transaction_ammount'].min(),Aggre_transfor_mapgrping['Transaction_ammount'].max()),
                            hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                            height=650,width=600)
    india_map_2.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map_2)

    return Aggre_transfor_map


def Transaction_amount_count_Y_Quater(df,Quarters):
    Aggre_transfor_map=df[df['Quarter']==Quarters]
    Aggre_transfor_map.reset_index(drop=True,inplace=True)

    Aggre_transfor_mapgrping=Aggre_transfor_map.groupby("States")[["Transaction_count","Transaction_ammount"]].sum()
    Aggre_transfor_mapgrping.reset_index(inplace=True)


    figure_pie=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_ammount",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_1=response.json()
    states_name=[]
    for features in data_1['features']:
        states_name.append(features["properties"]['ST_NM'])
    states_name.sort()
    
    #Formap plotting
    india_map=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="temps",
                            range_color=(Aggre_transfor_mapgrping['Transaction_count'].min(),Aggre_transfor_mapgrping['Transaction_count'].max()),
                            hover_name="States",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",fitbounds="locations",
                            height=650,width=600)
    india_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map)
    india_map_2=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_ammount",color_continuous_scale="turbo",
                            range_color=(Aggre_transfor_mapgrping['Transaction_ammount'].min(),Aggre_transfor_mapgrping['Transaction_ammount'].max()),
                            hover_name="States",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMMOUNT",fitbounds="locations",
                            height=650,width=600)
    india_map_2.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map_2)

    return Aggre_transfor_map

def Aggre_trans_type_pie(df,states):

    Aggre_transfor_map=df[df['States']==states]
    Aggre_transfor_map.reset_index(drop=True,inplace=True)


    Aggre_transfor_mapgrping=Aggre_transfor_map.groupby("Transaction_type")[["Transaction_count","Transaction_ammount"]].sum()
    Aggre_transfor_mapgrping.reset_index(inplace=True)
    figure_py=px.pie(data_frame=Aggre_transfor_mapgrping,names='Transaction_type',values='Transaction_ammount',
                        width=600,title=f'{states.upper()} Transaction Ammount',hole=0.5)
    st.plotly_chart(figure_py)
    figure_py_cc=px.pie(data_frame=Aggre_transfor_mapgrping,names='Transaction_type',values='Transaction_count',
                        width=600,title=f'{states.upper()} Transaction count',hole=0.5)
    st.plotly_chart(figure_py_cc)

def Agg_user_1(df,year):

    Agg_user_year=df[df['Years']==year]
    Agg_user_year.reset_index(drop=True,inplace=True)


    Agg_user_year_grp=pd.DataFrame(Agg_user_year.groupby("brands")["Transaction_count"].sum())
    Agg_user_year_grp.reset_index(inplace=True)
    

    Agg_userbar1=px.bar(Agg_user_year_grp,x="brands",y="Transaction_count",title=f"{year} Transaction count",
                        width=600,color_discrete_sequence=px.colors.sequential.BuPu_r,hover_name="brands")
    st.plotly_chart(Agg_userbar1)

    return Agg_user_year

def Agg_user_plot_2(df,quarter):
    Agg_user_q=df[df['Quarter']==quarter]
    Agg_user_q.reset_index(drop=True,inplace=True)

    Agg_user_q_grp=pd.DataFrame(Agg_user_q.groupby("brands")["Transaction_count"].sum())
    Agg_user_q_grp.reset_index(inplace=True)
    

    Agg_userbar1=px.bar(Agg_user_q_grp,x="brands",y="Transaction_count",title=f"{quarter} Quarter Transaction count",
                        width=600,color_discrete_sequence=px.colors.sequential.BuPu_r)
    st.plotly_chart(Agg_userbar1)

    return Agg_user_q

def Agg_user_plot_3(df,state):
    Agg_Year_quarter_s=df[df["States"]==state]
    Agg_Year_quarter_s.reset_index(drop=True,inplace=True)

    fig_line_qs=px.bar(Agg_Year_quarter_s,x="brands",y="Transaction_count",hover_data="percentage",
                        width=600,title=f"{state} BRANDS,TRANSACTION COUNT,PERCENTAGE")
    st.plotly_chart(fig_line_qs)

def Transaction_amount_count_Y_mapst(df,year):
    map_transfor_map=df[df['Years']==year]
    map_transfor_map.reset_index(drop=True,inplace=True)

    map_Aggre_transfor_mapgrping=map_transfor_map.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    map_Aggre_transfor_mapgrping.reset_index(inplace=True)


    figure_pie=px.bar(map_Aggre_transfor_mapgrping,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_1=response.json()
    states_name=[]
    for features in data_1['features']:
        states_name.append(features["properties"]['ST_NM'])
    states_name.sort()
    
    #Formap plotting
    india_map=px.choropleth(map_Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="temps",
                            range_color=(map_Aggre_transfor_mapgrping['Transaction_count'].min(),map_Aggre_transfor_mapgrping['Transaction_count'].max()),
                            hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                            height=650,width=600)
    india_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map)
    india_map_2=px.choropleth(map_Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_amount",color_continuous_scale="turbo",
                            range_color=(map_Aggre_transfor_mapgrping['Transaction_amount'].min(),map_Aggre_transfor_mapgrping['Transaction_amount'].max()),
                            hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                            height=650,width=600)
    india_map_2.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map_2)

    return map_transfor_map

def Transaction_amount_count_Y_mapst_dis(df,states):
    map_transfor_map=df[df['States']==states]
    map_transfor_map.reset_index(drop=True,inplace=True)

    map_Aggre_transfor_mapgrping=map_transfor_map.groupby("districts")[["Transaction_count","Transaction_amount"]].sum()
    map_Aggre_transfor_mapgrping.reset_index(inplace=True)

    figure_pie=px.bar(map_Aggre_transfor_mapgrping,x="districts",y="Transaction_amount",title= f"{states} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="districts",y="Transaction_count",title=f"{states} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)

def Transaction_amount_count_Y_Quater_mt(df,Quarters):
    map_transfor_map=df[df['Quarter']==Quarters]
    map_transfor_map.reset_index(drop=True,inplace=True)

    Aggre_transfor_mapgrping=map_transfor_map.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Aggre_transfor_mapgrping.reset_index(inplace=True)
    

    figure_pie=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_amount",title=f"{map_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{map_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_1=response.json()
    states_name=[]
    for features in data_1['features']:
        states_name.append(features["properties"]['ST_NM'])
    states_name.sort()
    
    #Formap plotting
    india_map=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="temps",
                            range_color=(Aggre_transfor_mapgrping['Transaction_count'].min(),Aggre_transfor_mapgrping['Transaction_count'].max()),
                            hover_name="States",title=f"{map_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",fitbounds="locations",
                            height=650,width=600)
    india_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map)
    india_map_2=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_amount",color_continuous_scale="turbo",
                            range_color=(Aggre_transfor_mapgrping['Transaction_amount'].min(),Aggre_transfor_mapgrping['Transaction_amount'].max()),
                            hover_name="States",title=f"{map_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMMOUNT",fitbounds="locations",
                            height=650,width=600)
    india_map_2.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map_2)

    return map_transfor_map


def Transaction_amount_count_Y_mapst_dis(df,states):
    map_transfor_map=df[df['States']==states]
    map_transfor_map.reset_index(drop=True,inplace=True)

    map_Aggre_transfor_mapgrping=map_transfor_map.groupby("districts")[["Transaction_count","Transaction_amount"]].sum()
    map_Aggre_transfor_mapgrping.reset_index(inplace=True)

    figure_pie=px.bar(map_Aggre_transfor_mapgrping,x="districts",y="Transaction_amount",title= f"{states} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="districts",y="Transaction_count",title=f"{states} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)    

def map_user_resandappopens(df,year):
    map_user_y=df[df['Years']==year]
    map_user_y.reset_index(drop=True,inplace=True)
    

    muyg=map_user_y.groupby("States")[["registeredUsers","appOpens"]].sum()
    muyg.reset_index(inplace=True)

    figure_pie=px.line(muyg,x="States",y=["registeredUsers","appOpens"],title=f"{year} REGISTEREDUSERS AND APPOPENS",
                    height=650,width=600,markers=True)
    st.plotly_chart(figure_pie)

    return map_user_y

def map_user_resandappopens_qua(df,quarter):
    map_user_y_qua=df[df['Quarter']==quarter]
    map_user_y_qua.reset_index(drop=True,inplace=True)
    

    muyg=map_user_y_qua.groupby("States")[["registeredUsers","appOpens"]].sum()
    muyg.reset_index(inplace=True)

    figure_pie=px.line(muyg,x="States",y=["registeredUsers","appOpens"],title=f"{df["Years"].min()} YEAR {quarter} QUARTER REGISTEREDUSERS AND APPOPENS",
                    height=659,width=600,markers=True)
    st.plotly_chart(figure_pie)

    return map_user_y_qua

def map_user_y_Q_3(df,States):
    map_user_y_qua_S=df[df['States']==States]
    map_user_y_qua_S.reset_index(drop=True,inplace=True)

   
    figure_pie=px.bar(map_user_y_qua_S,x="registeredUsers",y="districts",orientation="h",
                    title=f"{States.upper()} REGISTERED USERS",height=800,width=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(figure_pie)

    figure_pie_2=px.bar(map_user_y_qua_S,x="appOpens",y="districts",orientation="h",
                    title=f"{States.upper()} App Opens",height=800,width=800,color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(figure_pie_2)

def Map_transaction_map_1_year(df,year):

    map_transfor_map=df[df['Years']==year]
    map_transfor_map.reset_index(drop=True,inplace=True)

    map_Aggre_transfor_mapgrping=map_transfor_map.groupby("States")[["Transaction_count","Transaction_ammount"]].sum()
    map_Aggre_transfor_mapgrping.reset_index(inplace=True)

    figure_pie=px.bar(map_Aggre_transfor_mapgrping,x="States",y="Transaction_ammount",title=f"{year} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)


    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_1=response.json()
    states_name=[]
    for features in data_1['features']:
        states_name.append(features["properties"]['ST_NM'])
    states_name.sort()

    #Formap plotting
    india_map=px.choropleth(map_Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                        color="Transaction_count",color_continuous_scale="temps",
                        range_color=(map_Aggre_transfor_mapgrping['Transaction_count'].min(),map_Aggre_transfor_mapgrping['Transaction_count'].max()),
                        hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                        height=650,width=600)
    india_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map)
    india_map_2=px.choropleth(map_Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                        color="Transaction_ammount",color_continuous_scale="turbo",
                        range_color=(map_Aggre_transfor_mapgrping['Transaction_ammount'].min(),map_Aggre_transfor_mapgrping['Transaction_ammount'].max()),
                        hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                        height=650,width=600)
    india_map_2.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map_2)

    return map_transfor_map

def Top_trans_plot_1(df,states):
    Top_user_y_qua_S=df[df['States']==states]
    Top_user_y_qua_S.reset_index(drop=True,inplace=True)

    Top_trans_main=Top_user_y_qua_S.groupby("pincodes")[["Transaction_count","Transaction_ammount"]].sum()
    Top_trans_main.reset_index(inplace=True)


    figure_pie=px.bar(Top_user_y_qua_S,x="Quarter",y="Transaction_ammount",title=" TRANSACTION AMOUNT",hover_data="pincodes",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_1=px.bar(Top_user_y_qua_S,x="Quarter",y="Transaction_count",title=" TRANSACTION COUNT",hover_data="pincodes",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_1)


def Top_amount_count_Y_Quater(df,Quarters):
    Aggre_transfor_map=df[df['Quarter']==Quarters]
    Aggre_transfor_map.reset_index(drop=True,inplace=True)


    Aggre_transfor_mapgrping=Aggre_transfor_map.groupby("States")[["Transaction_count","Transaction_ammount"]].sum()
    Aggre_transfor_mapgrping.reset_index(inplace=True)
    




    figure_pie=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_ammount",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
    st.plotly_chart(figure_pie_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_1=response.json()
    states_name=[]
    for features in data_1['features']:
        states_name.append(features["properties"]['ST_NM'])
    states_name.sort()

    #Formap plotting
    india_map=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="temps",
                            range_color=(Aggre_transfor_mapgrping['Transaction_count'].min(),Aggre_transfor_mapgrping['Transaction_count'].max()),
                            hover_name="States",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",fitbounds="locations",
                            height=650,width=600)
    india_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map)
    india_map_2=px.choropleth(Aggre_transfor_mapgrping,geojson=data_1,locations='States',featureidkey="properties.ST_NM",
                            color="Transaction_ammount",color_continuous_scale="turbo",
                            range_color=(Aggre_transfor_mapgrping['Transaction_ammount'].min(),Aggre_transfor_mapgrping['Transaction_ammount'].max()),
                            hover_name="States",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMMOUNT",fitbounds="locations",
                            height=650,width=600)
    india_map_2.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(india_map_2)

    return Aggre_transfor_map


def top_user_1(df,year):
    map_transfor_map=df[df['Years']==year]
    map_transfor_map.reset_index(drop=True,inplace=True)
   

    map_Aggre_transfor_mapgrping=pd.DataFrame(map_transfor_map.groupby(["States","Quarter"])["registeredUsers"].sum())
    map_Aggre_transfor_mapgrping.reset_index(inplace=True)

    fig_bar_tu=px.bar(map_Aggre_transfor_mapgrping,x="States",y="registeredUsers",color="Quarter",width=1000,height=800,
                    color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_bar_tu)

    return map_transfor_map

def Top_user_regis(df,states):
    top_usersfor_map=df[df['States']==states]
    top_usersfor_map.reset_index(drop=True,inplace=True)


    bar_user_top=px.bar(top_usersfor_map,x="Quarter",y="registeredUsers",title="REGISTERED USERS",
                        width=1000,height=800,color="registeredUsers",hover_data="pincodes",
                        color_continuous_scale=px.colors.sequential.amp_r)
    st.plotly_chart(bar_user_top)






st.set_page_config(page_title="My Streamlit App",page_icon=":blue_circle:",layout="wide",initial_sidebar_state="expanded")
st.title(':violet[PHONEPE-PLUSE DATA VISUALIZATION]')



select=option_menu(menu_title=None,
                       options=["HOME","DATA EXPLORATION","TOP CHARTS","CONTACT"],
                       default_index=1,
                       orientation="horizontal",
                       styles={"container":{"padding":"0!important","background-color":"white","size":"cover","width":"80%"},
                               "icon":{"color":"viloet","font-size":"20px","font-color":"black"},
                               "nav-link":{"font-size":"20px","text-align":"center","margin":"-2px","--hover-color":"#8000ff"},
                               "nav-link-selected":{"background-color":"#8000ff"}})


if select=="HOME":
    pass

elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with tab1:
        col1,col2=st.columns(2)
        with col1:
            method=st.selectbox("Select the method",["Transaction Analysis","User Analysis"])
        with col2:
            pass
        if method=="Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:
                years=st.selectbox("Select the Years",Aggregated_transaction['Years'].unique())
                Aggre_transfor_map=Transaction_amount_count_Y(Aggregated_transaction,years)
            with col2:
                query_1='''select states,sum(Transaction_ammount) from aggregated_transaction group by states order by sum(Transaction_ammount)'''
                cursor.execute(query_1)
                result=cursor.fetchall()
                connection.commit()

                df_1=pd.DataFrame(result,columns=("States","Transaction ammount"))
                df_1
                query_2='''select states, sum(transaction_count) from aggregated_transaction group by States order by sum(Transaction_count)'''
                cursor.execute(query_2)
                result_1=cursor.fetchall()
                connection.commit()

                df_2=pd.DataFrame(result_1,columns=("States","Transaction count"))
                df_2

            col1,col2=st.columns(2)
            with col1:
                quarters_1=st.slider("Select the Quarter",Aggre_transfor_map['Quarter'].min(),Aggre_transfor_map["Quarter"].max(),key='quarters_1')
                Transaction_amount_count_Y_Quater(Aggre_transfor_map,quarters_1)
            with col2:
                query_5='''select Quarter,sum(Transaction_ammount) from aggregated_transaction group by Quarter order by sum(Transaction_ammount)'''
                cursor.execute(query_5)
                result_5=cursor.fetchall()
                connection.commit()

                df_5=pd.DataFrame(result_5,columns=("Quarter","Transaction amount"))
                df_5
                query_3='''select Quarter,sum(Transaction_count) from aggregated_transaction group by Quarter order by sum(Transaction_count)'''
                cursor.execute(query_3)
                result_3=cursor.fetchall()
                connection.commit()

                df_2=pd.DataFrame(result_3,columns=("Quarter","Transaction count"))
                df_2

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("please select the state",Aggre_transfor_map['States'].unique())
                Aggre_trans_type_pie(Aggre_transfor_map,states)
            with col2:
                 query_4='''select Transaction_type, sum(transaction_ammount) from aggregated_transaction group by Transaction_type order by sum(Transaction_ammount)'''
                 cursor.execute(query_4)
                 result_4=cursor.fetchall()
                 connection.commit()

                 df_4=pd.DataFrame(result_4,columns=("transaction type","Transaction amount"))
                 df_4


                 query_5='''select Transaction_type,sum(Transaction_count) from aggregated_transaction group by Transaction_type order by sum(Transaction_count)'''
                 cursor.execute(query_5)
                 result_5=cursor.fetchall()
                 connection.commit()

                 df_5=pd.DataFrame(result_5,columns=("Transaction type","Transaction count"))
                 df_5

            col1,col2=st.columns(2)
            with col1:
                quarters_2=st.slider("Select the Quarter",Aggre_transfor_map['Quarter'].min(),Aggre_transfor_map["Quarter"].max(),key="quarters_2")
                For_q=Transaction_amount_count_Y_Quater(Aggre_transfor_map,quarters_2)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state",Aggre_transfor_map['States'].unique())
                Aggre_trans_type_pie(For_q,states)
                

        elif method=="User Analysis":
                col1,col2=st.columns(2)
                with col1:
                    years=st.selectbox("Select the Years",Aggregated_users['Years'].unique())
                    Agg_user_Year=Agg_user_1(Aggregated_users,years)
                with col2:
                    query_7='''select states, sum(transaction_count) from aggregated_users group by States order by sum(Transaction_count)'''
                    cursor.execute(query_7)
                    result_7=cursor.fetchall()
                    connection.commit()

                    df_7=pd.DataFrame(result_7,columns=("States","Transaction count"))
                    df_7
                col1,col2=st.columns(2)
                with col1:
                    quarters_3=st.slider("Select the Quarter",Agg_user_Year['Quarter'].min(),Agg_user_Year["Quarter"].max(),key="quarters_2")
                    Agg_user_Year_Qurt=Agg_user_plot_2(Agg_user_Year,quarters_3)
                with col2:
                    query_8='''select Quarter,sum(Transaction_count) from aggregated_users group by Quarter order by sum(Transaction_count)'''
                    cursor.execute(query_8)
                    result_8=cursor.fetchall()
                    connection.commit()

                    df_8=pd.DataFrame(result_8,columns=("Quarter","Transaction count"))
                    df_8
                col1,col2=st.columns(2)
                with col1:
                    states=st.selectbox("please select the state",Agg_user_Year_Qurt['States'].unique())
                    Agg_user_plot_3(Agg_user_Year_Qurt,states)
                with col2:
                    query_9='''select brands, avg(percentage) from aggregated_users group by brands order by avg(percentage)'''
                    cursor.execute(query_9)
                    result_9=cursor.fetchall()
                    connection.commit()

                    df_9=pd.DataFrame(result_9,columns=("brands"," percentge"))
                    df_9

    with tab2:
        method_2=st.selectbox("Select the method",["Map Transaction","Map User"])

        if method_2=="Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                year=st.selectbox("Select the Years_mt",Map_transactions['Years'].unique())
                Map_transactions_year=Transaction_amount_count_Y_mapst(Map_transactions,year)
            with col2:
                query_10='''select states, sum(Transaction_amount) from map_transaction group by States order by sum(Transaction_amount);'''
                cursor.execute(query_10)
                result_10=cursor.fetchall()
                connection.commit()

                df_10=pd.DataFrame(result_10,columns=("States","Transaction amount"))
                df_10

                query_11='''select states, sum(Transaction_count) from map_transaction group by States order by sum(Transaction_count)'''
                cursor.execute(query_11)
                result_11=cursor.fetchall()
                connection.commit()

                df_11=pd.DataFrame(result_11,columns=("States","Transaction count"))
                df_11
                
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("please select the state map_Tr",Map_transactions_year['States'].unique())
                Transaction_amount_count_Y_mapst_dis(Map_transactions_year,states)
            with col2:
                 query_12='''select States,districts from map_transaction '''
                 cursor.execute(query_12)
                 result_12=cursor.fetchall()
                 connection.commit()

                 df_12=pd.DataFrame(result_12,columns=("transaction type","Transaction amount"))
                 df_12

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter",Map_transactions_year['Quarter'].min(),Map_transactions_year["Quarter"].max(),key="quarter")
                map_trans_qua=Transaction_amount_count_Y_Quater_mt(Map_transactions_year,quarters)
            with col2:
                query_14='''select Quarter,sum(Transaction_amount) from map_transaction group by Quarter order by sum(Transaction_amount)'''
                cursor.execute(query_14)
                result_14=cursor.fetchall()
                connection.commit()

                df_14=pd.DataFrame(result_14,columns=("Quarter","Transaction amount"))
                df_14
                query_15='''select Quarter,sum(Transaction_count) from map_transaction group by Quarter order by sum(Transaction_count)'''
                cursor.execute(query_15)
                result_15=cursor.fetchall()
                connection.commit()

                df_15=pd.DataFrame(result_15,columns=("Quarter","Transaction count"))
                df_15
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("please select the state mt",map_trans_qua['States'].unique())
                Transaction_amount_count_Y_mapst_dis(map_trans_qua,states)

        if method_2=="Map User":
            col1,col2=st.columns(2)
            with col1:
                year=st.selectbox("Select the Years_mu",Map_users['Years'].unique())
                map_for_reandop=map_user_resandappopens(Map_users,year)
            with col2:
                 
                query_16='''select States,registeredUsers,appOpens from map_users '''
                cursor.execute(query_16)
                result_16=cursor.fetchall()
                connection.commit()

                df_16=pd.DataFrame(result_16,columns=("States ","registeredUsers","appOpens"))
                df_16
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_muq",map_for_reandop['Quarter'].min(),map_for_reandop["Quarter"].max(),key="quarter")
                MAP_USER_PLOTQ=map_user_resandappopens_qua(map_for_reandop,quarters)

            with col2:
                query_17='''select Quarter,sum(registeredUsers) from map_users group by Quarter order by sum(registeredUsers)'''
                cursor.execute(query_17)
                result_17=cursor.fetchall()
                connection.commit()

                df_17=pd.DataFrame(result_17,columns=("Quarter"," registeredUsers"))
                df_17
                query_18='''select Quarter,sum(appOpens) from map_users group by Quarter order by sum(appOpens)'''
                cursor.execute(query_18)
                result_18=cursor.fetchall()
                connection.commit()

                df_18=pd.DataFrame(result_18,columns=("Quarter"," appOpens"))
                df_18
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("please select the state mts",MAP_USER_PLOTQ['States'].unique())
                map_user_y_Q_3(MAP_USER_PLOTQ,states)
            with col2:
                query_19='''select States ,districts from map_users '''
                cursor.execute(query_19)
                result_19=cursor.fetchall()
                connection.commit()

                df_19=pd.DataFrame(result_19,columns=("States","districts"))
                df_19

    with tab3:
        method_3=st.selectbox("Select the method",["Top Transaction","Top User"])

        if method_3=="Top Transaction":
            col1,col2=st.columns(2)
            with col1:
                year=st.selectbox("Select the Years_tt",Top_transaction['Years'].unique())
                Top_trans_plot=Map_transaction_map_1_year(Top_transaction,year)
            with col2:
                query_20='''select States, sum(Transaction_amount) from top_transaction group by States order by sum(Transaction_amount)'''
                cursor.execute(query_20)
                result_20=cursor.fetchall()
                connection.commit()

                df_20=pd.DataFrame(result_20,columns=("States","Transaction amount"))
                df_20
                query_21='''select States, sum(Transaction_count) from top_transaction group by States order by sum(Transaction_count)'''
                cursor.execute(query_21)
                result_21=cursor.fetchall()
                connection.commit()

                df_21=pd.DataFrame(result_21,columns=("States","Transaction count"))
                df_21
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("please select the state tt",Top_trans_plot['States'].unique())
                Top_trans_plot_1(Top_trans_plot,states)
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_ttq",Top_trans_plot['Quarter'].min(),Top_trans_plot["Quarter"].max(),key="quarter_1")
                Top_trans_plot_Q=Top_amount_count_Y_Quater(Top_trans_plot,quarters)
              

        elif method_3=="Top User":
            col1,col2=st.columns(2)
            with col1:
                year=st.selectbox("Select the Years_tt",Top_user['Years'].unique())
                Top_user_1_ru=top_user_1(Top_user,year)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("please select the state tu",Top_user_1_ru['States'].unique())
                Top_user_regis(Top_user_1_ru,states)

elif select=="TOP CHARTS":
    questions=st.selectbox("Seelct the Questions")