import polars as pl
import pandas as pd
from setup.create_codebook import create_dict_pd
from setup.create_codebook import create_dict_pl
 
## Pandas
csv_codebook_pd = pd.read_csv("./data/grad_app_codebook.csv")

nested_dict_pd = create_dict_pd(df = csv_codebook_pd,
                                col_name="column_name",
                                old_val_col="old_values",
                                new_val_col="new_labels")

data_pd = pd.read_csv("./data/grad_app_data.csv")

data_pd.replace(to_replace=nested_dict_pd)


## Polars
csv_codebook_pl = pl.read_csv("./data/grad_app_codebook.csv")
nested_dict_pl = create_dict_pl(df = csv_codebook_pl,
                                col_name="column_name",
                                old_val_col="old_values",
                                new_val_col="new_labels")

data_pl = pl.read_csv("./data/grad_app_data.csv")

# One way to apply the transformation across columns
(
    data_pl
            .with_columns(
                pl.col(col)
                    .replace(nested_dict_pl[col])
                        .alias(col)
                        for col in list(nested_dict_pl)
                    )
 )

# Another way to apply the transformation across columns
recode_expr_list = [ pl.col(col)
                        .replace(nested_dict_pl[col])
                        .alias(col)
                        for col in list(nested_dict_pl)
                    ]

data_pl.with_columns(recode_expr_list)


