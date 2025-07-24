import pandas as pd
import os

# Basisverzeichnis
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "Messdaten_Dach")

# Relativer Pfad zu clean_data.csv
clean_data_path = os.path.join(base_dir, "clean_data.csv")

# Relativer Pfad
gs_path = os.path.join(data_dir, "gs_dach_wei11m_5001_filtered.csv")
r_path = os.path.join(data_dir, "r_dach_wei11m_5001_filtered.csv")
t_path = os.path.join(data_dir, "t_dach_wei11m_5001_filtered.csv")

# CSVs einlesen
clean_data = pd.read_csv(clean_data_path, parse_dates=['zeit'])
gs_data = pd.read_csv(gs_path, parse_dates=['time'])
r_data = pd.read_csv(r_path, parse_dates=['time'])
t_data = pd.read_csv(t_path, parse_dates=['time'])

# Umbenennen
gs_data = gs_data.rename(columns={'time': 'zeit', 'value': 'globalstrahlung'})
r_data = r_data.rename(columns={'time': 'zeit', 'value': 'regen'})
t_data = t_data.rename(columns={'time': 'zeit', 'value': 'aussentemperatur'})

# Sortieren für merge_asof
clean_data = clean_data.sort_values('zeit')
gs_data = gs_data.sort_values('zeit')
r_data = r_data.sort_values('zeit')
t_data = t_data.sort_values('zeit')

# Zeitlicher Merge mit ±15 Sekunden Toleranz
merged = pd.merge_asof(clean_data, gs_data, on='zeit', direction='nearest', tolerance=pd.Timedelta(seconds=15))
merged = pd.merge_asof(merged, r_data, on='zeit', direction='nearest', tolerance=pd.Timedelta(seconds=15))
merged = pd.merge_asof(merged, t_data, on='zeit', direction='nearest', tolerance=pd.Timedelta(seconds=15))

# Binärkodierung von regen
merged['regen'] = merged['regen'].replace({'CLOSED': 0, 'OPEN': 1})
merged['regen'] = pd.to_numeric(merged['regen'], errors='coerce')

# Data-Cleaning

def data_preparation(df):
    
    # Fehlende Werte entfernen
    df = df.dropna()

    # Typkonvertierung der hinzugefügten Messwerte
    df['globalstrahlung'] = df['globalstrahlung'].astype('float32')
    df['aussentemperatur'] = df['aussentemperatur'].astype('float32')
    df['regen'] = df['regen'].astype('int8')  # da nur 0/1

    return df

merged_cleaned = data_preparation(merged)

# Optional speichern
merged_cleaned.to_csv(os.path.join(base_dir, "merged_data.csv"), index=False)
