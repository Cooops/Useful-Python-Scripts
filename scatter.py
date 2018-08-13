import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import pandas as pd
import plotly.graph_objs as go
import psycopg2
from gen_utils import get_trace_and_log
import datetime
import json

#TODO: add static data folder?
global_renames = {
    'completed_product_nick': 'Nickname',
    'completed_product_titles': 'Card Title',
    'completed_product_prices': 'Price',
    'completed_product_end': 'End Date',
    'completed_product_lst_type': 'Listing Type',
    'completed_product_img_url': 'URL',
}

# formatting/style/css
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        # 'background-color': '#D3D3D3',
        'overflowX': 'scroll',
    }
}

colors = {
    'background': '#000000',
}

test = ['black', 'green', 'blue', 'yellow', 'red', 'orange']

app = dash.Dash()


def fetch_data(query):
    """(query: str) -> str

    Takes in a query, connects to the database and returns the result."""
    result = pd.read_sql(
        sql=query,
        con=psycopg2.connect(
            "dbname='EBAYMAGIC' user='postgres' host='localhost' password='magicarb123' port='5432'"))
    return result


def get_data_alpha():
    """() -> list

       Returns a list of the alpha data in the database."""
    # completed_product_start,
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, completed_product_prices, completed_product_end, completed_product_lst_type, completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Alpha Black Lotus', 'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Pearl', 'Alpha Mox Ruby', 'Alpha Mox Emerald', 'Alpha Timetwister', 'Alpha Ancestral Recall', 'Alpha Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_beta():
    """() -> list

       Returns a list of the beta card data in the database."""
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, completed_product_prices, completed_product_end, completed_product_lst_type, completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Beta Black Lotus MTG', 'Beta Mox Sapphire', 'Beta Mox Jet', 'Beta Mox Pearl', 'Beta Mox Ruby', 'Beta Mox Emerald', 'Beta Timetwister', 'Beta Ancestral Recall', 'Beta Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_unlimited():
    """() -> list

       Returns a list of the unlimited card data in the database."""
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, completed_product_prices, completed_product_end, completed_product_lst_type, completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Unlimited Black Lotus MTG', 'Unlimited Mox Sapphire', 'Unlimited Mox Jet', 'Unlimited Mox Pearl', 'Unlimited Mox Ruby', 'Unlimited Mox Emerald', 'Unlimited Timetwister', 'Unlimited Ancestral Recall', 'Unlimited Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_alpha_avg():
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT completed_product_index_avg
        FROM completed_products_index
        WHERE completed_product_set_id = '1'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_avg'])
    return f'${data[0]:,.2f}'


def get_data_alpha_min():
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT completed_product_index_min
        FROM completed_products_index
        WHERE completed_product_set_id = '1'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_min'])
    return f'${data[0]:,.2f}'


def get_data_alpha_max():
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT completed_product_index_max
        FROM completed_products_index
        WHERE completed_product_set_id = '1'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_max'])
    return f'${data[0]:,.2f}'


