# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as dd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import warnings
warnings.filterwarnings('ignore')
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import pandas as pd

mc_responses=pd.read_csv('multipleChoiceResponses.csv',encoding='ISO-8859-1')
c_rates=pd.read_csv('conversionRates.csv')

cnt_gender = mc_responses["GenderSelect"].value_counts(ascending=True)
cnt_country = mc_responses["Country"].value_counts()[:25].to_frame()
cnt_country=cnt_country['Country'].sort_values(ascending=True)
app = dash.Dash(__name__)
server = app.server
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}

markdown_text_gender='''
---
#### About me
* I am [Harisyam Manda](https://www.linkedin.com/in/harisyammanda/) and a Computational Sci graduate with immense passion for the field of AI and ML.
* I am an Udacity Machine learning Graduate [link](https://github.com/harisyammnv/Machine_Learning_Nano_degree_Udacity)
#### Goal of the Dashboard
**To illustrate that I could do Exploratory Data Analysis and build up dashboards from scratch in a day**.

This is an exemplary dashboard which i built using the [Kaggle ML 2017 Survey dataset](https://www.kaggle.com/kaggle/kaggle-survey-2017)
   * This dashboard is built using Plotly + DASH open source libraries
   * It illustrates about Data scientist job and working culture around the world
---
'''
c_rates.drop('Unnamed: 0',axis=1,inplace=True)
mc_responses['CompensationAmount']=mc_responses['CompensationAmount'].str.replace(',','')
mc_responses['CompensationAmount']=mc_responses['CompensationAmount'].str.replace('-','')


metricscale1=[[0, 'rgb(102,194,165)'], [0.05, 'rgb(102,194,165)'], [0.15, 'rgb(171,221,164)'], 
              [0.2, 'rgb(230,245,152)'], [0.25, 'rgb(255,255,191)'], [0.35, 'rgb(254,224,139)'], 
              [0.45, 'rgb(253,174,97)'], [0.55, 'rgb(213,62,79)'], [1.0, 'rgb(158,1,66)']]




salary=mc_responses[['CompensationAmount','CompensationCurrency','GenderSelect','Country','CurrentJobTitleSelect']].dropna()
salary=salary.merge(c_rates,left_on='CompensationCurrency',right_on='originCountry',how='left')
salary['Salary']=pd.to_numeric(salary['CompensationAmount'])*salary['exchangeRate']
salary=salary[salary['Salary']<1000000]

male_salary=salary[salary['GenderSelect']=="Male"]
female_salary=salary[salary['GenderSelect']=="Female"]
diff_salary=salary[salary['GenderSelect']=="A different identity"]
rem_salary=salary[salary['GenderSelect']=="Non-binary, genderqueer, or gender non-conforming"]

ys=[male_salary.Salary.values,female_salary.Salary.values,diff_salary.Salary.values,rem_salary.Salary.values]
names=['Male','Female','A different identity','Non-binary']
colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)']


cnt_srs=mc_responses['Age'].value_counts()
cnt_parents = mc_responses['ParentsEducation'].value_counts()

trace = []
sal_coun=salary.groupby('Country')['Salary'].median().sort_values(ascending=False)[:25].to_frame()
max_coun=salary.groupby('Country')['Salary'].median().to_frame()
max_coun=max_coun[max_coun.index.isin(cnt_country.index)]
max_coun=max_coun.sort_values(by='Salary',ascending=True)


edu =  mc_responses['FormalEducation'].value_counts()
values_edu = (np.array((edu / edu.sum())*100))

cnt_major= mc_responses["MajorSelect"].value_counts().sort_values(ascending=True)
cnt_profession = mc_responses["CurrentJobTitleSelect"].value_counts().sort_values(ascending=True)

scientist=mc_responses[mc_responses['DataScienceIdentitySelect']=='Yes']
comp_edu=scientist.merge(salary,left_index=True,right_index=True,how='left')
comp_edu=comp_edu[['FormalEducation','Salary']]

names_edu=comp_edu.FormalEducation.unique().tolist()
trace_edu = []

for i in range(len(names_edu)):
    trace_edu.append ( 
        go.Box(
            y=comp_edu[comp_edu['FormalEducation']==names_edu[i]].Salary.values,
            name=names_edu[i],
        )
    )

names_gender=salary.GenderSelect.unique().tolist()
trace_gender = []

for i in range(len(names_gender)):
    trace_gender.append ( 
        go.Box(
            y=salary[salary['GenderSelect']==names_gender[i]].Salary.values,
            name=names_gender[i],
        )
    )



