import paho.mqtt.client as mqtt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe("ritalobo")

def on_message(client, userdata, msg):
    print("saving")
    print("")
    print("received message =" + str(msg.payload.decode()))
    main()
    print("")
    print("Done")

data_t20 = pd.read_csv("D1_1.csv", header=None)
data_t20.columns = ["Timestamp", "Accx", "Accy", "Accz", "Gyrox", "Gyroy", "Gyroz"]
data_t2=data_t20.drop("Timestamp", axis=1)

def M_Learning():
    # No spyder (e depois no Raspberry) tem de estar todos os ficheiros csv (D1, D2, Eq, Ex) utilizados para treinar o modelo
    #Datasets de treino
    
    #D1 - desiquilíbrio acentuado para a frente
    dataD1 = pd.read_csv("D1.csv", header=None)
    dataD1.columns = ["Timestamp", "Accx", "Accy", "Accz", "Gyrox", "Gyroy", "Gyroz"]

    #D2 - desiquilíbrio acentuado para trás
    dataD2 = pd.read_csv("D2.csv", header=None)
    dataD2.columns = ["Timestamp", "Accx", "Accy", "Accz", "Gyrox", "Gyroy", "Gyroz"]

    #Eq - equilíbrio
    dataEq = pd.read_csv("Eq.csv", header=None)
    dataEq.columns = ["Timestamp", "Accx", "Accy", "Accz", "Gyrox", "Gyroy", "Gyroz"]

    #Ex - exclusão
    dataEx = pd.read_csv("Ex.csv", header=None)
    dataEx.columns = ["Timestamp", "Accx", "Accy", "Accz", "Gyrox", "Gyroy", "Gyroz"]

    #----------------------------------------------------------------------------------------------
    #Definição janelas
    # Cortar o dataset de 175 amostras até 1567, ficando com 1392 amostras. Dividindo por 116 temos os 12 grupos
    D1_menor=dataD1.loc[175:1567]
    D1_menor=D1_menor.drop("Timestamp", axis=1)

    # Vamos ter os dividers em: 175, 291, 407, 523, 639,755, 871, 987, 1103, 1219, 1335, 1451, 1567

    t_D1 = [i for i in D1_menor.index if ((i-D1_menor.index[0]) % 116) == 0]

    # Cortar o dataset a partir de 116 amostras, ficando com 14 grupos
    D2_menor=dataD2.loc[116:]
    D2_menor=D2_menor.drop("Timestamp", axis=1)

    # Vamos ter os dividers em: 116, 216, 316,416, 516, 616, 716, 816, 916, 1016, 1116, 1216, 1316, 1416, 1516

    t_D2 = [i for i in D2_menor.index if ((i-D2_menor.index[0]) % 100) == 0]

    # Cortar o dataset de 150 amostras ao final, ficando com 1375 amostras. Dividindo por 110 temos os 12 grupos
    Eq_menor=dataEq.loc[150:]
    Eq_menor=Eq_menor.drop("Timestamp", axis=1)

    # Vamos ter os dividers em: 150, 260, 370, 480, 590, 700, 810, 920, 1030, 1140, 1250, 1360, 1470

    t_Eq = [i for i in Eq_menor.index if ((i-Eq_menor.index[0]) % 110) == 0]

    # Cortar o dataset a partir de 342 amostras. Dividindo por 108 temos os 25 grupos
    Ex_menor=dataEx.loc[342:]
    Ex_menor=Ex_menor.drop("Timestamp", axis=1)

    # Vamos ter os dividers em: 342, 450, 558, 666, 774, 882, 990, 1098, 1206, 1314, 1422, 1530, 1638, etc

    t_Ex = [i for i in Ex_menor.index if ((i-Ex_menor.index[0]) % 108) == 0]

    #------------------------------------------------------------------------------------
    #Feature extraction
    features = []

    labels = []

    #Para o Desiquilíbrio D1 estamos a associar uma label 1
    for p in range(len(t_D1)-1):
        new_D1_df = dataD1.drop("Timestamp", axis=1)[t_D1[p]:t_D1[p+1]]
        w_features_list = [i for j in [new_D1_df.median(axis=0).tolist(), new_D1_df.mean(axis=0).tolist(), new_D1_df.max(axis=0).tolist(),new_D1_df.min(axis=0).tolist(),new_D1_df.std(axis=0).tolist()]for i in j]
        features.append(w_features_list)
        labels.append(1)

    #Para o Desiquilíbrio D2 estamos a associar uma label 2
    for p in range(len(t_D2)-1):
        new_D2_df = dataD2.drop("Timestamp", axis=1)[t_D2[p]:t_D2[p+1]]
        w_features_list = [i for j in [new_D2_df.median(axis=0).tolist(), new_D2_df.mean(axis=0).tolist(), new_D2_df.max(axis=0).tolist(), new_D2_df.min(axis=0).tolist(), new_D2_df.std(axis=0).tolist()]for i in j]
        features.append(w_features_list)
        labels.append(2)
        
    #Para o Equilíbrio Eq estamos a associar uma label 3
    for p in range(len(t_Eq)-1):
        new_Eq_df = dataEq.drop("Timestamp", axis=1)[t_Eq[p]:t_Eq[p+1]]
        w_features_list = [i for j in [new_Eq_df.median(axis=0).tolist(), new_Eq_df.mean(axis=0).tolist(), new_Eq_df.max(axis=0).tolist(), new_Eq_df.min(axis=0).tolist(), new_Eq_df.std(axis=0).tolist()]for i in j]
        features.append(w_features_list)
        labels.append(3)

    #Para a classe de exclusão Ex, estamos a associar uma label0
    for p in range(len(t_Ex)-1):
        new_Ex_df = dataEx.drop("Timestamp", axis=1)[t_Ex[p]:t_Ex[p+1]]
        w_features_list = [i for j in [new_Ex_df.median(axis=0).tolist(), new_Ex_df.mean(axis=0).tolist(), new_Ex_df.max(axis=0).tolist(), new_Ex_df.min(axis=0).tolist(), new_Ex_df.std(axis=0).tolist()]for i in j]
        features.append(w_features_list)
        labels.append(0)
        
    #------------------------------------------------------------------------------------------------
    #Feature selection (lista_features_ideal) e teste and train. Random Forest com os melhores critérios que se encontrou
    data = pd.DataFrame(features, columns=["Median_Accx", "Median_Accy", "Median_Accz", "Median_Gyrx", "Median_Gyry", "Median_Gyrz", "Mean_Accx", "Mean_Accy", "Mean_Accz", "Mean_Gyrx", "Mean_Gyry", "Mean_Gyrz", "Max_Accx", "Max_Accy", "Max_Accz", "Max_Gyrx", "Max_Gyry", "Max_Gyrz", "Min_Accx", "Min_Accy", "Min_Accz", "Min_Gyrx", "Min_Gyry", "Min_Gyrz", "std_Accx", "std_Accy", "std_Accz", "std_Gyrx", "std_Gyry", "std_Gyrz"])

    data["Classe"]=labels
    
    lista_features_ideal=['Max_Gyrz','Median_Accz','Median_Accy','Mean_Accy','std_Gyry','Max_Accz','Mean_Gyrx','Min_Accz','std_Accz','Median_Accx']
    y2=data["Classe"]
    X2=data.drop(columns="Classe")
    X2=X2[lista_features_ideal]

    X_traint, X_testt, y_traint, y_testt = train_test_split(X2, y2, test_size=0.33, random_state=42)

    model=RandomForestClassifier(n_estimators=10, criterion="entropy", max_depth=10, max_features=3).fit(X_traint, y_traint)
    #------------------------------------------------------------------------------------------------
    #Tirar as features da primeira janela do D1: D1_1.csv
    
    w_features_list = [i for j in [data_t2.median(axis=0).tolist(), data_t2.mean(axis=0).tolist(), data_t2.max(axis=0).tolist(),data_t2.min(axis=0).tolist(),data_t2.std(axis=0).tolist()]for i in j]
    ddd = pd.DataFrame(w_features_list).T
    ddd.columns=["Median_Accx", "Median_Accy", "Median_Accz", "Median_Gyrx", "Median_Gyry", "Median_Gyrz", "Mean_Accx", "Mean_Accy", "Mean_Accz", "Mean_Gyrx", "Mean_Gyry", "Mean_Gyrz", "Max_Accx", "Max_Accy", "Max_Accz", "Max_Gyrx", "Max_Gyry", "Max_Gyrz", "Min_Accx", "Min_Accy", "Min_Accz", "Min_Gyrx", "Min_Gyry", "Min_Gyrz", "std_Accx", "std_Accy", "std_Accz", "std_Gyrx", "std_Gyry", "std_Gyrz"]
    ddd=ddd[lista_features_ideal]

    predictions = model.predict(ddd)
    return predictions[0]
    
def main():
    #Treinar os novos dados e classificar com a função anterior
    classe = M_Learning() 
    
    #Depois de já se ter a classe certa, adicionar à dataframe anterior assim
    data_t20["Classe"] =classe
    
    #Depois de DataFrame passa-se para lista
    
    lista_df= data_t20.values.tolist()
    
    #De lista passar para String
    string_lista = str(lista_df)
    
    #Publicar a string anterior
    client.publish("ritalobo22", string_lista)

    print("Acabei")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.loop_forever()
