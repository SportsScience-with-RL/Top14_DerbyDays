import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from functions.data_functions import load_data, descriptive_tbl
from functions.plot_functions import plot_timeline, plot_boxplot, plot_field, plot_boxplot_anova
from functions.stat_functions import stat_report_ttest, stat_report_anova

##############################################
#                                            #
#                  SETTINGS                  #
#                                            #
##############################################

page_title = 'Top 14 - Analyse Séquences de Jeu'
page_icon = 'Top_14.png'
st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_icon=page_icon, page_title=page_title)

##################################################
#                                                #
#                  INOFS & DATA                  #
#                                                #
##################################################

games_dict = {'Stade Français Paris - Racing 92': '9 - 13',
              'Oyonnax Rugby - LOU Rugby': '38 - 20',
              'Aviron Bayonnais - Section Paloise': '35 - 16',
              'USAP - Montpellier Hérault Rugby': '23 - 16',
              'ASM Clermont - Rugby Club Toulonnais': '27 - 30',
              'Castres Olympique - Stade Toulousain': '31 - 23',
              'Stade Rochelais - Union Bordeaux-Bègles': '25 - 21'}

teams_img = {'ASM Clermont': 'teams_logo/clermont.png',
             'Aviron Bayonnais': 'teams_logo/bayonne.png',
             'Castres Olympique': 'teams_logo/castres.png',
             'LOU Rugby': 'teams_logo/lyon.png',
             'Montpellier Hérault Rugby': 'teams_logo/montpellier.png',
             'Oyonnax Rugby': 'teams_logo/oyonnax.png',
             'Racing 92': 'teams_logo/racing.png',
             'Rugby Club Toulonnais': 'teams_logo/toulon.png',
             'Stade Français Paris': 'teams_logo/paris.png',
             'Section Paloise': 'teams_logo/pau.png',
             'Stade Rochelais': 'teams_logo/larochelle.png',
             'Stade Toulousain': 'teams_logo/toulouse.png',
             'Union Bordeaux-Bègles': 'teams_logo/bordeaux.png',
             'USAP': 'teams_logo/perpignan.png'}

teams_color = {'ASM Clermont': '#cc0',
               'Aviron Bayonnais': '#62ecff',
               'Castres Olympique': '#0e93ff',
               'LOU Rugby': '#990014',
               'Montpellier Hérault Rugby': '#094a80',
               'Oyonnax Rugby': '#e45746',
               'Racing 92': '#6a96ff',
               'Rugby Club Toulonnais': '#e60100',
               'Stade Français Paris': '#ee519e',
               'Section Paloise': '#1a812b',
               'Stade Rochelais': '#cc0',
               'Stade Toulousain': '#e60100',
               'Union Bordeaux-Bègles': '#763754',
               'USAP': '#fc3'}

@st.cache_data
def get_data():
    return load_data()

#############################################
#                                           #
#                  SIDEBAR                  #
#                                           #
#############################################

with st.sidebar:
    st.markdown(
    """
    <style>
    [data-testid=stSidebar]
    {background-color: black;}
    <style>
    """, unsafe_allow_html=True)
    st.image('Top_14.png')
    ''
    ''
    menu = option_menu(menu_title='Menu',
                       menu_icon='list',
                       options=['Statistiques descriptives', 'Statistiques inférentielles'],
                       icons=['bar-chart-line-fill', 'sliders2-vertical'],
                       default_index=0)
        
