    return render_template(
        'index.html' ,
        bar_chart_kildare=bar_chart_kildare_html,
        bar_chart_dublin=bar_chart_dublin_html,
        bar_chart_galway=bar_chart_galway_html,
        line_chart=line_chart,
        scatter_plot=scatter_plot
    )


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Plotly Charts</title>
</head>
<body>
    <h1>Charts</h1>

    <h2>Co.Kildare Bar Chart</h2>
    {{ bar_chart_kildare|safe }}
    
    <h2>Co.Dublin Bar Chart</h2>
    {{ bar_chart_dublin|safe }}
    
    <h2>Co.Galway Bar Chart</h2>
    {{ bar_chart_galway|safe }}
    
    <h2>Line Chart</h2>
    {{ line_chart|safe }}
    
    <h2>Scatter Plot</h2>
    {{ scatter_plot|safe }}
</body>
</html>
