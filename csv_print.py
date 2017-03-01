"""
Generate HTML reports from CSV data.
"""

import pandas as pd
from jinja2 import Environment, FileSystemLoader

if __name__ == "__main__":

    # Read CSV File
    df = pd.read_csv('csvdata.csv', sep=';')

    #Parse the Date to convert to standard datetime
    df['Date'] = pd.to_datetime(df['Date'], format = ' %d:%m:%y')
    print df[['Date', 'Time', 'Distance']]
    # Convert Data Frame to HTML
    df_to_html = df.to_html()

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("report.html")
    template_vars = {"title": "Microtunnel Drive Data", "drive_data": (df_to_html) }

    html_out = template.render(template_vars)

    # Output as html file.

    f = open('html_out.html', 'w')
    f.write(html_out)
    f.close()