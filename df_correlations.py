
# coding: utf-8

# In[57]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
from scipy import stats as ss


# In[59]:


def cramers(x,y):
    """
    Function to calculate Cramers Correlation
    
    Input: column_1, column_2
    Output: correlation r (float)
    """
    confusion_matrix = pd.crosstab(x,y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    rcorr = r-((r-1)**2)/(n-1)
    kcorr = k-((k-1)**2)/(n-1)
    corr = np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))
        
    return corr


# In[60]:


def correlation(x, y, method='pearson'): #option for type of correlation added 
    
    """
    Function to calculate correlation in given method
    
    Input: column_1, column_2, method = ['pearson','spearman','kendall','cramers']
    Output: correlation r (float)
    """
    try:
        if (method == 'pearson'): 
            corr, _ = ss.pearsonr(x,y)
        elif (method == 'spearman'): 
            corr, _ = ss.spearmanr(x,y)
        elif (method == 'kendall'): 
            corr, _ = ss.kendalltau(x,y)
        elif (method == 'cramers'): 
            corr = cramers(x,y)
    except:
        corr = cramers(x,y)
        
    return corr


# In[67]:


def make_corr_dict(df, method='pearson'):
    
    """
    Function to make dictionaries of all column combinations and correlations
    
    Input: dataframe, method = ['pearson','spearman','kendall','cramers']
    Output: (correlation dictionary : singles, correlation dictionary : mirrored), Prints (Unused columns number and names)
    """
    
    variables = dict(df.dtypes)
    for_corr = df[list(col for col in df.columns if (len(set(df[col]))!=len(df[col])) & df[col].notna().any())].copy()
    for_corr.fillna(0, inplace = True)
    col_combinations = list(itertools.combinations(for_corr.columns,2))
    corr_dict = dict(((x,y),correlation(for_corr[x],for_corr[y], method)) for x,y in col_combinations)
    mirrors = dict(((b,a),(c)) for ((a,b),(c)) in corr_dict.items())
    corr_dict_mirror = corr_dict.copy()
    corr_dict_mirror.update(mirrors)
    
    print("Used Columns : ", len(for_corr.columns))
    print("Unused Columns : ", len(df.columns)-len(for_corr.columns), "\nUnused Col Names: ", np.setdiff1d(df.columns,for_corr.columns))
    
    return(corr_dict, corr_dict_mirror)


# In[62]:


def corr_table(corr_dict_mirror):
    
    """
    Function to visualize all correlations
    
    Input: mirrored dictionary of correlations
    Output: Prints (heatmap)
    """
    
    corr_table = pd.DataFrame(corr_dict_mirror, index=[0]).T.reset_index(level=[0,1]).pivot(index='level_0', columns='level_1')
    corr_table.columns = corr_table.columns.droplevel(0)

    plt.figure(figsize=(10,10))
    sns.heatmap(corr_table)


# In[63]:


def significance(corr_dict, min_value, max_value):   
    
    """
    Function to print all significant correlations between columns
    
    Input: Dictionary of Correlations: Singles, minimum value of correlational significance, maximum value of correlational significance
    Output: List of all significant column combinations
    """
    
    large_corr = pd.DataFrame(range(0,len(corr_dict)),corr_dict).reset_index(level=[0,1])
    large_corr = large_corr[(large_corr[0]>max_value)| (large_corr[0]<min_value)]
    print(large_corr.to_string(), "\n\n")

