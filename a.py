
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import plotly.express as px
# import pandas as pd

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv(r'C:\Users\ACER\Desktop\study\Data Visualisasi\UAS\openweatherdata-denpasar-1990-2020.csv')
df['date'] = pd.to_datetime(df['dt_iso'], format='%Y-%m-%d %H:%M:%S %z UTC')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

fig_monthly = df.groupby(['year', 'month']).agg({
    'temp': 'mean',
    'rain_today': 'sum'
}).reset_index()

fig_monthly_temp = px.line(
    fig_monthly,
    x='month',
    y='temp',
    color='year',
    labels={'month': 'Bulan', 'temp': 'Rata-rata Suhu (°C)'},
    title='Rata-rata Suhu Bulanan per Tahun'
)

app = Dash(__name__)
app.layout = html.Div([
    html.H1("📊 Dashboard Cuaca Denpasar, Bali", style={'textAlign': 'center', 'color': '#007bff'}),
    
    html.Div([
        html.Label("Pilih Tahun:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': y, 'value': y} for y in sorted(df['year'].unique())],
            value=sorted(df['year'].unique())[0],
            clearable=False
        ),
    ], style={'width': '30%', 'margin': '20px auto'}),

    html.Div([
        html.Div([
            dcc.Graph(id='temp-vs-rain')
        ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'margin': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='line-temp')
        ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'margin': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='bar-rain')
        ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'margin': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(figure=fig_monthly_temp)
        ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'margin': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ])
])

@app.callback(
    [Output('temp-vs-rain', 'figure'),
     Output('line-temp', 'figure'),
     Output('bar-rain', 'figure')],
    Input('year-dropdown', 'value')
)
def update_graphs(selected_year):
    dff = df[df['year'] == selected_year]

    scatter = px.scatter(
        dff,
        x='temp',
        y='rain_today',
        title=f'Suhu vs Curah Hujan — Tahun {selected_year}',
        trendline='ols',
        labels={'temp': 'Suhu (°C)', 'rain_today': 'Curah Hujan (mm)'}
    )

    line = px.line(
        dff,
        x='date',
        y='temp',
        title=f'Suhu Harian Tahun {selected_year}',
        labels={'date': 'Tanggal', 'temp': 'Suhu (°C)'}
    )

    bar = px.bar(
        dff,
        x='date',
        y='rain_today',
        title=f'Curah Hujan Harian Tahun {selected_year}',
        labels={'date': 'Tanggal', 'rain_today': 'Curah Hujan (mm)'}
    )

    return scatter, line, bar

# app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
