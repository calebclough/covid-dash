import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import boto3
import s3fs

longdata = pd.read_csv('s3://coviddash/owid-longitudinal-data.csv')
scatterdata = pd.read_csv('s3://coviddash/owid-scatter-data.csv')

external_stylesheets = [
    'https://coviddash.s3-us-west-1.amazonaws.com/format/custom.css',
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#440154',
    'text': '#DCDCDC'
}

countrieslist = [
    {'label':'Afghanistan', 'value': 'AFG'},
    {'label':'Albania', 'value': 'ALB'},
    {'label':'Algeria', 'value': 'DZA'},
    {'label':'Andorra', 'value': 'AND'},
    {'label':'Angola', 'value': 'AGO'},
    {'label':'Antigua and Barbuda', 'value': 'ATG'},
    {'label':'Argentina', 'value': 'ARG'},
    {'label':'Armenia', 'value': 'ARM'},
    {'label':'Australia', 'value': 'AUS'},
    {'label':'Austria', 'value': 'AUT'},
    {'label':'Azerbaijan', 'value': 'AZE'},
    {'label':'Bahamas', 'value': 'BHS'},
    {'label':'Bahrain', 'value': 'BHR'},
    {'label':'Bangladesh', 'value': 'BGD'},
    {'label':'Barbados', 'value': 'BRB'},
    {'label':'Belarus', 'value': 'BLR'},
    {'label':'Belgium', 'value': 'BEL'},
    {'label':'Belize', 'value': 'BLZ'},
    {'label':'Benin', 'value': 'BEN'},
    {'label':'Bermuda', 'value': 'BMU'},
    {'label':'Bhutan', 'value': 'BTN'},
    {'label':'Bolivia', 'value': 'BOL'},
    {'label':'Bosnia and Herzegovina', 'value': 'BIH'},
    {'label':'Botswana', 'value': 'BWA'},
    {'label':'Brazil', 'value': 'BRA'},
    {'label':'Brunei', 'value': 'BRN'},
    {'label':'Bulgaria', 'value': 'BGR'},
    {'label':'Burkina Faso', 'value': 'BFA'},
    {'label':'Burundi', 'value': 'BDI'},
    {'label':'Cambodia', 'value': 'KHM'},
    {'label':'Cameroon', 'value': 'CMR'},
    {'label':'Canada', 'value': 'CAN'},
    {'label':'Cape Verde', 'value': 'CPV'},
    {'label':'Central African Republic', 'value': 'CAF'},
    {'label':'Chad', 'value': 'TCD'},
    {'label':'Chile', 'value': 'CHL'},
    {'label':'China', 'value': 'CHN'},
    {'label':'Colombia', 'value': 'COL'},
    {'label':'Comoros', 'value': 'COM'},
    {'label':'Congo', 'value': 'COG'},
    {'label':'Costa Rica', 'value': 'CRI'},
    {'label':'Cote dIvoire', 'value': 'CIV'},
    {'label':'Croatia', 'value': 'HRV'},
    {'label':'Cuba', 'value': 'CUB'},
    {'label':'Cyprus', 'value': 'CYP'},
    {'label':'Czech Republic', 'value': 'CZE'},
    {'label':'Democratic Republic of Congo', 'value': 'COD'},
    {'label':'Denmark', 'value': 'DNK'},
    {'label':'Djibouti', 'value': 'DJI'},
    {'label':'Dominica', 'value': 'DMA'},
    {'label':'Dominican Republic', 'value': 'DOM'},
    {'label':'Ecuador', 'value': 'ECU'},
    {'label':'Egypt', 'value': 'EGY'},
    {'label':'El Salvador', 'value': 'SLV'},
    {'label':'Equatorial Guinea', 'value': 'GNQ'},
    {'label':'Eritrea', 'value': 'ERI'},
    {'label':'Estonia', 'value': 'EST'},
    {'label':'Ethiopia', 'value': 'ETH'},
    {'label':'Fiji', 'value': 'FJI'},
    {'label':'Finland', 'value': 'FIN'},
    {'label':'France', 'value': 'FRA'},
    {'label':'Gabon', 'value': 'GAB'},
    {'label':'Gambia', 'value': 'GMB'},
    {'label':'Georgia', 'value': 'GEO'},
    {'label':'Germany', 'value': 'DEU'},
    {'label':'Ghana', 'value': 'GHA'},
    {'label':'Greece', 'value': 'GRC'},
    {'label':'Grenada', 'value': 'GRD'},
    {'label':'Guatemala', 'value': 'GTM'},
    {'label':'Guinea', 'value': 'GIN'},
    {'label':'Guinea-Bissau', 'value': 'GNB'},
    {'label':'Guyana', 'value': 'GUY'},
    {'label':'Haiti', 'value': 'HTI'},
    {'label':'Honduras', 'value': 'HND'},
    {'label':'Hong Kong', 'value': 'HKG'},
    {'label':'Hungary', 'value': 'HUN'},
    {'label':'Iceland', 'value': 'ISL'},
    {'label':'India', 'value': 'IND'},
    {'label':'Indonesia', 'value': 'IDN'},
    {'label':'Iran', 'value': 'IRN'},
    {'label':'Iraq', 'value': 'IRQ'},
    {'label':'Ireland', 'value': 'IRL'},
    {'label':'Israel', 'value': 'ISR'},
    {'label':'Italy', 'value': 'ITA'},
    {'label':'Jamaica', 'value': 'JAM'},
    {'label':'Japan', 'value': 'JPN'},
    {'label':'Jordan', 'value': 'JOR'},
    {'label':'Kazakhstan', 'value': 'KAZ'},
    {'label':'Kenya', 'value': 'KEN'},
    {'label':'Kuwait', 'value': 'KWT'},
    {'label':'Kyrgyzstan', 'value': 'KGZ'},
    {'label':'Laos', 'value': 'LAO'},
    {'label':'Latvia', 'value': 'LVA'},
    {'label':'Lebanon', 'value': 'LBN'},
    {'label':'Lesotho', 'value': 'LSO'},
    {'label':'Liberia', 'value': 'LBR'},
    {'label':'Libya', 'value': 'LBY'},
    {'label':'Lithuania', 'value': 'LTU'},
    {'label':'Luxembourg', 'value': 'LUX'},
    {'label':'Macedonia', 'value': 'MKD'},
    {'label':'Madagascar', 'value': 'MDG'},
    {'label':'Malawi', 'value': 'MWI'},
    {'label':'Malaysia', 'value': 'MYS'},
    {'label':'Maldives', 'value': 'MDV'},
    {'label':'Mali', 'value': 'MLI'},
    {'label':'Malta', 'value': 'MLT'},
    {'label':'Marshall Islands', 'value': 'MHL'},
    {'label':'Mauritania', 'value': 'MRT'},
    {'label':'Mauritius', 'value': 'MUS'},
    {'label':'Mexico', 'value': 'MEX'},
    {'label':'Moldova', 'value': 'MDA'},
    {'label':'Mongolia', 'value': 'MNG'},
    {'label':'Montenegro', 'value': 'MNE'},
    {'label':'Morocco', 'value': 'MAR'},
    {'label':'Mozambique', 'value': 'MOZ'},
    {'label':'Myanmar', 'value': 'MMR'},
    {'label':'Namibia', 'value': 'NAM'},
    {'label':'Nepal', 'value': 'NPL'},
    {'label':'Netherlands', 'value': 'NLD'},
    {'label':'New Zealand', 'value': 'NZL'},
    {'label':'Nicaragua', 'value': 'NIC'},
    {'label':'Niger', 'value': 'NER'},
    {'label':'Nigeria', 'value': 'NGA'},
    {'label':'Norway', 'value': 'NOR'},
    {'label':'Oman', 'value': 'OMN'},
    {'label':'Pakistan', 'value': 'PAK'},
    {'label':'Palestine', 'value': 'PSE'},
    {'label':'Panama', 'value': 'PAN'},
    {'label':'Papua New Guinea', 'value': 'PNG'},
    {'label':'Paraguay', 'value': 'PRY'},
    {'label':'Peru', 'value': 'PER'},
    {'label':'Philippines', 'value': 'PHL'},
    {'label':'Poland', 'value': 'POL'},
    {'label':'Portugal', 'value': 'PRT'},
    {'label':'Puerto Rico', 'value': 'PRI'},
    {'label':'Qatar', 'value': 'QAT'},
    {'label':'Romania', 'value': 'ROU'},
    {'label':'Russia', 'value': 'RUS'},
    {'label':'Rwanda', 'value': 'RWA'},
    {'label':'Saint Kitts and Nevis', 'value': 'KNA'},
    {'label':'Saint Lucia', 'value': 'LCA'},
    {'label':'Saint Vincent and the Grenadines', 'value': 'VCT'},
    {'label':'San Marino', 'value': 'SMR'},
    {'label':'Sao Tome and Principe', 'value': 'STP'},
    {'label':'Saudi Arabia', 'value': 'SAU'},
    {'label':'Senegal', 'value': 'SEN'},
    {'label':'Serbia', 'value': 'SRB'},
    {'label':'Seychelles', 'value': 'SYC'},
    {'label':'Sierra Leone', 'value': 'SLE'},
    {'label':'Singapore', 'value': 'SGP'},
    {'label':'Slovakia', 'value': 'SVK'},
    {'label':'Slovenia', 'value': 'SVN'},
    {'label':'Solomon Islands', 'value': 'SLB'},
    {'label':'Somalia', 'value': 'SOM'},
    {'label':'South Africa', 'value': 'ZAF'},
    {'label':'South Korea', 'value': 'KOR'},
    {'label':'Spain', 'value': 'ESP'},
    {'label':'Sri Lanka', 'value': 'LKA'},
    {'label':'Sudan', 'value': 'SDN'},
    {'label':'Suriname', 'value': 'SUR'},
    {'label':'Swaziland', 'value': 'SWZ'},
    {'label':'Sweden', 'value': 'SWE'},
    {'label':'Switzerland', 'value': 'CHE'},
    {'label':'Taiwan', 'value': 'TWN'},
    {'label':'Tajikistan', 'value': 'TJK'},
    {'label':'Tanzania', 'value': 'TZA'},
    {'label':'Thailand', 'value': 'THA'},
    {'label':'Timor', 'value': 'TLS'},
    {'label':'Togo', 'value': 'TGO'},
    {'label':'Trinidad and Tobago', 'value': 'TTO'},
    {'label':'Tunisia', 'value': 'TUN'},
    {'label':'Turkey', 'value': 'TUR'},
    {'label':'Uganda', 'value': 'UGA'},
    {'label':'Ukraine', 'value': 'UKR'},
    {'label':'United Arab Emirates', 'value': 'ARE'},
    {'label':'United Kingdom', 'value': 'GBR'},
    {'label':'United States', 'value': 'USA'},
    {'label':'United States Virgin Islands', 'value': 'VIR'},
    {'label':'Uruguay', 'value': 'URY'},
    {'label':'Uzbekistan', 'value': 'UZB'},
    {'label':'Venezuela', 'value': 'VEN'},
    {'label':'Vietnam', 'value': 'VNM'},
    {'label':'Yemen', 'value': 'YEM'},
    {'label':'Zambia', 'value': 'ZMB'},
    {'label':'Zimbabwe', 'value': 'ZWE'},
]

