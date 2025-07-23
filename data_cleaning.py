import numpy as np
import pandas as pd
import typing
import matplotlib.pyplot as plt
import pandas as pd


def drop_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df = df.drop(columns=col, errors='ignore')  #remove the column from the dataset, 
    return df                                   #return the dataset without the given column


def categorical_to_num(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df[col] = df[col].astype('category')                #change the type of col to category
    df[col] = df[col].cat.codes                         #replace the category with the coresponding integer  
    return df


def replace_nan_with_mean_class(df: pd.DataFrame, col: str, refcol: str) -> pd.DataFrame:
    df['catmeans'] = df.groupby(refcol)[col].transform('mean')      #create a new column where the mean for the refcol is stored
    df[col] = df[col].fillna(df['catmeans'])                        #fill the NaNs in the column with the means from the new column
    df = df.drop(columns=['catmeans'])                              #remove the new column again
    return df


def remove_nan_rows(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df = df.dropna(subset=[col])    #drop rows in the given column that includes any NaNs
    return df


def remove_row_within_range(df: pd.DataFrame, col: str, min_val: float, max_val: float) -> pd.DataFrame:
    outOfRange = []                                     #create an empty list
    for index, row in df.iterrows():                    #iterate over the dataset and receiving the index and the values from the corresponding row
        if min_val > row[col] or row[col] > max_val:    #check if the column value in the row lays outside the min/max values
            outOfRange.append(index)                    #if it lays outside: the index is stored in the list. procedure is done with every row in dataset
    df = df.drop(outOfRange)                            #with the list of indexes all rows are dropped where the column value is outside the range
    return df


def get_cat_ID_dict(df: pd.DataFrame, col: str) -> dict:
    df[col] = df[col].astype('category')                #change the type of col to category
    catIDs = dict(enumerate(df[col].cat.categories))    #create a dictionary to convert the numbers back to categories later on: {0:'category 1', 1:'category 2',...}
    return catIDs

def find_outlier(df: pd.DataFrame, col: str, new_col: str = None):
    if new_col is None:
        new_col = f"{col}_diff"
    df[new_col] = df[col].diff().abs()
    return df

def plots(df: pd.DataFrame, startdatum: str, tage: int,
          licht_limits: tuple = None,
          temperatur_limits: tuple = None,
          feuchtigkeit_limits: tuple = None):
    df['zeit'] = pd.to_datetime(df['zeit'])
    start = pd.to_datetime(startdatum)
    ende = start + pd.Timedelta(days=tage)
    df_filter = df[(df['zeit'] >= start) & (df['zeit'] < ende)]
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    axs[0].plot(df_filter['zeit'], df_filter['licht'], color='orange')
    axs[0].set_ylabel('Licht')
    axs[0].set_title('Lichtverlauf')
    if licht_limits:
        axs[0].set_ylim(licht_limits)

    axs[1].plot(df_filter['zeit'], df_filter['temperatur'], color='red')
    axs[1].set_ylabel('Temperatur [°C]')
    axs[1].set_title('Temperaturverlauf')
    if temperatur_limits:
        axs[1].set_ylim(temperatur_limits)

    axs[2].plot(df_filter['zeit'], df_filter['feuchtigkeit'], color='blue')
    axs[2].set_ylabel('Feuchtigkeit [%]')
    axs[2].set_title('Feuchtigkeitsverlauf')
    axs[2].set_xlabel('Zeit')
    if feuchtigkeit_limits:
        axs[2].set_ylim(feuchtigkeit_limits)

    plt.tight_layout()
    plt.show()

#def drop_outlier(df)