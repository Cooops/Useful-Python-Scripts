import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import pandas as pd
import plotly.graph_objs as go
import psycopg2
import json
import datetime
import datetime as dt
from datetime import datetime

# global_columns = ['Nickname', 'Card Title', 'Price', 'End Date', 'List Type']

#TODO: add static data folder?
global_renames = {
    'completed_product_nick': 'Nickname',
    'completed_product_titles': 'Card Title',
    'completed_product_prices': 'Price',
    'completed_product_end': 'End Date',
    'completed_product_lst_type': 'List Type',
    'completed_product_img_url': 'URL',
}

product_colors = {
    1: '#414a4c',
    0: '#000000',

}

# formatting/style/css
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

colors = {
    # 'background': '#eef0f5',
    'background': '#f3eef5',
}

test = ['black', 'green', 'blue', 'yellow', 'red', 'orange']

app = dash.Dash()


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

#
# def generate_table_urls(dataframe, max_rows=10):
#     """(dataframe: dataframe, max_row: int) -> table"""
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
#         # TODO: Add one of these for Images (html.Img) as well?
#         # Body for Hyperlinks (html.A)
#         # [html.Tr([
#         #      html.A(dataframe.iloc[i][col], href=dataframe.iloc[i][col]) for col in dataframe.columns
#         #      ]) for i in range(min(len(dataframe), max_rows))]
#         # # Body
#         [html.Tr([
#              html.A(html.Button('Explore...'), href=dataframe.iloc[i][col]) for col in dataframe.columns
#              ]) for i in range(min(len(dataframe), max_rows))]
#     )

#TODO: pretty this up(?) -- this loads the initial dataframe
df = get_data_alpha()

