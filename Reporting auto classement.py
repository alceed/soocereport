#!/usr/bin/env python
# coding: utf-8

# In[13]:


def generate_report(url, table_id,europa,europa2,relegated):
    # Import necessary libraries
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    from plottable import ColumnDefinition, Table
    from plottable.cmap import normed_cmap
    from plottable.plots import image

    # Read the HTML table from the given URL and table ID
    df = pd.read_html(url, attrs={"id": table_id})[0]


    # Select relevant columns for display
    df = df[['Rk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'Pts/MP',
             'xG', 'xGA', 'xGD']]
    matplotlib.use('TkAgg')
    # Define colors for background, text, and row highlights
    bg_colors = "#FFFFFF"
    text_colors = '#000000'
    row_colors = {
        "top4": "#E1FABC", "top6": "#FFFC97", "barrage": "#E1A356", "relegation": "#AF3434"
    }

    # Set global matplotlib text and font style
    plt.rcParams["text.color"] = text_colors
    plt.rcParams["font.family"] = "monospace"

    # Define the table columns and their display properties
    col_defs = [
    ColumnDefinition(
        name='Rk',
        textprops={"ha":"center"},
        width=0.5
    ),
     ColumnDefinition(
        name="Squad",
        textprops={"ha":"left", "weight":"bold"},
        width=1.5,   
    ),
      # Matches Played group columns
    ColumnDefinition(
        name="MP",
        group="Matches Played",
        textprops={"ha":"center"},
        width=0.5
    ),
     ColumnDefinition(
        name="W",
        group="Matches Played",
        textprops={"ha":"center"},
        width=0.5
    ),
     ColumnDefinition(
        name="D",
        group="Matches Played",
        textprops={"ha":"center"},
        width=0.5
    ),
    ColumnDefinition(
        name="L",
        group="Matches Played",
        textprops={"ha":"center"},
        width=0.5
    ),
    # Goals group columns
     ColumnDefinition(
        name="GF",
        group="Goals",
        textprops={"ha":"center"},
        width=0.5
    ),
     ColumnDefinition(
        name="GA",
        group="Goals",
        textprops={"ha":"center"},
        width=0.5
    ),
     ColumnDefinition(
        name="GD",
        group="Goals",
        textprops={"ha":"center"},
        width=0.5
    ),
    # Points group columns
    ColumnDefinition(
        name="Pts",
        group="points",
        textprops={"ha":"center"},
        width=0.5,
    ),
        ColumnDefinition(
        name="Pts/MP",
        group="points",
        textprops={"ha":"center"},
        width=0.5
    ),
   # Expected Goals group columns with color mapping
    
    ColumnDefinition(
            name="xG",
            group="expected goals",
            textprops={"ha":"center","color": text_colors, "weight":"bold", "bbox": {"boxstyle":"circle", "pad":.10}},
            cmap=normed_cmap(df["xG"], cmap=matplotlib.cm.PiYG, num_stds=2)
        ),
        ColumnDefinition(
            name="xGA",
            group="expected goals",
            textprops={"ha":"center","color": text_colors, "weight":"bold", "bbox": {"boxstyle":"circle", "pad":.10}},
            cmap=normed_cmap(df["xGA"], cmap=matplotlib.cm.PiYG_r, num_stds=2)  # Fixed: was using xG instead of xGA
        ),
        ColumnDefinition(
            name="xGD",
            group="expected goals",
            textprops={"ha":"center","color": text_colors, "weight":"bold", "bbox": {"boxstyle":"circle", "pad":.10}},
            cmap=normed_cmap(df["xGD"], cmap=matplotlib.cm.PiYG, num_stds=2)  # Fixed: was using xG instead of xGD
        )
    ]   

# Create matplotlib figure and axis with specified size and background color
    fig, ax = plt.subplots(figsize=(10, 12))
    fig.set_facecolor(bg_colors)
    ax.set_facecolor(bg_colors)
# Create the table visualization using plottable library
    table = Table(
    df,
    column_definitions=col_defs,
    index_col="Rk",
    row_dividers=True,
    row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
    footer_divider=True,
    textprops={"fontsize": 14},
    ax=ax
).autoset_fontcolors(colnames=["xG", "xGA", "xGD"]) # Auto set font colors for these columns


# Convert input strings of indices ("0,1,2") to lists of integers
    europa = list(map(int, europa.split(",")))
    europa2 = list(map(int, europa2.split(",")))
    relegated = list(map(int, relegated.split(",")))


# Apply conditional coloring on rows according to qualification/relegation
    for idx in europa:
        table.rows[idx].set_facecolor(row_colors["top4"])# Champions League teams
    for idx in europa2:
        table.rows[idx].set_facecolor(row_colors["top6"]) # Europa / Conference League teams
    for idx in relegated:
        table.rows[idx].set_facecolor(row_colors["relegation"])# Relegated teams
    # Display the final table plot
    plt.show()
