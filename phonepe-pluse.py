import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import toml
from PIL import Image
import mysql.connector
import requests


settings=toml.load(r"C:/Users/rdavi/OneDrive/Desktop/phonepe-pulse/config.toml")

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
                        color_discrete_sequence=px.colors.sequential.amp_r,height=650,width=600)
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
                    color_discrete_sequence=px.colors.sequential.algae_r,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
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
                        width=600,color_discrete_sequence=px.colors.sequential.Emrld_r,hover_name="brands")
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
                    color_discrete_sequence=px.colors.sequential.deep_r,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.RdBu,height=650,width=600)
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
                    color_discrete_sequence=px.colors.sequential.Redor,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="districts",y="Transaction_count",title=f"{states} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.speed_r,height=650,width=600)
    st.plotly_chart(figure_pie_count)

def Transaction_amount_count_Y_Quater_mt(df,Quarters):
    map_transfor_map=df[df['Quarter']==Quarters]
    map_transfor_map.reset_index(drop=True,inplace=True)

    Aggre_transfor_mapgrping=map_transfor_map.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Aggre_transfor_mapgrping.reset_index(inplace=True)
    

    figure_pie=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_amount",title=f"{map_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Oryel,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{map_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Pinkyl_r,height=650,width=600)
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
                    color_discrete_sequence=px.colors.sequential.Purples_r,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="districts",y="Transaction_count",title=f"{states} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Reds_r,height=650,width=600)
    st.plotly_chart(figure_pie_count)    

def map_user_resandappopens(df,year):
    map_user_y=df[df['Years']==year]
    map_user_y.reset_index(drop=True,inplace=True)
    

    muyg=map_user_y.groupby("States")[["registeredUsers","appOpens"]].sum()
    muyg.reset_index(inplace=True)

    figure_pie=px.line(muyg,x="States",y=["registeredUsers","appOpens"],title=f"{year} REGISTEREDUSERS AND APPOPENS",color_discrete_sequence=px.colors.sequential.Rainbow,
                    height=650,width=600,markers=True)
    st.plotly_chart(figure_pie)

    return map_user_y

def map_user_resandappopens_qua(df,quarter):
    map_user_y_qua=df[df['Quarter']==quarter]
    map_user_y_qua.reset_index(drop=True,inplace=True)
    

    muyg=map_user_y_qua.groupby("States")[["registeredUsers","appOpens"]].sum()
    muyg.reset_index(inplace=True)

    figure_pie=px.line(muyg,x="States",y=["registeredUsers","appOpens"],title=f"{df["Years"].min()} YEAR {quarter} QUARTER REGISTEREDUSERS AND APPOPENS",color_discrete_sequence=px.colors.sequential.Rainbow_r,
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
                    color_discrete_sequence=px.colors.sequential.Magenta_r,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(map_Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Magma,height=650,width=600)
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
                    color_discrete_sequence=px.colors.sequential.BuGn,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_1=px.bar(Top_user_y_qua_S,x="Quarter",y="Transaction_count",title=" TRANSACTION COUNT",hover_data="pincodes",
                    color_discrete_sequence=px.colors.sequential.Cividis_r,height=650,width=600)
    st.plotly_chart(figure_pie_1)


def Top_amount_count_Y_Quater(df,Quarters):
    Aggre_transfor_map=df[df['Quarter']==Quarters]
    Aggre_transfor_map.reset_index(drop=True,inplace=True)


    Aggre_transfor_mapgrping=Aggre_transfor_map.groupby("States")[["Transaction_count","Transaction_ammount"]].sum()
    Aggre_transfor_mapgrping.reset_index(inplace=True)
    




    figure_pie=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_ammount",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters} TRANSACTION AMMOUNT",
                    color_discrete_sequence=px.colors.sequential.Tealgrn_r,height=650,width=600)
    st.plotly_chart(figure_pie)

    figure_pie_count=px.bar(Aggre_transfor_mapgrping,x="States",y="Transaction_count",title=f"{Aggre_transfor_map['Years'].min()} YEAR{Quarters}  TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Darkmint,height=650,width=600)
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

    fig_bar_tu=px.bar(map_Aggre_transfor_mapgrping,x="States",y="registeredUsers",color="Quarter",width=600,height=600,
                    color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_bar_tu)

    return map_transfor_map

def Top_user_regis(df,states):
    top_usersfor_map=df[df['States']==states]
    top_usersfor_map.reset_index(drop=True,inplace=True)


    bar_user_top=px.bar(top_usersfor_map,x="Quarter",y="registeredUsers",title="REGISTERED USERS",
                        width=600,height=600,color="registeredUsers",hover_data="pincodes",
                        color_continuous_scale=px.colors.sequential.amp_r)
    st.plotly_chart(bar_user_top)






st.set_page_config(page_title="My Streamlit App",page_icon=":blue_circle:",layout="wide",initial_sidebar_state="expanded")
select=option_menu(menu_title=None,
                        options=["HOME","DATA ANALYSIS","CHARTS","CONTACT"],
                        default_index=0,
                        orientation="horizontal",
                        styles={"container":{"padding":"0!important","background-color":"viloet","size":"cover","width":"100%"},
                                "icon":{"color":"viloet","font-size":"20px","font-color":"black"},
                                "nav-link":{"font-size":"20px","text-align":"center","margin":"-2px","--hover-color":"#8000ff"},
                                "nav-link-selected":{"background-color":"#8000ff"}})

if select=="HOME":
    st.image(Image.open(r'C:\Users\rdavi\OneDrive\Desktop\phonepe-pulse\images\th (1).jpeg'))
    st.download_button("DOWNLOAD","https://www.phonepe.com/app-download/")
    col1,col2=st.columns(2)
    with col1:
        st.header(":violet[PHONE PE]")
        st.write('PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India.PhonePe was founded in December 2015,by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.The PhonePe app is accessible in 11 Indian languages.It enables users to perform various financial transactions such as sending and receiving money, recharging mobile and DTH, making utility payments, conducting in-store payments.')
        st.header(":violet[HISTORY]")
        st.write('PhonePe was incorporated in December 2015.In April 2016, the company was acquired by Flipkart and as part of the acquisition, the FxMart license was transferred to PhonePe and rebranded as the PhonePe wallet. PhonePes founder Sameer Nigam was appointed as the CEO of the company.In August 2016, the company partnered with Yes Bank to launch a UPI-based mobile payment app, based on the government-backed UPI platform.')
    with col2:
        st.image(Image.open(r"C:\Users\rdavi\OneDrive\Desktop\phonepe-pulse\images\gettyimages-1245605085-612x612.jpg"))
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col1,col2=st.columns(2)
    with col1:
        st.video(r"C:\Users\rdavi\OneDrive\Desktop\phonepe-pulse\images\home-fast-secure-v3.mp4")
    with col2:
        st.header(":violet[Simple, Fast & Secure]")
        st.subheader("One app for all things money.")
        st.write("Pay bills, recharge, send money, buy gold, invest and shop at your favourite stores.")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.subheader("Pay whenever you like, wherever you like.")
        st.write("Choose from options like UPI, the PhonePe wallet or your Debit and Credit Card.")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.subheader("Find all your favourite apps on PhonePe Switch.")
        st.write("Book flights, order food or buy groceries. Use all your favourite apps without downloading them.")

    col1,col2=st.columns(2)
    with col1:
        st.header(":violet[UPI]")
        st.write(" ")
        st.write(" ")
        st.write("The unified payments interface or the UPI is an interface via which you can transfer money between bank accounts across a single window. This means you can send or receive money or scan a quick response (QR) code to pay an individual, a merchant or a service provider to shop, pay bills or authorise payments.UPI QR Code. Create dynamic UPI QR Codes with custom amount. Customer can scan and pay with WhatsApp, Google Pay, Paytm, PhonePe or any BHIM UPI app.")
    with col2:
        st.write(" ")
        st.write(" ")
        st.image(Image.open(r"C:\Users\rdavi\OneDrive\Desktop\phonepe-pulse\images\th (2).jpeg"))

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col1,col2=st.columns(2)
    with col2:
        st.header(":violet[UPI ACROSS GLOBE]")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write("Unified Payments Interface (UPI) is predominantly used in India and has not yet seen widespread adoption globally. However, similar instant payment systems, allowing for quick and convenient bank-to-bank transactions via mobile phones, have gained traction internationally. For instance, China's Alipay and WeChat Pay, Europe's SEPA Instant Credit Transfer (SCT Inst) scheme, and the United States' Zelle and Venmo are notable examples. While UPI itself remains largely confined to India, the broader concept of instant mobile payments is being explored and implemented in various forms across the globe to cater to evolving consumer demands and technological advancements. ")
    with col1:
        st.write(" ")
        st.write(" ")
        st.video(r"C:\Users\rdavi\OneDrive\Desktop\phonepe-pulse\images\gettyimages-1482248444-640_adpp.mp4")

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write("Payments on PhonePe are safe, reliable and fast. One in three Indians are now using the PhonePe app to send money, recharge, pay bills and do so much more, in just a few simple clicks. PhonePe has also introduced several Insurance products and Investment options that offer every Indian an equal opportunity to unlock the flow of money, and get access to financial services.#KarteJaBadhteJa")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write("© 2024, All rights reserved ")
        
elif select=="DATA ANALYSIS":
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

                 df_4=pd.DataFrame(result_4,columns=("Transaction type","Transaction amount"))
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

                 df_12=pd.DataFrame(result_12,columns=("States","districts"))
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
            with col2:
                query_22='''select States, Quarter,pincodes from top_transaction'''
                cursor.execute(query_22)
                result_22=cursor.fetchall()
                connection.commit()

                df_22=pd.DataFrame(result_22,columns=("States","quarter","pincodes"))
                df_22
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_ttq",Top_trans_plot['Quarter'].min(),Top_trans_plot["Quarter"].max(),key="quarter_1")
                Top_trans_plot_Q=Top_amount_count_Y_Quater(Top_trans_plot,quarters)
            with col2:
                query_23='''select Quarter,sum(Transaction_amount) from top_transaction group by Quarter order by sum(Transaction_amount)'''
                cursor.execute(query_23)
                result_23=cursor.fetchall()
                connection.commit()

                df_23=pd.DataFrame(result_23,columns=("Quarter"," Transaction_amount"))
                df_23

                query_24='''select Quarter,sum(Transaction_count) from top_transaction group by Quarter order by sum(Transaction_count)'''
                cursor.execute(query_24)
                result_24=cursor.fetchall()
                connection.commit()

                df_24=pd.DataFrame(result_24,columns=("Quarter"," Transaction_count"))
                df_24

        elif method_3=="Top User":
            col1,col2=st.columns(2)
            with col1:
                year=st.selectbox("Select the Years_tt",Top_user['Years'].unique())
                Top_user_1_ru=top_user_1(Top_user,year)
            with col2:
                query_25='''select States, sum(registeredUsers) from top_user group by States order by sum(registeredUsers)'''
                cursor.execute(query_25)
                result_25=cursor.fetchall()
                connection.commit()

                df_25=pd.DataFrame(result_25,columns=("States","registeredUsers"))
                df_25

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("please select the state tu",Top_user_1_ru['States'].unique())
                Top_user_regis(Top_user_1_ru,states)
            with col2:
                query_26='''select States, Quarter,pincodes from top_user '''
                cursor.execute(query_26)
                result_26=cursor.fetchall()
                connection.commit()

                df_26=pd.DataFrame(result_26,columns=("States","Quarter","pincodes"))
                df_26

elif select=="CHARTS":
    questions=st.selectbox("Select the Questions",["1.Which are the Top 10 states have the most number of Transaction amount and count in Aggregated Transaction?.",
                                                   "2.What are the different types of Quarters and sum of the Transaction amount and count of each Quarters in Aggregated Transaction?.",
                                                   "3.What are the names of brands and their corresponding transaction count and percentage in Aggregated users?.",
                                                   "4.Name the states and their total of transaction count and percentage in Aggregated users?.",
                                                   "5.Which are the Top 10 states have the most number of Transaction amount and count in Map transaction?.",
                                                   "6.Name all their States and corresponding districts in Map transaction?.",
                                                   "7.What are the names of states and their corresponding registeredUsers and AppOpens in map_user?.",
                                                   "8.Which are the Top 10 states have the most number of Transaction amount and count in Top Transaction?.",
                                                   "9.Name the states and their total of transaction count and transaction ammount in top transaction?.",
                                                   "10.Which are the top 10 states have the most number of registeredUsers in top User?."],index=0)


                                                                                                        


    if questions=="1.Which are the Top 10 states have the most number of Transaction amount and count in Aggregated Transaction?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute(""" select States,sum(Transaction_ammount) from aggregated_transaction group by States order by sum(Transaction_ammount) DESC LIMIT 10;""")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['States', 'Transaction_ammount'])
            st.write(df)
        
        with col2:

            figure_pie=px.bar(df,x="States",y="Transaction_ammount",title="TRANSACTION AMMOUNT",
                        color_discrete_sequence=px.colors.sequential.Oryel_r,height=650,width=600)
            st.plotly_chart(figure_pie)
        col1,col2=st.columns(2)
        with col1:

            cursor.execute(""" select States,sum(Transaction_count) from aggregated_transaction group by States order by sum(Transaction_count) DESC LIMIT 10;""")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['States', 'Transaction_count'])
            st.write(df)
        with col2:
            figure_pie_1=px.bar(df,x="States",y="Transaction_count",title="TRANSACTION count",
                        color_discrete_sequence=px.colors.sequential.matter_r,height=650,width=600)
            st.plotly_chart(figure_pie_1)

    if questions=="2.What are the different types of Quarters and sum of the Transaction amount and count of each Quarters in Aggregated Transaction?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute(""" select Quarter,sum(Transaction_ammount) from aggregated_transaction group by Quarter order by sum(Transaction_ammount) ;""")
            data_1 = cursor.fetchall()
            df_1= pd.DataFrame(data_1, columns=['Quarter', 'Transaction_amount'])
            st.write(df_1)
        with col2:
            figure_pie=px.line(df_1,x="Quarter",y="Transaction_amount",title="TRANSACTION AMMOUNT",orientation="v",
                            color_discrete_sequence=px.colors.sequential.Oryel,height=400,width=350)
            st.plotly_chart(figure_pie)
        col1,col2=st.columns(2)
        with col1:
            cursor.execute(""" select Quarter,sum(Transaction_count) from aggregated_transaction group by Quarter order by sum(Transaction_count) ;""")
            data_2 = cursor.fetchall()
            df_2= pd.DataFrame(data_2, columns=['Quarter', 'transaction count'])
            st.write(df_2)
        with col2:
        
            figure_pie=px.line(df_2,x="Quarter",y="transaction count",title="TRANSACTION AMMOUNT",orientation="v",
                            color_discrete_sequence=px.colors.sequential.Oryel_r,height=400,width=350)
            st.plotly_chart(figure_pie)
    if questions=="3.What are the names of brands and their corresponding transaction count and percentage in Aggregated users?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute("""select brands,sum(Transaction_count),sum(percentage) from aggregated_users group by brands order by sum(Transaction_count),sum(percentage) ;""")
            data_90 = cursor.fetchall()
            df_90= pd.DataFrame(data_90, columns=['brands', 'Transaction_count','percentage'])
            st.write(df_90) 
        with col2:
            figure_py=px.pie(data_frame=df_90,names='brands',values='Transaction_count',
                        width=600,title='Transaction counts',hole=0.5)
            st.plotly_chart(figure_py)

            figure_py=px.pie(data_frame=df_90,names='brands',values='percentage',
                        width=600,title='percentage',hole=0.5)
            st.plotly_chart(figure_py)
    if questions=="4.Name the states and their total of transaction count and percentage in Aggregated users?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute("""select States,sum(Transaction_count),sum(percentage) from aggregated_users group by States order by sum(Transaction_count),sum(percentage)  ;""")
            data_91 = cursor.fetchall()
            df_91= pd.DataFrame(data_91, columns=['States', 'Transaction_count','percentage'])
            st.write(df_91)
       
            fig_bar_tu=px.bar(df_91,x="States",y="Transaction_count",color="percentage",width=1000,height=900,
                    color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",title="STATES TC AND PERCENTAGE")
            st.plotly_chart(fig_bar_tu)
    if questions=="5.Which are the Top 10 states have the most number of Transaction amount and count in Map transaction?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute(""" select States,sum(Transaction_amount) from map_transaction group by States order by sum(Transaction_amount) DESC LIMIT 10;""")
            data_92 = cursor.fetchall()
            df_92= pd.DataFrame(data_92, columns=['States', 'Transaction_amount'])
            st.write(df_92)
        
        with col2:

            figure_pie=px.line(df_92,x="States",y="Transaction_amount",title="TRANSACTION AMMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
            st.plotly_chart(figure_pie)
        col1,col2=st.columns(2)
        with col1:

            cursor.execute(""" select States,sum(Transaction_count) from map_transaction group by States order by sum(Transaction_count) DESC LIMIT 10;""")
            data_93= cursor.fetchall()
            df_93= pd.DataFrame(data_93, columns=['States', 'Transaction_count'])
            st.write(df_93)
        with col2:
            figure_pie_1=px.line(df_93,x="States",y="Transaction_count",title="TRANSACTION count",
                        color_discrete_sequence=px.colors.sequential.Plotly3_r,height=650,width=600)
            st.plotly_chart(figure_pie_1)
    if questions=="6.Name all their States and corresponding districts in Map transaction?.":
        cursor.execute("""select States,districts from map_transaction;""")
        data_84=cursor.fetchall()
        df_84 =pd.DataFrame(data_84,columns=['States','districts'])
        st.write(df_84)
        figure_pie_1=px.line(df_84,x="States",y="districts",
                        color_discrete_sequence=px.colors.sequential.Oryel_r,height=2000,width=1800)
        st.plotly_chart(figure_pie_1)

    if questions=="7.What are the names of states and their corresponding registeredUsers and AppOpens in map_user?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute("""select states,sum(registeredUsers),sum(appOpens) from map_users group by States order by sum(registeredUsers),sum(appOpens) ;""")
            data_95 = cursor.fetchall()
            df_95= pd.DataFrame(data_95, columns=['states', 'registeredUsers','appOpens'])
            st.write(df_95) 
        with col2:
            figure_py=px.pie(data_frame=df_95,names='states',values='registeredUsers',
                        width=600,title='REgisteredUsers',hole=0.5)
            st.plotly_chart(figure_py)

            figure_py=px.pie(data_frame=df_95,names='states',values='appOpens',
                        width=600,title='appopens',hole=0.5)
            st.plotly_chart(figure_py)

    if questions=="8.Which are the Top 10 states have the most number of Transaction amount and count in Top Transaction?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute(""" select States,sum(Transaction_amount) from top_transaction group by States order by sum(Transaction_amount) DESC LIMIT 10;""")
            data_45 = cursor.fetchall()
            df_45= pd.DataFrame(data_45, columns=['States', 'Transaction_amount'])
            st.write(df_45)
        
        with col2:

            figure_pie=px.bar(df_45,x="States",y="Transaction_amount",title="TRANSACTION AMMOUNT",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r,height=650,width=600)
            st.plotly_chart(figure_pie)
        col1,col2=st.columns(2)
        with col1:

            cursor.execute(""" select States,sum(Transaction_count) from top_transaction group by States order by sum(Transaction_count) DESC LIMIT 10;""")
            data_46= cursor.fetchall()
            df_46= pd.DataFrame(data_46, columns=['States', 'Transaction_count'])
            st.write(df_46)
        with col2:
            figure_pie_1=px.bar(df_46,x="States",y="Transaction_count",title="TRANSACTION count",
                        color_discrete_sequence=px.colors.sequential.Sunsetdark,height=650,width=600)
            st.plotly_chart(figure_pie_1)
        
    if questions=="9.Name the states and their total of transaction count and transaction ammount in top transaction?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute("""select States,sum(Transaction_count),sum(Transaction_amount) from top_transaction group by States order by sum(Transaction_count),sum(Transaction_amount)  ;""")
            data_78= cursor.fetchall()
            df_78= pd.DataFrame(data_78, columns=['States', 'Transaction_count','Transaction_amount'])
            st.write(df_78)
       
            fig_bar_tu=px.bar(df_78,x="States",y="Transaction_amount",color="Transaction_count",width=1000,height=900,
                    color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",title="STATES COUNNT AND AMMOUNT")
            st.plotly_chart(fig_bar_tu)
    if questions=="10.Which are the top 10 states have the most number of registeredUsers in top User?.":
        col1,col2=st.columns(2)
        with col1:
            cursor.execute(""" select States,sum(registeredUsers) from top_user group by States order by sum(registeredUsers) DESC LIMIT 10;""")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['States', 'registeredUsers'])
            st.write(df)
        
        with col2:

            figure_pie=px.bar(df,x="States",y="registeredUsers",title="registeredUsers ",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
            st.plotly_chart(figure_pie)

elif select=="CONTACT":
    st.title("CONTACT")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.subheader("DAVID JEROME R")
    st.write("rdavidjerome2004@gmail.com")
    st.write(" 8220879646")
    st.write(" THIS PROJECT IS DONE BY ME IF YOU HAVE ANY SUGGESTIONS LETS WORK TOGETHER")

    

