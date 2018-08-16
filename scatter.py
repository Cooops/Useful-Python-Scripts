import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import pandas as pd
import plotly.graph_objs as go
import psycopg2
import datetime
from datetime import datetime

#TODO: add static data folder?
# Formatting/style/css
global_renames = {
    'completed_product_nick': 'Nickname',
    'completed_product_titles': 'Card Title',
    'completed_product_prices': 'Price',
    'completed_product_end': 'End Date',
    'completed_product_lst_type': 'List Type',
    'completed_product_img_url': 'URL',
}
styles = {
    'pre': {
        # 'padding-top': '20px',
        'padding-bottom': '0px',
        # 'border': 'thin lightgrey solid',
        # 'background-color': '#eef0f5',
        # 'background-color': '#D3D3D3',
        'overflowX': 'scroll',
    }
}


def fetch_data(query):
    """(query: str) -> str

    Takes in a query, connects to the database and returns the result."""
    result = pd.read_sql(
        sql=query,
        con=psycopg2.connect(
            "dbname='a' user='b' host='c' password='d' port='e'"))
    return result


def get_data_alpha():
    """() -> list

       Returns a list of the alpha data in the database."""
    # completed_product_start, completed_product_img_url
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, CAST (CAST (completed_product_prices AS text) AS money), CAST (completed_product_end as timestamp), completed_product_lst_type, completed_product_img_url
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
        SELECT completed_product_nick, completed_product_titles, CAST (CAST (completed_product_prices AS text) AS money), CAST (completed_product_end AS timestamp), completed_product_lst_type, completed_product_img_url
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
        SELECT completed_product_nick, completed_product_titles, CAST (CAST (completed_product_prices AS text) AS money), CAST (completed_product_end AS timestamp), completed_product_lst_type, completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Unlimited Black Lotus MTG', 'Unlimited Mox Sapphire', 'Unlimited Mox Jet', 'Unlimited Mox Pearl', 'Unlimited Mox Ruby', 'Unlimited Mox Emerald', 'Unlimited Timetwister', 'Unlimited Ancestral Recall', 'Unlimited Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_alpha_urls():
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Alpha Black Lotus', 'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Pearl', 'Alpha Mox Ruby', 'Alpha Mox Emerald', 'Alpha Timetwister', 'Alpha Ancestral Recall', 'Alpha Time Walk')
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
        LIMIT 2
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_avg'])
    calc = ((data[0]-data[1])/data[1])*100
    if calc > 0:
        return f'${data[0]:,.0f} (+{calc:,.2f}%)'
    else:
        return f'${data[0]:,.0f} ({calc:,.2f}%)'


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
    return f'${data[0]:,.0f}'


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
    return f'${data[0]:,.0f}'