import base64
image_filename = 'Capture.PNG' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


import base64
gif_filename = 'giphy.gif' # replace with your own image
encoded_gif = base64.b64encode(open(gif_filename, 'rb').read())

# Controls (dropdowns)
group = ['All']
cntry=mc_responses.Country.value_counts().index.tolist()
cntry.sort()
group = group +  cntry
group_class = [{'label': str(item),
                      'value': str(item)}
                     for item in group]
gender=mc_responses.GenderSelect.value_counts().index.tolist()
group_gender=[{'label': str(item),
                      'value': str(item)}
                     for item in gender]

profession=cnt_profession.index.tolist()
profession=profession+['All']
profession.sort()
group_prof=[{'label': str(item),'value': str(item)} for item in profession]



resp=mc_responses.dropna(subset=['WorkToolsSelect'])
resp=resp.merge(c_rates,left_on='CompensationCurrency',right_on='originCountry',how='left')
python=resp[(resp['WorkToolsSelect'].str.contains('Python'))&(~resp['WorkToolsSelect'].str.contains('R'))]
R=resp[(~resp['WorkToolsSelect'].str.contains('Python'))&(resp['WorkToolsSelect'].str.contains('R'))]



layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor=app_colors['background'],
    paper_bgcolor=app_colors['background'],
)

app.layout = html.Div([
        html.Div([
    html.H1('Kaggle Machine Learning Survey', style={'font-family': 'Helvetica',
                       "margin-top": "15",
                       "margin-bottom": "0","margin-left": "5",'color': app_colors['text']
        },className='eight columns'),
html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                className='two columns',
                style={
                    'height': '6%',
                    'width': '6%',
                    'float': 'right',
                    'position': 'relative',
                    'padding-top': 20,
                    'padding-right': 10
                },
            ),
            html.P(
                'Decoding the sexiest job of 21st Century',
                style={'font-family': 'Helvetica',
                       "font-size": "120%",
                       "width": "80%", 'color':app_colors['text'],},
                className='four columns',
            ),],className='container-fluid',),
        
        html.Div([
        html.Img(
                src='data:image/gif;base64,{}'.format(encoded_gif.decode()),
                className='six columns',
                style={
                    'height': '15%',
                    'width': '30%',
                    'float': 'center',
                    'position': 'relative',
                    'padding-top': 5,
                    'padding-left': 20
                },
            ),
            html.Div(
    dcc.Markdown(markdown_text_gender,),className='six columns',style={'margin-left': '10','margin-bottom': '10','color':app_colors['text'],}),#'text-align': 'center'
],className='row'),

        html.Div([
        html.Div(dcc.Graph(
        id='example5',
        figure={
            'data': [dict(
        type = 'choropleth',
        autocolorscale = False,
        colorscale = metricscale1,
        showscale = False,
        locations = mc_responses.Country.value_counts().index,
        z = mc_responses.Country.value_counts().values,
        locationmode = 'country names',
        text = mc_responses.Country.value_counts().index,
        marker = dict(
            line = dict(color = 'rgb(250,250,225)', width = 0.5)),
            colorbar = dict(autotick = True, tickprefix = '', 
            title = 'Number of Respondees')
            )
                
            ],
            'layout': dict(width= 900,
        height= 450,
    title = 'Number of People Surveyed in the world',
    margin=go.Margin(l=10,r=10,t=30,b=10,),
    plot_bgcolor= app_colors['background'],
                paper_bgcolor=app_colors['background'],
                font= {'color': app_colors['text']},
    geo = dict(
        showframe = False,
        showocean = True,
        oceancolor = 'rgb(28,107,160)',
        #oceancolor = 'rgb(222,243,246)',
        projection = dict(
        type = 'Mercator',
        ),
        lonaxis =  dict(
                showgrid = False,
                gridcolor = 'rgb(102, 102, 102)'
            ),
        lataxis = dict(
                showgrid = False,
                gridcolor = 'rgb(102, 102, 102)'
                )
            ),
        )}
    ),className='six columns',style={'margin-top': '10','padding':'5'}),
 html.Div(dcc.Graph(
        id='freq',
        ),className='six columns',style={'margin-left': '5','margin-bottom': '5','padding':'5'}),        
],className='row'),
     html.Div([
             html.Div([
                    html.P('Country Select:', style={'font-family': 'Helvetica',
                       "font-size": "120%",
                       "width": "80%", 'color':app_colors['text'],},),
                    
                    dcc.Dropdown(
                        id='country',
                        options= group_class,
                        multi=False,
                        value='All'
                    )
                ],
                className='two columns',
                style={'margin-top': '10','margin-left': '10','margin-bottom': '10','padding':'5'},),
              ],className='row'),
    
        html.Div([
               html.Div(dcc.Graph(
                       id='formal_edu',),
        className='four columns',),
            
                html.Div(dcc.Graph(
        id='profession',
    ),className='four columns',),
            html.Div(dcc.Graph(
        id='salary',
    ),className='four columns'),
                ]),
    
     html.Div([
             html.Div([
                    html.P('Profession Select:', style={'font-family': 'Helvetica',
                       "font-size": "120%",
                       "width": "80%", 'color':app_colors['text'],},),
                    
                    dcc.Dropdown(
                        id='prof_sel',
                        options= group_prof,
                        multi=False,
                        value='All'
                    )
                ],
                className='two columns',
                style={'margin-top': '10','margin-left': '10','margin-bottom': '10','padding':'5'},),
              ],className='row'),
    
    html.Div([
               html.Div(dcc.Graph(
                       id='pyr',),
        className='six columns',),
         html.Div(dcc.Graph(
                       id='mlmethod',),
        className='six columns',),
                ]),
    
    
],className='container-fluid',style={'backgroundColor': app_colors['background'], 'margin-left':'-10px','margin-top':'-5px','margin-right':'-5px','height':'2200px',})#

