# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 20:09:35 2017

@author: ruben
"""
import os
from functools import wraps

import pandas as pd

def persist_timeseries_to_file(filename_cache=None):
    """
    Persits a Pandas DataFrame object returned by a function into cache file
    using a decorator, so it decorates the function that returns the
    pd.DataFrame.

    The function receives some extra parameters to be used by the
    decorator (and to make it explicit it is advised to add them in the
    definition of the function even if they are not used in the non-cached
    version). This approach allows to modify them in each instance of the
    function:
    - enable_cache=False : actually enables the cache (allows to choose it)
    - path_cache=None : path where the cache file is saved. If None, it takes
                        the current path
    - update_cache=False : It forces to update the cache file, even if there
                            are data in it
    Also time : pd.DatetimeIndex that is the index of the pd.DataFrame should
    be the name of the parameter in the original function

    Parameters
    ----------
    filename_cache : String, default None
        Name of cache file

    Returns
    -------
    decorator : function
        Function that will persist data into cache file
    """
    if filename_cache is None:
        raise ValueError('A cache-file name is required.')

    persistence_type = filename_cache.split('.')[1]

    def decorator(original_func):
        """
        Decorator function
        """
        # The main intended use for @wraps() is to wrap the decorated function
        # and return the wrapper.
        # If the wrapper function is not updated, the metadata of the returned
        # function will reflect the wrapper definition rather than the original
        # function definition, which is typically less than helpful.
        @wraps(original_func)
        def new_func(time, enable_cache=False, path_cache=None, update_cache=False, **kwargs):
            """
            Decorated function
            """
            if not enable_cache:
                return original_func(time, **kwargs)

            if path_cache is None:
                path_cache = os.path.abspath('')
            if not os.path.exists(path_cache):
                os.makedirs(path_cache)

            path_file_cache = os.path.join(path_cache, filename_cache)
            print('Path cache:', path_file_cache)

            try:
                if persistence_type == 'csv':
                    cache = pd.read_csv(path_file_cache, index_col=0, parse_dates=True)
                elif persistence_type == 'pickle':
                    cache = pd.read_pickle(path_file_cache)
                elif persistence_type == 'json':
                    cache = pd.read_json(path_file_cache)
                else:
                    raise ValueError('Unknown type of persistence', persistence_type)

                print('> Reading cache...')

            except (IOError, ValueError):
                print('> Cache empty')
                cache = pd.DataFrame()
            
            if not update_cache:
                if time.isin(cache.index).all():
                    data = cache.loc[time]
                    print('> Cache with requested data')
    
                else:
                    print('Lee estacion')
                    data = original_func(time, **kwargs)
                    if not data.empty:
                        if persistence_type == 'csv':
                            pd.concat([data, cache], join='inner').to_csv(path_file_cache)
                        elif persistence_type == 'pickle':
                            pd.concat([data, cache], join='inner').to_pickle(path_file_cache)
                        elif persistence_type == 'json':
                            pd.concat([data, cache], join='inner').to_json(path_file_cache)
                        else:
                            raise ValueError('Unknown type of persistence', persistence_type)
                        
                        print('> Updating cache with requested data...')
                    else:
                        print('> Cache not updated because requested data is empty')
            else:
                data = original_func(time, **kwargs)
                if persistence_type == 'csv':
                    data.to_csv(path_file_cache)
                elif persistence_type == 'pickle':
                    data.to_pickle(path_file_cache)
                elif persistence_type == 'json':
                    data.to_json(path_file_cache)

                print('> Saving data in cache...')

            return data
        return new_func
    return decorator
