import streamlit as st
import pandas as pd
import streamlit_folium
import numpy as np
import matplotlib.pyplot as plt
import squarify
import plotly.graph_objs as go
import plotly.express as px


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
    fig = go.Figure()
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'pink', 'gray', 'black']
    top_10 = df['employer'].value_counts().head(10)
    chart = fig.add_trace(go.Bar(
        x=top_10.values,
        y=top_10.index,
        orientation='h',
        marker=dict(color=colors)
    ))
    return chart
def draw_plot_2():
    fig_1 = go.Figure()
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'pink', 'gray', 'black']
    top_10 = df['profession'].value_counts().head(10)
    chart_1 = fig_1.add_trace(go.Bar(
        x=top_10.values,
        y=top_10.index,
        orientation='h',
        marker=dict(color=colors)
    ))
    return chart_1


def draw_plot_3():
    df_newgraph = df.groupby('profession').size().reset_index(name='counts').sort_values('counts', ascending=False)[:10]
    df_newgraph['labels'] = df_newgraph.apply(lambda x: str(x[0]) + "<br>(" + str(x[1]) + ")", axis=1)
    colors = ['#' + ''.join([np.random.choice(list('0123456789ABCDEF')) for j in range(6)])
          for i in range(len(df_newgraph))]

    fig = px.treemap(df_newgraph, path=['labels'], values='counts', color=colors,
                 color_discrete_sequence=px.colors.qualitative.Set3, 
                 title='Наиболее востребованные специалисты на рынке труда в Нижнем Новгороде')
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig


show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "Собранные данный с сайта hh.ru")
    st.write(df)
 

select_event = st.sidebar.selectbox('Show plot', ('компании-лидеры по привлечению новых кадров', 'самые востребованные специалисты', 'новый график', 'тепловая карта вакансий'))

if select_event == 'компании-лидеры по привлечению новых кадров':
    st.plotly_chart(draw_plot_1(), use_column_width=True)

if select_event == 'новый график':
    st.plotly_chart(draw_plot_3(), use_column_width=True)

if select_event == 'самые востребованные специалисты':
    st.plotly_chart(draw_plot_2(), use_column_width=True)
