"""
For loading the data as well as manipulating the data 

"""


import logging
import requests
import pandas as pd
import streamlit as st

from io import StringIO
from config import Config
from app.logger import logger


def from_deaths_to_deaths_per_million(config: Config, data: pd.DataFrame) -> pd.DataFrame:
    ita_ppl = pd.read_csv(str(config.INPUT_PATH / 'italian_population_per_region.csv'))

    data['year'] = data.date.dt.year
    data = data.merge(
        ita_ppl,
        on=['region', 'year']
    )

    data['deaths_per_million'] = (1e6 * data.deaths / data.ppl).round(2)

    # Select only useful columns
    final_table_columns = ['date', 'region', 'deaths_per_million']
    data.drop(columns=data.columns.difference(final_table_columns), inplace=True)
    return data


@st.cache(suppress_st_warning=True, allow_output_mutation=True)

# Downloading covid data passing through the Config, output will pandas dataframe
def download_covid_data(config: Config) -> pd.DataFrame:
    # Download covid deaths data
    try:
        r = requests.get(config.COVID_URL, allow_redirects=True)
        urlData = r.content.decode('utf-8')
        df = pd.read_csv(StringIO(urlData), sep=',', parse_dates=[0])
        logger.info(f"Successfully loaded the the Italian population dataset from '{config.COVID_URL}'.")
    except:
        logger.critical(f"Unable to find/download the covid-19 cumulative deaths dataset from '{config.COVID_URL}'.")
        return None

    # Rename relevant columns translating them in english
    df.rename(columns={
        'data': 'date',
        'denominazione_regione': 'region',
        'deceduti': 'deaths'
    }, inplace=True)

    # Fix regions names
    autonomous_province_to_region = {
        'P.A. Bolzano': 'Trentino-Alto Adige',
        'P.A. Trento': 'Trentino-Alto Adige',
    }
    df.replace(to_replace={
        'region': autonomous_province_to_region
    }, inplace=True)
    df = df.groupby(['date', 'region']).deaths.sum().reset_index()

    # Keep only dates
    df['date'] = df['date'].dt.normalize()

    # Select only useful columns
    final_table_columns = ['date', 'region', 'deaths']
    df.drop(columns=df.columns.difference(final_table_columns), inplace=True)
    return df


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def cumulative_to_daily_deaths(data):
    
    y_col = [col for col in data.columns if 'deaths' in col][0]

    cum_deaths_x_region = pd.pivot_table(
        data=data,
        index=['date'],
        columns=['region'],
        values=y_col,
        aggfunc='sum'
    )
    regions = cum_deaths_x_region.columns
    fake_row = pd.DataFrame(
        data={r: 0 for r in regions},
        index=[cum_deaths_x_region.index.min() - pd.DateOffset(days=1)]
    )
    cum_deaths_x_region = pd.concat([fake_row, cum_deaths_x_region], axis=0)
    inc_deaths_x_region = cum_deaths_x_region.diff(periods=1)
    inc_deaths_x_region.dropna(axis=0, how='all', inplace=True) # Discard the first row
    
    # Assert: inc_deaths_x_region[inc_deaths_x_region < 0].dropna()

    # Search for inconsistent data 
    errors = {
        r: (inc_deaths_x_region[r] < 0).sum() for r in regions 
        if (inc_deaths_x_region[r] < 0).sum() > 0
    }

    if len(errors) > 0:
        logger.warning(f"Found some inconsistent data with negative daily deaths: {errors}.")
    # Flatten the dataset 
    df = pd.DataFrame()
    for col in regions:
        tmp_df = pd.DataFrame({
            'date': inc_deaths_x_region.index,
            'region': col,
            y_col: inc_deaths_x_region[col].values,
        })
        df = df.append(tmp_df)
    logger.info(f"Successfully prepared the covid-19 daily deaths dataset with shape {df.shape}.")
    return df