if menu == 'Statistiques descriptives':
    c1, _ = st.columns([.4, .6])
    with c1:
        game_sel = st.selectbox('Sélectionner un match', list(games_dict.keys()))
        data = get_data()
        data = data[data['Match']==game_sel].reset_index(drop=True).copy()
        colors = [teams_color[game_sel.split(' - ')[0]], teams_color[game_sel.split(' - ')[1]]]
        order = [game_sel.split(' - ')[0], game_sel.split(' - ')[1]]
    ''
    ''
    _, c1, c2, c3, _ = st.columns([.3, .15, .18, .15, .17])
    c1.image(teams_img[game_sel.split(' - ')[0]])
    c2.title(games_dict[game_sel])
    c3.image(teams_img[game_sel.split(' - ')[1]])
    '---'
    st.header('Timeline')
    plot_timeline(data, colors)
    ''
    st.header('Distributions')
    st.subheader('Boxplots')
    c_box = [column for row in [st.columns(3) for _ in range(3)] for column in row]
    with c_box[0]:
        plot_boxplot(data, 'Durée', colors, order)
    with c_box[1]:
        plot_boxplot(data, 'Ruck', colors, order)
    with c_box[2]:
        plot_boxplot(data, 'Progression Zones', colors, order)
    with c_box[3]:
        plot_boxplot(data, 'Jeu debout', colors, order)
    with c_box[4]:
        plot_boxplot(data, 'Ratio Rucks/Passes', colors, order)
    with c_box[5]:
        plot_boxplot(data[data['Dernière action'].isin(['Jeu au pied', 'Dégagement'])], 'Durée séq. fin Jeu au pied', colors, order)

    st.subheader('Tables descriptives')
    with st.expander('**:blue[Match complet]**'):
        for m in ['Durée', 'Passe', 'Ruck', 'Départ ruck', 'Ratio Rucks/Passes', 'Progression Zones']:
            st.caption(m)
            st.dataframe(descriptive_tbl(data, m), use_container_width=True, hide_index=True)

        st.caption('Durée séq. fin Jeu au pied')
        st.dataframe(descriptive_tbl(data[data['Dernière action'].isin(['Jeu au pied', 'Dégagement'])], 'Durée'), use_container_width=True, hide_index=True)

    with st.expander('**:blue[Périodes de 20min]**'):
        for m in ['Durée', 'Passe', 'Ruck', 'Départ ruck', 'Ratio Rucks/Passes', 'Progression Zones']:
            st.caption(m)
            st.table(descriptive_tbl(data, m, period=True))

        st.caption('Durée séq. fin Jeu au pied')
        st.table(descriptive_tbl(data[data['Dernière action'].isin(['Jeu au pied', 'Dégagement'])], 'Durée', period=True))
    ''
    st.header('Progression (médiane du nb de zones) selon zone de départ des séquences')
    st.subheader('**:blue[Match complet]**')
    c1, c2 = st.columns(2)
    with c1:
        st.write(game_sel.split(' - ')[0])
        plot_field(data[data['Possession']==game_sel.split(' - ')[0]])
    with c2:
        st.write(game_sel.split(' - ')[1])
        plot_field(data[data['Possession']==game_sel.split(' - ')[1]])

    st.subheader('**:blue[Périodes de 20min]**')
    c1, c2 = st.columns(2)
    with c1:
        st.write(game_sel.split(' - ')[0])
        c11, c12 = st.columns(2)
        with c11:
            st.write("0'-20'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[0])
                                & (data['Chrono']=="0'-20'")])
            st.write("40'-60'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[0])
                                & (data['Chrono']=="40'-60'")])
        with c12:
            st.write("20'-40'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[0])
                                & (data['Chrono']=="20'-40'")])
            st.write("60'-80'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[0])
                                & (data['Chrono']=="60'-80'")])

    with c2:
        st.write(game_sel.split(' - ')[1])
        c21, c22 = st.columns(2)
        with c21:
            st.write("0'-20'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[1])
                                & (data['Chrono']=="0'-20'")])
            st.write("40'-60'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[1])
                                & (data['Chrono']=="40'-60'")])
        with c22:
            st.write("20'-40'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[1])
                                & (data['Chrono']=="20'-40'")])
            st.write("60'-80'")
            plot_field(data[(data['Possession']==game_sel.split(' - ')[1])
                                & (data['Chrono']=="60'-80'")])
            