@app.callback(
    dash.dependencies.Output('freq', 'figure'),
    [dash.dependencies.Input('country', 'value')]
)
def update_freq(country_value):
    mcr=mc_responses.copy()
    if country_value!='All':
        mcr=mcr[mcr['Country']==country_value]
        cnt_gender = mcr["GenderSelect"].value_counts(ascending=True)
    else:
        cnt_gender = mcr["GenderSelect"].value_counts(ascending=True)
    return {
            'data': [
                {'y': cnt_gender.index, 'x':cnt_gender.values , 'type': 'bar', 'name': 'Gender Dist.','marker':dict(color = cnt_gender.values,),'orientation':'h'},
            ],
            'layout': go.Layout(
                title= 'Gender Frequency of the survey respondents',
                margin= go.Margin(t=50,l=350,),
                plot_bgcolor= app_colors['background'],
                paper_bgcolor= app_colors['background'],
                font= {'color': app_colors['text']}
            )}



            
@app.callback(
    dash.dependencies.Output('formal_edu', 'figure'),
    [dash.dependencies.Input('country', 'value')]
)
def update_value(country_value):
    mcr=mc_responses.copy()
    if country_value!='All':
        mcr=mcr[mcr['Country']==country_value]
        edu =  mcr['FormalEducation'].value_counts()
        values_edu = (np.array((edu / edu.sum())*100))
    else:
        edu =  mcr['FormalEducation'].value_counts()
        values_edu = (np.array((edu / edu.sum())*100))
    return {
            'data': [
                    go.Pie(labels=['Master Degree','Bachelor Degree','Doctoral Degree','Some Other','Professional Degree','No formal ed','I prefer not to answer'], values=values_edu,
                   textfont=dict(size=12, color=app_colors['text']),
                   marker=dict(line=dict(color=app_colors['background'], width=2)))
                
            ],
            'layout': go.Layout(
                title= 'Formal Education of the survey participants',
                margin= go.Margin(t=50,l=50,),
                plot_bgcolor= app_colors['background'],
                paper_bgcolor= app_colors['background'],
                font= {'color': app_colors['text']}
            )}

@app.callback(
    dash.dependencies.Output('profession', 'figure'),
    [dash.dependencies.Input('country', 'value')]
)
def update_profession(country_value):
    mcr=mc_responses.copy()
    if country_value!='All':
        mcr=mcr[mcr['Country']==country_value]
        cnt_profession = mcr["CurrentJobTitleSelect"].value_counts().sort_values(ascending=True)
    else:
        cnt_profession = mcr["CurrentJobTitleSelect"].value_counts().sort_values(ascending=True)

    return{
            'data': [
                {'x': cnt_profession.values, 'y':cnt_profession.index , 'type': 'bar', 'name': 'Majors','marker':dict(color = cnt_profession.values,),'orientation':'h'},
            ],
            'layout': go.Layout(
                title= 'Profession of the respondents',
                margin= go.Margin(t=50,l=250,),
                plot_bgcolor= app_colors['background'],
                paper_bgcolor= app_colors['background'],
                font= {'color': app_colors['text']}
            )}

