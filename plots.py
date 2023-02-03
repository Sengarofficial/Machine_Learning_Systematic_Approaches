import altair as alt


def lineplot_cumulative_daily_deaths(data):
    # Press `Shift`+`legend entry` to select multiple regions
    selection = alt.selection_multi(fields=['region'], bind='legend')
    
    y_col = [col for col in data.columns if 'deaths' in col][0]

    # The basic line
    line = alt.Chart(data).mark_line().encode(
        x=alt.X('date:T', axis=alt.Axis(title=None)),
        y=alt.Y(f'{y_col}:Q', axis=alt.Axis(title='Cumulative deaths per million people')),
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
    return line


def lineplot_daily_deaths(data, region):
    selection = alt.selection(type='interval', encodings=['x'])
    
    y_col = [col for col in data.columns if 'deaths' in col][0]

    # Line-plot
    line = alt.Chart().mark_line().encode(
        x=alt.X('date:T', axis=alt.Axis(title=None)),   
        y=alt.Y(
            f'{y_col}:Q',
            axis=alt.Axis(title='Daily deaths per million people')
        ),
        opacity=alt.condition(selection, alt.OpacityValue(1), alt.OpacityValue(0.7)),
        size=alt.value(3)
    ).add_selection(
        selection
    )

    mean_line = alt.Chart().mark_rule(color='firebrick').encode(
        y=f'mean({y_col}):Q',
        size=alt.SizeValue(3)
    ).transform_filter(
        selection
    )

    fig = alt.layer(
        line,
        mean_line,
        data=data.loc[data.region == region]
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).properties(
        width=650,
        height=400
    )
    return fig