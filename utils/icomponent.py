import numpy as np
import pandas as pd
from typing import Union

# The class `IComponent` defines methods for getting daily return, compound annual growth rate (CAGR),
# and standard deviation.
class IComponent:
    def get_daily_return(self) -> Union[pd.Series, pd.DataFrame]:
        """
        This function is intended to calculate and return the daily return of a financial asset.
        """
        pass
    
    def get_cagr(self) -> Union[np.float64, np.ndarray]:
        """
        The function `get_cagr` calculates the compound annual growth rate (CAGR) and returns it as a
        NumPy float or array.
        """
        pass
    
    def get_std(self) -> Union[np.float64, np.ndarray]:
        """
        The function `get_std` returns either a single `np.float64` value or a `np.ndarray` in Python.
        """
        pass