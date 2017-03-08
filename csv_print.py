"""
Generate HTML reports from CSV data.
"""
import glob
import pandas as pd
import time
from jinja2 import Environment, FileSystemLoader

start_time = time.time()


def create_dataframe(path):
    """ Creates a master dataframe from multiple csv files.
    Reads and compiles all CSV data from the specified path. Columns must be identical.
    :param path: string of the path where csv files will reside.
    :return: pandas dataframe with all data.
    """

    all_files = glob.glob(path + '*.CSV')
    df = pd.concat((pd.read_csv(f, sep=';') for f in all_files))
    return df


def print_df_to_html(dataframe):
    """Create templated html output file from dataframe.
    :param html_output_object: Rendered pandas dataframe to html from jinja2.
    :return: none
    """

    df_to_html = dataframe.to_html()
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("report.html")
    template_vars = {"title": "Microtunnel Drive Data", "drive_data": (df_to_html)}
    html_out = template.render(template_vars)

    file_name = 'dataframe.html' # need to figure out how to automatically name files
    f = open(file_name, 'w')
    f.write(html_out)
    f.close()

if __name__ == "__main__":

    starting_station = 5383  # Starting station of the tunnel STA = 53+83.
    ending_station = 6081 # Ending station of tunnel STA = 60+81

    df = create_dataframe('../csv-print/csv_data/')
    df_length = len(df)
    df = df.sort_values('Distance', ascending=True)

    # parse the Date to convert to standard datetime
    # and convert distance to feet and stationing

    df['Date'] = pd.to_datetime(df['Date'], format = ' %d:%m:%y')
    df['Dist_ft'] = df.Distance * 3.28
    df['Station'] = df.Dist_ft + starting_station

    # Document

    df_time_station = df[['Date', 'Time', 'Dist_ft', 'Station', 'Gradient', 'F Jacks', 'Pres Jacks']]
    df_time_station = df_time_station.round({'Dist_ft': 1, 'Station': 1})   # Round distance variables
    df_time_station = df_time_station.drop_duplicates(subset=['Dist_ft'])   # Culls duplicate data based on distance
    df_time_station = df_time_station.reset_index(drop=True)

    # Debug only
    #print df_time_station
    #print df_temp
    #print df

    # Convert Data Frame to HTML template and render
    # send HTML out to write file method

    # df_to_html = df_time_station.to_html()
    # env = Environment(loader=FileSystemLoader('.'))
    # template = env.get_template("report.html")
    # template_vars = {"title": "Microtunnel Drive Data", "drive_data": (df_to_html) }
    # html_out = template.render(template_vars)
    # print_to_html(html_out)

    # Document performance of the script and data processing
    print 'It took', round(time.time()-start_time, 2), 'seconds to run the scipt.'
    print 'The script processed', df_length, 'rows of CSV data.'
    print 'That\'s', df_length*22, 'variables!'

    # Group data by date and distance.
    df_min = df_time_station['Dist_ft'].groupby(df_time_station['Date']).min()
    df_max = df_time_station['Dist_ft'].groupby(df_time_station['Date']).max()
    df_combined = pd.concat([df_min, df_max], axis=1).reset_index()
    print_df_to_html(df_combined)