quantitativemetricslist = [
    {'label':'Total Cases', 'value': 'total_cases'},
    {'label':'Total Deaths', 'value': 'total_deaths'},
    {'label':'Total Cases Per Million', 'value': 'total_cases_per_million'},
    {'label':'Total Deaths Per Million', 'value': 'total_deaths_per_million'},
    {'label':'Total Tests', 'value': 'total_tests'},
    {'label':'Total Tests Per Thousand', 'value': 'total_tests_per_thousand'},
    {'label':'Population', 'value': 'population'},
    {'label':'Population Density', 'value': 'population_density'},
    {'label':'Median Age', 'value': 'median_age'},
    {'label':'% Aged 65 and Older', 'value': 'aged_65_older'},
    {'label':'% Aged 70 and Older', 'value': 'aged_70_older'},
    {'label':'GDP Per Capita', 'value': 'gdp_per_capita'},
    {'label':'Cardiovascular Death Rate', 'value': 'cardiovasc_death_rate'},
    {'label':'Diabetes Prevalence', 'value': 'diabetes_prevalence'},
    {'label':'Hospital Beds Per Thousand', 'value': 'hospital_beds_per_thousand'},
    {'label':'Life Expectancy', 'value': 'life_expectancy'},
    {'label':'Human Development Index', 'value': 'human_development_index'},
    {'label':'Trust in Scientists Index', 'value': 'Wellcome Global Monitor Trust in Scientists Index (recoded into 3 categories) High Trust'},
    {'label':'Trust in Doctors? (% Responding A lot)', 'value': 'Q11E How much do you trust each of the following? How about doctors and nurses in this country? Do you trust them a lot, some, not much, or not at all? A lot'},
    {'label':'Trust in National Government? (% Responding A lot)', 'value': 'Q11B How much do you trust each of the following? How about the national government in this country? Do you trust them a lot, some, not much, or not at all? A lot'}
]