def get_data_beta_urls():
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Beta Black Lotus MTG', 'Beta Mox Sapphire', 'Beta Mox Jet', 'Beta Mox Pearl', 'Beta Mox Ruby', 'Beta Mox Emerald', 'Beta Timetwister', 'Beta Ancestral Recall', 'Beta Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_beta_avg():
    """() -> list

       Returns a list of the beta data in the database."""
    query = (
        f'''
        SELECT completed_product_index_avg
        FROM completed_products_index
        WHERE completed_product_set_id = '2'
        ORDER BY primary_ids DESC
        LIMIT 2
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_avg'])
    calc = ((data[0]-data[1])/data[1])*100
    if calc > 0:
        return f'${data[0]:,.0f} (+{calc:,.2f}%)'
    else:
        return f'${data[0]:,.0f} ({calc:,.2f}%)'


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
    return f'${data[0]:,.0f}'


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
    return f'${data[0]:,.0f}'


def get_data_unlimited_urls():
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Unlimited Black Lotus MTG', 'Unlimited Mox Sapphire', 'Unlimited Mox Jet', 'Unlimited Mox Pearl', 'Unlimited Mox Ruby', 'Unlimited Mox Emerald', 'Unlimited Timetwister', 'Unlimited Ancestral Recall', 'Unlimited Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_unlimited_avg():
    """() -> list

       Returns a list of the unlimited data in the database."""
    query = (
        f'''
        SELECT completed_product_index_avg
        FROM completed_products_index
        WHERE completed_product_set_id = '3'
        ORDER BY primary_ids DESC
        LIMIT 2
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_avg'])
    calc = ((data[0]-data[1])/data[1])*100
    if calc > 0:
        return f'${data[0]:,.0f} (+{calc:,.2f}%)'
    else:
        return f'${data[0]:,.0f} ({calc:,.2f}%)'


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
    return f'${data[0]:,.0f}'


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
    return f'${data[0]:,.0f}'


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


def get_data_single(value):
    """() -> list

       Returns a list of the alpha data in the database."""
    query = (
        f'''
        SELECT *
        FROM completed_products
        WHERE completed_product_titles = '{value}'
        ''')
    data = fetch_data(query)
    return data.values

# TODO: Add one of these for Images (html.Img) as well?
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

# def generate_table_urls(dataframe, max_rows=10):
#     """(dataframe: dataframe, max_row: int) -> table"""
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
#         # Body for Hyperlinks (html.A)
#         # [html.Tr([
#         #      html.A(dataframe.iloc[i][col], href=dataframe.iloc[i][col]) for col in dataframe.columns
#         #      ]) for i in range(min(len(dataframe), max_rows))]
#         # # Body
#         [html.Tr([
#              html.A(html.Button('Explore...'), href=dataframe.iloc[i][col]) for col in dataframe.columns
#              ]) for i in range(min(len(dataframe), max_rows))]
#     )

# Initialize app
app = dash.Dash()
# Load the initial dataframe
df = get_data_alpha()
# # Get current time
# time = datetime.now()

app.layout = html.Div([
    # Page Header
    html.Div(className='text', children=[
        #TODO: markdown here?
        # html.Img(src='https://cdn.iconscout.com/icon/premium/png-256-thumb/bullseye-38-229114.png', id='first-header-image', className='one columns'),
        html.Div('P9 Price Tracker. No nonsense, just the real deal.', id='first-header', className='twelve columns'),
        # dcc.Link('Go to listing...', href='http://www.ebay.com'),
    ]),
    # Dropdown
    html.Div([
        #TODO: Make these buttons/radio items instead?
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Alpha ', 'value': 'Alpha'},
                {'label': 'Beta ', 'value': 'Beta'},
                {'label': 'Unlimited ', 'value': 'Unlimited'}
            ],
            value='Alpha',
            className='two columns',
        )
    ]),
    # Spacer/equalizer div
    html.Div(
        [
            html.Div(),
        ],
        className='one columns'),
    # Alpha Index Prices
    html.Div(
        [
        html.Div(f'Alpha Index Average: {get_data_alpha_avg()}', id='alpha-avg'),
        html.Div(f'Alpha Index Min: {get_data_alpha_min()}', id='alpha-min'),
        html.Div(f'Alpha Index Max: {get_data_alpha_max()}', id='alpha-max'),
        ],
        className='three columns'),
    # Beta Index Prices
    html.Div(
        [
        html.Div(f'Beta Index Average: {get_data_beta_avg()}', id='beta-avg'),
        html.Div(f'Beta Index Min: {get_data_beta_min()}', id='beta-min'),
        html.Div(f'Beta Index Max: {get_data_beta_max()}', id='beta-max'),
        ],
        className='three columns'),
    # Unlimited Index Prices
    html.Div(
        [
        html.Div(f'Unlimited Index Average: {get_data_unlimited_avg()}', id='unl-avg'),
        html.Div(f'Unlimited Index Min: {get_data_unlimited_min()}', id='unl-min'),
        html.Div(f'Unlimited Index Max: {get_data_unlimited_max()}', id='unl-max'),
        ],
        className='three columns'),
    #TODO: Add linear fit somehow
    #  Scatter plot
    html.Div(
        [
        dcc.Graph(
            className='eight columns',
            config={'displayModeBar': False},
            id='price-vs-time',
            style={'height': '65vh',},
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['completed_product_nick'] == i]['completed_product_end'],
                        y=df[df['completed_product_nick'] == i]['completed_product_prices'],
                        text=df[df['completed_product_nick'] == i]['completed_product_titles'],
                        customdata=df[df['completed_product_nick'] == i]['completed_product_nick'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 10,
                            'line': {'width': 0.5, 'color': 'white'},
                        },
                        name=i,
                    ) for i in df.completed_product_nick.unique()
                ],
                'layout': go.Layout(
                xaxis={
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                },
                yaxis={
                    'color': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                    legend=dict(
                        x=0,
                        y=1,
                        bgcolor='rgba(0,0,0,0)',
                    ),
                hovermode='closest',
                plot_bgcolor='#474747',
                paper_bgcolor='#474747',
                font=dict(color='rgb(214,236,255)'),
            )
        }
    ),
    ]),
    # Click-data title & body
    html.Div(className='row', children=[
        html.Div([

            html.P('Click on any of the data points in the chart for more information.', id="click-data-title"),
            html.Pre(id='click-data', style=styles['pre']),
        ], id="click-data-results", className='four columns'),
    ]),
    # Output Results Table
    html.Div([
        html.Div(
            html.Table(id='output-container'),
            className='twelve columns'),
    ]),
    html.Div(id='footer-buttons', className='twelve columns', children=[

        html.P(
            f"""
            My goal was to create a functional, interactive, and lightweight site that allows MTG players to keep tabs on sold ABU Power9 from eBay. I pre-filtered all of the chaff you may find when sending normal queries on eBay (CE, ICE, Proxies, Deck Boxes, etc.). No google analytics, no affiliate links, no data snooping.
            Feel free to shoot me a tweet or an email, I would love to hear any and all feedback :).
            """, id='goal', className='twelve columns'),

        html.A(html.Button('Twitter', id='twitter-footer', className='four columns'),
        href='https://twitter.com/Coopesmtg', target='blank'),
        html.A(html.Button('Github', id='github-footer', className='four columns'),
        href='https://github.com/Cooops', target='blank'),
        html.A(html.Button('Email', id='email-footer', className='four columns'),
        href='mailto:cooperlimond@gmail.com', target='blank'),
        html.P(
            """
            The information presented on this site about Magic: The Gathering, both literal and graphical, is copyrighted by Wizards of the Coast (a subsidiary of Hasbro, Inc.), which includes, but is not limited to, card images, the mana symbols, and Oracle text.
            This website is not produced, endorsed, supported, or affiliated with Wizards of the Coast.
            """, id='wotc-rights', className='twelve columns'),
        html.P(f"""""", id='spacer-1', className='four columns'),
        html.P(f"""Last updated: {datetime.now()}""", id='last-updated', className='four columns'),
        html.P(f"""""", id='spacer-2', className='four columns'),
        # html.P(
        #     """
        #     Original Content <copyright here> P9prices.com
        #     """, id='trademark', className='twelve columns'),
    ]),
    ])


