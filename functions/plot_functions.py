import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_timeline(data, colors):
    data['Color_timeline'] = [colors[0] if s1<0 else colors[1] if s2<0 else '#1B212C'
                              for s1, s2 in zip(data['Score_team1'].diff(-1), data['Score_team2'].diff(-1))]
    
    fig, ax = plt.subplots(figsize=(15, 6), facecolor='#1B212C')
    sns.barplot(data=data, x=data.index, y='Durée_timeline', hue=data.index, legend=False, ax=ax, edgecolor='.6', palette=list(data['Color_timeline']))
    plt.xlabel('')
    plt.ylabel('Durée de la séquence\n(valeur absolue)', fontsize=8, color='white')
    ylim_ = np.max(data['Durée'])
    plt.ylim((-ylim_, ylim_+20))
    plt.yticks(fontsize=6, color='white')
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.tick_params(axis='y', colors='white')
    for c in data['Chrono'].unique():
        c_cut = data[data['Chrono']==c].index[0]
        plt.axvline(c_cut-.5, color='gray', linestyle=':', linewidth=1)
        if c == "0'-20'":
            plt.text(x=(data[data['Chrono']==c].shape[0]/2)-2, y=ylim_+10, s=c, color='gray')
        else:
            plt.text(x=c_cut+(data[data['Chrono']==c].shape[0]/2)-2, y=ylim_+10, s=c, color='gray')
    plt.axhline(0, color='gray', linewidth=1)
    ax.set_facecolor('#1B212C')
    ax1 = plt.gca()
    ax1.spines['left'].set_color('white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    st.pyplot(fig)


def plot_boxplot(data, metric, colors, order):
    title = metric

    if metric == 'Durée séq. fin Jeu au pied':
        metric = 'Durée'
        title = 'Durée séq. fin Jeu au pied'
    if metric == 'Phases de jeu':
        metric = 'Ruck'
        title = 'Phases de jeu'

    fig, ax = plt.subplots(facecolor='#1B212C')
    PROPS = {'boxprops':{'facecolor':'none', 'edgecolor':'gray'},
             'medianprops':{'color':'gray'},
             'whiskerprops':{'color':'gray'},
             'capprops':{'color':'gray'}}
    sns.boxplot(data=data, x='Possession', hue='Possession', legend=False, y=metric, width=.5, ax=ax, **PROPS, flierprops={'markeredgecolor':'gray'}, order=order)
    sns.swarmplot(data=data, x='Possession', hue='Possession', legend=False, y=metric, palette=colors, size=6, zorder=1, ax=ax, order=order)
    ax.set_facecolor('#1B212C')
    ax.tick_params(axis='both', colors='white')
    ax1 = plt.gca()
    ax1.spines['left'].set_color('white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    plt.xlabel('')
    plt.ylabel('')
    plt.yticks(fontsize=10)
    plt.title(title, color='white', fontsize=15)

    st.pyplot(fig)


def plot_field(data):
    zone_start = data.groupby('Start_zone')['Progression Zones'].median().to_frame()
    zone_start['PZ_%'] = round((zone_start['Progression Zones']-zone_start['Progression Zones'].min()) 
                               / (zone_start['Progression Zones'].max()-zone_start['Progression Zones'].min()), 2)

    for z in ['22m1', '22m2', '40m1', '40m2', '10m1', '10m2', '40m3', '40m4', '22m3', '22m4']:
        if z not in zone_start.index.tolist():
            zone_start.loc[z, ['Progression Zones', 'PZ_%']] = 0, 0 

    fig, ax = plt.subplots(figsize=(15, 6), facecolor='green')
    ax.set_aspect('equal')
    ax.set_facecolor('green')
    plt.xlim(0, 100)
    plt.ylim(0, 70)
    for vl in [22, 50, 78]:
        plt.axvline(vl, color='white')

    hl_dict = {22: [19.5, 24.5], 40: [37.5, 42.5], 50: [47.5, 52.5],
               60: [57.5, 62.5], 78: [75.5, 80.5],
               5: [5, 10], 95: [90, 95]}

    for hl in hl_dict:
        ax.hlines(55, hl_dict[hl][0], hl_dict[hl][1], color='white')
        ax.hlines(15, hl_dict[hl][0], hl_dict[hl][1], color='white')
        ax.hlines(65, hl_dict[hl][0], hl_dict[hl][1], color='white')
        ax.hlines(5, hl_dict[hl][0], hl_dict[hl][1], color='white')

    for tl in [5, 40, 60, 95]:
        ax.vlines(tl, 52.5, 57.5, color='white')
        ax.vlines(tl, 12.5, 17.5, color='white')
        ax.vlines(tl, 62.5, 67.5, color='white')
        ax.vlines(tl, 2.5, 7.5, color='white')

    for gl in [5, 95]:
        ax.vlines(gl, 27, 32, color='white')
        ax.vlines(gl, 39, 44, color='white')

    for l10 in [40, 60]:
        ax.vlines(l10, 22.5, 27.5, colors='white')
        ax.vlines(l10, 32.5, 37.5, colors='white')
        ax.vlines(l10, 42.5, 47.5, colors='white')

    plt.text(19.2, 10, s='22', fontsize=15, fontweight='medium', color='white')
    plt.text(37.2, 10, s='10', fontsize=15, fontweight='medium', color='white')
    plt.text(47.2, 10, s='50', fontsize=15, fontweight='medium', color='white')
    plt.text(57.2, 10, s='10', fontsize=15, fontweight='medium', color='white')
    plt.text(75.2, 10, s='22', fontsize=15, fontweight='medium', color='white')

    ax1 = plt.gca()
    ax1.spines['left'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['right'].set_color('white')

    zone_dict = {'22m1': [0, 11, 4], '22m2': [11, 22, 15],
                 '40m1': [22, 31, 26], '40m2': [31, 40, 35],
                 '10m1': [40, 50, 44], '10m2': [50, 60, 54],
                 '40m3': [60, 69, 64], '40m4': [69, 78, 73],
                 '22m3': [78, 89, 82], '22m4': [89, 100, 93]}
    
    for z in zone_dict:
        ax.axvspan(zone_dict[z][0], zone_dict[z][1], color='orange', alpha=zone_start.loc[z, 'PZ_%'])
        plt.text(zone_dict[z][2], 22, s=int(zone_start.loc[z, 'Progression Zones']), color='black', fontweight='bold')

    plt.yticks([])
    plt.xticks([])

    plt.text(41.2, 51, s='Sens du jeu', color='black', fontweight='bold')
    ax.arrow(41, 48, 18, 0, head_width=2.5, length_includes_head=True, color='black')

    st.pyplot(fig)


def plot_boxplot_anova(data, metric, color, order):
    if metric == 'Durée séq. fin Jeu au pied':
        metric = 'Durée'
    if metric == 'Phases de jeu':
        metric = 'Ruck'

    fig, ax = plt.subplots(figsize=(4, 3), facecolor='#1B212C')
    PROPS = {'boxprops':{'facecolor':'none', 'edgecolor':'gray'},
             'medianprops':{'color':'gray'},
             'whiskerprops':{'color':'gray'},
             'capprops':{'color':'gray'}}
    sns.boxplot(data=data, x='Chrono', y=metric, order=order, width=.5, ax=ax, **PROPS, flierprops={'markeredgecolor':'gray'})
    sns.swarmplot(data=data, x='Chrono', y=metric, order=order, color=color, legend=False, size=4, zorder=1, ax=ax)
    ax.set_facecolor('#1B212C')
    ax.tick_params(axis='both', colors='white')
    ax1 = plt.gca()
    ax1.spines['left'].set_color('white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    plt.xlabel('')
    plt.ylabel('')
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    st.pyplot(fig)