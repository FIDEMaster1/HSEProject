import streamlit as st
import pandas as pd
import folium
from folium import plugins
import branca
import streamlit_folium
import numpy as np
import squarify
import plotly.graph_objs as go
from streamlit_folium import folium_static
import plotly.express as px
import matplotlib.pyplot as plt


@st.cache_data()
def load_data():
    df = pd.read_csv('project.csv')
    return df 

df = load_data() 

st.title('Vacancies in hh.ru')
st.write("""Мы проектная команда, оубчающаяся на 3 курсе ОП Экономика задались вопросом о будущем трудоутройстве. Для этого нужно проанализировать рынок труда. Мы взяли данные по вакансиям с сайта hh.ru и визуализировали их""")


st.sidebar.title("About")
st.sidebar.info(
    """
    Здесь вы можете нажать на интересующую вас информацию о рынке труда
    """
)   

def draw_plot_1():
    df_employer = df.groupby('employer').size().reset_index(name='counts')
    df_employer = df_employer.sort_values('counts', ascending=False)[:10]
    df_employer['labels'] = df_employer.apply(lambda x: str(x[0]) + "\n (" + str(x[1]) + ")", axis=1)
    fig = px.treemap(df_employer, path=['labels'], values='counts',
                 color_discrete_sequence=['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#19d3f3', 
                                          '#e763fa', '#FFA15A', '#FF6692', '#B6E880', '#FF97FF'])
    fig.update_layout(title='Компании-лидеры по привлечению сотрудников через hh.ru в Нижнем Новгороде')
    return fig

def draw_plot_3():
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'pink', 'gray', 'black']
    grouped = df.groupby('profession')['salary_from'].mean()
    top_10 = df['profession'].value_counts().head(10)
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=top_10.values,
    y=top_10.index,
    orientation='h',
    marker_color=colors,
    text=[f'{grouped[index].round():,}' for index in top_10.index],
    textposition='outside',
    ))
    fig.update_layout(
    title='Самые востребованные специалисты',
    xaxis_title='Количество вакансий',
    yaxis_title='Название профессии',
    yaxis=dict(autorange="reversed"),
    )
    return fig
def draw_plot_4():
    mean_salary_by_profession = df.groupby('profession')['salary_from'].mean()
    top_mean_salaries = mean_salary_by_profession.sort_values(ascending=False).head(10)
    colors = plt.cm.get_cmap('plasma', len(top_mean_salaries))
    fig, ax = plt.subplots()
    for i, (profession, salary) in enumerate(top_mean_salaries.iteritems()):
        ax.barh(profession, salary, color=colors(i))
        ax.text(salary + 500, i, f'{salary:,.0f}', ha='left', va='center', fontsize=12)
    ax.set_title('Топ 10 высокооплачиваемы специалистов', fontsize=16)
    ax.set_xlabel('Средняя зарплата', fontsize=14)
    ax.set_ylabel('Профессия', fontsize=14)
    ax.tick_params(axis='y', labelsize=12)
    fig.set_size_inches(12, 8)
    return  fig

mapObj = folium.Map(location=[56.3287, 44.002])
heat_data = df[['latitude', 'longitude']].dropna()
plugins.HeatMap(heat_data, radius=18, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(mapObj)
colormap = branca.colormap.LinearColormap(['blue', 'lime', 'red'],
vmin=1,
vmax=df.isna()['city'].value_counts()[0],
caption='Насыщение рынка по количеству вакансий')
colormap.add_to(mapObj)

show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "Собранные данный с сайта hh.ru")
    st.write(df)
 

select_event = st.sidebar.selectbox('Show plot', ('компании-лидеры по привлечению новых кадров', 'самые востребованные специалисты', 'тепловая карта вакансий', 'Топ 10 высокооплачиваемых специалистов'))

if select_event == 'компании-лидеры по привлечению новых кадров':
    st.plotly_chart(draw_plot_1(), use_column_width=True)

if select_event == 'самые востребованные специалисты':
    st.plotly_chart(draw_plot_3(), use_column_width=True)
if select_event == 'тепловая карта вакансий':
    folium_static(mapObj)
if select_event == 'Топ 10 высокооплачиваемых специалистов':
    st.pyplot(draw_plot_4())