@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown', 'value')]
)
def update_table(value):
    if value == 'Alpha':
        results = get_data_alpha().rename(columns=global_renames)
        return generate_table(results, max_rows=25)
    elif value == 'Beta':
        results = get_data_beta().rename(columns=global_renames)
        return generate_table(results, max_rows=25)
    elif value == 'Unlimited':
        results = get_data_unlimited().rename(columns=global_renames)
        return generate_table(results, max_rows=25)
    else:
        results = get_data_alpha().rename(columns=global_renames)
        return generate_table(results, max_rows=25)


@app.callback(
    Output('price-vs-time', component_property='figure'),
    [Input('dropdown', component_property='value'),])
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
                    },
                    name=i,
                ) for i in df.completed_product_nick.unique()
                ],
            'layout': go.Layout(
                xaxis={
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                },
                yaxis={
                    'color': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend=dict(
                    x=0,
                    y=1,
                    bgcolor='rgba(0,0,0,0)',
                ),
                hovermode='closest',
                plot_bgcolor='#474747',
                paper_bgcolor='#474747',
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
                    customdata=df[df['completed_product_nick'] == i]['completed_product_nick'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'},
                    },
                    name=i,
                ) for i in df.completed_product_nick.unique()
                ],
            'layout': go.Layout(
                xaxis={
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                },
                yaxis={
                    'color': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend=dict(
                    x=0,
                    y=1,
                    bgcolor='rgba(0,0,0,0)',
                ),
                hovermode='closest',
                #TODO: this changes the background color
                plot_bgcolor='#474747',
                paper_bgcolor='#474747',
                font=dict(color='rgb(214,236,255)'),
            )
        }
    elif value == 'Unlimited':
        df = get_data_unlimited()
        return {
            'data': [go.Scatter(
                #TODO: make this display a pretty date and prices?
                x=df[df['completed_product_nick'] == i]['completed_product_end'],
                y=df[df['completed_product_nick'] == i]['completed_product_prices'],
                text=df[df['completed_product_nick'] == i]['completed_product_titles'],
                customdata=df[df['completed_product_nick'] == i]['completed_product_nick'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 10,
                    'line': {'width': 0.5, 'color': 'white'},
                },
                name=i,
            ) for i in df.completed_product_nick.unique()
                     ],
            'layout': go.Layout(
                xaxis={
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                },
                yaxis={
                    'color': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend=dict(
                    x=0,
                    y=1,
                    bgcolor='rgba(0,0,0,0)',
                ),
                hovermode='closest',
                plot_bgcolor='#474747',
                paper_bgcolor='#474747',
                font=dict(color='rgb(214,236,255)'),
            )
        }
    else:
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
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend=dict(
                    x=0,
                    y=1,
                    # traceorder='normal',
                    # font=dict(
                    #     # family='sans-serif',
                    #     size=10,
                    #     # color='#000'
                    # ),
                    bgcolor='rgba(0,0,0,0)',
                    # bordercolor='#FFFFFF',
                    # borderwidth=2
                ),
                hovermode='closest',  # compare
                # plot_bgcolor='#f5f5f5',
                plot_bgcolor='rgb(0, 12, 77)',
                paper_bgcolor='rgb(0, 12, 77)',
                font=dict(color='rgb(214,236,255)'),
            )
        }


