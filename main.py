import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output
import copy
import random
#выкачка информации gapminder
df = px.data.gapminder().query("year == 2007").copy()  # таблица стран
df = df.reset_index(drop=True)  # Чтобы нумерация в таблице начиналась с нуля
df.rename(columns={'pop': 'population'}, inplace=True) # переименование столбца
df.population = np.int64(1)
df.loc[1, 'population'] = np.int64(100000)  # loc[1, ..] в первом столбце gapminder находится population
color = px.colors.sequential.YlOrRd; # градиент цвета
fig = px.choropleth(df, locations="iso_alpha",
                    color="population",
                    color_continuous_scale=color)

# построение карты
def generate_map():
    return dcc.Graph(id='myGraph', figure=fig)
#    return Plotly.newPlot("myDiv", data, layout, {showLink: false});


#external_stylesheets = ['C:/Users/Dekinus/Desktop/untitled/World_countries.json']
# такты
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    dcc.Interval(id='interval-component',
                interval=500, # милисекунды
                n_intervals=1000),
    generate_map() # строится карта
])
@app.callback(
    Output("myGraph", "figure"),
    [Input('interval-component', 'n_intervals')])

#
def start_infection(n):

    for i in range(0, 142): # число стран
        if (i != 1) and (df.loc[i, 'population'] < 1000000): #max
            b = random.uniform(0.1, 0.25) # рандомный float коэффициент заражения
            df.loc[i, 'population'] = df.population[i] + b*df.population[i]
        if df.loc[i, 'population'] > 1000000:
            df.loc[i, 'population'] = 1000000
    fig = px.choropleth(df, locations="iso_alpha",
                            color="population",
                            hover_name="country",
                            color_continuous_scale=color)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)