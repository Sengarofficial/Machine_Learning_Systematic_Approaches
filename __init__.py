"""
init file returns in python convention & is the access point for the module we are creating. 
Inside the init file we will define the app such that it ingest the config file. 

"""


from app.views import (
    navbar,
    cumulative_daily_deaths_view,
    daily_deaths_view,
)
from app.loader import (
    download_covid_data,
    cumulative_to_daily_deaths,
    from_deaths_to_deaths_per_million,
)
from config import Config


def app(config: Config):
    # Import / manipulate the data 
    cum_covid_dd = download_covid_data(config)
    covid_dd = cumulative_to_daily_deaths(cum_covid_dd)

    # NavBar(Navigation) through streamlit 
    view, normalize = navbar()

    # Display Page
    if view == 'Cumulative deaths':
        cumulative_daily_deaths_view(
           from_deaths_to_deaths_per_million(config, cum_covid_dd)
           if normalize else cum_covid_dd
        )
    elif view == 'Daily deaths':
        daily_deaths_view(config, 
           from_deaths_to_deaths_per_million(config, covid_dd)
           if normalize else covid_dd
        )