@app.callback(
    dash.dependencies.Output('salary', 'figure'),
    [dash.dependencies.Input('country', 'value')]
)
def update_salary(country_value):
    sal=salary.copy()
    if country_value!='All':
        sal=sal[sal['Country']==country_value]
        names_gender=sal.GenderSelect.unique().tolist()
        trace_gender = []
        
        for i in range(len(names_gender)):
            trace_gender.append ( 
                go.Box(
                    y=sal[sal['GenderSelect']==names_gender[i]].Salary.values,
                    name=names_gender[i],
                )
            )

    else:
        names_gender=sal.GenderSelect.unique().tolist()
        trace_gender = []
        
        for i in range(len(names_gender)):
            trace_gender.append ( 
                go.Box(
                    y=sal[sal['GenderSelect']==names_gender[i]].Salary.values,
                    name=names_gender[i],
                )
            )
        

    return{
            'data': trace_gender,
            'layout': go.Layout(
                title= 'Salary with respect to Gender',
                margin= go.Margin(t=50,l=50,),
                plot_bgcolor= app_colors['background'],
                paper_bgcolor= app_colors['background'],
                font= {'color': app_colors['text']},
                showlegend=False
            )}


@app.callback(
    dash.dependencies.Output('pyr', 'figure'),
    [dash.dependencies.Input('prof_sel', 'value')]
)
def update_pyr(prof_value):
    pyp=python.copy()
    rp=R.copy()
    if prof_value!='All':
        pyp=pyp[pyp['CurrentJobTitleSelect']==prof_value]
        rp=rp[rp['CurrentJobTitleSelect']==prof_value]
        labels1=pyp['LanguageRecommendationSelect'].value_counts()[:5].index
        sizes1=pyp['LanguageRecommendationSelect'].value_counts()[:5].values
        
        labels2=rp['LanguageRecommendationSelect'].value_counts()[:5].index
        sizes2=rp['LanguageRecommendationSelect'].value_counts()[:5].values
    else:
        labels1=pyp['LanguageRecommendationSelect'].value_counts()[:5].index
        sizes1=pyp['LanguageRecommendationSelect'].value_counts()[:5].values
        
        labels2=rp['LanguageRecommendationSelect'].value_counts()[:5].index
        sizes2=rp['LanguageRecommendationSelect'].value_counts()[:5].values

    return{
  "data": [
    {
      "values": sizes1,
      "labels": labels1,
      "domain": {"x": [0, .48]},
      "name": "Language",
      "hoverinfo":"label+percent+name",
      "hole": .4,
      "type": "pie"
    },     
    {
      "values": sizes2 ,
      "labels": labels2,
      "text":"CO2",
      "textposition":"inside",
      "domain": {"x": [.54, 1]},
      "name": "Language",
      "hoverinfo":"label+percent+name",
      "hole": .4,
      "type": "pie"
    }],
  "layout": {
        "title":"Language Recommended By Python and R users based on Profession",
        "plot_bgcolor": app_colors['background'],
        "paper_bgcolor": app_colors['background'],
        "font": {'color': app_colors['text']},
        "annotations": [
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": "Python",
                "x": 0.18,
                "y": 0.5
            },
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": "R",
                "x": 0.78,
                "y": 0.5}]}}