else:
    c1, _ = st.columns([.4, .6])
    with c1:
        game_sel = st.selectbox('Sélectionner un match', list(games_dict.keys()))
        data = get_data()
        data = data[data['Match']==game_sel].reset_index(drop=True).copy()
        colors = [teams_color[game_sel.split(' - ')[0]], teams_color[game_sel.split(' - ')[1]]]
        order = game_sel.split(' - ')
    ''
    ''
    _, c1, c2, c3, _ = st.columns([.3, .15, .18, .15, .17])
    c1.image(teams_img[game_sel.split(' - ')[0]])
    c2.title(games_dict[game_sel])
    c3.image(teams_img[game_sel.split(' - ')[1]])
    '---'
    stat_anova = st.multiselect('Choisir les statistiques/métriques à analyser', ['Durée', 'Phases de jeu', 'Jeu debout', 'Progression Zones', 'Ratio Rucks/Passes'], 'Durée')
    '---'
    st.header('Approche fréquentiste')
    st.subheader('**:blue[Comparaison des deux équipes sur tout le match]**')
    st.write("""Un test de Shapiro-Wilk est réalisé pour chaque équipe afin de tester l'hypothèse nulle selon laquelle les valeurs de la variable sont normalement ditribuées.
             Un test de Levene est également réalisé afin de tester l'hypothèse nulle d'homogénéité des variances entre les deux équipes pour la variable choisie.""")
    st.write("""Pour une valeur p du test de Shapiro-Wilk inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : la variable de l'équipe ne semble pas suivre une loi normale (distribution normale).
             Pour une valeur p du test de Levene inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : nous supposons l'absence d'homogénéité des variances (homoscédasticité) entre les deux équipes pour la variable choisie.""")
    st.write("Pour une valeur p > 0.05 au test de Shapiro-Wilk et test de Levene, nous réaliserons un test-t de Student pour échantillons indépendants.")
    st.write("Pour une valeur p > 0.05 au test de Shapiro-Wilk et < 0.05 au test de Levene, nous réaliserons un test de Welch.")
    st.write("Pour une valeur p < 0.05 au test de Shapiro-Wilk, nous réaliserons un test U de Mann-Whitney.")
    ''
    for s in stat_anova:
        c1, c2 = st.columns(2)
        with c1:
            plot_boxplot(data, s, colors, order)
        with c2:
            stat_report_ttest(data, s, game_sel.split(' - '))
    ''
    ''
    st.subheader('**:blue[Comparaison des périodes de 20min de chaque équipe]**')
    st.write("""Un test de Shapiro-Wilk est réalisé pour chaque période de l'équipe afin de tester l'hypothèse nulle selon laquelle les valeurs de la variable de chaque période sont normalement ditribuées.
             Un test de Levene est également réalisé afin de tester l'hypothèse nulle d'homogénéité des variances entre les périodes pour la variable choisie.""")
    st.write("""Pour une valeur p du test de Shapiro-Wilk inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : la variable ne semble pas suivre une loi normale (distribution normale) pour la période.
             Pour une valeur p du test de Levene inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : nous supposons l'absence d'homogénéité des variances (homoscédasticité) entre les périodes pour la variable choisie.""")
    ''
    st.write("Pour une valeur p > 0.05 au test de Shapiro-Wilk et test de Levene, nous réaliserons une ANOVA à un facteur, afin de tester l'hypothèse nulle selon laquelle les moyennes de la variable des périodes sont égales.")
    st.write("Pour une valeur p < 0.05 au test de Shapiro-Wilk, nous réaliserons un test de Kruskall-Wallis, afin de tester l'hypothèse nulle selon laquelle la distribution de la variable est la même pour toutes les périodes.")
    st.write("""Pour une valeur p de l'ANOVA inférieur au seuil de 95%, nous rejetons l'hypothèse nulle : la moyenne d'au moins une période est différente de celle d'une autre période (au moins).
             Dans ce cas un test post-hoc de Tukey est réalisé afin de tester toutes les combinaisons de comparaison des différentes périodes. 
             Une valeur p < 0.05 au test de Tukey suggère une différence statistiquement significative entre les deux périodes.""")
    st.write("""Pour une valeur p du test de Kruskall-Wallis au seuil de 95%, nous rejetons l'hypothèse nulle : la distribution d'au moins une période est différente de celle d'une autre période (au moins).
             Dans ce cas un test post-hoc de Conover est réalisé afin de tester toutes les combinaisons de comparaison des différentes périodes. 
             Une valeur p < 0.05 au test de Conover suggère une différence statistiquement significative entre les deux périodes.""")
    st.write("""Pour chaque test post-hoc significatif, le d de Cohen est calculé afin de caractériser la taille de l'effet. 
             Plus la valeur absolue du d est grande plus la taille de l'effet est importante (la différence est grande entre les périodes).
             Le signe du d (positif ou négatif) indique le sens de la différence entre les périodes.""")
    st.write("Pour plus d'informations sur l'interprétation du d de Cohen, se rendre au lien suivant : [https://rpsychologist.com/fr/cohend/](https://rpsychologist.com/fr/cohend/)")
    
    for s in stat_anova:
        st.write(f"**:blue[{s}]**")
        c1, c2 = st.columns(2)
        with c1:
            st.write(game_sel.split(' - ')[0])
            plot_boxplot_anova(data[data['Possession']==game_sel.split(' - ')[0]],
                               s, colors[0], ["0'-20'", "20'-40'", "40'-60'", "60'-80'"])
            stat_report_anova(data[data['Possession']==game_sel.split(' - ')[0]],
                              s, ["0'-20'", "20'-40'", "40'-60'", "60'-80'"])
            ''
            ''
        with c2:
            st.write(game_sel.split(' - ')[1])
            plot_boxplot_anova(data[data['Possession']==game_sel.split(' - ')[1]],
                               s, colors[1], ["0'-20'", "20'-40'", "40'-60'", "60'-80'"])
            stat_report_anova(data[data['Possession']==game_sel.split(' - ')[1]],
                              s, ["0'-20'", "20'-40'", "40'-60'", "60'-80'"])
            ''
            ''