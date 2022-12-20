import streamlit as st
import time 
import pandas as pd
import numpy as np
import csv
import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import threading
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx

st.title("Cloud Logger de Instrumentação")

st.subheader("Comunicação de dados adquiridos através do MQTT Broker")

with st.sidebar:
    st.write("Projeto desenvolvido para a disciplina de Aplicações Avançadas de Instrumentação Biomédica.")
    st.write("O botão Start permite começar a gravação de som com o computador durante um certo número de segundos pré-definido.")
    st.write("Escolher a característica:")
    checkbox_one = st.checkbox("Sonograma")
    checkbox_two = st.checkbox("RMSE")
    checkbox_three = st.checkbox("Dados Adquiridos")
    checkbox_four = st.checkbox("FFT")
    
#Botão Start
start_button = st.empty()
if start_button.button("Start", key='start', type="secondary", disabled=False):
    client = mqtt.Client("Comando_gravar")
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.publish("ritalobo", payload = 'Start')

#Dataframe
df = pd.read_csv("outro_teste2.csv", header=None)
df.index = ["Tempo", "Sound Wave", "Tempo RMSE" ,"RMSE", "Y", "FRQ", "F0"]
final_df=df.T

def plotd():
    st.line_chart(final_df, x = "Tempo", y="Sound Wave")

graph = st.empty;

if checkbox_one:
    st.write("Este primeiro gráfico represenda a amplitude da onda de som que foi gravada em função do tempo de gravação.")   
    plotd()

if checkbox_two:
    st.write("O segundo gráfico representa a Energia RMS")
    st.line_chart(final_df, x = "Tempo RMSE", y="RMSE")

if checkbox_three:
    st.write("Esta é a DataFrame com todos os dados que foram retirados a partir do ficheiro de som:", final_df)

col1, col2 = st.columns([2,2])
with col1:
    if checkbox_four:
        st.write("Este é o FFT do sinal.")
        st.line_chart(final_df, x = "FRQ", y="Y")

f0=final_df["F0"][0]
with col2:
    if checkbox_four:
        st.write("A frequência fundamental é : ", f"{f0}")
