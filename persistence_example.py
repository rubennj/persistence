# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 18:19:57 2016

@author: Ruben
"""
import pandas as pd

from persistence import persist_timeseries_to_file

ENABLE_CACHE = True
PATH_CACHE = r'C:\Users\ruben\Desktop\buffer_lectura_python'
UPDATE_CACHE = False

# accepts 'csv', 'pickle' and 'json'
@persist_timeseries_to_file(file_name_cache='example_cache.json')
def test_func(time, enable_cache=True, path_cache=None, update_cache=False):
    """
    Test function of decorator persist_timeseries_to_file()

    Parameters
    ----------
    time : pd.DatetimeIndex
        Timeseries index

    [From decorator 'persist_timeseries_to_file', to activate the cache]
    enable_cache : boolean, default False
        actually enables the cache (allows to choose it)
    path_cache : string, default None
        path where the cache file is saved. If None, it takes the current path
    update_cache : boolean, default False
        It forces to update the cache file, even if there are data in it

    Returns
    -------
    df : pd.DataFrame
        Timeseries dataframe with the corresponding data
    """
    return pd.get_dummies(time).T

test_func(time=pd.date_range(start='2016-12-01', periods=5),
          enable_cache=ENABLE_CACHE, update_cache=UPDATE_CACHE)

test_func(time=pd.date_range(start='2016-12-01', periods=3))

test_func(time=pd.date_range(start='2016-12-01', periods=2),
          enable_cache=ENABLE_CACHE, path_cache=PATH_CACHE)

