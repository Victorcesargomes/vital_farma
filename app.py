from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import calendar


# import from folders/theme changer
from dash_bootstrap_templates import ThemeSwitchAIO
import dash


FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server


# ======== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph={"displayModeBar": False, "showTips": False}

template_theme1 = "morph"
template_theme2 = "flatly"
url_theme1 = dbc.themes.MORPH
url_theme2 = dbc.themes.FLATLY

# Dicionário de tradução de nomes de meses em inglês para português
meses_em_portugues = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}

# Função para obter o nome do mês em português a partir do número do mês
def get_month_name(month_number):
    return meses_em_portugues[calendar.month_name[month_number]]


# ======== Reading n cleaning file ======= #
df = pd.read_csv('faturamento_2021_2022.csv')
df_cru = df.copy()



df['Ano_Mes'] = df['Ano'].astype(str) + '-' + df['Mês'].astype(str).str.zfill(2)
df_2021 = df[df['Ano'] == 2021][['Faturamento', 'Mês', 'Ano_Mes']]
df_2022 = df[df['Ano'] == 2022][['Faturamento', 'Mês', 'Ano_Mes']]

df_desp = pd.read_csv('despesas_farmacia.csv')
df_desp_cru = df_desp.copy()

df_desp1 = pd.read_csv('DESPESAS_2022.csv')
df_desp1 = df_desp1.copy()


df_cliente = pd.read_csv('dataset_clientes.csv')



# ====== Layout ======== #
app.layout = dbc.Container(children=[
    # Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("VitalFarma")
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-database', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Data Wealth")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://datawealth4.wordpress.com/", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend("Faturamento - 2021-2022")
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1' , className='dbc', config=config_graph)
                        ])
                    ])
                ])
            ], style=tab_card)
        ])
    ], className='g-2 my-auto', style={'margin-top': '7px'}),


    # Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id='graph6', className='dbc', config=config_graph)
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph7', className='dbc', config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),



], fluid=True, style={'height': '100vh'})




# Crie uma nova coluna no DataFrame que combine ano e mês
df['Ano_Mes'] = df['Ano'].astype(str) + '-' + df['Mês'].astype(str).str.zfill(2)



# ======== Callbacks ========== #

# graph 1 
@app.callback(
    Output('graph1', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def graph1(toggle):
    template = template_theme1 if toggle else template_theme2
    
    df_1 = df[df['Ano'] == 2022][['Faturamento', 'Mês', 'Ano_Mes']]
    df_2 = df[df['Ano'] == 2021][['Faturamento', 'Mês','Ano_Mes']]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df_1['Mês'].apply(get_month_name), y=df_1['Faturamento'], name='Faturamento 2022', textposition='auto', text=df_1['Faturamento'], offsetgroup=1))
    fig1.add_trace(go.Bar(x=df_2['Mês'].apply(get_month_name), y=df_2['Faturamento'], name='Faturamento 2021', textposition='auto', text=df_2['Faturamento'], offsetgroup=2))

    fig1.update_layout(main_config, height=200, template=template, showlegend=True, barmode='group', xaxis={'categoryorder':'array', 'categoryarray': [get_month_name(i) for i in range(1, 13)]})
    
    return fig1

# Graph 2
@app.callback(
    Output('graph2', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph2(toggle):
    template = template_theme1 if toggle else template_theme2

    fig2 = go.Figure(go.Pie(labels=df_desp["Categoria"],values=df_desp["Despesas"], hole= .7 ))

    fig2.update_layout(main_config, height=400, template=template, showlegend=False, 
                       title={"text": f"<span style='font-size:150%'>Despesas em 2021</span><br><span style='font-size:70%'>Em Reais</span><br>"},  margin=dict(t=50) )

    return fig2




# Graph 3
@app.callback(
    Output('graph3', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph3(toggle):
    template = template_theme1 if toggle else template_theme2

    fig3 = go.Figure(go.Pie(labels=df_desp1["Categoria"],values=df_desp1["Despesas"], hole= .7 ))

    fig3.update_layout(main_config, height=400, template=template, showlegend=False, 
                       title={"text": f"<span style='font-size:150%'>Despesas em 2022</span><br><span style='font-size:70%'>Em Reais</span><br>"},  margin=dict(t=50) )

    return fig3


@app.callback(
    Output('graph4', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph4(toggle):
    template = template_theme1 if toggle else template_theme2

    fig4 = go.Figure()
    fig4.add_trace(go.Indicator(mode='number',
                            title= {"text": f"<span style='font-size:100%'>Faturamento Total em 2021</span><br><span style='font-size:70%'>Em Reais</span><br>"},
                            value = df_2021['Faturamento'].sum(), number = {'prefix': "R$"}))
    
    fig4.update_layout(main_config, height=250, template=template, showlegend=False)

    return fig4



@app.callback(
    Output('graph5', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph5(toggle):
    template = template_theme1 if toggle else template_theme2

    fig5 = go.Figure()
    fig5.add_trace(go.Indicator(mode='number',
                            title= {"text": f"<span style='font-size:100%'>Faturamento Total em 2022</span><br><span style='font-size:70%'>Em Reais</span><br>"},
                            value = df_2022['Faturamento'].sum(), number = {'prefix': "R$"}))
    
    fig5.update_layout(main_config, height=250, template=template, showlegend=False)

    return fig5

@app.callback(
    Output('graph6', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph6(toggle):
    template = template_theme1 if toggle else template_theme2

    fig6 = go.Figure()
    fig6.add_trace(go.Indicator(mode='number',
                            title= {"text": f"<span style='font-size:100%'>Faturamento Total Consolidado 2021-2022</span><br><span style='font-size:70%'>Em Reais</span><br>"},
                            value = df['Faturamento'].sum(), number = {'prefix': "R$"}))
    
    fig6.update_layout(main_config, height=580, template=template, showlegend=False)

    return fig6

# Graph 7
@app.callback(
    Output('graph7', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(toggle):
    template = template_theme1 if toggle else template_theme2

    df_mean = df.groupby('Ano')['Faturamento'].mean().reset_index()

    fig7 = go.Figure(go.Pie(labels=df_mean["Ano"],values=df_mean["Faturamento"], hole= .7 ))

    fig7.update_layout(main_config, height=900, template=template, showlegend=False, 
                       title={"text": f"<span style='font-size:150%'>Média de Faturamento 2021-2022</span><br><span style='font-size:70%'>Em Reais</span><br>"},  margin=dict(t=50) )

    return fig7


# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
