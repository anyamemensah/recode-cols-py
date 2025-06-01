import polars as pl
import pandas as pd


def create_dict_pl(df:pl.DataFrame,
                   col_name:str = "column_name",
                   old_val_col:str = "values", 
                   new_val_col:str = "labels")->dict[str, dict[int|str, int|str]]:
    """
    Create a nested dictionary from a polars DataFrame

    This function creates a two-level nested dictionary from a polars DataFrame.
    The DataFrame should contain at least three columns: (1) one column that
    contains unique dataset variable names (col_name); (2) one column that contains
    old values to be recoded (old_val_col); and (3) one column that contains new
    values or labels to replace old values with.
    

    Args:
        df: a polars data frame.
        value_col: column name for old variable values.
        label_col: column name of new values/labels.

    
    Returns:
        A nested dictionary with dataset column names as outer keys and inner 
        dictionaries mapping old values to new labels.
    """
    # returned nested dictionary 
    return {
            row[col_name]: dict(zip(row[old_val_col], row[new_val_col]))
            for row in (df.group_by(col_name, maintain_order=True)
                            .agg(pl.col(old_val_col),
                                 pl.col(new_val_col))
                                 .iter_rows(named=True)
                        )
            }


def create_dict_pd(df:pd.DataFrame,
                   col_name:str = "column_name",
                   old_val_col:str = "values", 
                   new_val_col:str = "labels")->dict[str, dict[int|str, int|str]]:
    """
    Create a nested dictionary from a pandas DataFrame

    This function creates a two-level nested dictionary from a pandas DataFrame.
    The DataFrame should contain at least three columns: (1) one column that
    contains unique dataset variable names (col_name); (2) one column that contains
    old values to be recoded (old_val_col); and (3) one column that contains new
    values or labels to replace old values with.
    

    Args:
        df: a pandas data frame.
        value_col: column name for old variable values.
        label_col: column name of new values/labels.

    
    Returns:
        A nested dictionary with dataset column names as outer keys and inner 
        dictionaries mapping old values to new labels.
    """
    nested_dict = {}
    for var, col in df.groupby(col_name, sort=False):
         nested_dict[var] = dict(zip(col[old_val_col], col[new_val_col]))

    return nested_dict


