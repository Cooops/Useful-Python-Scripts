import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import pandas as pd
import plotly.graph_objs as go
import psycopg2
from datetime import datetime

# vertical = True

#TODO: add static data folder?
# Formatting/style/css
global_renames = {
    'completed_product_nick': 'Nickname',
    'completed_product_titles': 'Title',
    'completed_product_prices': 'Price',
    'completed_product_end': 'End Date',
    'completed_product_start': 'Start Date',
    'completed_product_lst_type': 'List Type',
    'completed_product_img_url': 'URL',
    'completed_product_loc': 'Location',
}
styles = {
    'center': {
        # 'text-align': 'center',
    },
    'pre': {
        # 'position': 'relative',
        'font-weight': 'normal',
        'color': '#b4a793',
        'padding': '0px',
        'margin': '0px',
        'text-align': 'center',
        # 'background-color': 'light grey',
        # 'padding-bottom': '0px',
        # 'overflowX': 'visible',
        # 'word-break': 'break-all',
    },
    'test': {
        'height': '100%',
        'color': '#b4a793',
        'background-color': '#b4a793',

    },
    'indexChanges': {
        'color': '#417b9d',
    },
    'tabs': {
        '-moz-border-radius': '5px',
        '-webkit-border-radius': '5px',
        # 'height': '50px',
        'line-height': '10px',
        'text-align': 'center',
        'color': '#B4A793',
        'background': '#474747',
        # 'primary': '#417B9D',
        # 'border-color': '#798084',
        # 'border-right': '1px solid #798084',
    },
    'selected-tab': {
        '-moz-border-radius': '5px',
        '-webkit-border-radius': '5px',
        'line-height': '10px',
        'text-align': 'center',
        'color': '#FFFFFF',
        'background': '#417B9D',
        # 'primary': '#417B9D',
        # 'border': '#B4A793',
        'border-color': '#B4A793',
        'bottom-border': '#B4A793',
    },
    'tab-div': {
        'border-color': '#798084',
        'bottom-border': '#B4A793',
        'margin': '0px',
        'height': '100%',
        # 'color': '#FFFFFF',
        # 'background': '#417B9D',
        # # 'primary': '#417B9D',
        # 'border': '#B4A793',
        # 'border-color': '#798084',
    },
    'button': {
        # 'color': '#FFFFFF',
    },
}
scatterLayout = go.Layout(
                # autosize=True,
                xaxis={
                    'color': '#d9d1be',
                    'tickcolor': '#d9d1be',
                },
                yaxis={
                    'color': '#d9d1be',
                },
                margin={'l': 40, 'b': 40, 't': 15, 'r': 15},
                legend=dict(
                    x=0,
                    y=1,
                    bgcolor='rgba(0,0,0,0)',
                ),
                hovermode='closest',
                plot_bgcolor='#212127',
                paper_bgcolor='#212127',
                font=dict(color='#d9d1be', size=10)
)

def fetch_data(query):
    """(query: str) -> str

    Takes in a query, connects to the database and returns the result."""
    result = pd.read_sql(
        sql=query,
        con=psycopg2.connect(
            "dbname='a' user='b' host='c' password='d'"))
    return result


