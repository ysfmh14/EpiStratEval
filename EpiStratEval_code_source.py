import dash
from dash import Dash, dcc, html, Input, Output, callback,clientside_callback
from dash.dependencies import Input, Output, State
import folium
from folium import Element
from folium import plugins
from folium.plugins import MousePosition, MiniMap, Fullscreen
import dash_bootstrap_components as dbc
import pandas as pd
import inflect
import io 
from flask import Flask, request
import dash_bootstrap_components as dbc

df1 = pd.read_excel('C:/Users/ysfmh/Downloads/location_extracted_information_S2.xlsx')
df2 = pd.read_excel('C:/Users\ysfmh/Downloads/location_extracted_information_S5.xlsx')
df1 = df1.dropna(subset=['latitude', 'longitude'])
df2 = df2.dropna(subset=['latitude', 'longitude'])
df1 = df1.dropna(subset=['diseases'])
df2 = df2.dropna(subset=['diseases'])
df1 = df1.drop_duplicates(subset=['article','latitude', 'longitude'])
df2 = df2.drop_duplicates(subset=['article','latitude', 'longitude'])
df1['publication_date'] = pd.to_datetime(df1['publication_date'], format='%y-%m-%d')
df2['publication_date'] = pd.to_datetime(df2['publication_date'], format='%y-%m-%d')
df1['validation'] = None
df2['validation'] = None
df1['location_type'] = None


# Attribuer 'Continent' lorsque geonames_class est 'L' et geonames_code est 'CONT'
df1.loc[(df1['geonames_class'] == 'L') & (df1['geonames_code'] == 'CONT'), 'location_type'] = 'Continent'

# Attribuer 'Country' lorsque geonames_class est 'A' et geonames_code est 'PCLI'
df1.loc[(df1['geonames_class'] == 'A') & (df1['geonames_code'] == 'PCLI'), 'location_type'] = 'Country'

# Attribuer 'Region' lorsque geonames_class est 'A' et geonames_code est 'ADM1'
# ou lorsque geonames_class est 'P' et geonames_code est 'PPLA'
# ou lorsque geonames_class est 'L' et geonames_code est 'RGN' ou 'RGNL'
df1.loc[((df1['geonames_class'] == 'A') & (df1['geonames_code'] == 'ADM1')) |
        ((df1['geonames_class'] == 'P') & (df1['geonames_code'] == 'PPLA')) |
        ((df1['geonames_class'] == 'L') & (df1['geonames_code'].isin(['RGN', 'RGNL']))),
        'location_type'] = 'Region'

# Attribuer 'City' lorsque geonames_class est 'P' et geonames_code n'est pas 'PPLF'
df1.loc[(df1['geonames_class'] == 'P') & (df1['geonames_code'] != 'PPLF'), 'location_type'] = 'City'

# Attribuer 'Village' lorsque geonames_class est 'P' et geonames_code est 'PPLF'
df1.loc[(df1['geonames_class'] == 'P') & (df1['geonames_code'] == 'PPLF'), 'location_type'] = 'Village'


df2['location_type'] = None

# Appliquer les conditions et définir les valeurs pour la colonne 'location_type'
df2.loc[(df2['geonames_class'] == 'L') & (df2['geonames_code'] == 'CONT'), 'location_type'] = 'continent'
df2.loc[(df2['geonames_class'] == 'A') & (df2['geonames_code'] == 'PCLI'), 'location_type'] = 'region'
df2.loc[(df2['geonames_class'] == 'A') & (df2['geonames_code'] != 'PCLI'), 'location_type'] = 'country'
df2.loc[(df2['geonames_class'] == 'P'), 'location_type'] = 'city'
    
# Ajouter une colonne vide "impression" à df1
df1['strategie'] = "1"
# Ajouter une colonne vide "impression" à df2
df2['strategie'] = "2"
external_scripts = ["https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js"
]
external_stylesheets = ["https://use.fontawesome.com/releases/v6.4.2/css/all.css",dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, suppress_callback_exceptions=True,external_scripts=external_scripts,external_stylesheets=external_stylesheets)


app.head = [
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    )
]

