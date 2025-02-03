import pandas as pd 
import numpy as np
import re
import os

# importando archivo excel a analizar y se convierte en dataframe de pandas
df = pd.read_excel(r'C:\Users\Santiago\Documents\PDF Pagarés Fisicos.xlsx')

print(df.columns)