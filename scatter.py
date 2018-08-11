import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import psycopg2
from gen_utils import get_trace_and_log
import datetime

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
    query = (
        f'''
        SELECT completed_product_nick, completed_product_titles, completed_product_prices, completed_product_start, completed_product_end, completed_product_lst_type, completed_product_img_url
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
        SELECT completed_product_nick, completed_product_titles, completed_product_prices, completed_product_start, completed_product_end, completed_product_lst_type, completed_product_img_url
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
        SELECT completed_product_nick, completed_product_titles, completed_product_prices, completed_product_start, completed_product_end, completed_product_lst_type, completed_product_img_url
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
        '''
    )
    data = fetch_data(query)
    data = list(data['completed_product_index_max'])
    return f'${data[0]:,.2f}'

#TODO: pretty this up -- this makes the dataframe
df1 = get_data_alpha()
df2 = get_data_beta()
df3 = get_data_unlimited()

def onload_alpha():
    """Actions to perform upon initial page load"""
    type_options = (
        [{'label': type, 'value': type}
         for type in get_data_alpha()])
    return type_options

# def onload_max():
#     '''Actions to perform upon initial page load'''
#     type_options = (
#         [{'label': type, 'value': type}
#          for type in get_data_max()])
#     print(type_options)
#     return type_options


# create tables for alpha, beta, unlimited?
def get_data(value):
    """() -> list

       Returns a list of the respective data in the database."""
    print(value)
    for valuex in value:
        print(valuex)
        if valuex == 'Beta':
            data = (
                f'''
                SELECT completed_product_img_url
                FROM completed_products_alpha
                ''')
            return data
        elif valuex == 'Alpha':
            data = (
                f'''
                SELECT completed_product_titles, completed_product_prices, completed_product_img_thumb, completed_product_img_url completed_product_start, completed_product_end
                FROM completed_products_alpha
                ''')
            data = fetch_data(data)
            return data


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

app.layout = html.Div([

    # Page Header
    html.Div([
        html.H1('P9 Price Tracker', className='first-header'),
        html.Div(className='header-image')
    ]),
    # Page Time
    html.Div([
       html.Div(f'{str(datetime.datetime.now())}', className='time')
    ]),
    # Page Header 5
    html.Div([
        html.H5('No nonsense. Just the real deal.', className='second-header'),
    ]),
    #Dropdown -- #TODO: wrap this in a div? _&_ Make it a button?
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Alpha', 'value': 'Alpha'},
            {'label': 'Beta', 'value': 'Beta'},
            {'label': 'Unlimited', 'value': 'Unlimited'}
        ],
        value=['Alpha'],  # this decides what is initially loaded?
        className='two columns'
        # labelStyle={'display': 'inline-block'},
    ),

    # Index Prices
    html.Div(
        [
        html.Div(f'Alpha Index Average: {get_data_alpha_avg()}'),
        html.Div(f'Alpha Index Min: {get_data_alpha_min()}'),
        html.Div(f'Alpha Index Max: {get_data_alpha_max()}'),
        ],
        className='alpha-div'),
    html.Div(
        [
        html.Div(f'Beta Index Average: {get_data_beta_avg()}'),
        html.Div(f'Beta Index Min: {get_data_beta_min()}'),
        html.Div(f'Beta Index Max: {get_data_beta_max()}'),
        ],
        className='beta-div'),
    html.Div(
        [
        html.Div(f'Unlimited Index Average: {get_data_unlimited_avg()}'),
        html.Div(f'Unlimited Index Min: {get_data_unlimited_min()}'),
        html.Div(f'Unlimited Index Max: {get_data_unlimited_max()}'),
        ],
        className='unlimited-div'),
    # Scatter plot
    html.Div([
        dcc.Graph(
            className='twelve columns',
            config={'displayModeBar': False},
            id='price-vs-time',
            figure={
                'data': [
                    go.Scatter(
                        x=df3[df3['completed_product_nick'] == i]['completed_product_end'],
                        y=df3[df3['completed_product_nick'] == i]['completed_product_prices'],
                        text=df3[df3['completed_product_nick'] == i]['completed_product_titles'],
                        #text=df[df['completed_product_titles'] == i]['name'],
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
                    ) for i in df3.completed_product_nick.unique()
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Price'},
                    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'  #compare
                )

        }
    ),]),
# # Scatter plot
#     html.Div([
#         dcc.Graph(
#             className='six columns',
#             config={'displayModeBar': False},
#             id='price-vs-time2',
#             figure={
#                 'data': [
#                     go.Scatter(
#                         x=df2[df2['completed_product_nick'] == i]['completed_product_end'],
#                         y=df2[df2['completed_product_nick'] == i]['completed_product_prices'],
#                         text=df2[df2['completed_product_nick'] == i]['completed_product_titles'],
#                         #text=df[df['completed_product_titles'] == i]['name'],
#                         mode='markers',
#                         opacity=0.7,
#                         marker={
#                             'size': 8,
#                             'line': {'width': 0.5, 'color': 'white'},
#                             # 'color': ['black'],
#                         },
#                         name=i,
#                         # Change the name of the legends
#                         # name=[i for i in df.name.unique()]
#                     ) for i in df2.completed_product_nick.unique()
#                 ],
#                 'layout': go.Layout(
#                     xaxis={'title': 'Date'},
#                     yaxis={'title': 'Price'},
#                     # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                     legend={'x': 0, 'y': 1},
#                     hovermode='closest'  #compare
#                 )
#
#         }
#     ),]),
    html.Div([

        # Output Results Table
        html.Div(
            html.Table(id='output-container'),
            className='twelve columns'
        ),
    ], ),
])


# @app.callback(
#     dash.dependencies.Output('output-container', 'children'),
#     [dash.dependencies.Input('dropdown', 'value')]
# )
# def update_table(value):
#     if value == 'Alpha':
#         results = get_data_alpha()
#         return generate_table(results, max_rows=15)
#     elif value == 'Beta':
#         results = get_data_beta()
#         return generate_table(results, max_rows=15)
#     else:
#         results = get_data_unlimited()
#         return generate_table(results, max_rows=15)

@app.callback(
    dash.dependencies.Output('price-vs-time', 'figure'),
    [dash.dependencies.Input('dropdown', 'value'),])
def update_graph(value):
    print(value)
    if value == 'Unlimited':
        print('called')
        df3 = get_data_unlimited()
        return {
            'data': [go.Scatter(
                x=df3[df3['completed_product_nick'] == i]['completed_product_end'],
                y=df3[df3['completed_product_nick'] == i]['completed_product_prices'],
                text=df3[df3['completed_product_nick'] == i]['completed_product_titles'],
                # text=df[df['completed_product_titles'] == i]['name'],
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
            ) for i in df3.completed_product_nick.unique()
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price'},
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'  # compare
        )

    }
    # elif value == 'Beta':
    #     results = get_data_beta()
    #     return generate_table(results, max_rows=15)
    # else:
    #     results = get_data_unlimited()
    #     return generate_table(results, max_rows=15)


#TODO: update index averages as well (same callback or new one?)

external_css = [
    # "https://codepen.io/anon/pen/pVNqEz.css",
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.css",
    # "https://fonts.googleapis.com/css?family=Economica",
]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