country_dropdown = dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in df1['country'].unique() if pd.notnull(country)],
    multi=True,
    placeholder='Country',
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            id="loading",
                            type="default",
                            children=[
                                html.Iframe(
                                    id='map-container',
                                    width='100%',
                                    height='750px',
                                ),
                                

                                       
                            ],
                        ),
                        
                       html.Div(
    [
        country_dropdown,
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df1['publication_date'].min(),
            end_date=df1['publication_date'].max(),
            display_format='YYYY-MM-DD',
            style={'margin-top': '10px',
                  'margin-bottom': '0.5vw'}
        ),
        html.Button(html.I(className="fa-solid fa-magnifying-glass", style={"font-size": "2vw"}), id='search-btn', n_clicks=0, className='btn btn-primary',
                    style={'margin-left': '0.3vw','margin-right': '0.3vw'}),
        html.Button(html.I(className="fa-solid fa-rotate-right", style={"font-size": "2vw"}), className="btn btn-primary", id='reload',style={'margin-left': '0.3vw', 'margin-right': '1vw'}),
        html.Button(html.I(className="fa-solid fa-paw", style={"font-size": "2vw"}), id="info-window-toggle-btn", className="btn btn-secondary",style={'margin-left': '0.3vw','margin-right': '0.3vw'}),
        dcc.Download(id="download-df1"),
        html.Button(html.I(className="fa-solid fa-download", style={"font-size": "2vw"}), className="btn btn-secondary", id='button-df1',style={'margin-right': '0.3vw', 'backgroundColor': 'darkred'}),
        dcc.Download(id="download-df2"),
        html.Button(html.I(className="fa-solid fa-download", style={"font-size": "2vw"}), className="btn btn-secondary", id='button-df2',style={'margin-right': '0.3vw', 'backgroundColor': 'darkgreen'}),
        html.Div(id='hidden-div', style={'display': 'none'}),
        dcc.Input(id='input-valide', type='hidden', value=''),                
    ],
    style={
        'position': 'fixed',
        'z-index': '1',
        'top': '10px',
        'left': '27vw',
        'right': '27vw',
        'background-color': 'white',
        'padding': '1vw', 
        'box-shadow': '0px 0px 10px 2px rgba(0, 0, 0, 0.1)',
    },
),

                        

                         html.Div([
    html.Div(id='output-div'),
]),

                         html.Div(
                                    [
                                               

                                            
                                         dbc.Collapse(
                                            [
                                                html.Div(
                                                    id='info-window-content',
                                                    style={
                                                        'background-color': 'white',
                                                        'padding': '10px',
                                                        'box-shadow': '0px 0px 10px 2px rgba(0, 0, 0, 0.1)',
                                                        'position': 'absolute',
                                                        'z-index': '1',
                                                        'top': '650px',
                                                        'left': '20px',
                                                        'width': '300px',
                                                        'border-radius': '4px',
                                                        'max-height': '120px',
                                                        'overflow-y': 'auto',
                                                    },
                                                ),
                                            ],
                                            id="collapse-info-window",
                                            is_open=False,
                                        ),
                                      
                                    ],
                                ),
                         html.Div(id="valide-output1"),

                    ],
                    width=12,
                ),
            ],
        ),
       
    ],
    fluid=True,
)








@app.callback(
    Output("download-df1", "data"),
    Input("button-df1", "n_clicks"),
    prevent_initial_call=True,
)
def download_df1(n_clicks_df1):
     if n_clicks_df1:
        df1_without_column = df1.drop(['strategie'], axis=1)
        return dcc.send_data_frame(df1_without_column.to_excel, "df1.xlsx", sheet_name="Sheet_name_1")
     return no_update
    
@app.callback(
    Output("download-df2", "data"),
    Input("button-df2", "n_clicks"),
    prevent_initial_call=True,
)
def download_df1(n_clicks_df2):
    if n_clicks_df2:
        df2_without_column = df2.drop(['strategie'], axis=1)
        return dcc.send_data_frame(df2_without_column.to_excel, "df2.xlsx", sheet_name="Sheet_name_2")
    return no_update