longitudinalemetricslist = [
    {'label':'Total Cases', 'value': 'total_cases'},
    {'label':'New Cases', 'value': 'new_cases'},
    {'label':'New Cases Smoothed', 'value': 'new_cases_smoothed'},
    {'label':'Total Deaths', 'value': 'total_deaths'},
    {'label':'New Deaths', 'value': 'new_deaths'},
    {'label':'New Deaths Smoothed', 'value': 'new_deaths_smoothed'},
    {'label':'Total Cases Per Million', 'value': 'total_cases_per_million'},
    {'label':'New Cases Per Million', 'value': 'new_cases_per_million'},
    {'label':'New Cases Smoothed Per Million', 'value': 'new_cases_smoothed_per_million'},
    {'label':'Total Deaths Per Million', 'value': 'total_deaths_per_million'},
    {'label':'New Deaths Per Million', 'value': 'new_deaths_per_million'},
    {'label':'New Deaths Smoothed Per Million', 'value': 'new_deaths_smoothed_per_million'},
    {'label':'Reproduction Rate', 'value': 'reproduction_rate'},
    {'label':'Total Tests', 'value': 'total_tests'},
    {'label':'New Tests', 'value': 'new_tests'},
    {'label':'Total Tests Per Thousand', 'value': 'total_tests_per_thousand'},
    {'label':'New Tests Per Thousand', 'value': 'new_tests_per_thousand'},
    {'label':'New Tests Smoothed', 'value': 'new_tests_smoothed'},
    {'label':'New Tests Smoothed Per Thousand', 'value': 'new_tests_smoothed_per_thousand'},
    {'label':'Tests Per Case', 'value': 'tests_per_case'},
    {'label':'Positive Rate', 'value': 'positive_rate'}
]

