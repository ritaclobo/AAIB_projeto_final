import streamlit as st
import time 
import pandas as pd
import numpy as np
import csv
import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import threading
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx

st.title("Projeto de AAIB")

st.subheader("Distinção entre 4 classes relativas a movimentos em ballet")

with st.sidebar:
    st.write("O objetivo deste projeto foi a utilização do Raspberry PI para adquirir dados de movimento, mais concretamente de acelerómetro e giroscópio, classificando-os mais tarde com o uso de Machine Learning.")
    st.write("Desta forma, nesta página pode-se visualizar os dados adquiridos em dois gráficos, estando também disponível a informação relativamente à classe do movimento.")
    st.write("Considerou-se 4 posições diferentes: D1 (desiquilíbrio para a frente), D2 (desiquilíbrio para trás), Eq (Equilíbrio), Ex (classe de exclusão).")
    st.write("Estas vão ser equivalentes às classes: 1, 2, 3 e 0, respetivamente.")
    st.write("")
    st.write("Escolher o que se quer vizualizar:")
    checkbox_one = st.checkbox("Acelerómetro")
    checkbox_two = st.checkbox("Giroscópio")
    
#Botão Start
start_button = st.empty()
if start_button.button("Start", key='start', type="secondary", disabled=False):
    client = mqtt.Client("Comando_gravar")
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.publish("ritalobo", payload = 'Start')
    
#Dataframe
df = pd.read_csv("outro_teste2.csv", header=None)
df.columns = ["Timestamp", "Accx", "Accy", "Accz", "Gyrox", "Gyroy", "Gyroz", "Classe"]
data_Sub1 = df.drop("Timestamp", axis=1)

#DataFrame com dados do Acelerómetro
data_Acc = data_Sub1[["Accx","Accy","Accz"]]

#DataFrame com dados do Giroscópio
data_Gyr = data_Sub1[["Gyrox","Gyroy","Gyroz"]]

f0=int(data_Sub1["Classe"][0])
#f0=2
predict = [[0,1,2,3],["Classe de exclusão", "Desiquílibrio para a frente", "Desiquilíbrio para trás", "Equilíbrio"]]

classe_df = pd.DataFrame(predict)
cl=classe_df.T
cl.columns = ["classe", "pos"]

f1=str(cl["pos"][f0])

col1, col2 = st.columns([2,2])
with col1:
    st.write("Realizou-se o movimento da classe: ", f"{f0}")

with col2:
    st.write("A classe é: ", f1)



#Acc
if checkbox_one:
    st.line_chart(data_Acc)
    
#Gyr
if checkbox_two:
    st.line_chart(data_Gyr)
