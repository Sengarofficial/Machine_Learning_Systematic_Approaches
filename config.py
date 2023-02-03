"""
Config file will retrieve data from website, using python file 
to store configuration but you can use yaml, json etc file.

"""

import altair as alt

from pathlib import Path

# Defining class for data path retrieve
class Config:
    alt.data_transformers.disable_max_rows() # Maximum rows warning will disable 


    INPUT_PATH = Path('./data')  # Define Path 

    """
    Link for retrieving the data 

    """
    COVID_URL = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
    
    # Analyzing specific regions 
    
    REGIONS = [
        'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
        'Friuli Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche',
        'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana',
        'Trentino-Alto Adige', 'Umbria', "Valle d'Aosta", 'Veneto'
    ]