def get_data_beta_avg():
    """() -> list

       Returns a list of the beta data in the database."""
    query = (
        f'''
        SELECT completed_product_index_avg
        FROM completed_products_index
        WHERE completed_product_set_id = '2'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_avg'])
    return f'${data[0]:,.2f}'


def get_data_beta_min():
    """() -> list

       Returns a list of the beta data in the database."""
    query = (
        f'''
        SELECT completed_product_index_min
        FROM completed_products_index
        WHERE completed_product_set_id = '2'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_min'])
    return f'${data[0]:,.2f}'


def get_data_beta_max():
    """() -> list

       Returns a list of the beta data in the database."""
    query = (
        f'''
        SELECT completed_product_index_max
        FROM completed_products_index
        WHERE completed_product_set_id = '2'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_max'])
    return f'${data[0]:,.2f}'


def get_data_unlimited_avg():
    """() -> list

       Returns a list of the unlimited data in the database."""
    query = (
        f'''
        SELECT completed_product_index_avg
        FROM completed_products_index
        WHERE completed_product_set_id = '3'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_avg'])
    return f'${data[0]:,.2f}'


def get_data_unlimited_min():
    """() -> list

       Returns a list of the unlimited data in the database."""
    query = (
        f'''
        SELECT completed_product_index_min
        FROM completed_products_index
        WHERE completed_product_set_id = '3'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_min'])
    return f'${data[0]:,.2f}'


def get_data_unlimited_max():
    """() -> list

       Returns a list of the unlimited data in the database."""
    query = (
        f'''
        SELECT completed_product_index_max
        FROM completed_products_index
        WHERE completed_product_set_id = '3'
        ORDER BY primary_ids DESC
        LIMIT 1
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_max'])
    return f'${data[0]:,.2f}'


def get_data_single_stats(value):
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT completed_product_nick, completed_product_avg, completed_product_min, completed_product_max
        FROM completed_products_stats
        WHERE completed_product_nick = '{value}'
        ORDER BY primary_ids DESC
        LIMIT 1;
        ''')
    data = fetch_data(query)
    return data.values


def generate_table(dataframe, max_rows=10):
    """(dataframe: dataframe, max_row: int) -> table"""
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
                     html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                     ]) for i in range(min(len(dataframe), max_rows))]
    )

#TODO: pretty this up -- this makes the dataframe
df1 = get_data_alpha()
df2 = get_data_beta()
df3 = get_data_unlimited()

app.layout = html.Div([

    # Page Header
    html.Div(className='text', children=[
        html.Div('P9 Price Tracker', className='first-header'),
        html.Div('without the nonsense.', className='first-underline'),
        dcc.Link('Go to listing...', href='http://www.ebay.com'),
        html.Img()
        # html.Div(className='header-image')
    ]),
    # # Page Time
    # html.Div([
    #    html.Div(f'{str(datetime.datetime.now())}', className='time')
    # ]),
    # # Page Header 5
    # html.Div([
    #     html.H5('No nonsense. Just the real deal.', className='second-header'),
    # ]),
    html.Div([
        #Dropdown -- #TODO: wrap this in a div? _&_ Make it a button? -- center this too w/ css
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Alpha', 'value': 'Alpha'},
                {'label': 'Beta', 'value': 'Beta'},
                {'label': 'Unlimited', 'value': 'Unlimited'}
            ],
            value=['Unlimited'],  # this decides what is initially loaded?
            className='three columns',
            # style={'color': colors['background']},
            # labelStyle={'display': 'inline-block'},
        )
    ]),
    # Index Prices
    html.Div(
        [
        # html.Div(f':Test: {get_data_alpha()}:'),
        html.Div(f'Alpha Index Average: {get_data_alpha_avg()}'),
        html.Div(f'Alpha Index Min: {get_data_alpha_min()}'),
        html.Div(f'Alpha Index Max: {get_data_alpha_max()}'),
        ],
        className='three columns'),
    html.Div(
        [
        html.Div(f'Beta Index Average: {get_data_beta_avg()}'),
        html.Div(f'Beta Index Min: {get_data_beta_min()}'),
        html.Div(f'Beta Index Max: {get_data_beta_max()}'),
        ],
        className='three columns',
        style={'color': colors['background']},
    ),
    html.Div(
        [
        html.Div(f'Unlimited Index Average: {get_data_unlimited_avg()}'),
        html.Div(f'Unlimited Index Min: {get_data_unlimited_min()}'),
        html.Div(f'Unlimited Index Max: {get_data_unlimited_max()}'),
        ],
        className='three columns'),
    #TODO: Change formatting on hover data to actually display something readable
    # Scatter plot
    html.Div([
        dcc.Graph(
            className='eight columns',
            config={'displayModeBar': False},
            id='price-vs-time',
            style={'height': '65vh',},
            figure={
                'data': [
                    go.Scatter(
                        x=df3[df3['completed_product_nick'] == i]['completed_product_end'],
                        y=df3[df3['completed_product_nick'] == i]['completed_product_prices'],
                        text=df3[df3['completed_product_nick'] == i]['completed_product_titles'],
                        customdata=df3[df3['completed_product_nick'] == i]['completed_product_nick'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 10,
                            'line': {'width': 0.5, 'color': 'white'},
                        },
                        name=i,
                    ) for i in df3.completed_product_nick.unique()
                ],
                'layout': go.Layout(
                xaxis={
                    # 'title': 'Date',
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                },
                yaxis={
                    # 'title': 'Price',
                    'color': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',  # compare
                plot_bgcolor='rgb(0, 12, 77)',
                paper_bgcolor='rgb(0, 12, 77)',
                font=dict(color='rgb(214,236,255)'),
            )
        }
    ),]),
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown(d("""**![img_thumb](http://thumbs1.ebaystatic.com/m/m3zc_zBO42GNgO2lH0noBig/140.jpg)**""")),
            # style=setyles['pre']
            html.Pre(id='click-data', style=styles['pre']),
        ], className='four columns'),
    html.Div([
        # Output Results Table
        html.Div(
            html.Table(id='output-container'),
            className='twelve columns'),
    ], ),
    ]),
    ])


@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def update_table(value):
    if value == 'Alpha':
        results = get_data_alpha().rename(columns=global_renames)
        return generate_table(results, max_rows=15)
    elif value == 'Beta':
        results = get_data_beta().rename(columns=global_renames)
        return generate_table(results, max_rows=15)
    else:
        results = get_data_unlimited().rename(columns=global_renames)
        return generate_table(results, max_rows=15)

@app.callback(
    dash.dependencies.Output('price-vs-time', component_property='figure'),
    [dash.dependencies.Input('dropdown', component_property='value'),])
def update_graph(value):
    if value == 'Alpha':
        df = get_data_alpha()
        return {
            'data': [go.Scatter(
                    x=df[df['completed_product_nick'] == i]['completed_product_end'],
                    y=df[df['completed_product_nick'] == i]['completed_product_prices'],
                    text=df[df['completed_product_nick'] == i]['completed_product_titles'],
                    customdata=df[df['completed_product_nick'] == i]['completed_product_nick'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'},
                        # 'color': ['black'],
                    },
                    name=i,
                    # Change the name of the legends
                    # name=[i for i in df.name.unique()]
                ) for i in df.completed_product_nick.unique()
                ],
            'layout': go.Layout(
                xaxis={
                    # 'title': 'Date',
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                    # 'linecolor': 'rgb(214,236,255)',
                },
                yaxis={
                    # 'title': 'Price ($)',
                    'color': 'rgb(214,236,255)',
                    # 'linecolor': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',  # compare
                # plot_bgcolor='#f5f5f5',
                plot_bgcolor='rgb(0, 12, 77)',
                paper_bgcolor='rgb(0, 12, 77)',
                font=dict(color='rgb(214,236,255)'),
            )
        }
    elif value == 'Beta':
        df = get_data_beta()
        return {
            'data': [go.Scatter(
                    x=df[df['completed_product_nick'] == i]['completed_product_end'],
                    y=df[df['completed_product_nick'] == i]['completed_product_prices'],
                    text=df[df['completed_product_nick'] == i]['completed_product_titles'],
                    # customdata={
                    #     'test': '1',
                    #     'test2': '2',
                    # },
                    customdata=df[df['completed_product_nick'] == i]['completed_product_nick'],
                    # text=df[df['completed_product_titles'] == i]['name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'},
                        # 'color': ['yellow' for i in df.completed_product_nick.unique()],
                    },
                    name=i,
                    # Change the name of the legends
                    # name=[i for i in df.name.unique()]
                ) for i in df.completed_product_nick.unique()
                ],
            'layout': go.Layout(
                xaxis={
                    # 'title': 'Date',
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                    # 'linecolor': 'rgb(214,236,255)',
                },
                yaxis={
                    # 'title': 'Price',
                    'color': 'rgb(214,236,255)',
                    # 'linecolor': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest', # compare
                #TODO: this changes the background color
                plot_bgcolor='rgb(0, 12, 77)',
                paper_bgcolor='rgb(0, 12, 77)',
                font=dict(color='rgb(214,236,255)'),
                # plot_bgcolor='rgb(187, 179, 159)',
                # paper_bgcolor='rgb(108, 85, 87)',
                # font=dict(family='sans-serif', size=12, color='#000'),
                # paper_bgcolor='rgba(255, 0, 0, 0.8)',
            )
        }
    else:
        df = get_data_unlimited()
        return {
            'data': [go.Scatter(
                #TODO: make this display a pretty date and prices?
                x=df[df['completed_product_nick'] == i]['completed_product_end'],
                y=df[df['completed_product_nick'] == i]['completed_product_prices'],
                text=df[df['completed_product_nick'] == i]['completed_product_titles'],
                # customdata='test',
                customdata=df[df['completed_product_nick'] == i]['completed_product_nick'],
                #mode='lines+markers',
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 10,
                    'line': {'width': 0.5, 'color': 'white'},
                    # 'color': ['black'],
                },
                # name=i,
                name=i,
                # Change the name of the legends
                # name=[i for i in df.name.unique()]
            ) for i in df.completed_product_nick.unique()
                     ],
            'layout': go.Layout(
                xaxis={
                    # 'title': 'Date',
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                    # 'linecolor': 'rgb(214,236,255)',
                },
                yaxis={
                    # 'title': 'Price',
                    'color': 'rgb(214,236,255)',
                    # 'tickcolor': 'white',
                    # 'linecolor': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',  # compare
                plot_bgcolor='rgb(0, 12, 77)',
                paper_bgcolor='rgb(0, 12, 77)',
                font=dict(color='rgb(214,236,255)'),
            )
        }

@app.callback(
    Output('click-data', 'children'),
    # TODO: can be clickData as well
    [Input('price-vs-time', 'hoverData')])
def display_click_data(hoverData):
    # TODO: send query(?) and return avg/min/max etc for respective clicked data point
    # if 'mox jet' in clickData['points'][0]['text'].lower():
    #     text = 'Unlimited Mox Jet'
    #     dbStatData = get_data_single_stats(text)
    #     print(text)
    #     print([df3['completed_product_nick'] for df3['completed_product_nick'] in text if df3['completed_product_nick'] in ])
    # if 'mox jet' in hoverData['points'][0]['text'].lower():
    text = hoverData['points'][0]['customdata']
    if text == 'Unlimited Black Lotus MTG':  #TODO: Fix this section, it's incredibly redundant and sloppy...but works for now @ 8/12/2018
        stats = get_data_single_stats(text)
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - hoverData['points'][0]['y'])/((stats[0][3] + hoverData['points'][0]['y']) / 2)
        data = {
            "name": f"{hoverData['points'][0]['customdata']}",
            "price": f"${hoverData['points'][0]['y']:,.2f}",
            "avg": f"${stats[0][1]:,.2f}",
            "min": f"${stats[0][2]:,.2f}",
            "max": f"${stats[0][3]:,.2f}",
            "price/max % diff": f"{percentDiff:,.2f}%",
            "title": f"{hoverData['points'][0]['text']}",
            # "name": "Mox Jet",
            "end": f"{hoverData['points'][0]['x']}",
            # "card": f"{df3['completed_product_nick']}",
            # "avg": f"{dbStatData}",
        }
        return json.dumps(data, indent=2)
    elif text == 'Unlimited Mox Jet':
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - hoverData['points'][0]['y'])/((stats[0][3] + hoverData['points'][0]['y']) / 2)
        data = {
            "name": f"{hoverData['points'][0]['customdata']}",
            "price": f"${hoverData['points'][0]['y']}",
            "avg": f"${stats[0][1]:,.2f}",
            "min": f"${stats[0][2]:,.2f}",
            "max": f"${stats[0][3]:,.2f}",
            "price/max % diff": f"{percentDiff:,.2f}%",
            "title": f"{hoverData['points'][0]['text']}",
            "end": f"{hoverData['points'][0]['x']}",
        }
        return json.dumps(data, indent=2)
    elif text == 'Unlimited Mox Jet':
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - hoverData['points'][0]['y']) / (
        (stats[0][3] + hoverData['points'][0]['y']) / 2)
        data = {
            "name": f"{hoverData['points'][0]['customdata']}",
            "price": f"${hoverData['points'][0]['y']}",
            "avg": f"${stats[0][1]:,.2f}",
            "min": f"${stats[0][2]:,.2f}",
            "max": f"${stats[0][3]:,.2f}",
            "price/max % diff": f"{percentDiff:,.2f}%",
            "title": f"{hoverData['points'][0]['text']}",
            "end": f"{hoverData['points'][0]['x']}",
        }
        return json.dumps(data, indent=2)
#         WHERE completed_product_nick IN ('Unlimited Black Lotus MTG', 'Unlimited Mox Sapphire', 'Unlimited Mox Jet', 'Unlimited Mox Pearl', 'Unlimited Mox Ruby', 'Unlimited Mox Emerald', 'Unlimited Timetwister', 'Unlimited Ancestral Recall', 'Unlimited Time Walk')

    # else:
    #     data = {
    #         "name": f"{hoverData['points'][0]['customdata']}",
    #         "title": f"{hoverData['points'][0]['text']}",
    #         # "name": f"{df3['completed_product_nick']}",
    #         "price": f"{hoverData['points'][0]['y']}",
    #         "end": f"{hoverData['points'][0]['x']}",
    #         # "card": f"{df3['completed_product_nick']}",
    #         # "avg": f"{dbStatData}",
    #     }
    #     return json.dumps(data, indent=2)

#TODO: update index averages as well (same callback or new one?)

external_css = [
    # "https://codepen.io/anon/pen/pVNqEz.css",
    # "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.css",
    # "https://codepen.io/anon/pen/RBvqzG.css",
    # "https://codepen.io/chriddyp/pen/bWLwgP.css",
    # "https://fonts.googleapis.com/css?family=Economica",
    # "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
    # "https://codepen.io/anon/pen/VBRaey.css",
    "https://codepen.io/anon/pen/qyvZNj.css",
]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
