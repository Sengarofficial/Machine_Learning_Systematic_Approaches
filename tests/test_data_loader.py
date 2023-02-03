"""
We will check whether file is loading properly from our defined codes or not.

"""

import unittest
import pandas as pd

from config import Config
from app.loader import (
    download_covid_data,
    cumulative_to_daily_deaths,
)

class TestDataLoader(unittest.TestCase):
    def test_download_one_day_covid_data(self):
        config = Config()

        date = '20201231'
        config.COVID_URL = f'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{date}.csv'
        data = download_covid_data(config)
        self.assertEqual(data.shape, (len(config.REGIONS), 3))

    def test_download_invalid_covid_data(self):
        config = Config()

        config.COVID_URL = 'https://google.com'
        data = download_covid_data(config)
        self.assertIsNone(data)

    def test_download_invalid_link(self):
        config = Config()

        config.COVID_URL = 'https://fsnaigerigbeksgneur.com'
        data = download_covid_data(config)
        self.assertIsNone(data)
    
    def test_fake_daily_deaths(self):
        config = Config()

        data = pd.DataFrame({
            'date': pd.date_range(start='1/1/2020', periods=10),
            'region': ['X']*10,
            'deaths': range(10),
        })
        df = cumulative_to_daily_deaths(data)
        print(data)
        print(df)

        mask = df.deaths < 0
        self.assertEqual(sum(mask), 0)
        self.assertEqual(sum(df.deaths), 9)