categoricalmetricslist = [
    {'label':'continent', 'value': 'continent'}
]

months = {
    1:{'label':"Jan 2020",'style':{'color':colors['text']}},
    2:{'label':"Feb 2020",'style':{'color':colors['text']}},
    3:{'label':"Mar 2020",'style':{'color':colors['text']}},
    4:{'label':"Apr 2020",'style':{'color':colors['text']}},
    5:{'label':"May 2020",'style':{'color':colors['text']}},
    6:{'label':"Jun 2020",'style':{'color':colors['text']}},
    7:{'label':"Jly 2020",'style':{'color':colors['text']}},
    8:{'label':"Aug 2020",'style':{'color':colors['text']}},
    9:{'label':"Sep 2020",'style':{'color':colors['text']}},
    10:{'label':"Oct 2020",'style':{'color':colors['text']}},
    11:{'label':"Nov 2020",'style':{'color':colors['text']}},
    12:{'label':"Dec 2020",'style':{'color':colors['text']}}
}

slidervaluetodatemap = {
    1:"1/1/2020",
    2:"2/1/2020",
    3:"3/1/2020",
    4:"4/1/2020",
    5:"5/1/2020",
    6:"6/1/2020",
    7:"7/1/2020",
    8:"8/1/2020",
    9:"9/1/2020",
    10:"10/1/2020",
    11:"11/1/2020",
    12:"12/1/2020"
}

