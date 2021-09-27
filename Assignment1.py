#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as plt


# In[2]:


url = "https://raw.githubusercontent.com/umaimehm/Intro_to_AI_2021/main/assignment1/Ruter_data.csv"
df = pd.read_csv(url, sep=';')


# In[3]:


#Gjør om tidene til timedate formatet.
df["Tidspunkt_Faktisk_Ankomst_Holdeplass_Fra"] = pd.to_datetime(df["Tidspunkt_Faktisk_Ankomst_Holdeplass_Fra"], errors = "coerce")
df["Tidspunkt_Faktisk_Avgang_Holdeplass_Fra"] = pd.to_datetime(df["Tidspunkt_Faktisk_Avgang_Holdeplass_Fra"], errors = "coerce")
df["Tidspunkt_Planlagt_Ankomst_Holdeplass_Fra"] = pd.to_datetime(df["Tidspunkt_Planlagt_Ankomst_Holdeplass_Fra"], errors = "coerce")
df["Tidspunkt_Planlagt_Avgang_Holdeplass_Fra"] = pd.to_datetime(df["Tidspunkt_Planlagt_Avgang_Holdeplass_Fra"], errors = "coerce")


# In[4]:


#Regner ut hvor lange Bussen er på stasjon
df["Tid_Faktisk_Brukt_På_Stasjon"] = df["Tidspunkt_Faktisk_Avgang_Holdeplass_Fra"] - df["Tidspunkt_Faktisk_Ankomst_Holdeplass_Fra"]
df["Tid_Planlagt_Brukt_På_Stasjon"] = df["Tidspunkt_Planlagt_Avgang_Holdeplass_Fra"] - df["Tidspunkt_Planlagt_Ankomst_Holdeplass_Fra"]

df["Tid_Faktisk_Brukt_På_Stasjon"] = df["Tid_Faktisk_Brukt_På_Stasjon"].dt.total_seconds()
df["Tid_Planlagt_Brukt_På_Stasjon"] = df["Tid_Planlagt_Brukt_På_Stasjon"].dt.total_seconds()

#Regner ut hvor mange ledige plasser det er og setter dette inn i en egen collonne.
df["Ledig_kapasitet"] = df["Kjøretøy_Kapasitet"] - df["Passasjerer_Ombord"]


# In[5]:


#Cleaning
df = df[df['Passasjerer_Ombord'] >= 0]
df = df.dropna()
df=df.drop_duplicates()
df=df.replace(r'^\s*$', np.nan, regex=True)


# In[6]:


#Sorterer ut boolsk verdi om det er ledig plass eller ikke
df["Ledig_Bool"] = df["Ledig_kapasitet"].astype(bool)

#Sorterer ut om bussen er forsinket med mer enn ett minutt
df["Buss_Is_Late"] = np.where(df["Tidspunkt_Faktisk_Ankomst_Holdeplass_Fra"] > '00:01:00', False, True)

#Plotter de forskjellige radene i grafen:
df["Tid_Faktisk_Brukt_På_Stasjon"].plot.line().set_xlim(0,100)
df["Tid_Planlagt_Brukt_På_Stasjon"].plot.line().set_xlim(0,100)
df["Ledig_kapasitet"].astype(int).plot.line().set_xlim(0,100)
df["Ledig_Bool"].astype(int).plot.line().set_xlim(0,100)
df["Buss_Is_Late"].astype(int).plot.line().set_xlim(0,100)

