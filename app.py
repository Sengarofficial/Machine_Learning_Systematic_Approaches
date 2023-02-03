import base64
import altair as alt
import pandas as pd
import streamlit as st

from pathlib import Path

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# Global settings
alt.data_transformers.disable_max_rows()
INPUT_PATH = Path('./data')

# Load data
@st.cache(suppress_st_warning=True)
def load_cum_deaths():
    return pd.read_csv(
        str(INPUT_PATH / 'cumulative_covid_daily_deaths_per_million_ppl.csv'),
        parse_dates=[0]
    )
@st.cache(suppress_st_warning=True)
def load_inc_deaths():
    return pd.read_csv(
        str(INPUT_PATH / 'covid_daily_deaths_per_million_ppl.csv'),
        parse_dates=[0]
    )
@st.cache(suppress_st_warning=True)
def load_hist_deaths():
    return pd.read_csv(
        str(INPUT_PATH / 'covid_monthly_deaths_per_million_ppl.csv')
    )
cum_covid_dd = load_cum_deaths()
inc_covid_dd = load_inc_deaths()
hist_comp_md = load_hist_deaths()
REGIONS = sorted(cum_covid_dd.region.unique())

# Dashboard title
st.title('COVID-19 deaths analysis')

# Sidebar
st.sidebar.title('Navigation Bar')
view = st.sidebar.radio(
    'Select one',
    ('Cumulative deaths', 'Daily deaths', 'Monthly deaths'),
    index=0
)
header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=100%>".format(
    img_to_bytes("./imgs/italy_regions-wanderingitaly.com.png")
)
st.sidebar.markdown(
    header_html, unsafe_allow_html=True,
)


# Display Page
if view == 'Cumulative deaths':
    st.header('Cumulative daily deaths during 2020')

    ###########
    # Plot  1 #
    ###########
    # Press `Shift`+`legend entry` to select multiple regions
    selection = alt.selection_multi(fields=['region'], bind='legend')

    # The basic line
    line = alt.Chart(cum_covid_dd).mark_line().encode(
        x=alt.X('date:T', axis=alt.Axis(title=None)),
        y=alt.Y('deaths_per_million:Q', axis=alt.Axis(title='Cumulative deaths per million people')),
        color=alt.Color('region:N', scale=alt.Scale(scheme='category20'), legend=alt.Legend(title='Region')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        size=alt.value(4)
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_legend(
        titleFontSize=14,
        labelFontSize=12,
        symbolStrokeWidth=8
    ).add_selection(
        selection
    ).properties(
        width=600,
        height=500
    )

    st.altair_chart(line)

elif view == 'Daily deaths':
    st.header('Daily deaths during 2020')

    selected_region = st.selectbox(
        'Regions',
        REGIONS
    )
    ###########
    # Plot  2 #
    ###########
    brush = alt.selection(type='interval', encodings=['x'])

    # Line-plot
    line = alt.Chart().mark_line().encode(
        x=alt.X('date:T', axis=alt.Axis(title=None)),
        y=alt.Y(
            'deaths_per_million:Q',
            axis=alt.Axis(title='Daily deaths per million people')
        ),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
        size=alt.value(3)
    ).add_selection(
        brush
    )

    mean_line = alt.Chart().mark_rule(color='firebrick').encode(
        y='mean(deaths_per_million):Q',
        size=alt.SizeValue(3)
    ).transform_filter(
        brush
    )

    fig = alt.layer(
        line,
        mean_line,
        data=inc_covid_dd.loc[inc_covid_dd.region == selected_region]
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).properties(
        width=650,
        height=400
    )
    st.altair_chart(fig)

elif view == 'Monthly deaths':
    st.header('Monthly deaths during 2020 against historical data')

    selected_region = st.selectbox(
        'Regions',
        REGIONS
    )

    ###########
    # Plot  3 #
    ###########
    domain = ['non-covid', 'covid']
    range_ = ['#1f77b4', '#ff7f0e']

    # Base chart
    base = alt.Chart(hist_comp_md).encode(
        x=alt.X('month:O', axis=alt.Axis(title=None, labelAngle=0)),
        y=alt.Y(
            'deaths_per_million:Q',
            axis=alt.Axis(title='Monthly deaths per million people'),
        )
    ).transform_filter(
        alt.FieldEqualPredicate(field='region', equal=selected_region)
    )

    # Bar-plot (with legend selection)
    selection = alt.selection_multi(fields=['death_type'], bind='legend')
    bar = base.mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        opacity=0.5
    ).encode(
        color=alt.Color(
            'death_type:N',
            scale=alt.Scale(domain=domain, range=range_),
            legend=alt.Legend(title='Death type')
        ),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.01)),
        tooltip=[
            alt.Tooltip('region', title='Region'),
            alt.Tooltip('death_type', title='Death type'),
            alt.Tooltip('deaths_per_million', title='Deaths per million')
        ]
    ).transform_filter(
        # death_type != 'total'
        alt.FieldOneOfPredicate(field='death_type', oneOf=['covid', 'non-covid'])
    ).add_selection(
        selection
    )

    # Line-plot
    selection2 = alt.selection_multi(fields=['year'], bind='legend')
    line = base.mark_line(color='black').encode(
        detail='year:N'
    ).transform_filter(
        # death_type == 'total'
        alt.FieldEqualPredicate(field='death_type', equal='total')
    ).transform_filter(
        # year < 2020
        alt.FieldLTPredicate(field='year', lt=2020)
    ).add_selection(
        selection2
    )

    # Complete plot
    fig = alt.layer(
        bar,
        line
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=22
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(fig)