df = pd.DataFrame({
    "Fruit": ["Apples"],
    "Amount": [4],
})

fig = px.bar(df, x="Fruit", y="Amount")

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(
        children='Covid-19 Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.H3(
        children='CSPB 4122 - Caleb Clough', 
        style={
        'textAlign': 'center',
        'color': colors['text']
        }
    ),

    html.Hr(),

    dcc.Tabs([
        dcc.Tab(label='Covid Metric Heatmap', style={'color': colors['background']}, children=[
            html.Hr(),
            
            html.Label('Name of Metric', style={
                'color': colors['text']}
            ),

            dcc.Dropdown(
                id='heatmap-metric-dropdown',
                options=longitudinalemetricslist,
            ),

            html.Br(),

            html.Label('Countries', style={
                'color': colors['text']}
            ),

            dcc.Dropdown(
                id='heatmap-country-dropdown-1',
                options=countrieslist,
            ),

            dcc.Dropdown(
                id='heatmap-country-dropdown-2',
                options=countrieslist,
            ),

            dcc.Dropdown(
                id='heatmap-country-dropdown-3',
                options=countrieslist,
            ),

            dcc.Dropdown(
                id='heatmap-country-dropdown-4',
                options=countrieslist,
            ),

            dcc.Dropdown(
                id='heatmap-country-dropdown-5',
                options=countrieslist,
            ),

            dcc.Dropdown(
                id='heatmap-country-dropdown-6',
                options=countrieslist,
            ),

            html.Br(),

            html.Label('Heatmap', style={
                'color': colors['text']}
            ),

            dcc.Graph(
                id='heatmap-graph',
                figure=fig
            )   
        ]),

        dcc.Tab(label='Covid Metrics Between Countries Scatterplot', children=[
            html.Hr(),
            
            html.Label('Name of 1st Metric', style={
                'color': colors['text']}
            ),

            dcc.Dropdown(
                id='scatter-metric-dropdown-1',
                options=quantitativemetricslist,
            ),

            html.Br(),
            
            html.Label('Name of 2nd Metric', style={
                'color': colors['text']}
            ),

            dcc.Dropdown(
                id='scatter-metric-dropdown-2',
                options=quantitativemetricslist,
            ),

            html.Br(),

            html.Label('Grouping Scheme', style={
                'color': colors['text']}
            ),

            dcc.Dropdown(
                id='scatter-grouping-dropdown',
                options=categoricalmetricslist,
            ),

            html.Br(),

            html.Label('Scatterplot', style={
                'color': colors['text']}
            ),

            dcc.Graph(
                id='scatterplot-graph',
                figure=fig
            )  

        ]),

        dcc.Tab(label='Covid Metric Over Time Within a Country', children=[
            html.Hr(),
            
            html.Label('Name of Metric', style={
                'color': colors['text']}
            ),

            dcc.Dropdown(
                id='line-metric-dropdown',
                options=longitudinalemetricslist,
            ),

            html.Br(),
            
            html.Label('Name of Country', style={
                'color': colors['text']}
            ),

            dcc.Dropdown(
                id='line-country-dropdown',
                options=countrieslist,
            ), 

            html.Br(),

            html.Label('Line Graph', style={
                'color': colors['text']}
            ),

            dcc.Graph(
                id='line-graph',
                figure=fig
            )

        ])
    ])       
])

