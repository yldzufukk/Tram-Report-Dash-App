from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Link(
                html.Button(page['name'], style={
                    'padding': '12px 24px',
                    'margin': '5px',
                    'fontSize': '16px',
                    'backgroundColor': '#99BC85',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '10px',
                    'cursor': 'pointer',
                    'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
                }),
                href=page['relative_path'],
                style={'textDecoration': 'none'}
            )
            for page in dash.page_registry.values()
        ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'})
    ], style={'marginBottom': '30px'}),

    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)