@app.callback(
    Output('click-data', 'children'),
    [Input('price-vs-time', 'clickData')])
def display_click_data(clickData):
    # TODO: send query(?) and return avg/min/max etc for respective clicked data point
    # TODO: can easily add more data-points here -- give this json api its own page perhaps?
    # TODO: Fix this section, it's incredibly redundant and sloppy...but works for now @ 8/12/2018
    # TODO: update index averages as well (same callback or new one?)
    text = clickData['points'][0]['customdata']
    # alpha_avg_index = get_data_alpha_avg().split('$')[1].split(' ')[0].split('%')[0]
    # # alpha_avg_index = alpha_avg_index.lstrip().rstrip()
    # beta_avg_index = get_data_beta_avg().split('$')[1].split(' ')[0].split('%')[0]
    # unlimited_avg_index = get_data_unlimited_avg().split('$')[1].split(' ')[0].split('%')[0]
    if text == 'Alpha Black Lotus':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
         **Title**: {clickData['points'][0]['text']}
         **Selected Price**: ${clickData['points'][0]['y']:,.2f}
         **Average Price**: ${stats[0][1]:,.2f}
         **Lowest Price**: ${stats[0][2]:,.2f}
         **Highest Price**: ${stats[0][3]:,.2f}
         **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
         **Listing Type**: {dbData[0][9]}
         **Item Location**: {dbData[0][11]}
         **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
         **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
         **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
         **Listing URL**: {dbData[0][8]}
         """))
        return data
    elif text == 'Alpha Mox Sapphire':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
         **Title**: {clickData['points'][0]['text']}
         **Selected Price**: ${clickData['points'][0]['y']:,.2f}
         **Average Price**: ${stats[0][1]:,.2f}
         **Lowest Price**: ${stats[0][2]:,.2f}
         **Highest Price**: ${stats[0][3]:,.2f}
         **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
         **Listing Type**: {dbData[0][9]}
         **Item Location**: {dbData[0][11]}
         **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
         **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
         **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
         **Listing URL**: {dbData[0][8]}
         """))
        return data
    elif text == 'Alpha Mox Jet':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Alpha Mox Pearl':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Alpha Mox Ruby':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Alpha Mox Emerald':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Alpha Timetwister':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Alpha Ancestral Recall':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Alpha Time Walk':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Black Lotus MTG':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Mox Sapphire':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Mox Jet':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Mox Pearl':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Mox Ruby':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Mox Emerald':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Timetwister':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Ancestral Recall':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Beta Time Walk':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Black Lotus MTG':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Mox Sapphire':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Mox Jet':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Mox Pearl':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Mox Ruby':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Mox Emerald':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Timetwister':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Ancestral Recall':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data
    elif text == 'Unlimited Time Walk':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        listingLen = listingEndDate - listingStartDate
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                 **Title**: {clickData['points'][0]['text']}
                 **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                 **Average Price**: ${stats[0][1]:,.2f}
                 **Lowest Price**: ${stats[0][2]:,.2f}
                 **Highest Price**: ${stats[0][3]:,.2f}
                 **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                 **Listing Type**: {dbData[0][9]}
                 **Item Location**: {dbData[0][11]}
                 **Listing Start Date**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
                 **Listing End Date**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year}
                 **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
                 **Listing URL**: {dbData[0][8]}
                 """))
        return data


external_css = [
    # "https://codepen.io/anon/pen/OweJPB.css",
    # "https://codepen.io/anon/pen/jpjExG.css",
    # "https://codepen.io/anon/pen/RBzWGJ.css",
    # "https://codepen.io/anon/pen/rrEMWJ.css",
    # "https://codepen.io/anon/pen/ZjdrjN.css",
    "https://codepen.io/anon/pen/zLVjdj.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