@app.callback(
    Output('heatmap-graph','figure'),
    Input('heatmap-metric-dropdown','value'),
    Input('heatmap-country-dropdown-1','value'),
    Input('heatmap-country-dropdown-2','value'),
    Input('heatmap-country-dropdown-3','value'),
    Input('heatmap-country-dropdown-4','value'),
    Input('heatmap-country-dropdown-5','value'),
    Input('heatmap-country-dropdown-6','value'))
def updateheatmap(inputmetric,country1,country2,country3,country4,country5,country6):
    countrieslist = []
    for i in [country1,country2,country3,country4,country5,country6]:
        if i != None and i not in countrieslist:
            countrieslist.append(i)
    if len(countrieslist) >= 1 and inputmetric != None:
        quantdataswithiso = ['iso_code','date',inputmetric]
        quantdatas = ['date',inputmetric]
        
        filteredlongdata = longdata.filter(items=quantdataswithiso)
        joineddata = pd.DataFrame()

        if len(countrieslist) >= 1:
            country = countrieslist[0]
            joineddata = filteredlongdata[filteredlongdata['iso_code']==country]
            joineddata = joineddata.filter(items=quantdatas)
            joineddata = joineddata.rename(columns={inputmetric:country})

            for country in countrieslist[1:]:
                countrydata = filteredlongdata[filteredlongdata['iso_code']==country]
                countrydata =  countrydata.filter(items=quantdatas)
                countrydata = countrydata.rename(columns={inputmetric:country})
                joineddata = joineddata.join(countrydata.set_index('date'), on='date')

            joineddata = joineddata.fillna(0)

            zarray = []

            for country in countrieslist:
                zarray.append(joineddata[country].tolist())

            datelist = joineddata['date'].tolist()

        figheat = go.Figure(data=go.Heatmap(z=zarray,x=datelist,y=countrieslist,colorscale='Viridis'))
        figheat.update_layout(title_text = 'Metric Over Time by Country', legend_title_text = 'Value')
        figheat.update_xaxes(title_text = 'Date')
        figheat.update_yaxes(title_text = 'Country')

        return figheat

    else:
        return {}

@app.callback(
    Output('scatterplot-graph','figure'),
    Input('scatter-metric-dropdown-1','value'),
    Input('scatter-metric-dropdown-2','value'),
    Input('scatter-grouping-dropdown','value'))
def updatescatter(metric1,metric2,group):
    finalscatterdata = pd.DataFrame()

    if group != None and metric1 != None and metric2 != None and metric1 != metric2:
        
        filter = ['location',metric1,metric2,group]
        finalscatterdata = scatterdata.filter(items=filter)
        
        return px.scatter(finalscatterdata, x = metric1, y = metric2, color = group, hover_data=['location'])

    elif group == None and metric1 != None and metric2 != None and metric1 != metric2:
        filter = ['location',metric1,metric2]
        finalscatterdata = scatterdata.filter(items=filter)

        return px.scatter(finalscatterdata, x = metric1, y = metric2, hover_data=['location'], title='Metric Scatterplot by Country')

    else:
        return {}

@app.callback(
    Output('line-graph','figure'),
    Input('line-metric-dropdown','value'),
    Input('line-country-dropdown','value'))
def updatelinegraph(inputmetric,country):

    if inputmetric != None and country != None:
        quantdataswithiso = ['iso_code','date',inputmetric]
        quantdatas = ['date',inputmetric]
        
        filteredlongdata = longdata.filter(items=quantdataswithiso)
        countrydata = filteredlongdata[filteredlongdata['iso_code']==country]

        return px.line(countrydata, x="date",y = inputmetric, title="Metric Over Time")

    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)