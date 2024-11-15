# Dash is the application class
# dcc are Dash components, buttons, dropdowns, etc.
# html are HTML components
# Input, Output, State, and callback are all used to define what happens
#  when we interact with components like buttons and menus

from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px

from src.my_data import AnimalDB, get_random_data

# Create the application
app = Dash(__name__)

# Title (will appear in the browser tab)
app.title = 'Hello World!'

def layout() -> list:
    # Various items on the webpage
    children = []

    header = html.H1('The Best Dashboard Ever!')
    children += [header]

    # First dropdown menu
    cat_label = html.Label('Select a category')
    cat_dd = dcc.Dropdown(id='cat-dd', 
                          options=[''] + AnimalDB().get_category_list(),
                          value=''
                          )
    children += [cat_label, cat_dd]

    # Second dropdown menu, options based on the first one
    subcat_label = html.Label('Select a subcategory', id='subcat-label')
    subcat_dd = dcc.Dropdown(id='subcat-dd', 
                             options=[],
                             value=''
                             )
    children += [subcat_label, subcat_dd]

    # Third dropdown menu
    item_label = html.Label('Select an animal', id='item-label')
    item_dd = dcc.Dropdown(id='item-dd',
                           options=[],
                           value=''
                           )
    children += [item_label, item_dd]

    figure_title = html.H2(id='figure-title')
    children += [figure_title]

    df = get_random_data()
    fig = px.scatter(df, x='x', y='y')
    children += [dcc.Graph(figure=fig, id='my-figure')]

    update_figure_button = html.Button('Update Figure',
                                       id='update-figure-button',
                                       n_clicks=0
                                       )
    children += [update_figure_button]

    return children

# Add the layout to the application
app.layout = html.Div(id='main-div', children=layout())

#===================Callbacks=======================
# Update the subcat list based on the cat selection
@callback(Output('subcat-dd', 'options'),
          Output('subcat-dd', 'style'),
          Output('subcat-label', 'style'),
          Input('cat-dd', 'value')
          )
def update_subcats(category: str):
    vals = AnimalDB().get_subcategory_list(category)

    if len(vals):
        style = {'display': 'block'}
    else:
        style = {'display': 'none'}
    return ['']+vals, style, style

@callback(Output('item-dd', 'options'),
          Output('item-dd', 'style'),
          Output('item-label', 'style'),
          Input('cat-dd', 'value'),
          Input('subcat-dd', 'value')
          )
def update_items(cat, subcat):
    vals = AnimalDB().get_item_list(cat, subcat)
    if len(vals):
        style = {'display': 'block'}
    else:
        style = {'display': 'none'}
    return ['']+vals, style, style

@callback(Output('my-figure', 'figure'),
          Input('update-figure-button', 'n_clicks'),
          prevent_initial_call=True
          )
def update_figure(_):
    df = get_random_data()
    fig = px.scatter(df, x='x', y='y')
    print(f'The button has been clicked {_} times')
    return fig

@callback(Output('figure-title', 'children'),
          Input('cat-dd', 'value'),
          Input('subcat-dd', 'value'),
          Input('item-dd', 'value')
          )
def update_figure_title(cat='', subcat='', item=''):
    title = ''
    if len(cat):
        title += f'Data for {cat}'
    if len(subcat):
        title += f':{subcat}'
    if len(item):
        title += f':{item}'
    return title

if __name__ == '__main__':
    # debug=True will show some errors on the webpage
    app.run(debug=True)