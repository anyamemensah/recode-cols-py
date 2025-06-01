# Recoding (Column) Values in Python


<!-- #region -->

Not too long ago, I wrote a post on renaming Pandas and Polars DataFrame
Columns. In this post, I will show you a quick and easy way to recode
variable (i.e., column) values in a DataFrame.

**Spoiler** Yes, it uses a “codebook”

Is R more your thing? Check out my post on [Recoding Variable Values in
R](https://www.anyamemensah.com/blog/recoding).

–

#### Value Recoding

Data recoding is a dreaded task, but the results are well worth the
effort. We often transform or modify data to make it usable for
analysis. This can involve changing data types, grouping/binning values,
or mapping old values to new ones. This post will focus on mapping old
values to new ones.

When recoding variable values, it is important to have at least three
pieces of information:

- Names of the variables to recode
- Original values/labels
- New values/labels

#### The Value of a Codebook

Most people use a programming language like Python to automate data
workflows. And having a trusty codebook can help streamline those
processes. A codebook acts as a map or rulebook for your data. It
removes (some) ambiguity, supports automation, and enables
collaboration, especially on large-scale projects with many moving
parts.

The value of a codebook lies in its ability to provide an accounting of
the variables in a dataset. Successful codebooks typically contain the
following information about each variable in the dataset:

- `Variable Name`: The name assigned to each variable
- `New Variable Name`: A new name you wish to assign to each variable
- `Variable Label`: A brief description outlining what the variable is
  measuring.
- `Level of Measurement`: How the variable was measured (e.g., nominal,
  ordinal, interval, ratio scale)
- `Variable Values`: List of the values a variable can take
- `Value Labels`: Descriptions for each unique variable value

While many people choose to automate codebook creation, I usually build
mine manually, at least in part. Doing it this way gives me more control
over what information is used during the data processing phase.

#### Setup

I generated a fake dataset for this post, loosely based on some data
about graduate applicants to a large university. The dataset contains
demographic and educational information about the applicants, as well as
information about the programs to which they applied.

The dataset has 5,000 rows and 14 columns: ![Image of the fake dataset
containing demographic and educational information about the applicants
and information about the programs they applied
to.](./images/grad_app_data.png)

I also created a codebook similar to one I would use in a typical data
cleaning workflow. The codebook has four columns:

- `column_name`: The name assigned to each variable in the dataset
- `column_description`: A description of the variable
- `old_values`: Values each variable can have
- `new_labels` : Descriptions for each unique variable value

One significant difference between this codebook and the codebooks I
typically use is that this codebook presents data in the long format. In
other words, there are multiple records for each column. For example,
the `school_decision` column in our dataset has three possible values
and therefore three entries in our codebook: ![Image of the code with
school_decision’s three rows
highligted.](./images/codebook_student_decision.png)

We will convert these codebook entries into a nested (i.e., two-level)
dictionary.

Recoding column values in a Pandas DataFrame The easiest way to recode
column values in a Pandas DataFrame is to use the
[`.replace`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html)
method. To replace values in select columns, we are going to take
advantage of the fact that you can pass a dictionary to
[`.replace`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html)’s
first argument, `to_replace`. Specifically, we want to pass a nested
dictionary to the `to_replace` argument, where column names from our
dataset serve as outer keys, and inner dictionaries give the mapping of
old values to new values. Remember, our codebook data is in the long
format, so before we can use the
[`.replace`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html)
method, we need to group values/labels by unique variables (i.e.,
`column_name`) and then return a nested dictionary.

First, import the codebook and dataset using the
[`.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
method: <!-- #endregion -->

``` python
import pandas as pd

# codebook
csv_codebook_pd = pd.read_csv("./data/grad_app_codebook.csv")

# dataset
data_pd = pd.read_csv("./data/grad_app_data.csv")
```

Then create the nested dictionary. One way to create the nested
dictionary we want is to use a regular for loop:

``` python
nested_dict_pd = {}
for var, col in csv_codebook_pd.groupby("column_name", sort=False):
     nested_dict_pd[var] = dict(zip(col["old_values"], col["new_labels"]))
```

Here’s a breakdown of what the code does:

1.  Starts with an empty dictionary.
2.  Creates a nested dictionary from a DataFrame by:
    - Looping through each group of rows that share the same value in
      the column `column_name` (which in this case is the variable name
      in our dataset).
      - `var` is the group key — a unique variable in our dataset.
      - `group` represents the set of rows (a subset of the original
        DataFrame) that match the `var` key.
      - For each group, it goes row by row, pairing values from the
        `old_values` column with values from the `new_labels` column to
        form key-value pairs in an inner dictionary.

The end result?

A two-level nested dictionary:

``` python
nested_dict_pd
```

    {'school_decision': {'A': 'Accepted', 'W': 'Waitlisted', 'R': 'Rejected'},
     'student_decision': {'A': 'Accepted Offer', 'D': 'Declined Offer'},
     'ft_pt': {'pt': 'Part-time', 'ft': 'Full-time', 'sub': 'Submatriculate'},
     'applied_dual_prg': {'NODUAL': 'No', 'YES': 'Yes'},
     'gender': {'W': 'Woman', 'M': 'Man', 'NB': 'Non-Binary'},
     'ethnicity': {'AN': 'Indigenous',
      'HL': 'Hispanic/Latino',
      'ME': 'Middle Eastern/Arab',
      'W': 'White',
      'B': 'Black /African American',
      'AP': 'Asian or Pacific Islander'},
     'low_income': {'N': 'No', 'Y': 'Yes'}}

To use the dictionary, set the `to_replace` argument in the replace
method to our dictionary `nested_dict_pd`. For those columns whose names
appear in both the dataset and as outer keys in the nested dictionary,
the column values in the dataset have been recoded.

``` python
data_pd.replace(to_replace=nested_dict_pd)
```

<div>

|  | applicant_id | email | email_preferred | school_decision | student_decision | ft_pt | gre_verbal | gre_quant | gre_analytical | applied_dual_prg | birth_date | gender | ethnicity | low_income |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 401 | karin.walborn@gmail.com | walborn_karin@Outlook.com | Accepted | Accepted Offer | Part-time | 151.0 | 161.0 | 3.0 | No | 3/22/95 | Woman | Indigenous | No |
| 1 | 386 | yareli.granados@yahoo.com | NaN | Accepted | Accepted Offer | Full-time | 164.0 | 161.0 | 3.5 | Yes | 4/12/89 | Man | Hispanic/Latino | No |
| 2 | 2905 | sulaimaan.al-demian@this.university.edu | al-demian_sulaimaan@Outlook.com | Waitlisted | NaN | Full-time | 152.0 | 137.0 | 5.0 | No | 1/10/91 | Woman | Middle Eastern/Arab | No |
| 3 | 3043 | ryan.burt@this.university.edu | burt_ryan@Outlook.com | Accepted | Declined Offer | Part-time | 135.0 | 134.0 | 5.0 | Yes | 12/1/98 | Non-Binary | White | Yes |
| 4 | 1546 | ryan.villalobos@Outlook.com | villalobos_ryan@Outlook.com | Waitlisted | NaN | Full-time | 154.0 | 164.0 | 3.0 | No | 11/3/89 | Man | Hispanic/Latino | No |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 4995 | 2130 | schyeler.martzloff@this.university.edu | NaN | Accepted | Accepted Offer | Submatriculate | 153.0 | 169.0 | 4.0 | No | 5/24/90 | Man | Indigenous | No |
| 4996 | 4894 | kasey.schwarz@gmail.com | schwarz_kasey@this.university.edu | Accepted | Accepted Offer | Submatriculate | 130.0 | 134.0 | 6.0 | No | 12/23/98 | Woman | White | No |
| 4997 | 4592 | jerrod.apple@gmail.com | apple_jerrod@this.university.edu | Accepted | Accepted Offer | Full-time | 150.0 | NaN | 3.0 | No | 9/11/92 | Man | White | No |
| 4998 | 2684 | natasha.fossum@Outlook.com | NaN | Accepted | Accepted Offer | Full-time | 135.0 | 170.0 | 5.0 | No | 11/24/86 | Non-Binary | White | Yes |
| 4999 | 1345 | jaimin.lott@this.university.edu | lott_jaimin@gmail.com | Rejected | NaN | Submatriculate | 136.0 | 166.0 | 5.0 | Yes | 11/3/86 | Woman | Indigenous | No |

<p>5000 rows × 14 columns</p>
</div>

If this is a process you envision using across various workflows,
consider wrapping it in a function:

``` python
def create_dict_pd(df:pd.DataFrame,
                   col_name:str = "column_name",
                   old_val_col:str = "values", 
                   new_val_col:str = "labels"
                   )->dict[str, dict[int|str, int|str]]:
    
    nested_dict = {}
    for var, col in df.groupby(col_name, sort=False):
        nested_dict[var] = dict(zip(col[old_val_col], col[new_val_col]))

    return nested_dict
```

Then build the nested dictionary:

``` python
nested_dict_pd = create_dict_pd(df = csv_codebook_pd,
                                col_name="column_name",
                                old_val_col="old_values",
                                new_val_col="new_labels")
```

And finally, use the dictionary:

``` python
data_pd.replace(to_replace= nested_dict_pd)
```

<div>

|  | applicant_id | email | email_preferred | school_decision | student_decision | ft_pt | gre_verbal | gre_quant | gre_analytical | applied_dual_prg | birth_date | gender | ethnicity | low_income |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 401 | karin.walborn@gmail.com | walborn_karin@Outlook.com | Accepted | Accepted Offer | Part-time | 151.0 | 161.0 | 3.0 | No | 3/22/95 | Woman | Indigenous | No |
| 1 | 386 | yareli.granados@yahoo.com | NaN | Accepted | Accepted Offer | Full-time | 164.0 | 161.0 | 3.5 | Yes | 4/12/89 | Man | Hispanic/Latino | No |
| 2 | 2905 | sulaimaan.al-demian@this.university.edu | al-demian_sulaimaan@Outlook.com | Waitlisted | NaN | Full-time | 152.0 | 137.0 | 5.0 | No | 1/10/91 | Woman | Middle Eastern/Arab | No |
| 3 | 3043 | ryan.burt@this.university.edu | burt_ryan@Outlook.com | Accepted | Declined Offer | Part-time | 135.0 | 134.0 | 5.0 | Yes | 12/1/98 | Non-Binary | White | Yes |
| 4 | 1546 | ryan.villalobos@Outlook.com | villalobos_ryan@Outlook.com | Waitlisted | NaN | Full-time | 154.0 | 164.0 | 3.0 | No | 11/3/89 | Man | Hispanic/Latino | No |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 4995 | 2130 | schyeler.martzloff@this.university.edu | NaN | Accepted | Accepted Offer | Submatriculate | 153.0 | 169.0 | 4.0 | No | 5/24/90 | Man | Indigenous | No |
| 4996 | 4894 | kasey.schwarz@gmail.com | schwarz_kasey@this.university.edu | Accepted | Accepted Offer | Submatriculate | 130.0 | 134.0 | 6.0 | No | 12/23/98 | Woman | White | No |
| 4997 | 4592 | jerrod.apple@gmail.com | apple_jerrod@this.university.edu | Accepted | Accepted Offer | Full-time | 150.0 | NaN | 3.0 | No | 9/11/92 | Man | White | No |
| 4998 | 2684 | natasha.fossum@Outlook.com | NaN | Accepted | Accepted Offer | Full-time | 135.0 | 170.0 | 5.0 | No | 11/24/86 | Non-Binary | White | Yes |
| 4999 | 1345 | jaimin.lott@this.university.edu | lott_jaimin@gmail.com | Rejected | NaN | Submatriculate | 136.0 | 166.0 | 5.0 | Yes | 11/3/86 | Woman | Indigenous | No |

<p>5000 rows × 14 columns</p>
</div>

#### Recoding column values in a Polars DataFrame

Much like when using Pandas, the easiest way to recode column values in
a Polars DataFrame is to use the
[`.replace`](https://docs.pola.rs/api/python/dev/reference/expressions/api/polars.Expr.replace.html)
method.

First, import the codebook and dataset using the
[`.read_csv`](https://docs.pola.rs/api/python/dev/reference/api/polars.read_csv.html)
method:

``` python
import polars as pl

# codebook
csv_codebook_pl = pl.read_csv("./data/grad_app_codebook.csv")

# dataset
data_pl = pl.read_csv("./data/grad_app_data.csv")
```

Next, we need to create the nested dictionary. Here’s sample code you
can use to convert the codebook (as a Polars DataFrame) into a two-level
nested dictionary:

``` python
nested_dict_pl = {
    row["column_name"]: dict(zip(row["old_values"], row["new_labels"]))
    for row in (csv_codebook_pl.group_by("column_name", maintain_order=True)
                    .agg(pl.col("old_values"),pl.col("new_labels"))
                    .iter_rows(named=True)
                )
        }
```

Let’s rewrite the code in two parts so you can see what’s happening
underneath the hood:

In this first part, we are creating a grouped Polars DataFrame. Then,
with that grouped DataFrame, we are aggregating the data in the
`old_values` and `new_labels` columns into lists.

``` python
csv_cb_pl = (
        csv_codebook_pl
            .group_by("column_name", maintain_order=True)
            .agg(
                pl.col("old_values"), 
                pl.col("new_labels")
                )
        )

csv_cb_pl
```

<div>
<small>shape: (7, 3)</small>

| column_name | old_values | new_labels |
|----|----|----|
| str | list\[str\] | list\[str\] |
| "school_decision" | \["A", "W", "R"\] | \["Accepted", "Waitlisted", "Rejected"\] |
| "student_decision" | \["A", "D"\] | \["Accepted Offer", "Declined Offer"\] |
| "ft_pt" | \["pt", "ft", "sub"\] | \["Part-time", "Full-time", "Submatriculate"\] |
| "applied_dual_prg" | \["NODUAL", "YES"\] | \["No", "Yes"\] |
| "gender" | \["W", "M", "NB"\] | \["Woman", "Man", "Non-Binary"\] |
| "ethnicity" | \["AN", "HL", … "AP"\] | \["Indigenous", "Hispanic/Latino", … "Asian or Pacific Islander"\] |
| "low_income" | \["N", "Y"\] | \["No", "Yes"\] |

</div>

However, we’re not done yet; we need to convert this DataFrame into a
nested dictionary, where the values under `column_name` will become our
outer keys, and the latter two DataFrame columns will become our inner
keys and values, respectively.

One way you can approach it is to use a dict(ionary) comprehension:

``` python
nested_dict_pl = {
                row["column_name"]: dict(zip(row["old_values"], row["new_labels"]))
                for row in csv_cb_pl.iter_rows(named=True)
                }
```

A dict comprehension needs two things to work:

1.  Two expressions separated by a colon
2.  “for” and “if” clauses

In our code:

1.  The two expressions separated by a colon are our key-value pairs.
2.  The for loop is right beneath it.

If you take a closer look, however, you’ll notice that:

- The outer keys in our nested dictionary are represented by the
  expression to the left of the colon: `row["column_name"]`.
- The inner dictionaries are populated by the expression to the right of
  the colon `dict(zip(row["old_values"], row["new_labels"]))`.
- The for-loop loops through each row in our transformed Polars
  DataFrame, returning an iterator of dictionaries of row values.
  Importantly, we can access values in these dictionaries by column
  name.

Now, if you’re not comfortable with comprehensions or if the logic you
are using to populate the dictionary is more complex, feel free to
convert the comprehension into a more expressive for loop:

``` python
nested_dict_pl={}
for row in csv_cb_pl.iter_rows(named=True):
     nested_dict_pl[row["column_name"]] = dict(zip(row["old_values"], row["new_labels"]))
```

You might even consider using a dict comprehension, but instead of
returning an iterator of dictionaries, return tuples, whose elements you
access via index. (Granted, this option requires knowing each element’s
exact position.)

``` python
nested_dict_pl = {
                row[0]: dict(zip(row[1], row[2]))
                for row in csv_cb_pl.iter_rows()
                }
```

Whatever option you use, the result should be the same: A two-level
nested dictionary.

``` python
nested_dict_pl
```

    {'school_decision': {'A': 'Accepted', 'W': 'Waitlisted', 'R': 'Rejected'},
     'student_decision': {'A': 'Accepted Offer', 'D': 'Declined Offer'},
     'ft_pt': {'pt': 'Part-time', 'ft': 'Full-time', 'sub': 'Submatriculate'},
     'applied_dual_prg': {'NODUAL': 'No', 'YES': 'Yes'},
     'gender': {'W': 'Woman', 'M': 'Man', 'NB': 'Non-Binary'},
     'ethnicity': {'AN': 'Indigenous',
      'HL': 'Hispanic/Latino',
      'ME': 'Middle Eastern/Arab',
      'W': 'White',
      'B': 'Black /African American',
      'AP': 'Asian or Pacific Islander'},
     'low_income': {'N': 'No', 'Y': 'Yes'}}

Here’s one way you can use the dictionary:

Say you wanted to recode the values we have for the `school_decision`
column. Here’s one way you could approach it:

``` python
(
    data_pl
        .with_columns(
            pl.col("school_decision")
                .replace(nested_dict_pl["school_decision"])
                .alias("school_decision")
                )
)
```

<div>
<small>shape: (5_000, 14)</small>

| applicant_id | email | email_preferred | school_decision | student_decision | ft_pt | gre_verbal | gre_quant | gre_analytical | applied_dual_prg | birth_date | gender | ethnicity | low_income |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| i64 | str | str | str | str | str | i64 | i64 | f64 | str | str | str | str | str |
| 401 | "karin.walborn@gmail.com" | "walborn_karin@Outlook.com" | "Accepted" | "A" | "pt" | 151 | 161 | 3.0 | "NODUAL" | "3/22/95" | "W" | "AN" | "N" |
| 386 | "yareli.granados@yahoo.com" | null | "Accepted" | "A" | "ft" | 164 | 161 | 3.5 | "YES" | "4/12/89" | "M" | "HL" | "N" |
| 2905 | "sulaimaan.al-demian@this.unive… | "al-demian_sulaimaan@Outlook.co… | "Waitlisted" | null | "ft" | 152 | 137 | 5.0 | "NODUAL" | "1/10/91" | "W" | "ME" | "N" |
| 3043 | "ryan.burt@this.university.edu" | "burt_ryan@Outlook.com" | "Accepted" | "D" | "pt" | 135 | 134 | 5.0 | "YES" | "12/1/98" | "NB" | "W" | "Y" |
| 1546 | "ryan.villalobos@Outlook.com" | "villalobos_ryan@Outlook.com" | "Waitlisted" | null | "ft" | 154 | 164 | 3.0 | "NODUAL" | "11/3/89" | "M" | "HL" | "N" |
| … | … | … | … | … | … | … | … | … | … | … | … | … | … |
| 2130 | "schyeler.martzloff@this.univer… | null | "Accepted" | "A" | "sub" | 153 | 169 | 4.0 | "NODUAL" | "5/24/90" | "M" | "AN" | "N" |
| 4894 | "kasey.schwarz@gmail.com" | "schwarz_kasey@this.university.… | "Accepted" | "A" | "sub" | 130 | 134 | 6.0 | "NODUAL" | "12/23/98" | "W" | "W" | "N" |
| 4592 | "jerrod.apple@gmail.com" | "apple_jerrod@this.university.e… | "Accepted" | "A" | "ft" | 150 | null | 3.0 | "NODUAL" | "9/11/92" | "M" | "W" | "N" |
| 2684 | "natasha.fossum@Outlook.com" | null | "Accepted" | "A" | "ft" | 135 | 170 | 5.0 | "NODUAL" | "11/24/86" | "NB" | "W" | "Y" |
| 1345 | "jaimin.lott@this.university.ed… | "lott_jaimin@gmail.com" | "Rejected" | null | "sub" | 136 | 166 | 5.0 | "YES" | "11/3/86" | "W" | "AN" | "N" |

</div>

Great, only five more columns to go…

Kidding. No one has the time to sit and write all of that out. When you
apply the same transformation to multiple columns, I recommend looping
over the column names within the
[`.with_columns`](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.with_columns.html)
method like so:

``` python
(
     data_pl
        .with_columns(
            pl.col(col)
                .replace(nested_dict_pl[col])
                .alias(col)
        for col in list(nested_dict_pl)
                )
    )
```

<div>
<small>shape: (5_000, 14)</small>

| applicant_id | email | email_preferred | school_decision | student_decision | ft_pt | gre_verbal | gre_quant | gre_analytical | applied_dual_prg | birth_date | gender | ethnicity | low_income |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| i64 | str | str | str | str | str | i64 | i64 | f64 | str | str | str | str | str |
| 401 | "karin.walborn@gmail.com" | "walborn_karin@Outlook.com" | "Accepted" | "Accepted Offer" | "Part-time" | 151 | 161 | 3.0 | "No" | "3/22/95" | "Woman" | "Indigenous" | "No" |
| 386 | "yareli.granados@yahoo.com" | null | "Accepted" | "Accepted Offer" | "Full-time" | 164 | 161 | 3.5 | "Yes" | "4/12/89" | "Man" | "Hispanic/Latino" | "No" |
| 2905 | "sulaimaan.al-demian@this.unive… | "al-demian_sulaimaan@Outlook.co… | "Waitlisted" | null | "Full-time" | 152 | 137 | 5.0 | "No" | "1/10/91" | "Woman" | "Middle Eastern/Arab" | "No" |
| 3043 | "ryan.burt@this.university.edu" | "burt_ryan@Outlook.com" | "Accepted" | "Declined Offer" | "Part-time" | 135 | 134 | 5.0 | "Yes" | "12/1/98" | "Non-Binary" | "White" | "Yes" |
| 1546 | "ryan.villalobos@Outlook.com" | "villalobos_ryan@Outlook.com" | "Waitlisted" | null | "Full-time" | 154 | 164 | 3.0 | "No" | "11/3/89" | "Man" | "Hispanic/Latino" | "No" |
| … | … | … | … | … | … | … | … | … | … | … | … | … | … |
| 2130 | "schyeler.martzloff@this.univer… | null | "Accepted" | "Accepted Offer" | "Submatriculate" | 153 | 169 | 4.0 | "No" | "5/24/90" | "Man" | "Indigenous" | "No" |
| 4894 | "kasey.schwarz@gmail.com" | "schwarz_kasey@this.university.… | "Accepted" | "Accepted Offer" | "Submatriculate" | 130 | 134 | 6.0 | "No" | "12/23/98" | "Woman" | "White" | "No" |
| 4592 | "jerrod.apple@gmail.com" | "apple_jerrod@this.university.e… | "Accepted" | "Accepted Offer" | "Full-time" | 150 | null | 3.0 | "No" | "9/11/92" | "Man" | "White" | "No" |
| 2684 | "natasha.fossum@Outlook.com" | null | "Accepted" | "Accepted Offer" | "Full-time" | 135 | 170 | 5.0 | "No" | "11/24/86" | "Non-Binary" | "White" | "Yes" |
| 1345 | "jaimin.lott@this.university.ed… | "lott_jaimin@gmail.com" | "Rejected" | null | "Submatriculate" | 136 | 166 | 5.0 | "Yes" | "11/3/86" | "Woman" | "Indigenous" | "No" |

</div>

Note, we are using `list(nested_dict_pl)` to return a list of the
(outer) keys of our nested dictionary. These are the only columns to
which we want to apply this transformation.

Now, if you want to keep things a little neater, you may consider
building lists of expressions:

``` python
recode_expr_list = [ pl.col(col)
                        .replace(nested_dict_pl[col])
                        .alias(col)
                    for col in list(nested_dict_pl)
                    ]
```

Then pass the expressions to the
[`.with_columns`](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.with_columns.html)
method:

``` python
data_pl.with_columns(recode_expr_list)
```

<div>
<small>shape: (5_000, 14)</small>

| applicant_id | email | email_preferred | school_decision | student_decision | ft_pt | gre_verbal | gre_quant | gre_analytical | applied_dual_prg | birth_date | gender | ethnicity | low_income |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| i64 | str | str | str | str | str | i64 | i64 | f64 | str | str | str | str | str |
| 401 | "karin.walborn@gmail.com" | "walborn_karin@Outlook.com" | "Accepted" | "Accepted Offer" | "Part-time" | 151 | 161 | 3.0 | "No" | "3/22/95" | "Woman" | "Indigenous" | "No" |
| 386 | "yareli.granados@yahoo.com" | null | "Accepted" | "Accepted Offer" | "Full-time" | 164 | 161 | 3.5 | "Yes" | "4/12/89" | "Man" | "Hispanic/Latino" | "No" |
| 2905 | "sulaimaan.al-demian@this.unive… | "al-demian_sulaimaan@Outlook.co… | "Waitlisted" | null | "Full-time" | 152 | 137 | 5.0 | "No" | "1/10/91" | "Woman" | "Middle Eastern/Arab" | "No" |
| 3043 | "ryan.burt@this.university.edu" | "burt_ryan@Outlook.com" | "Accepted" | "Declined Offer" | "Part-time" | 135 | 134 | 5.0 | "Yes" | "12/1/98" | "Non-Binary" | "White" | "Yes" |
| 1546 | "ryan.villalobos@Outlook.com" | "villalobos_ryan@Outlook.com" | "Waitlisted" | null | "Full-time" | 154 | 164 | 3.0 | "No" | "11/3/89" | "Man" | "Hispanic/Latino" | "No" |
| … | … | … | … | … | … | … | … | … | … | … | … | … | … |
| 2130 | "schyeler.martzloff@this.univer… | null | "Accepted" | "Accepted Offer" | "Submatriculate" | 153 | 169 | 4.0 | "No" | "5/24/90" | "Man" | "Indigenous" | "No" |
| 4894 | "kasey.schwarz@gmail.com" | "schwarz_kasey@this.university.… | "Accepted" | "Accepted Offer" | "Submatriculate" | 130 | 134 | 6.0 | "No" | "12/23/98" | "Woman" | "White" | "No" |
| 4592 | "jerrod.apple@gmail.com" | "apple_jerrod@this.university.e… | "Accepted" | "Accepted Offer" | "Full-time" | 150 | null | 3.0 | "No" | "9/11/92" | "Man" | "White" | "No" |
| 2684 | "natasha.fossum@Outlook.com" | null | "Accepted" | "Accepted Offer" | "Full-time" | 135 | 170 | 5.0 | "No" | "11/24/86" | "Non-Binary" | "White" | "Yes" |
| 1345 | "jaimin.lott@this.university.ed… | "lott_jaimin@gmail.com" | "Rejected" | null | "Submatriculate" | 136 | 166 | 5.0 | "Yes" | "11/3/86" | "Woman" | "Indigenous" | "No" |

</div>

Again, if this is a process you envision using across various workflows,
consider wrapping it in a function:

``` python
def create_dict_pl(df:pl.DataFrame,
                       col_name:str = "column_name",
                       old_val_col:str = "values", 
                       new_val_col:str = "labels")->dict[str, dict[int|str, int|str]]:
    return {
                row[col_name]: dict(zip(row[old_val_col], row[new_val_col]))
                for row in (df.group_by(col_name, maintain_order=True)
                                .agg(pl.col(old_val_col),
                                     pl.col(new_val_col))
                                     .iter_rows(named=True)
                            )
            }
```

Then build the nested dictionary:

``` python
nested_dict_pl = create_dict_pl(df = csv_codebook_pl,
                                col_name="column_name",
                                old_val_col="old_values",
                                new_val_col="new_labels")
```

And finally, use the dictionary:

``` python
recode_expr_list = [ pl.col(col)
                        .replace(nested_dict_pl[col])
                        .alias(col)
                    for col in list(nested_dict_pl)
                    ]

data_pl.with_columns(recode_expr_list)
```

<div>
<small>shape: (5_000, 14)</small>

| applicant_id | email | email_preferred | school_decision | student_decision | ft_pt | gre_verbal | gre_quant | gre_analytical | applied_dual_prg | birth_date | gender | ethnicity | low_income |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| i64 | str | str | str | str | str | i64 | i64 | f64 | str | str | str | str | str |
| 401 | "karin.walborn@gmail.com" | "walborn_karin@Outlook.com" | "Accepted" | "Accepted Offer" | "Part-time" | 151 | 161 | 3.0 | "No" | "3/22/95" | "Woman" | "Indigenous" | "No" |
| 386 | "yareli.granados@yahoo.com" | null | "Accepted" | "Accepted Offer" | "Full-time" | 164 | 161 | 3.5 | "Yes" | "4/12/89" | "Man" | "Hispanic/Latino" | "No" |
| 2905 | "sulaimaan.al-demian@this.unive… | "al-demian_sulaimaan@Outlook.co… | "Waitlisted" | null | "Full-time" | 152 | 137 | 5.0 | "No" | "1/10/91" | "Woman" | "Middle Eastern/Arab" | "No" |
| 3043 | "ryan.burt@this.university.edu" | "burt_ryan@Outlook.com" | "Accepted" | "Declined Offer" | "Part-time" | 135 | 134 | 5.0 | "Yes" | "12/1/98" | "Non-Binary" | "White" | "Yes" |
| 1546 | "ryan.villalobos@Outlook.com" | "villalobos_ryan@Outlook.com" | "Waitlisted" | null | "Full-time" | 154 | 164 | 3.0 | "No" | "11/3/89" | "Man" | "Hispanic/Latino" | "No" |
| … | … | … | … | … | … | … | … | … | … | … | … | … | … |
| 2130 | "schyeler.martzloff@this.univer… | null | "Accepted" | "Accepted Offer" | "Submatriculate" | 153 | 169 | 4.0 | "No" | "5/24/90" | "Man" | "Indigenous" | "No" |
| 4894 | "kasey.schwarz@gmail.com" | "schwarz_kasey@this.university.… | "Accepted" | "Accepted Offer" | "Submatriculate" | 130 | 134 | 6.0 | "No" | "12/23/98" | "Woman" | "White" | "No" |
| 4592 | "jerrod.apple@gmail.com" | "apple_jerrod@this.university.e… | "Accepted" | "Accepted Offer" | "Full-time" | 150 | null | 3.0 | "No" | "9/11/92" | "Man" | "White" | "No" |
| 2684 | "natasha.fossum@Outlook.com" | null | "Accepted" | "Accepted Offer" | "Full-time" | 135 | 170 | 5.0 | "No" | "11/24/86" | "Non-Binary" | "White" | "Yes" |
| 1345 | "jaimin.lott@this.university.ed… | "lott_jaimin@gmail.com" | "Rejected" | null | "Submatriculate" | 136 | 166 | 5.0 | "Yes" | "11/3/86" | "Woman" | "Indigenous" | "No" |

</div>

<!-- #region -->

See, a codebook can make a world of difference when developing and
implementing a data workflow.

What is your favorite method for recoding variable values in Python?
Share your code in the comments below.

Need help thinking through the design and development of a data
pipeline? At Analytics Made Accessible, we can help you turn messy data
into streamlined systems and stories that stick—[get in touch
today](https://www.anyamemensah.com/blog/renaming)! <!-- #endregion -->
