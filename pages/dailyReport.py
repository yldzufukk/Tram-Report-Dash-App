from dash import html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from reportDaily import Report
import dash

dash.register_page(__name__, path="/", name="Günlük Rapor")

selected_tram = "4101"
report = Report(f"e014_{selected_tram}_dbarchives")

def generate_pie_chart(tram_number):
    report = Report(f"e014_{tram_number}_dbarchives")
    hareket_suresi = float(report.getTramMoveTime().replace(":", "."))
    bekleme_suresi = float(report.getTramZeroTime().replace(":", "."))
    calisma_suresi = float(report.getTramWorkTime().replace(":", "."))

    df = pd.DataFrame({
        "Durum": ["Hatta Çalışma Süresi", "Depo Bekleme Süresi", "Araç Canlı Kalma Süresi"],
        "Süre": [hareket_suresi, bekleme_suresi, calisma_suresi]
    })

    fig = px.pie(df, names="Durum", values="Süre", color_discrete_sequence=px.colors.sequential.RdBu,
                 title=f"Tramvay {tram_number} Süre Dağılımı (Saat)", template="none")

    fig.update_traces(textinfo="label+value", textposition="outside")

    fig.update_layout(height=450, width=620, showlegend=True)

    return fig

def generate_box_plot(tram_number):
    report = Report(f"e014_{tram_number}_dbarchives")
    tram_km = float(report.getTramKm().replace(" km", ""))
    gnl_km = float(report.getTramDailyKm().replace(" km", ""))

    df = pd.DataFrame({
        "Kategori": ["Toplam KM", "Günlük KM"],
        "Değer": [tram_km, gnl_km]
    })

    fig = px.funnel(df, title=f"Tramvay {tram_number} KM Dağılımı (Km)", color="Kategori", template="seaborn")

    fig.update_layout(
        height=450,
        width=600,
        showlegend=True,
        yaxis=dict(title='', showticklabels=False, showgrid=False, zeroline=False),
        plot_bgcolor='white',
    )

    return fig

def generate_energy_subplots(tram_number):
    report = Report(f"e014_{tram_number}_dbarchives")
    cekis_power = int(report.getTramTotalCekisPower())
    back_gain_energy = int(report.getTramBackGainEnergy())
    break_res_energy = int(report.getTramBreakResEnergy())
    tcu_energy = int(report.getTramTcuEnergy())

    energy_data = {
        "Enerji Türü": ["CER Motoru Tüketilen", "Geri Kazanılan Enerji", "Rezistörde Yakılan Enerji", "Yardımcı Güç Tüketilen"],
        "Değer (kW/kWh)": [cekis_power, back_gain_energy, break_res_energy, tcu_energy]
    }
    df_energy = pd.DataFrame(energy_data)

    fig = px.bar(df_energy, x="Enerji Türü", y="Değer (kW/kWh)", title=f"Tramvay {tram_number} Enerji Dağılımı (kW/kWh)", template="seaborn")
    fig.update_traces(text=df_energy["Değer (kW/kWh)"], textposition="outside")

    fig.update_layout(
        height=470,
        width=600,
        showlegend=False,
        xaxis_title="Enerji Türü",
        yaxis_title="Enerji Değeri (kW/kWh)",
        plot_bgcolor='white',
    )

    return fig

