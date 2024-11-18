import streamlit as st

import pandas as pd
import numpy as np
import math 
import statistics 
import plotly.express as px

ussu_hesap_df = pd.DataFrame()
ortalamalar_df = pd.DataFrame()


st.title("MikroAlg Hesapları")

st.sidebar.write("Örnek dosyadaki formata uygun bir **excel dosyası** yüklemelisiniz")
st.sidebar.write("--- buraya indirme linki gelecek ---")

uploaded_file = st.sidebar.file_uploader("Dosya Yükleme")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df_olcumler=pd.read_excel(uploaded_file, engine = 'openpyxl',header=25, usecols='D, E, I, O, U, AA, AG, AM, AS', nrows=33)
    df_olcumler = df_olcumler.drop([0])
    df_olcumler.rename(columns = { 'Unnamed: 3': 'NAME','bactyin HOUSEKEEPİNG': 'bactyin'}, inplace = True)

    st.subheader("Ölçümler")
    st.write(df_olcumler)


if uploaded_file is not None:
    sutunlar = df_olcumler.columns
    avr_DCT_list = []

    for i in sutunlar[2:]:
        df_gecici = df_olcumler.replace(np.nan, 0)
        sutun_index = df_olcumler.columns.get_loc(i)

        NAME = df_olcumler.NAME

        DCT = df_gecici[i] - df_gecici.bactyin
    
        DCT_Control = []
        for k in range(len(DCT)):
            if NAME[k+1] == 'Control':
                DCT_Control.append(float(DCT[k+1]))

        avr_DCT = statistics.mean(DCT_Control)
        
        DDCT = DCT - avr_DCT
        FOLDS = 2 ** (-DDCT)
        
        
        ussu_hesap_df['NAME'] = NAME
        ussu_hesap_df[i+'  DCT'] = DCT
        ussu_hesap_df[i+'  DDCT'] = DDCT
        ussu_hesap_df[i+'  FOLDS'] = FOLDS
        
        FOLDS_Control = []
        FOLDS_Ch =[]
        FOLDS_Sc = []
        FOLDS_Ch_Sc = []
        for k in range(len(FOLDS)):
            if (NAME[k+1] == 'Control') and (FOLDS[k+1] < (10 ** 5)):
                FOLDS_Control.append(float(FOLDS[k+1]))
            elif (NAME[k+1] == 'Ch') and (FOLDS[k+1] < (10 ** 5)):
                FOLDS_Ch.append(FOLDS[k+1])
            elif (NAME[k+1] == 'Sc') and (FOLDS[k+1] < (10 ** 5)):
                FOLDS_Sc.append(FOLDS[k+1])
            elif (NAME[k+1] == 'Ch+Sc') and (FOLDS[k+1] < (10 ** 5)):
                FOLDS_Ch_Sc.append(FOLDS[k+1])
        
        geo_Control = statistics.geometric_mean(FOLDS_Control)
        geo_Ch = statistics.geometric_mean(FOLDS_Ch)
        geo_Sc = statistics.geometric_mean(FOLDS_Sc)
        geo_Ch_Sc = statistics.geometric_mean(FOLDS_Ch_Sc)
        
        sd_Control = statistics.stdev(FOLDS_Control)
        sd_Ch = statistics.stdev(FOLDS_Ch)
        sd_Sc = statistics.stdev(FOLDS_Sc)
        sd_Ch_Sc = statistics.stdev(FOLDS_Ch_Sc)
        
        se_Control = sd_Control / math.sqrt(3)
        se_Ch = sd_Ch / math.sqrt(3)
        se_Sc = sd_Sc / math.sqrt(3)
        se_Ch_Sc = sd_Ch_Sc / math.sqrt(3)

        geo_sonuclar = []
        SD_sonuclar = []
        SE_sonuclar = []
        isimler = []
        
        geo_sonuclar.append('-')
        geo_sonuclar.append('Mean')
        geo_sonuclar.append(geo_Control)
        geo_sonuclar.append(geo_Ch)
        geo_sonuclar.append(geo_Sc)
        geo_sonuclar.append(geo_Ch_Sc)

        SD_sonuclar.append('Avr')
        SD_sonuclar.append('Sd')
        SD_sonuclar.append(sd_Control)
        SD_sonuclar.append(sd_Ch)
        SD_sonuclar.append(sd_Sc)
        SD_sonuclar.append(sd_Ch_Sc)

        SE_sonuclar.append(avr_DCT)
        SE_sonuclar.append('Se')
        SE_sonuclar.append(se_Control)
        SE_sonuclar.append(se_Ch)
        SE_sonuclar.append(se_Sc)
        SE_sonuclar.append(se_Ch_Sc)

        isimler.append(' ')
        isimler.append(' ')
        isimler.append('Control')
        isimler.append('Ch')
        isimler.append('Sc')
        isimler.append('Ch+Sc')

        ortalamalar_df['NAME'] = isimler
        ortalamalar_df[i] = geo_sonuclar
        ortalamalar_df[i+' '] = SD_sonuclar
        ortalamalar_df[i+'  '] = SE_sonuclar



    st.subheader("2^-DDCT Method")
    st.write(ussu_hesap_df)

    st.subheader("Ortalamalar")
    st.write(ortalamalar_df)

    st.subheader("Grafikler")

    isim_list = ortalamalar_df.loc[2:5, 'NAME'].tolist()
    for j in sutunlar[2:]:
        geo_list = ortalamalar_df.loc[2:5, j].tolist()
        Sd_list = ortalamalar_df.loc[2:5, j+' '].tolist()
        Se_list = ortalamalar_df.loc[2:5, j+'  '].tolist()

        st.bar_chart(geo_list)

    
        
        



    

