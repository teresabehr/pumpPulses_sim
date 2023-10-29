import dash
try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# # if creating a multi-page app: use base_app to start the app server and create each page in a different file
# from base_app import app
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
                external_stylesheets=[dbc.themes.FLATLY])
server = app.server

from pages import widgets,about,lightFuncs 

import os
## comment this bit out before deploying to AWS!!
# os.chdir("..\\fcm_dashApp")
# os.chdir("\\Users\\Teresa Behr\\Desktop\\scripts_and_such_2022-07-02\\fortune-cookie-movies")
cwd = os.getcwd()
# print(cwd)

navbar_style = {
    'font-family': 'Radio Canada',
    'padding': '0.6rem',
    # 'color': 'white', #'#595959',
    'font-weight': '600',
    'font-size': '1.5rem',
    'padding-top': '1rem',
    'padding-left': '1.5rem',
    'padding-right':'1.5rem',
    }


fav_cookie = html.Img(src=app.get_asset_url('Fortune_cookie.png'),
                      style={'height': '2%', 'width': '2%', 'margin-right': '1rem'},
                      )

app.title = "Phred the Photon"

app.layout = html.Div([
    html.Div([
        html.Div([

            dbc.Nav(id='page_nav', children=
                [
                    dbc.NavLink("About this App", href="/about", style=navbar_style,
                                external_link=True),
                    dbc.NavLink("Widgets", href="/widgets", style=navbar_style,
                                external_link=True),
                ],
                fill=True,
            ),
        ],
            className='twelve columns',
            style={'padding-bottom': '5rem',
                   'padding-top': '1rem',
                   'text-align': 'center',
                   'position': 'fixed',
                   }

        ),

    ]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', 
            #  className='ten columns offset-by-one',
            style={
                'padding': '10rem'
            }
    )
])


############################### index page callbacks ############################################

@app.callback(
    [Output('page-content', 'children'),
    # Output('pageTitle', 'children') 
    ],
    Input('url', 'href'),
)
def display_page(href):

    # print('href is: ', href)
    pathname = href.split('/')[-1]
    # print('pathname is: ', href)

    if (pathname == 'about'):
        title = "Frankly, my dear, you don't give a damn... "
        return [about.layout] #, (fav_cookie, title, fav_cookie)
    else:
        return [widgets.layout]


if __name__ == '__main__':
    app.run_server(port=8050, debug=True) # use for dev
    # app.run_server(host='0.0.0.0', port=8050, debug=False) # use when deploying
