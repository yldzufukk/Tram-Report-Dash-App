from dash import html, dcc
import plotly.express as px
import pandas as pd
from reportWeekly import ReportWeekly
import dash

dash.register_page(__name__, path="/weekly", name="Haftalık Rapor")

tram_numbers = [f"41{i:02d}" for i in range(1, 19)]  # 4101-4118

data = []
for tram in tram_numbers:
    try:
        report = ReportWeekly(f"e014_{tram}_dbarchives")
        hareket_saat = float(report.getTramMoveTime().replace(":", ".")) if report.getTramMoveTime() else 0
        bekleme_saat = float(report.getTramZeroTime().replace(":", ".")) if report.getTramZeroTime() else 0
        enerji = report.getTramTotalCekisPower() + report.getTramTcuEnergy()
        gunluk_km = float(report.getTramDailyKm().replace(" km", "")) if report.getTramDailyKm() else 0

        data.append({
            "Tramvay": tram,
            "Hareket Süresi (saat)": hareket_saat,
            "Bekleme Süresi (saat)": bekleme_saat,
            "Enerji Tüketimi (Wh)": enerji,
            "Günlük Ortalama KM": gunluk_km
        })
    except Exception as e:
        print(f"{tram} verisi alınırken hata oluştu: {e}")
        data.append({
            "Tramvay": tram,
            "Hareket Süresi (saat)": 0,
            "Bekleme Süresi (saat)": 0,
            "Enerji Tüketimi (Wh)": 0,
            "Günlük Ortalama KM": 0
        })

df_all = pd.DataFrame(data).fillna(0)

common_layout = dict(
    template="plotly_white",
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(family="Arial", size=14, color="#4B4B4B"),
    margin=dict(l=40, r=40, t=60, b=40),
)

hareket_fig = px.bar(
    df_all, x="Tramvay", y="Hareket Süresi (saat)",
    title="Haftalık Hareket Süresi", color="Hareket Süresi (saat)",
    color_continuous_scale="YlGnBu", text_auto=".2f"
)
hareket_fig.update_layout(**common_layout)

bekleme_fig = px.bar(
    df_all, x="Tramvay", y="Bekleme Süresi (saat)",
    title="Haftalık Bekleme Süresi", color="Bekleme Süresi (saat)",
    color_continuous_scale="OrRd", text_auto=".2f"
)
bekleme_fig.update_layout(**common_layout)

enerji_fig = px.bar(
    df_all, x="Tramvay", y="Enerji Tüketimi (Wh)",
    title="Toplam Enerji Tüketimi", color="Enerji Tüketimi (Wh)",
    color_continuous_scale="Blues", text_auto=".2s"
)
enerji_fig.update_layout(**common_layout)

km_fig = px.bar(
    df_all, x="Tramvay", y="Günlük Ortalama KM",
    title="Günlük Ortalama KM", color="Günlük Ortalama KM",
    color_continuous_scale="Greens", text_auto=".1f"
)
km_fig.update_layout(**common_layout)

layout = html.Div(
    children=[
        html.Div(
            children=html.H1("HAFTALIK RAPOR", style={
                'textAlign': 'center', 'color': '#99BC85', 'padding': '10px'
            }),
            style={'backgroundColor': '#FAF1E6', 'padding': '10px', 'borderRadius': '10px'}
        ),

        html.Div(
            children=[
                html.Div([dcc.Graph(figure=hareket_fig)], style={
                    'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'
                }),
                html.Div([dcc.Graph(figure=bekleme_fig)], style={
                    'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'
                }),
                html.Div([dcc.Graph(figure=enerji_fig)], style={
                    'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'
                }),
                html.Div([dcc.Graph(figure=km_fig)], style={
                    'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'
                }),
            ],
            style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}
        )
    ],
    style={'width': '100%', 'padding': '20px', 'backgroundColor': '#FFFFFF'}
)