def get_data_alpha():
    """() -> list

    Returns a list of the alpha data in the database, in descending order by end date."""
    # completed_product_img_url
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, CAST (CAST (completed_product_prices AS text) AS money), completed_product_end::timestamp::date, completed_product_start::timestamp::date, completed_product_lst_type, completed_product_loc, completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Alpha Black Lotus', 'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Pearl', 'Alpha Mox Ruby', 'Alpha Mox Emerald', 'Alpha Timetwister', 'Alpha Ancestral Recall', 'Alpha Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_beta():
    """() -> list

    Returns a list of the beta data in the database, in descending order by end date."""
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, CAST (CAST (completed_product_prices AS text) AS money), completed_product_end::timestamp::date, completed_product_start::timestamp::date,completed_product_lst_type, completed_product_loc, completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Beta Black Lotus MTG', 'Beta Mox Sapphire', 'Beta Mox Jet', 'Beta Mox Pearl', 'Beta Mox Ruby', 'Beta Mox Emerald', 'Beta Timetwister', 'Beta Ancestral Recall', 'Beta Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_unlimited():
    """() -> list

    Returns a list of the unlimited data in the database, in descending order by end date."""
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, CAST (CAST (completed_product_prices AS text) AS money), completed_product_end::timestamp::date, completed_product_start::timestamp::date, completed_product_lst_type, completed_product_loc, completed_product_img_url
        FROM completed_products
        WHERE completed_product_nick IN ('Unlimited Black Lotus MTG', 'Unlimited Mox Sapphire', 'Unlimited Mox Jet', 'Unlimited Mox Pearl', 'Unlimited Mox Ruby', 'Unlimited Mox Emerald', 'Unlimited Timetwister', 'Unlimited Ancestral Recall', 'Unlimited Time Walk')
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_graded():
    """() -> list

    Returns a list of the BGS & PSA data in the database, in descending order by end date."""
    # completed_product_img_url
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, CAST (CAST (completed_product_prices AS text) AS money), completed_product_end::timestamp::date, completed_product_start::timestamp::date, completed_product_lst_type, completed_product_loc, completed_product_img_url
        FROM completed_products
        WHERE completed_product_titles SIMILAR TO '%(BGS)%' OR completed_product_titles SIMILAR TO '%(PSA)%'
        ORDER BY completed_product_end DESC;
        ''')
    data = fetch_data(query)
    return data


def get_data_alpha_avg():
    """() -> list

    Returns a list of last 2 values avg inserted into the database, in descending order by the primary id."""
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

    Returns a list of last value's min inserted into the database, in descending order by the primary id."""
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

    Returns a list of last value's max inserted into the database, in descending order by the primary id."""
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


def get_data_beta_avg():
    """() -> list

    Returns a list of last 2 values avg inserted into the database, in descending order by the primary id."""
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

    Returns a list of last value's min inserted into the database, in descending order by the primary id."""
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

    Returns a list of last value's max inserted into the database, in descending order by the primary id."""
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


def get_data_unlimited_avg():
    """() -> list

    Returns a list of last 2 values avg inserted into the database, in descending order by the primary id."""
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

    Returns a list of last value's min inserted into the database, in descending order by the primary id."""
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

    Returns a list of last value's max inserted into the database, in descending order by the primary id."""
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

    Returns a list of all of the stat related data in the database for the selected value."""
    query = (
        f'''
        SELECT completed_product_nick, completed_product_avg, completed_product_min, completed_product_max
        FROM completed_products_stats
        WHERE completed_product_nick = ('{value}')
        ORDER BY primary_ids DESC
        LIMIT 1;
        ''')
    data = fetch_data(query)
    return data.values


def get_data_single(value):
    """() -> list

    Returns a list of all of the data in the database for the select value."""
    query = (
        f'''
        SELECT *
        FROM completed_products
        WHERE completed_product_titles = ('{value}')
        ''')
    data = fetch_data(query)
    return data.values


def generate_table(dataframe, max_rows):
    """(dataframe: dataframe, max_row: int) -> table

    Takes in a dataframe and the desired number of rows  and breaks it up into a table, with the headers being the respective unique columns.
    Establishes predefined values `columns` to display as columns in table, rows are left as an empty array.
    Iterates over data points and use .iloc to match iterated value -> separate URL value in same row (uses Title currently)."""
    columns = ['Nickname', 'Title', 'Price', 'End Date', 'Start Date', 'List Type', 'Location']
    rows = []
    for i in range(min(len(dataframe), max_rows)):
        row = []
        for col in columns:
            value = dataframe.iloc[i][col]
            # Update this depending on which columns you want to show links for and what you want those links to be
            if col == 'Title':
                url = dataframe.iloc[i]['URL']
                cell = html.Td(html.A(href=f'{url}', children=value, target='_blank'))
            else:
                cell = html.Td(children=value)
            row.append(cell)
        rows.append(html.Tr(row))
    return html.Div(children=[
            html.Div(
                html.P(f"""
              Last {15} sold listings below.
              """
                       , id='table-notifier'),
            ),
            html.Table(
            # Header
            [html.Tr([html.Th(col) for col in columns])] + rows)])
# def test():
#     return dcc.Input(id='table-rows-notifier', value='rows', type='text')


# Initialize app
app = dash.Dash()
# Suppress callback exceptions, as we are performing callbacks on generated values (graphs based on selected-tab)
app.config['suppress_callback_exceptions'] = True
# Load the initial dataframe
df = get_data_alpha()
# Get averages
alphaAverage = get_data_alpha_avg()
betaAverage = get_data_beta_avg()
unlimitedAverage = get_data_unlimited_avg()

# clickData div -- set as variable for easy re-use
clickDataDiv = html.Pre(dcc.Markdown(d("""
    **Card Text** | Price
    **Title**
    (URL)
    **Average**
    **Low**
    **High**
    ***Percent Change**
    ___
    **Listing Length** | **End** | **Start**
    **Item Location**

     *_(average to selected)_
   """)), id='click-data', style=styles['pre'])

app.layout = html.Div([
    # Page Header
    html.Div(id='header-container', className='twelve columns', children=[
        #TODO: markdown here?
        # html.Img(src='https://cdn.iconscout.com/icon/premium/png-256-thumb/bullseye-38-229114.png', id='first-header-image', className='one columns'),
        html.Div(f'ABUPower <icon>', id='first-header'),
        # html.Img(src='https://cdn.iconscout.com/icon/premium/png-256-thumb/bullseye-38-229114.png', id='first-header-image'),
        # dcc.Link('Go to listing...', href='http://www.ebay.com'),
    ]),
    # Left Menu
    html.Div(id='left-container', className='two columns', style=styles['tab-div'], children=[
        # colors={'primary': '#474747'}
        # Tabs
        dcc.Tabs(id='tabs', value='P9', vertical=True, mobile_breakpoint=800, children=[
            # dcc.Tab(label='Logo here?', value='logo-tab', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='home-tab', label='Home', value='Home', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='p9-tab', label='Power 9', value='P9', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='alpha-tab', label='Alpha', value='Alpha', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='beta-tab', label='Beta', value='Beta', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='unl-tab', label='Unlimited', value='Unlimited', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='arn-tab', label='Arabian Nights', value='Arabian Nights', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='atq-tab', label='Antiquities', value='Antiquities', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='leg-tab', label='Legends', value='Legends', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='graded-tab', label='Graded Cards', value='Graded', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='csv-tab', label='CSV', value='CSV', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='about-tab', label='About', value='About', style=styles['tabs'], selected_style=styles['selected-tab']),
            # dcc.Tab(label='Completed Listings', value='Graded', style=styles['tabs'], selected_style=styles['selected-tab']),
            # dcc.Tab(label='Active Listings', value='Graded', style=styles['tabs'], selected_style=styles['selected-tab']),
        ]), # , style=styles['test']
    ]),
    html.Div(id='main container', className='ten columns', children=[
        html.Div([
        ], id='index-container', className='ten columns'),
        #TODO: Add linear fit somehow
        #  Scatter plot
        html.Div([
        ], id='graph-container', className='seven columns'),
        # Click-data title & body
        html.Div(id='click-data-container', className='three columns', children=[
        ]),
        # TODO: Add button here to show/hide table (default hide) ? Option for 10/25/100 most recent listings ? filterable ? click-able urls (Title as reference value) ?
        # Output Results Table
        html.Div([
            html.Div(
                html.Table(id='output-container'),
                ), # className='ten columns'
        ]),
        # # Footer text
    html.Div(id='footer-container', className='ten columns', children=[
        # wotc rights
        html.P(
            """
            The information presented on this site about Magic: The Gathering, both literal and graphical, is copyrighted by Wizards of the Coast (a subsidiary of Hasbro, Inc.), which includes, but is not limited to, card images, the mana symbols, and Oracle text.
            This website is not produced, endorsed, supported, or affiliated with Wizards of the Coast.
            """, id='wotc-rights'),
        # Still in development notice
        html.P("""This web app is also still in development. Please expect bugs and be kind <3.""", id='still-dev'),
        # Last updated
        html.P(f"""Last updated: {datetime.now()}""", id='last-updated'),
        ]),
    ])
])


@app.callback(
    Output('output-container', 'children'),
    [Input('tabs', 'value')]
)
def update_table(value):
    if value == 'Home':
        return html.Div()
    if value == 'About':
        return html.Div()
    elif value == 'CSV':
        return html.Div('Coming soon')
    elif value == 'Graded':
        # df = get_data_graded()
        # return html.Div([
        #     html.P(dcc.Markdown(d(
        #         'This graph is entirely interactive and responsive. **Click, drag,** and **pan** over data points or legend names to isolate traces. **Double-click** to zoom out.')),
        #         id="click-data-title"),
        #     html.Div(
        #         dcc.Graph(
        #             # className='eight columns',
        #             config={'displayModeBar': False},
        #             id='price-vs-time',
        #             style={'height': '55vh', 'width': '50vw'},
        #             figure={
        #                 'data': [
        #                     go.Scatter(
        #                         x=df[df['completed_product_nick'] == i]['completed_product_end'],
        #                         y=df[df['completed_product_nick'] == i]['completed_product_prices'],
        #                         text=df[df['completed_product_nick'] == i]['completed_product_titles'],
        #                         customdata=df[df['completed_product_nick'] == i]['completed_product_nick'],
        #                         mode='markers',
        #                         opacity=0.7,
        #                         marker={
        #                             'size': 10,
        #                             'line': {'width': 0.5, 'color': 'black'},
        #                         },
        #                         name=i,
        #                     ) for i in tuple(
        #                         ['Alpha Black Lotus', 'Alpha Ancestral Recall', 'Alpha Time Walk', 'Alpha Timetwister',
        #                          'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Emerald', 'Alpha Mox Ruby',
        #                          'Alpha Mox Pearl'])
        #                     ],
        #                 'layout': scatterLayout,
        #             }
        #         ), )
        # ])
        return html.Div()
    elif value == 'Alpha':
        results = get_data_alpha().rename(columns=global_renames)
        # for i in results.completed_product_end:
        #     results = results[results['completed_product_titles'] == i]['completed_product_end']
        return generate_table(results, max_rows=15)
    elif value == 'Beta':
        results = get_data_beta().rename(columns=global_renames)
        return generate_table(results, max_rows=15)
    elif value == 'Unlimited':
        results = get_data_unlimited().rename(columns=global_renames)
        return generate_table(results, max_rows=15)
    else:
        return html.Div()

@app.callback(
    Output('graph-container', 'style'),
    [Input('tabs', 'value'),])
def update_graph(value):
    outliers = ['Home', 'About', 'CSV']
    if any(i in value for i in outliers):
        return {'display': 'none'}
    else:
        return {'display':'block'}

@app.callback(
    Output('graph-container', 'children'),
    [Input('tabs2', 'value'),])
def update_graph(value):
    #TODO: General index trends for older card/all old cards trend as a whole/recently completed listings/etc?
    if value == 'Home':
        return html.Div()
    elif value == 'About':
        return html.Div()
    elif value == 'CSV':
        return html.Div()
    elif value == 'Graded':
        df = get_data_graded()
        return html.Div([
            html.P(dcc.Markdown(d(
                'This graph is entirely interactive and responsive. **Click, drag,** and **pan** over data points or legend names to isolate traces. **Double-click** to zoom out.')),
                id="click-data-title"),
            html.Div(
                dcc.Graph(
                    # className='eight columns',
                    config={'displayModeBar': False},
                    id='price-vs-time',
                    style={'height': '55vh', 'width': '50vw'},
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
                                    'line': {'width': 0.5, 'color': 'black'},
                                },
                                name=i,
                            ) for i in tuple(
                                ['Alpha Black Lotus', 'Alpha Ancestral Recall', 'Alpha Time Walk', 'Alpha Timetwister',
                                 'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Emerald', 'Alpha Mox Ruby',
                                 'Alpha Mox Pearl'])
                            ],
                        'layout': scatterLayout,
                    }
                ), )
        ])
    elif value == 'Alpha':
        df = get_data_alpha()
        return html.Div([
            html.P(dcc.Markdown(d('This graph is entirely interactive and responsive. **Click, drag,** and **pan** over data points or legend names to isolate traces. **Double-click** to zoom out.')), id="click-data-title"),
            html.Div(
                dcc.Graph(
                # className='eight columns',
                config={'displayModeBar': False},
                id='price-vs-time',
                style={'height': '55vh', 'width': '50vw'},
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
                                'line': {'width': 0.5, 'color': 'black'},
                            },
                            name=i,
                        ) for i in tuple(
                            ['Alpha Black Lotus', 'Alpha Ancestral Recall', 'Alpha Time Walk', 'Alpha Timetwister',
                             'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Emerald', 'Alpha Mox Ruby',
                             'Alpha Mox Pearl'])
                        ],
                    'layout': scatterLayout,
                }
                ),)
        ])
    elif value == 'Beta':
        df = get_data_beta()
        return html.Div([
            html.P(dcc.Markdown(d('This graph is entirely interactive and responsive. **Click, drag,** and **pan** over data points or legend names to isolate traces. **Double-click** to zoom out.')), id="click-data-title"),
            dcc.Graph(
                # className='eight columns',
                config={'displayModeBar': False},
                id='price-vs-time',
                style={'height': '55vh', 'width': '50vw'},
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
                                'line': {'width': 0.5, 'color': 'black'},
                            },
                            name=i,
                        ) for i in tuple(
                            ['Beta Black Lotus MTG', 'Beta Ancestral Recall', 'Beta Time Walk', 'Beta Timetwister',
                             'Beta Mox Sapphire', 'Beta Mox Jet', 'Beta Mox Emerald', 'Beta Mox Ruby',
                             'Beta Mox Pearl'])
                        ],
                    'layout': scatterLayout,
                })
            ])
    elif value == 'Unlimited':
        df = get_data_unlimited()
        return html.Div([
            html.P(dcc.Markdown(d('This graph is entirely interactive and responsive. **Click, drag,** and **pan** over data points or legend names to isolate traces. **Double-click** to zoom out.')), id="click-data-title"),
            dcc.Graph(
                # className='eight columns',
                config={'displayModeBar': False},
                id='price-vs-time',
                style={'height': '55vh', 'width': '50vw'},
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
                                'line': {'width': 0.5, 'color': 'black'},
                            },
                            name=i,
                        ) for i in tuple(
                            ['Unlimited Black Lotus MTG', 'Unlimited Ancestral Recall', 'Unlimited Time Walk',
                             'Unlimited Timetwister', 'Unlimited Mox Sapphire', 'Unlimited Mox Jet', 'Unlimited Mox Emerald',
                             'Unlimited Mox Ruby', 'Unlimited Mox Pearl'])
                        ],
                    'layout': scatterLayout,
                }
            )])
    else:
        return html.Div()


@app.callback(
    Output('click-data-container', 'children'),
    [Input('tabs', 'value'),])
def update_click_data_container(value):
    outliers = ['Home', 'About', 'CSV']
    if not any(i in value for i in outliers):
        return clickDataDiv


@app.callback(
    Output('click-data-container', 'style'),
    [Input('tabs', 'value'),])
def update_click_data_container2(value):
    outliers = ['Home', 'About', 'CSV']
    if not any(i in value for i in outliers):
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('index-container', 'children'),
    [Input('tabs', 'value'), ])
def update_index(value):
    if value == 'Home':
        return html.Div(children=[
            html.P(
            # f"""ABUPower is being developed to allow Magic: The Gathering players to more easily keep tabs on completed '93-94 cards by
            # keeping aggregating completed sales from eBay in one easy-to-view location. I have also provided some detailed statistics that
            # hopefully allow users to measure the price and trend of their older cards more accurately. Thanks for checking it out :).""",
            # id='welcome-statement'),
            f"""ABU card prices, aggregated from sales on eBay and plotted in one easy-to-use location. No nonsense, just the real deal.""",
            id='welcome-statement'),
            html.Div([
                html.Div([
                    html.Div( children=[
                        html.Div(f'Alpha Index Average: {alphaAverage}', id='alpha-avg'),
                        html.Div(f'Alpha Index Standard Deviation: {1}', id='alpha-dev'),
                        html.Div(f'Alpha Trend: {1}', id='alpha-trend'),
                    ], id='alpha-div', className='three columns'),
                ]),
            ]),
            html.Div([
                html.Div([
                    html.Div(children=[
                        html.Div(f'Beta Index Average: {betaAverage}', id='beta-avg'),
                        html.Div(f'Beta Index Standard Deviation: {1}', id='beta-dev'),
                        html.Div(f'Beta Trend* *90 days: {1}', id='beta-trend'),
                    ], id='beta-div', className='three columns')])
            ]),
            html.Div([
                html.Div([
                    html.Div( children=[
                        html.Div(f'Unlimited Index Average: {unlimitedAverage}', id='unl-avg'),
                        html.Div(f'Unlimited Index Standard Deviation: {1}', id='unl-dev'),
                        html.Div(f'Unlimited Trend: {1}', id='beta-trend'),
                    ], id='unl-div', className='three columns')])
            ]),
            html.Div([
                html.Div([
                    html.Div( children=[
                        html.Div(f'Arabian Nights Index Average: {1}', id='arn-avg'),
                        html.Div(f'Arabian Nights Standard Deviation: {1}', id='arn-dev'),
                        html.Div(f'Arabian Nights Trend: {1}', id='arn-trend'),
                    ], id='arn-div', className='three columns')])
            ]),
            html.Div([
                html.Div([
                    html.Div( children=[
                        html.Div(f'Antiquities Index Average: {1}', id='atq-avg'),
                        html.Div(f'Antiquities Standard Deviation: {1}', id='atq-dev'),
                        html.Div(f'Antiquities Trend: {1}', id='atq-trend'),
                    ], id='atq-div', className='three columns')])
            ]),
            html.Div([
                html.Div([
                    html.Div( children=[
                        html.Div(f'Legends Index Average: {1}', id='leg-avg'),
                        html.Div(f'Legends Standard Deviation: {1}', id='leg-dev'),
                        html.Div(f'Legends Trend: {1}', id='leg-trend'),
                    ], id='leg-div', className='three columns')])
            ]),
            html.Div([
                html.Div([
                    html.Div( children=[
                        html.Div(f'Power 9 Index Average: {1}', id='p9-avg'),
                        html.Div(f'Power 9 Standard Deviation: {1}', id='p9-dev'),
                        html.Div(f'Power 9 Trend: {1}', id='p9-trend'),
                    ], id='p9-div', className='three columns')])
            ]),
            html.Div([
                html.Div([
                    html.Div( children=[
                        html.Div(f'Graded Cards Index Average: {1}', id='graded-avg'),
                        html.Div(f'Graded Standard Deviation: {1}', id='graded-dev'),
                        html.Div(f'Graded Trend: {1}', id='graded-trend'),
                    ], id='graded-div', className='three columns')])
            ]),
            # html.Div(className='three columns')
        ])
    elif value == 'About':
        return  html.Div(className='ten columns', children=[
            html.Div('Social & Contact', id='button-notifier'),
            # Footer buttons
            html.Div(id='button-container', children=[
                html.A(html.Button('Twitter', id='twitter-button', className='three columns'),
                       href='https://twitter.com/Coopesmtg', target='blank'),
                html.A(html.Button('Github', id='github-button', className='three columns'),
                       href='https://github.com/Cooops', target='blank'),
                html.A(html.Button('Email', id='email-button', className='three columns'),
                       href='mailto:admin@abupower.com', target='blank'),
            ]),
            html.Br(),
            html.Br(),
            html.Div([
                    html.Div(id='goal-container', children=[
                        html.H1('Goal', id='goal-title'),
                        html.Pre(dcc.Markdown(d(
                        f"""
                        My goal was to create a functional, interactive, and relatively lightweight web app that allows MTG
                        players to keep tabs on sold ABU Power9 from eBay. This was a learning project first and foremost.

                         No google analytics or data snooping of any kind.

                        Feel free to shoot me a tweet or an email, I would love to hear any and all feedback :).
                        """)), id='goal', style=styles['center']),
                ]),
                html.Div(id='filtering-container', children=[
                    html.H1('Filtering', id='filtering-title'),
                        html.Pre(dcc.Markdown(d(
                    f"""
                    I am currently pre-filtering the chaff you may find when sending normal queries on eBay. I welcome
                    additions to expand the list <add link to github ref outliers> if you find any outliers.

                    **Currently filtering**:

                            "Collector's", "collector's edition", "Collectors", "International", "CE", "Ce", "IE", "Ie",
                            "Poster", "proxy", "PROXY", "Proxy", "Misprint","Puzzle", "READ DESCRIPTION", "PLAYTEST", "error",
                            "display", "promo", "display/promo","framed", "Reprint", "Booster", "Pack", "Factory Sealed", "RP",
                            "Sealed".
                    """)), id='pre-filter'),
                    ]),
                html.Div(id='faq-container', children=[
                    html.H1('FAQ', id='faq-title'),
                    html.Pre(dcc.Markdown(d(
                        f"""
                        * What stack did you build this with? Why?
                            * Built with [Linux](http://old-releases.ubuntu.com/releases/16.04.4/), [Apache](https://httpd.apache.org/), [PostgreSQL](https://www.postgresql.org/), and [Python](https://www.python.org/downloads/release/python-360/). Fast, easy to iterate over, and great for working
                        with anything data-related, especially data that needs to be generated by scripts.
                        * Ask me some questions and I can add them here...
                            * Maybe ;)
                        """)), id='faq'),
                ]),
            ], id='about-container'),
        ])
    elif value == 'P9':
        return html.Div(dcc.Tabs(id='tabs2', value='Alpha', vertical=False, mobile_breakpoint=800, children=[
            # dcc.Tab(label='Logo here?', value='logo-tab', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='Alpha', label='Alpha', value='Alpha', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='Beta', label='Beta', value='Beta', style=styles['tabs'], selected_style=styles['selected-tab']),
            dcc.Tab(id='Unlimited', label='Unlimited', value='Unlimited', style=styles['tabs'], selected_style=styles['selected-tab']),
        ]))
    elif value == 'CSV':
        return html.Div()
    elif value == 'Alpha':
        return html.Div([
            html.Div([
                #TODO: provide date of lowest/highest price, etc?
                html.Div(f'Alpha Index Average: {alphaAverage}', id='alpha-avg'),
                html.Div(f'Alpha Index Standard Deviation instead?: {get_data_alpha_min()}', id='alpha-min'),
                html.Div(f'Alpha Index Max: {get_data_alpha_max()}', id='alpha-max'),
            ], id='alpha-div', className='three columns'),
            html.Div([
                html.Div(f'Last Sold Listing: {1}', id='alpha-avg-len-30'),
                html.Div(f'Total Listings Sold (90): {1}', id='alpha-avg-len-60'),
                html.Div(f'Average Listing Sold (90): {1}', id='alpha-avg-len-90'),
            ], id='alpha-div', className='three columns'),
            html.Div([
                html.Div(f'Price Trend: {1}', id='alpha-price-trend'),
                html.Div(f'Depth Trend: {1}', id='alpha-depth-trend'),
                html.Div(f'Length Trend: {1}', id='alpha-length-trend'),
            ], id='alpha-div', className='three columns'),
        ])
    elif value == 'Beta':
        return html.Div([
            # Alpha Index Prices
            html.Div([
                html.Div(f'Beta Index Average: {get_data_beta_avg()}', id='beta-avg'),
                html.Div(f'Beta Index Min: {get_data_beta_min()}', id='beta-min'),
                html.Div(f'Beta Index Max: {get_data_beta_max()}', id='beta-max'),
            ], id='beta-div', className='three columns'),
        ])
    elif value == 'Unlimited':
        return html.Div([
            html.Div([
                html.Div(f'Unlimited Index Average: {get_data_unlimited_avg()}', id='unl-avg'),
                html.Div(f'Unlimited Index Min: {get_data_unlimited_min()}', id='unl-min'),
                html.Div(f'Unlimited Index Max: {get_data_unlimited_max()}', id='unl-max'),
            ], id='unl-div', className='three columns'),
        ])
    else:
        return html.Div()

@app.callback(
    Output('click-data', 'children'),
    [Input('price-vs-time', 'clickData')])
def display_click_data(clickData):
    # TODO: send query(?) and return avg/min/max etc for respective clicked data point
    # TODO: can easily add more data-points here -- give this json api its own page perhaps?
    # TODO: Fix this section, it's incredibly redundant and sloppy...but works for now @ 8/12/2018
    # TODO: update index averages as well (same callback or new one?)
    text = clickData['points'][0]['customdata']
    title = clickData['points'][0]['text']
    selectedPrice = clickData['points'][0]['y']
    dbData = get_data_single(title)
    stats = get_data_single_stats(text)
    percentChange = ((selectedPrice - stats[0][1]) / stats[0][1]) * 100
    # percentDiff = 100 * (stats[0][3] - selectedPrice) / ((stats[0][3] + selectedPrice) / 2)
    listingEndDate = datetime.strptime(clickData['points'][0]['x'].split(' ')[0], '%Y-%m-%d')
    listingStartDate = datetime.strptime(dbData[0][12].split('T')[0], '%Y-%m-%d')
    listingLen = listingEndDate - listingStartDate
    data = dcc.Markdown(d(f"""
             **{text}** | ${selectedPrice:,.2f}
             [{title}]({dbData[0][8]})
             **Average**: ${stats[0][1]:,.2f} | **Low**: ${stats[0][2]:,.2f} | **High**: ${stats[0][3]:,.2f}
             **Standard Deviation**: {1}
             **Percent change**: {percentChange:,.2f}%*
             ___
             **Listing Length**: {str(listingLen).split(' ')[0]} day(s)
             **End**: {listingEndDate.month}/{listingEndDate.day}/{listingEndDate.year} | **Start**: {listingStartDate.month}/{listingStartDate.day}/{listingStartDate.year}
             **Listing Type**: {dbData[0][9]}
             **Item Location**: {dbData[0][11]}

              *_(selected to average)_
             """))
    if text == 'Alpha Black Lotus':
        data = data
        return data
    elif text == 'Alpha Mox Sapphire':
        data = data
        return data
    elif text == 'Alpha Mox Jet':
        data = data
        return data
    elif text == 'Alpha Mox Pearl':
        data = data
        return data
    elif text == 'Alpha Mox Ruby':
        data = data
        return data
    elif text == 'Alpha Mox Emerald':
        data = data
        return data
    elif text == 'Alpha Timetwister':
        data = data
        return data
    elif text == 'Alpha Ancestral Recall':
        data = data
        return data
    elif text == 'Alpha Time Walk':
        data = data
        return data
    elif text == 'Beta Black Lotus MTG':
        data = data
        return data
    elif text == 'Beta Mox Sapphire':
        data = data
        return data
    elif text == 'Beta Mox Jet':
        data = data
        return data
    elif text == 'Beta Mox Pearl':
        data = data
        return data
    elif text == 'Beta Mox Ruby':
        data = data
        return data
    elif text == 'Beta Mox Emerald':
        data = data
        return data
    elif text == 'Beta Timetwister':
        data = data
        return data
    elif text == 'Beta Ancestral Recall':
        data = data
        return data
    elif text == 'Beta Time Walk':
        data = data
        return data
    elif text == 'Unlimited Black Lotus MTG':
        data = data
        return data
    elif text == 'Unlimited Mox Sapphire':
        data = data
        return data
    elif text == 'Unlimited Mox Jet':
        data = data
        return data
    elif text == 'Unlimited Mox Pearl':
        data = data
        return data
    elif text == 'Unlimited Mox Ruby':
        data = data
        return data
    elif text == 'Unlimited Mox Emerald':
        data = data
        return data
    elif text == 'Unlimited Timetwister':
        data = data
        return data
    elif text == 'Unlimited Ancestral Recall':
        data = data
        return data
    elif text == 'Unlimited Time Walk':
        data = data
        return data


external_css = [
    # "https://codepen.io/anon/pen/XPrEaW.css",
    # "https://codepen.io/anon/pen/yxNJoK.css",
    # "https://codepen.io/anon/pen/eLNQbQ.css",
    # "https://afeld.github.io/emoji-css/emoji.css",
    # "https://codepen.io/anon/pen/WgQwPQ.css",
    # "https://codepen.io/anon/pen/wEKzdy.css",
    # "https://codepen.io/anon/pen/GXpvBO.css",
    # "https://codepen.io/anon/pen/ZMbayv.css",
    "https://codepen.io/anon/pen/PdPOdz.css",
]

for css in external_css:
    app.css.append_css({"external_url": css})

# server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