app.layout = html.Div([
    # Page Header
    html.Div(className='text', children=[
        #TODO: markdown here?
        # html.Img(src='https://cdn.iconscout.com/icon/premium/png-256-thumb/bullseye-38-229114.png', id='first-header-image', className='one columns'),
        html.Div('P9 Price Tracker. No nonsense, just the real deal.', id='first-header', className='twelve columns'),
        # html.Div('No nonsense, just the real deal.', className='second-header'),
        # html.Div('without the nonsense.', className='first-underline'),
        # dcc.Link('Go to listing...', href='http://www.ebay.com'),
        # html.Img()
        # html.Div(className='header-image')
    ]),
    # # Page Time
    # html.Div([
    #    html.Div(f'{str(datetime.datetime.now())}', className='time')
    # ]),
    # Dropdown
    html.Div([
        #Dropdown -- #TODO: wrap this in a div? _&_ Make it a button? -- center this too w/ css
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Alpha ', 'value': 'Alpha'},
                {'label': 'Beta ', 'value': 'Beta'},
                {'label': 'Unlimited ', 'value': 'Unlimited'}
            ],
            # value=['Alpha'],  # this decides what is initially loaded
            value='Alpha',
            className='two columns',
            # styles={'color': colors['background']},
            # labelStyle={'display': 'inline-block'},
        )
    ]),
    # Spacer/equalizer div
    html.Div(
        [
            html.Div(),
        ],
        className='one columns'),
    # Index Prices
    html.Div(
        [
        html.Div(f'Alpha Index Average: {get_data_alpha_avg()}', id='alpha-avg'),
        html.Div(f'Alpha Index Min: {get_data_alpha_min()}', id='alpha-min'),
        html.Div(f'Alpha Index Max: {get_data_alpha_max()}', id='alpha-max'),
        # html.Img(src="https://d1rw89lz12ur5s.cloudfront.net/photo/discordiagamesstore/file/273063/large/alpha.png", style={'width': 25, 'height': 22}),
        ],
        className='three columns'),
    html.Div(
        [
        html.Div(f'Beta Index Average: {get_data_beta_avg()}', id='beta-avg'),
        html.Div(f'Beta Index Min: {get_data_beta_min()}', id='beta-min'),
        html.Div(f'Beta Index Max: {get_data_beta_max()}', id='beta-max'),
        ],
        className='three columns'),
        # style={'color': colors['background']},
    html.Div(
        [
        html.Div(f'Unlimited Index Average: {get_data_unlimited_avg()}', id='unl-avg'),
        html.Div(f'Unlimited Index Min: {get_data_unlimited_min()}', id='unl-min'),
        html.Div(f'Unlimited Index Max: {get_data_unlimited_max()}', id='unl-max'),
        ],
        className='three columns'),
    #TODO: Change formatting on hover data to actually display something readable
    # Scatter plot
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
                    # 'title': 'Date',
                    'color': 'rgb(214,236,255)',
                    'tickcolor': 'white',
                },
                yaxis={
                    # 'title': 'Price',
                    'color': 'rgb(214,236,255)',
                },
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend={'x': 0, 'y': 1},
                hovermode='closest',  # compare
                plot_bgcolor='#474747',
                paper_bgcolor='#474747',
                # plot_bgcolor='rgb(0, 12, 77)',
                # paper_bgcolor='rgb(0, 12, 77)',
                font=dict(color='rgb(214,236,255)'),
            )
        }
    ),
    ]),
    html.Div(className='row', children=[
        html.Div([
            # dcc.Markdown(d("""**![img_thumb](https://d1rw89lz12ur5s.cloudfront.net/photo/discordiagamesstore/file/273063/large/alpha.png)**""")),
            # style=setyles['pre']
            html.P('Click on any of the data points in the chart for more information.', id="click-data-title"),
            html.Pre(id='click-data', style=styles['pre']),
            # html.Table(id='click-data'),
        ], id="click-data-results", className='four columns'),
    ]),
    # html.Div([
    # Output Results Table
    html.Div([
        # Output Results Table
        html.Div(
            html.Table(id='output-container'),
            className='twelve columns'),
    # html.Div(
    #     html.A(html.Button('take me there', id='url-buttons-1'),
    #            href='https://twitter.com/Coopesmtg'), className='one columns'),
            # # Index Prices
            # html.Div(
            #     [
            #         html.Div(f'Alpha Index Average: {get_data_alpha_avg()}', id='alpha-avg'),
            #         html.Div(f'Alpha Index Min: {get_data_alpha_min()}', id='alpha-min'),
            #         html.Div(f'Alpha Index Max: {get_data_alpha_max()}', id='alpha-max'),
            #         # html.Img(src="https://d1rw89lz12ur5s.cloudfront.net/photo/discordiagamesstore/file/273063/large/alpha.png", style={'width': 25, 'height': 22}),
            #     ],
            #     className='three columns'),
    # ], className='twelve columns'),
    ]),
    html.Div(id='footer-buttons', className='twelve columns', children=[
        html.P(
            f"""
            My goal was to create a functional, interactive, and lightweight site that allows MTG players to keep tabs on sold ABU Power9 from eBay. I pre-filtered all of the chaff you may find when sending normal queries on eBay (CE, ICE, Proxies, Deck Boxes, etc.). No google analytics, no affiliate links, no data snooping.
            Feel free to shoot me a tweet or an email, I would love to hear any and all feedback :).
            """, id='goal', className='twelve columns'),
        # html.P(
        #     """
        #     Feel free to shoot me a tweet or an email, I would love to hear any an all feedback :).
        #     """, id='goal-2', className='twelve columns'),
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
        # html.P(
        #     """
        #     This website is not produced, endorsed, supported, or affiliated with Wizards of the Coast.
        #     """, id='wotc-rights-2', className='twelve columns'),
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
#
# @app.callback(
#     Output('output-container-2', 'children'),
#     [Input('dropdown', 'value')]
# )
# def update_table_urls(value):
#     if value == 'Alpha':
#         results = get_data_alpha_urls().rename(columns=global_renames)
#         return generate_table_urls(results, max_rows=25)
#     elif value == 'Beta':
#         results = get_data_beta_urls().rename(columns=global_renames)
#         return generate_table_urls(results, max_rows=25)
#     elif value == 'Unlimited':
#         results = get_data_unlimited_urls().rename(columns=global_renames)
#         return generate_table_urls(results, max_rows=25)
#     else:
#         results = get_data_alpha_urls().rename(columns=global_renames)
#         return generate_table_urls(results, max_rows=25)


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
                    # bgcolor='#E2E2E2',
                    # bordercolor='#FFFFFF',
                    # borderwidth=2
                ),
            hovermode='closest',  # compare
                # plot_bgcolor='#f5f5f5',
                # plot_bgcolor='rgb(0, 12, 77)',
                # paper_bgcolor='rgb(0, 12, 77)',
                # plot_bgcolor='rgb(190,198,217)',  #TODO: #d9d1be
                # paper_bgcolor='rgb(190,198,217)',
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
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend={'x': 0, 'y': 1},
                hovermode='closest', # compare
                #TODO: this changes the background color
                plot_bgcolor='#474747',
                paper_bgcolor='#474747',
                font=dict(color='rgb(214,236,255)'),
                # plot_bgcolor='rgb(187, 179, 159)',
                # paper_bgcolor='rgb(108, 85, 87)',
                # font=dict(family='sans-serif', size=12, color='#000'),
                # paper_bgcolor='rgba(255, 0, 0, 0.8)',
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
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend={'x': 0, 'y': 1},
                hovermode='closest',  # compare
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
                    # bgcolor='#E2E2E2',
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
    alpha_avg_index = get_data_alpha_avg().split('$')[1].split(' ')[0].split('%')[0]
    alpha_avg_index = alpha_avg_index.lstrip().rstrip()
    beta_avg_index = get_data_beta_avg().split('$')[1].split(' ')[0].split('%')[0]
    unlimited_avg_index = get_data_unlimited_avg().split('$')[1].split(' ')[0].split('%')[0]
    if text == 'Alpha Black Lotus':
        dbData = get_data_single(clickData['points'][0]['text'])
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        # percentChangeAvg = ((float(stats[0][1])-float(stats[1][1]))/float(stats[1][1]))*100
        listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        # date = datetime.strptime(listingEndDate, '%Y-%m-%d')
        # startDate = datetime.strptime(f"{dbData[0][12].split('T')[0]}", '%Y-%d-%m') # provide UTC time
        # listingLen = datetime.utcnow() - date
        listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
        # listingLen = date - dbData[0][12].split('T')[0]
        listingLen = listingEndDate - listingStartDate
        # **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
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
                     **Listing Length**: {listingLen}
                     **Listing URL**: {dbData[0][8]}
                     """))
        # data = f"Title: {clickData['points'][0]['text']}\n", \
        #        f"Name: {clickData['points'][0]['customdata']}\n", \
        #        f"Selected Price: ${clickData['points'][0]['y']:,.2f}\n", \
        #        f"Avg Price: ${stats[0][1]:,.2f}\n", \
        #        f"Lowest Price: ${stats[0][2]:,.2f}\n", \
        #        f"Highest Price: ${stats[0][3]:,.2f}\n", \
        #        f"Percent of Avg Index (Makeup): {percentAvg:,.2f}%\n", \
        #        f"Percent Difference (Selected->Highest): {percentDiff:,.2f}%\n", \
        #        f"Listing end date: {dt.month}/{dt.day}/{dt.year}\n",
        return data
    elif text == 'Alpha Mox Sapphire':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / (
            (stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Alpha Mox Jet':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Alpha Mox Pearl':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Alpha Mox Ruby':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Alpha Mox Emerald':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Alpha Timetwister':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Alpha Ancestral Recall':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Alpha Time Walk':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(alpha_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Black Lotus MTG':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Mox Sapphire':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Mox Jet':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Mox Pearl':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Mox Ruby':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Mox Emerald':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Timetwister':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Ancestral Recall':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Beta Time Walk':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(beta_avg_index.replace(',', ''))) * 100
        # spreadCalc = (stats[0][3]-stats[0][2])/stats[0][2]*100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
               **Title**: {clickData['points'][0]['text']}
               **Selected Price**: ${clickData['points'][0]['y']:,.2f}
               **Average Price**: ${stats[0][1]:,.2f}
               **Lowest Price**: ${stats[0][2]:,.2f}
               **Highest Price**: ${stats[0][3]:,.2f}
               **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
               **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
               **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Black Lotus MTG':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
              **Title**: {clickData['points'][0]['text']}
              **Selected Price**: ${clickData['points'][0]['y']:,.2f}
              **Average Price**: ${stats[0][1]:,.2f}
              **Lowest Price**: ${stats[0][2]:,.2f}
              **Highest Price**: ${stats[0][3]:,.2f}
              **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
              **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
              **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Mox Sapphire':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                     **Title**: {clickData['points'][0]['text']}
                     **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                     **Average Price**: ${stats[0][1]:,.2f}
                     **Lowest Price**: ${stats[0][2]:,.2f}
                     **Highest Price**: ${stats[0][3]:,.2f}
                     **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                     **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                     **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Mox Jet':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                     **Title**: {clickData['points'][0]['text']}
                     **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                     **Average Price**: ${stats[0][1]:,.2f}
                     **Lowest Price**: ${stats[0][2]:,.2f}
                     **Highest Price**: ${stats[0][3]:,.2f}
                     **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                     **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                     **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Mox Pearl':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                     **Title**: {clickData['points'][0]['text']}
                     **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                     **Average Price**: ${stats[0][1]:,.2f}
                     **Lowest Price**: ${stats[0][2]:,.2f}
                     **Highest Price**: ${stats[0][3]:,.2f}
                     **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                     **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                     **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Mox Ruby':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                     **Title**: {clickData['points'][0]['text']}
                     **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                     **Average Price**: ${stats[0][1]:,.2f}
                     **Lowest Price**: ${stats[0][2]:,.2f}
                     **Highest Price**: ${stats[0][3]:,.2f}
                     **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                     **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                     **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Mox Emerald':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                     **Title**: {clickData['points'][0]['text']}
                     **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                     **Average Price**: ${stats[0][1]:,.2f}
                     **Lowest Price**: ${stats[0][2]:,.2f}
                     **Highest Price**: ${stats[0][3]:,.2f}
                     **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                     **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                     **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Timetwister':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                     **Title**: {clickData['points'][0]['text']}
                     **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                     **Average Price**: ${stats[0][1]:,.2f}
                     **Lowest Price**: ${stats[0][2]:,.2f}
                     **Highest Price**: ${stats[0][3]:,.2f}
                     **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                     **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                     **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data
    elif text == 'Unlimited Ancestral Recall':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                     **Title**: {clickData['points'][0]['text']}
                     **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                     **Average Price**: ${stats[0][1]:,.2f}
                     **Lowest Price**: ${stats[0][2]:,.2f}
                     **Highest Price**: ${stats[0][3]:,.2f}
                     **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                     **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                     **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        # data = f"Title: {clickData['points'][0]['text']}\n", \
        #        f"Name: {clickData['points'][0]['customdata']}\n", \
        #        f"Selected Price: ${clickData['points'][0]['y']:,.2f}\n", \
        #        f"Avg Price: ${stats[0][1]:,.2f}\n", \
        #        f"Lowest Price: ${stats[0][2]:,.2f}\n", \
        #        f"Highest Price: ${stats[0][3]:,.2f}\n", \
        #        f"Percent of Avg Index (Makeup): {percentAvg:,.2f}%\n", \
        #        f"Percent Difference (Selected->Highest): {percentDiff:,.2f}%\n", \
        #        f"Listing end date: {dt.month}/{dt.day}/{dt.year}\n",
        return data
    elif text == 'Unlimited Time Walk':
        stats = get_data_single_stats(text)
        percentAvg = (stats[0][1] / float(unlimited_avg_index.replace(',', ''))) * 100
        percentDiff = 100 * (stats[0][3] - clickData['points'][0]['y']) / ((stats[0][3] + clickData['points'][0]['y']) / 2)
        dt = datetime.datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
        data = dcc.Markdown(d(f"""**Name**: {clickData['points'][0]['customdata']}
                          **Title**: {clickData['points'][0]['text']}
                          **Selected Price**: ${clickData['points'][0]['y']:,.2f}
                          **Average Price**: ${stats[0][1]:,.2f}
                          **Lowest Price**: ${stats[0][2]:,.2f}
                          **Highest Price**: ${stats[0][3]:,.2f}
                          **Percent of Avg Index (Makeup)**: {percentAvg:,.2f}%
                          **Percent Difference (Selected->Highest)**: {percentDiff:,.2f}%
                          **Listing End Date**: {dt.month}/{dt.day}/{dt.year}"""))
        return data


external_css = [
    # "https://codepen.io/anon/pen/OweJPB.css",
    # "https://codepen.io/anon/pen/jpjExG.css",
    # "https://codepen.io/anon/pen/RBzWGJ.css",
    "https://codepen.io/anon/pen/rrEMWJ.css",
]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
