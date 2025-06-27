from dash import html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
from reportWeekly import ReportWeekly
import dash

dash.register_page(__name__, path="/weekly", name="Haftalık Rapor")

selected_tram = "4101"
report = ReportWeekly(f"e014_{selected_tram}_dbarchives")

def generate_pie_chart(report: ReportWeekly):

    hareket_suresi = float(report.getTramMoveTime().replace(":", "."))
    bekleme_suresi = float(report.getTramZeroTime().replace(":", "."))
    calisma_suresi = float(report.getTramWorkTime().replace(":", "."))

    df = pd.DataFrame({
        "Durum": ["Hatta Çalışma Süresi", "Depo Bekleme Süresi", "Araç Canlı Kalma Süresi"],
        "Süre": [hareket_suresi, bekleme_suresi, calisma_suresi]
    })

    fig = px.pie(df, names="Durum", values="Süre", color_discrete_sequence=px.colors.sequential.RdBu,
                 title=f"Tramvay {selected_tram} Haftalık Süre Dağılımı (Saat)", template="none")

    fig.update_traces(textinfo="label+value", textposition="outside")
    fig.update_layout(height=450, width=620, showlegend=True)

    return fig


layout = html.Div([
    html.H1(f"Haftalık Rapor - Tramvay {selected_tram}"),

    html.Div([
        dcc.Graph(id="weekly-pie-chart", figure=generate_pie_chart(report)),
    ]),

    # Butonlar vs istersen buraya ekleyebilirsin
])

@callback(
    Output("weekly-pie-chart", "figure"),
    [Input(f"btn-410{i}", "n_clicks") for i in range(1, 10)] +
    [Input(f"btn-41{i}", "n_clicks") for i in range(10, 19)]
)
def update_chart(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        tram_number = selected_tram
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        tram_number = button_id.split("-")[1]

    report = ReportWeekly(f"e014_{tram_number}_dbarchives")
    return generate_pie_chart(report)
