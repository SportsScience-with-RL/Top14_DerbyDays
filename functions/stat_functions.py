import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def stat_report_ttest(data, metric, teams):
    if metric == 'Phases de jeu':
        metric = 'Ruck'
    team1_stat = data[metric][data['Possession']==teams[0]]
    team2_stat = data[metric][data['Possession']==teams[1]]

    #Normalité
    team1_shap_p = round(stats.shapiro(team1_stat).pvalue, 3)
    team2_shap_p = round(stats.shapiro(team2_stat).pvalue, 3)

    #Egalité variances
    lev_p = round(stats.levene(team1_stat, team2_stat, center='mean').pvalue, 3)

    if (team1_shap_p > .05) and (team2_shap_p > .05):
        if lev_p > .05:
            st.write('Tests de normalité')
            st.write(f"- {teams[0]} - Valeur p (Shapiro-Wilk) : {team1_shap_p}*\n- {teams[1]} - Valeur p (Shapiro-Wilk) : {team2_shap_p}*")
            ''
            st.write("Test d'homoscédasticité")
            st.write(f"Valeur p (Levene) : {lev_p}*")
            ''
            st.write('**Test réalisé : test-t de Student**')
            ttest_ = stats.ttest_ind(team1_stat, team2_stat)
            if ttest_.pvalue > 0.05:
                st.write(f"""Les valeurs semblent être les mêmes entre les deux équipes.
                         Un test-t de Student suggère que la différence n'est pas statistiquement significative 
                         (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}).""")
            else:
                st.write(f"""Les valeurs semblent être différentes entre les deux équipes.
                         Un test-t de Student suggère que la différence est statistiquement significative 
                         (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}).""")
        elif lev_p < .05:
            st.write('Tests de normalité')
            st.write(f"- {teams[0]} - Valeur p (Shapiro-Wilk) : {team1_shap_p}*\n- {teams[1]} - Valeur p (Shapiro-Wilk) : {team2_shap_p}*")
            ''
            st.write("Test d'homoscédasticité")
            st.write(f"Valeur p (Levene) : {lev_p}")
            ''
            st.write('**Test réalisé : test de Welch**')
            ttest_ = stats.ttest_ind(team1_stat, team2_stat, equal_var=False)
            if ttest_.pvalue > 0.05:
                st.write(f"""Les valeurs semblent être les mêmes entre les deux équipes.
                         Un test de Welch suggère que la différence n'est pas statistiquement significative 
                         (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}).""")
            else:
                st.write(f"""Les valeurs semblent être différentes entre les deux équipes.
                         Un test de Welch suggère que la différence est statistiquement significative 
                         (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}).""")
    else:
        st.write('Tests de normalité')
        st.write(f"- {teams[0]} - Valeur p (Shapiro-Wilk) : {team1_shap_p}\n- {teams[1]} - Valeur p (Shapiro-Wilk) : {team2_shap_p}")
        ''
        st.write('**Test réalisé : test U de Mann-Whitney**')
        mann_ = stats.mannwhitneyu(team1_stat, team2_stat)
        if mann_.pvalue > 0.05:
            st.write(f"""Les valeurs semblent être les mêmes entre les deux équipes.
                     Un test U de Mann-Whitney suggère que la différence n'est pas statistiquement significative 
                     (U={round(mann_.statistic, 2)}, p={round(mann_.pvalue, 2)}).""")
        else:
            st.write(f"""Les valeurs semblent être différentes entre les deux équipes.
                     Un test U de Mann-Whitney suggère que la différence est statistiquement significative 
                     (U={round(mann_.statistic, 2)}, p={round(mann_.pvalue, 2)}).""")
            

def cohen_d(x,y):
    n1, n2 = len(x), len(y)
    s1, s2 = np.var(x, ddof=1), np.var(y, ddof=1)
    s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    u1, u2 = np.mean(x), np.mean(y)
    return round((u1 - u2) / s, 3)