@app.callback(
    dash.dependencies.Output('mlmethod', 'figure'),
    [dash.dependencies.Input('prof_sel', 'value')]
)
def update_mlmethod(prof_value):
    mcr=mc_responses.copy()
    print('entered')
    if prof_value!='All':
        names = []
        rarely_count = []
        sometimes_count = []
        often_count = []
        mostly_count = []
        cols_to_use = ["WorkMethodsFrequencyBayesian",
                      "WorkMethodsFrequencyCNNs",
                      "WorkMethodsFrequencyDataVisualization", "WorkMethodsFrequencyDecisionTrees", "WorkMethodsFrequencyEnsembleMethods",
                      "WorkMethodsFrequencyGANs", "WorkMethodsFrequencyGBM",
                      "WorkMethodsFrequencyNLP", "WorkMethodsFrequencyNeuralNetworks", "WorkMethodsFrequencyPCA",
                      "WorkMethodsFrequencyRandomForests", "WorkMethodsFrequencyRecommenderSystems",
                      "WorkMethodsFrequencyRNNs",
                      "WorkMethodsFrequencySVMs", "WorkMethodsFrequencyTextAnalysis", "WorkMethodsFrequencyTimeSeriesAnalysis"]
        mcr=mcr[mcr['CurrentJobTitleSelect']==prof_value]
        
        for col in cols_to_use:
            cnt_srs = mcr[col].value_counts()
            stack_check=cnt_srs.index.tolist()
            names.append(col.replace("WorkMethodsFrequency",""))
            if "Rarely" in stack_check:
                rarely_count.append(cnt_srs["Rarely"])
               
            else:
                rarely_count.append(0)
            if "Sometimes" in stack_check:
                sometimes_count.append(cnt_srs["Sometimes"])
               
            else:
                sometimes_count.append(0)
            
            if "Often" in stack_check:
                often_count.append(cnt_srs["Often"])
                
            else:
                often_count.append(0)
            
            if "Most of the time" in stack_check:
                mostly_count.append(cnt_srs["Most of the time"])
                
            else:
                mostly_count.append(0)
        trace1 = go.Bar(
            x=names,
            y=rarely_count,
            #orientation = 'h',
            name = "Rarely",
            marker = dict(color='rgba(55, 128, 191, 0.7)')
        )
        trace2 = go.Bar(
            x=names,
            y=sometimes_count,
            #orientation = 'h',
            name = "Sometimes",
            marker = dict(color = 'rgba(246, 78, 139, 0.6)')
        )
        trace3 = go.Bar(
            x=names,
            y=often_count,
            #orientation = 'h',
            name = "Often",
            marker = dict(color = 'rgba(222,45,38,0.8)')
        )
        trace4 = go.Bar(
            x=names,
            y=mostly_count,
            #orientation = 'h',
            name = "Most of the time",
            marker = dict(color='rgba(50, 171, 96, 0.6)')
        )
    else:
        names = []
        rarely_count = []
        sometimes_count = []
        often_count = []
        mostly_count = []
        cols_to_use = ["WorkMethodsFrequencyBayesian",
                      "WorkMethodsFrequencyCNNs",
                      "WorkMethodsFrequencyDataVisualization", "WorkMethodsFrequencyDecisionTrees", "WorkMethodsFrequencyEnsembleMethods",
                      "WorkMethodsFrequencyGANs", "WorkMethodsFrequencyGBM",
                      "WorkMethodsFrequencyNLP", "WorkMethodsFrequencyNeuralNetworks", "WorkMethodsFrequencyPCA",
                      "WorkMethodsFrequencyRandomForests", "WorkMethodsFrequencyRecommenderSystems",
                      "WorkMethodsFrequencyRNNs",
                      "WorkMethodsFrequencySVMs", "WorkMethodsFrequencyTextAnalysis", "WorkMethodsFrequencyTimeSeriesAnalysis"]
        for col in cols_to_use:
            cnt_srs = mcr[col].value_counts()
            names.append(col.replace("WorkMethodsFrequency",""))
            rarely_count.append(cnt_srs["Rarely"])
            sometimes_count.append(cnt_srs["Sometimes"])
            often_count.append(cnt_srs["Often"])
            mostly_count.append(cnt_srs["Most of the time"])
        trace1 = go.Bar(
            x=names,
            y=rarely_count,
            #orientation = 'h',
            name = "Rarely",
            marker = dict(color='rgba(55, 128, 191, 0.7)')
        )
        trace2 = go.Bar(
            x=names,
            y=sometimes_count,
            #orientation = 'h',
            name = "Sometimes",
            marker = dict(color = 'rgba(246, 78, 139, 0.6)')
        )
        trace3 = go.Bar(
            x=names,
            y=often_count,
            #orientation = 'h',
            name = "Often",
            marker = dict(color = 'rgba(222,45,38,0.8)')
        )
        trace4 = go.Bar(
            x=names,
            y=mostly_count,
            #orientation = 'h',
            name = "Most of the time",
            marker = dict(color='rgba(50, 171, 96, 0.6)')
        )
            
    return{
            'data':[trace1,trace2,trace3,trace4],
            'layout':{'title':'How often do you the use given DS method?',
                    'barmode':'stack',"plot_bgcolor": app_colors['background'],
        "paper_bgcolor": app_colors['background'],
        "font": {'color': app_colors['text']},
                    'width' : 900,'height' : 400,'margin':go.Margin(l=150)}}


if __name__ == '__main__':
    app.run_server(debug=True)
