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

st.write("O objetivo deste projeto foi a utilização do Raspberry PI para adquiri dados de movimento, mais concretamente de acelerómetro e giroscópio, classficiando-os mais tarde com o uso de Machine Learning.")
st.write("Desta forma, nesta página pode-se visualizar os dados adquiridos num gráfico, e está também disponível a informação relativamente à classe do movimento.")
st.write("Considerou-se então: D1, D2")

with st.sidebar:
    st.write("Escolher o que se quer vizualizar:")
    checkbox_one = st.checkbox("Acelerómetro")
    checkbox_two = st.checkbox("Giroscópio")
    
#Dataframe
df = pd.read_csv("outro_teste2.csv", header=None)
df.columns = ["Timestamp", "Accx", "Accy", "Accz", "Gyrox", "Gyroy", "Gyroz", "Classe"]
data_Sub1 = data_Sub.drop("Timestamp", axis=1)

#DataFrame com dados do Acelerómetro
data_Acc = data_Sub1[["Accx","Accy","Accz"]]

#DataFrame com dados do Giroscópio
data_Gyr = data_Sub1[["Gyrox","Gyroy","Gyroz"]]

#Acc
if checkbox_one:
    st.line_chart(data_Acc)
    
#Gyr
if checkbox_two:
    st.line_chart(data_Gyr)

#f0=data_sub1["Classe"][0]
f0=2
st.write("A classe é : ", f"{f0}")