def stat_report_anova(data, metric, order):
    if metric == 'Phases de jeu':
        metric = 'Ruck'
    desc_table = pd.DataFrame()

    anova_groups = []
    shapiro_p = []

    for c in order:
        sub_chrono = data[data['Chrono']==c].copy()
        shap_p = round(stats.shapiro(sub_chrono[metric]).pvalue, 3)
        shapiro_p.append(shap_p)
        if shap_p < 0.05:
            shapiro_ = shap_p
        else:
            shapiro_ = f"{shap_p}*" 
        desc_table.loc[c, 'Shapiro-Wilk (p-value)'] = shapiro_
        anova_groups.append(sub_chrono[metric])

    lev_p = round(stats.levene(*anova_groups, center='mean').pvalue, 3)
    normality_check = [s for s in shapiro_p if s > .05]

    if len(normality_check) == len(shapiro_p) and lev_p > .05:
        anova_p = stats.f_oneway(*anova_groups).pvalue
        if anova_p > 0.05:
            st.write(f"ANOVA p-value: {round(anova_p, 3)}")
            st.write("Il n'y a pas de différence significative des valeurs entre les périodes du match")
        else:
            st.write(f"ANOVA p-value: {round(anova_p, 3)}*")
            st.write('Au moins une période du match a des valeurs significativement différentes avec une autre période')
            #Post-hoc
            post_hoc_matrix = sp.posthoc_tukey(data, val_col=metric, group_col='Chrono')
            post_hoc_matrix = post_hoc_matrix[order].reindex(order)

            fig, ax = plt.subplots(figsize=(5, 5), facecolor='#1B212C')
            ax.set_facecolor('#1B212C')
            ax.tick_params(axis='both', colors='white')
            sns.heatmap(post_hoc_matrix, annot=True, cmap='Blues_r', mask=np.triu(post_hoc_matrix), ax=ax, cbar=False)
            plt.yticks(rotation=0)
            plt.title('Résultats Post-hoc (p-value) - Test de Tukey', color='white')
            
            st.pyplot(fig)

            posthoc_res = pd.DataFrame(post_hoc_matrix.stack())
            posthoc_res = posthoc_res.rename(columns={0: 'Tukey (p-value)'})
            posthoc_res = round(posthoc_res, 3)
            posthoc_res['Tukey (p-value)'] = ['< 0.01*' if p==0 else f'{p}*' if p<.05 else str(p) for p in posthoc_res['Tukey (p-value)']]
            posthoc_res = posthoc_res[posthoc_res['Tukey (p-value)'].str.contains('*', regex=False)].copy()

            for idx in posthoc_res.index:
                posthoc_res.loc[idx, 'd de Cohen'] = cohen_d(data[metric][data['Chrono']==idx[0]],
                                                             data[metric][data['Chrono']==idx[1]])
            if posthoc_res.empty:
                st.write("Le test post-hoc n'a finalement pas trouvé de différence statistiquement significative.")
            else:
                st.dataframe(posthoc_res)
    else:
        kruskal_p = stats.kruskal(*anova_groups).pvalue
        if kruskal_p < 0.05:
            st.write(f"Kruksal-Wallis p-value: {round(kruskal_p, 3)}*")
            st.write('Au moins une période du match a des valeurs significativement différentes avec une autre période')
            #Post-hoc
            post_hoc_matrix = sp.posthoc_conover(data, val_col=metric, group_col='Chrono')
            post_hoc_matrix = post_hoc_matrix[order].reindex(order)

            fig, ax = plt.subplots(figsize=(5, 5), facecolor='#1B212C')
            ax.set_facecolor('#1B212C')
            ax.tick_params(axis='both', colors='white')
            sns.heatmap(post_hoc_matrix, annot=True, cmap='Blues_r', mask=np.triu(post_hoc_matrix), ax=ax, cbar=False)
            plt.yticks(rotation=0)
            plt.title('Résultats Post-hoc (p-value) - Test de Conover', color='white')

            st.pyplot(fig)

            posthoc_res = pd.DataFrame(post_hoc_matrix.stack())
            posthoc_res = posthoc_res.rename(columns={0: 'Conover (p-value)'})
            posthoc_res = round(posthoc_res, 3)
            posthoc_res['Conover (p-value)'] = ['< 0.01*' if p==0 else f'{p}*' if p<.05 else str(p) for p in posthoc_res['Conover (p-value)']]
            posthoc_res = posthoc_res[posthoc_res['Conover (p-value)'].str.contains('*', regex=False)].copy()
            
            for idx in posthoc_res.index:
                posthoc_res.loc[idx, 'd de Cohen'] = cohen_d(data[metric][data['Chrono']==idx[0]],
                                                             data[metric][data['Chrono']==idx[1]])
            if posthoc_res.empty:
                st.write("Le test post-hoc n'a finalement pas trouvé de différence statistiquement significative.")
            else:
                st.dataframe(posthoc_res)
        else:
            st.write(f"Kruksal-Wallis p-value: {round(kruskal_p, 3)}")
            st.write("Il n'y a pas de différence significative des valeurs entre les périodes du match")