def generate_daily_energy(tram_number):
    report = Report(f"e014_{tram_number}_dbarchives")

    cekis_power = int(report.getTramTotalCekisPower())
    back_gain_energy = int(report.getTramBackGainEnergy())
    break_res_energy = int(report.getTramBreakResEnergy())
    tcu_energy = int(report.getTramTcuEnergy())
    gnl_km = float(report.getTramDailyKm().replace(" km", ""))

    total_power = (cekis_power + break_res_energy + tcu_energy) - back_gain_energy
    cekisGnl_power = cekis_power / gnl_km
    totalDaily_power = total_power / gnl_km

    daily_energy_data = {
        "Enerji Türü": [
            "Toplam Tüketilen Enerji",
            "Km'de Tüketilen Enerji (Çekiş Ünitesi)",
            "Km'de Tüketilen Enerji (Toplam)"
        ],
        "Değer (kW/kWh)": [
            round(total_power, 2),
            round(cekisGnl_power, 2),
            round(totalDaily_power, 2)
        ]
    }

    df_energy = pd.DataFrame(daily_energy_data)

    fig = go.Figure(data=[go.Table(
        header=dict(values=["<b>Enerji Türü</b>", "<b>Değer (kW/kWh)</b>"], fill_color='lightblue', align='left'),
        cells=dict(values=[df_energy["Enerji Türü"], df_energy["Değer (kW/kWh)"]], fill_color='white', align='left')
    )])

    fig.update_layout(title=dict(
        text=f"Tramvay {tram_number} Günlük Enerji Dağılım Tablosu",
        x=0.5,
        xanchor='center',
        font=dict(size=18, color='#333')
    ))

    return fig

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2("TRAMVAY NUMARASI", style={'textAlign': 'center', "color": "#99BC85", "padding": "3px", 'marginBottom': '10px'}),
                html.Div([
                    html.Button(f"410{i}", id=f"btn-410{i}", n_clicks=0, style={
                        'width': '200%', 'padding': '10px', 'marginBottom': '8px',
                        'border': 'none', 'borderRadius': '10px',
                        'backgroundColor': '#E4EFE7', 'color': '#99BC85', 'cursor': 'pointer',
                        'fontSize': '20px', 'fontWeight': 'bold'
                    }) for i in range(1, 10)
                ], style={"background": "#FAF1E6", 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

                html.Div([
                    html.Button(f"41{i}", id=f"btn-41{i}", n_clicks=0, style={
                        'width': '200%', 'padding': '10px', 'marginBottom': '8px',
                        'border': 'none', 'borderRadius': '10px',
                        'backgroundColor': '#E4EFE7', 'color': '#99BC85', 'cursor': 'pointer',
                        'fontSize': '20px', 'fontWeight': 'bold'
                    }) for i in range(10, 19)
                ], style={"background": "#FAF1E6", 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
            ],
            style={'width': '10%', 'backgroundColor': '#FAF1E6', 'padding': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
        ),

        html.Div(
            children=[
                html.Div(
                    children=html.H1(f"Tramvay Verileri - {report.take_datetime()}", style={'textAlign': 'center', 'color': '#99BC85', 'padding': '10px'}),
                    style={'backgroundColor': '#FAF1E6', 'padding': '10px','borderRadius': '10px'}
                ),

                html.Div(
                    children=[
                        html.Div([dcc.Graph(id='tram-pie-chart', figure=generate_pie_chart(selected_tram))], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),
                        html.Div([dcc.Graph(id='tram-box-plot', figure=generate_box_plot(selected_tram))], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),
                        html.Div([dcc.Graph(id='tram-energy-subplots', figure=generate_energy_subplots(selected_tram))], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),
                        html.Div([dcc.Graph(id='tram-energy-dailyplots', figure=generate_daily_energy(selected_tram))], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),
                    ],
                    style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}
                )
            ],
            style={'width': '95%', 'backgroundColor': '#FFFFFF', 'padding': '10px', 'display': 'flex', 'flexDirection': 'column'}
        )
    ],
    style={'display': 'flex', 'height': '145vh', 'margin': '0', 'padding': '0', 'overflow': 'hidden'}
)

@callback(
    [Output('tram-pie-chart', 'figure'), Output('tram-box-plot', 'figure'), Output('tram-energy-subplots', 'figure'), Output('tram-energy-dailyplots', 'figure')],
    [Input(f"btn-410{i}", 'n_clicks') for i in range(1, 10)] +
    [Input(f"btn-41{i}", 'n_clicks') for i in range(10, 19)]
)
def update_chart(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return generate_pie_chart(selected_tram), generate_box_plot(selected_tram), generate_energy_subplots(selected_tram), generate_daily_energy(selected_tram)

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    tram_number = button_id.split('-')[1]
    return generate_pie_chart(tram_number), generate_box_plot(tram_number), generate_energy_subplots(tram_number), generate_daily_energy(tram_number)
