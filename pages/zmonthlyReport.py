from dash import html
import dash

dash.register_page(__name__, path="/monhtly-rapor", name="Aylık Rapor")

layout = html.Div(
    children=[
        html.H2("Aylık Rapor Sayfası", style={'textAlign': 'center', 'color': '#4F6F52'}),
        html.P("Buraya günlük toplam rapor özetleri, uyarılar, vs. gelecek.", style={'textAlign': 'center'}),
        html.Ul([
            html.Li("Toplam Enerji Kullanımı: 1240 kWh"),
            html.Li("Toplam KM: 980 km"),
            html.Li("En aktif tramvay: 4107"),
        ], style={'fontSize': '18px', 'marginTop': '20px'})
    ],
    style={'padding': '40px', 'backgroundColor': '#FAF1E6'}
)