@app.callback(
    Output("collapse-info-window", "is_open"),
    [Input("info-window-toggle-btn", "n_clicks")],
    [State("collapse-info-window", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(
    Output("collapse-info-window2", "is_open"),
    [Input("info-window-toggle-btn2", "n_clicks")],
    [State("collapse-info-window2", "is_open")],
)
def toggle_collapse(n, is_open2):
    if n:
        return not is_open2
    return is_open2



@app.callback(
    [Output('map-container', 'srcDoc'),
     Output('info-window-content', 'children')],
    [Input('search-btn', 'n_clicks'),
     Input('reload', 'n_clicks')

    ],
    [
        State('country-dropdown', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),

    ]
)
def update_map(search_clicks,reload, selected_countries, start_date, end_date):

    m = folium.Map(location=[50, 15], zoom_start=6)
    MousePosition().add_to(m)

    folium.TileLayer(tiles='cartodb positron', attr='Custom Attribution').add_to(m)

    cluster_css = """
        .marker-cluster {
            background-color: rgba(255, 165, 0, 0.7) !important;
            color: white !important;
            width: 22px !important;
            height: 22px !important;
            line-height: 26px !important;
            border-radius: 50% !important;
            text-align: center !important;
            position: relative;
        }

        .marker-cluster div {
            background-color: transparent !important;
            position: absolute;
            top: 30%;
            left: 30%;
            transform: translate(-50%, -50%);
        }
    """
    m.get_root().header.add_child(folium.Element("<style>{}</style>".format(cluster_css)))

    marker_cluster = plugins.MarkerCluster(max_cluster_radius=50).add_to(m)

    unique_species_set = set()
    p = inflect.engine()

    for df, color in zip([df1, df2], ['darkred', 'darkgreen']):
        df['publication_date'] = pd.to_datetime(df['publication_date'])
        
        if selected_countries:
            df = df[df['country'].isin(selected_countries)]

        filtered_df = df[(df['publication_date'] >= start_date) & (df['publication_date'] <= end_date)]

        for index, row in filtered_df.iterrows():
            valide1= "1"
            valide2 ="0"
            toltip_html = f"<div style='margin-left: 115px; margin-bottom: -17px;'><i class='fa-solid fa-earth-americas'></i> {row['location_type']}</div><br>Location: {row['location']}<br>Country: {row['country']}<br>Continent: {row['continent']}<br>Publication date: {row['publication_date']}<br>Diseases:{row['diseases']}<br>hosts:{row['species']} "
            popup_html = f"Article: <a href={row['url']} target='_blank'><i class='fa-solid fa-file-export'></i></a><br><br><button class='btn btn-success' onclick='buttonClickHandler1(\"{row['location']}\",\"{row['url']}\",\"{valide1}\",\"{row['strategie']}\",\"{index}\")'><i class='fa-regular fa-circle-check'></i></button>"
            popup_html += f"<button  style='margin-left: 5px;' class='btn btn-danger' onclick='buttonClickHandler1(\"{row['location']}\",\"{row['url']}\",\"{valide2}\",\"{row['strategie']}\")'><i class='fa-regular fa-circle-xmark'></i></button>"
            popup_text = f" Source d'article: <a href={row['url']} target='_blank'><i class='fa-solid fa-file-export'></i></a><br> "
            if row['validation'] == 'valid':
                toltip_html += f"<br>Impression: <span style='color: green;'>{row['validation']}</span>"
            elif row['validation'] == 'invalid':
                toltip_html += f"<br>Impression: <span style='color: red;'>{row['validation']}</span>"
            if pd.notnull(row['species']):
                species_list = [p.singular_noun(spec.strip().lower()) or spec.strip().lower() for spec in str(row['species']).split(',')]
                unique_species_set.update(species_list)
 
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=10,
                color=color,
                stroke=False,
                fill_opacity=1,
                fill=True,
                fill_color=color,
                tooltip = toltip_html ,
                popup=folium.Popup(
                    html=popup_html,
                    max_width=300
                ),
            ).add_to(marker_cluster)
    js_click_handler = """
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">
<script src="https://cdn.jsdelivr.net/npm/toastify-js"></script>
<script>

function buttonClickHandler1(location, url, valide, strategie, index) {
  let queryString = '';
  queryString += 'param1=' + location ;
  queryString += '&param2=' + url;
  queryString += '&param3=' + valide;
  queryString += '&param4=' + strategie;
  fetch(`/test?${queryString}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    // Vérifier si la réponse est OK (200)
    if (!response.ok) {
      throw new Error('Erreur lors de la requête');
    }
    
    return response.text();
  })
  .then(data => {
    console.log(data); 
    if (valide === "1") {
      Toastify({
        text: "location is saved as validated",
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top",
        position: "left",
        stopOnFocus: true, 
        style: {
          background: "linear-gradient(to right, #00b09b, #96c93d)",
          with : "100px"
        }
      }).showToast();
    } else if (valide === "0") {
      Toastify({
        text: "location is saved as unvalidated",
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top",
        position: "left",
        stopOnFocus: true, 
        style: {
          background: "linear-gradient(to right, #ff0000, #990000)",
          with : "100px"
        }
      }).showToast();
    }
    
    
  })
  .catch(error => {
    // Gérer les erreurs
    console.error('Erreur:', error);
  });
}


function buttonClickHandler2(location,url) {
  console.log('Bouton 2 cliqué');
}
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'map_position') {
        const mapState = event.data.payload;
        console.log('Map position:', mapState);
        // Envoyez mapState au serveur
        fetch('/update_map_position', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(mapState)
        });
    }
});
</script>

"""
    m.get_root().html.add_child(folium.Element(js_click_handler))
    species_string = ", ".join(unique_species_set)

    info_window_content = html.Div([
        html.Div([
            html.I(className="fa-solid fa-circle-info", style={"font-size": "24px", "margin-right": "5px"}),
            html.H5("List of hosts")], style={"display": "flex"}),
        species_string
    ])

    folium_map_html = m.get_root().render()
    return folium_map_html, info_window_content

@app.server.route('/test', methods=['GET'])
def test():
    location = request.args.get('param1')
    url = request.args.get('param2')
    valide = request.args.get('param3')
    strategie = request.args.get('param4')
    if valide == "1" and strategie == "1":
        df1.loc[(df1['article_url'] == url) & (df1['location'] == location), 'validation'] = "valid"
        return 'Données reçues avec succès !'
    elif  valide == "1" and strategie == "2":
        df2.loc[(df2['article_url'] == url) & (df2['location'] == location), 'validation'] = "valid"
        return 'Données reçues avec succès !'
    elif valide == "0" and strategie == "1":
        df1.loc[(df1['article_url'] == url) & (df1['location'] == location), 'validation'] = "invalid"
        return 'Données reçues avec succès !'
    elif  valide == "0" and strategie == "2":
        df2.loc[(df2['article_url'] == url) & (df2['location'] == location), 'validation'] = "invalid"

        return 'Données reçues avec succès !'

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)

