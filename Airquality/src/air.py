
import requests
import plotly
import plotly.express as px
import json
import fips
from urllib.request import urlopen
import dash
from dash import dcc, Dash
from dash import html 
from dash.dependencies import Input, Output


class get_data():
    '''
        Makes a plotly cloropleth mapbox, which uses data from an air quality api and from a county geojson,
        and it maps the aqi value to the correct city, based on what the user inputs. The final product is a 
        interactive dash app and map, where the air quality of any U.S. city can be viewed. 

    '''
    def __init__(self):
        
        self.fig = None
        self.data = {}
         #Opens a geojson filled with county borders, where each county can be identified by the fips code. 
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as self.response:
            self.counties = json.load(self.response)
    def build_map(self):

        #creates dictionary of all the relevent data coming from the api request
        self.data = {
                'Aqi': df["data"][0]['aqi'],
                "Fips": [first_fips],

                "o3": df["data"][0]["o3"],

                "so2":df["data"][0]['so2'],

                "no2":df["data"][0]['no2'],
                "co":df["data"][0]['co'],
                "pm10":df["data"][0]['pm10'],
                "pm25":df["data"][0]['pm25'],
                "pollen_level_tree": df["data"][0]['pollen_level_tree'],
                "pollen_level_grass": df["data"][0]['pollen_level_grass'],
                "pollen_level_weed": df["data"][0]['pollen_level_weed'],
                "mold_level": df["data"][0]['mold_level'],
                "predominant_pollen_type": df["data"][0]['predominant_pollen_type']
                }  
   

       
        

        #Creates a plotly cloropleth mapbox, where the newly created dictionary and geojson are used in order to map the correct county with the correct aqi value on an interactive map. 
        self.fig = px.choropleth_mapbox(self.data, geojson=self.counties, color='Aqi',
                           locations="Fips",hover_data=["o3","so2","no2", "co","pm25"],
                           center={"lat": fips.location.latitude, "lon": fips.location.longitude},
                           mapbox_style="carto-positron", zoom=6,color_continuous_scale='Bluered',range_color=[0,500])
        self.fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

  

if __name__=='__main__':
    
    # first call to the fips file, which takes in a comma seperated city and converts it to a county fips code

    first_fips = fips.change_place_to_cordinates('Los Angeles, CA')
    request = requests.get("https://api.weatherbit.io/v2.0/current/airquality?{coordinates}&key=614a9b8a89cd4fbaacd2d3003784d994".format(coordinates=fips.lat_long_txt))
    df = request.json()     
    run = get_data()
    run.build_map()
    


'''
This is the UI for the program, a plotly dash app. It places the interactive map on a dash app where the user can saily type in a random U.S.
city and get the resulting aqi value. 
'''
app = Dash(__name__)




app.layout = html.Div([
    
    html.H1('Real Time U.S. city AQI checker', style={'textAlign': 'center' }),
    html.H2("Created by: Ati Massengill", style={'textAlign': 'center'}),
    html.P("Type in a U.S. city for the AQI value (City, State Abbreviation):"),
    dcc.Input(
        id='city', 
        value="Los Angeles, CA",
        type='text',
        debounce=True
    ),html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    dcc.Graph(id="graph",figure=run.fig),
])

#handles the callbacks when the sumbit button is pressed, as well as the css loading symbol when each callback is made. 
@app.callback(
    Output("graph", "figure"),
    Input('submit-button-state', 'n_clicks'),
    Input("city", "value"))



#when each callback is made i.e. the sumbit button is pressed display_choropleth, making a new call to fips.change_place_to_cordinates with the new city, 
#It then makes another api requests with the new location and creates a new dictionry with the relevent data
#Lastly it updates the map with the new location and new dictionary
def display_choropleth(n_clicks,city):
    
    new_fips = fips.change_place_to_cordinates(city)
    

    run2 = get_data()
    request = requests.get("https://api.weatherbit.io/v2.0/current/airquality?{cordinates}&key=614a9b8a89cd4fbaacd2d3003784d994".format(cordinates=fips.lat_long_txt))
    df = request.json()
    run2.build_map()
    
    new_fips2 = {
            'Aqi': df["data"][0]['aqi'],
            "Fips": [new_fips],
            "3": df["data"][0]["o3"],
            "so2":df["data"][0]['so2'],
            "no2":df["data"][0]['no2'],
            "co":df["data"][0]['co'],
            "pm10":df["data"][0]['pm10'],
            "pm25":df["data"][0]['pm25'],
            "pollen_level_tree": df["data"][0]['pollen_level_tree'],
            "pollen_level_grass": df["data"][0]['pollen_level_grass'],
            "pollen_level_weed": df["data"][0]['pollen_level_weed'],
            "mold_level": df["data"][0]['mold_level'],
            "predominant_pollen_type": df["data"][0]['predominant_pollen_type']
            }
    run2.data.update(new_fips2)
    run2.fig = px.choropleth_mapbox(run2.data, geojson=run2.counties, color='Aqi',
                           locations="Fips", hover_data=["o3","so2","no2", "co","pm25"],
                           center={"lat": fips.location.latitude, "lon": fips.location.longitude},
                           mapbox_style="carto-positron", zoom=6,color_continuous_scale='Bluered',range_color=[0,500])
    
    
    run2.fig.update_geos(fitbounds="geojson", visible=False)
    run2.fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return run2.fig


app.run_server(debug=True)