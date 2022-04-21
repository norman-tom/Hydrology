import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gauge_data_path = '../gauge_data/back_creek_wilmores_lane.csv'
gauge_data_raw = pd.read_csv(gauge_data_path)

def main():
    print('Begin processing...', end='\n\n')
    print(gauge_data_raw.head(), end='\n\n')        #Print a suummary
    df = gauge_data_raw.copy()                      #copy the dataframe to manipluate
    
    #Convert date time string into datatime object
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M')

    #get a set of the years that the gauge data covers
    unique_years = np.unique(df['timestamp'].dt.year)

    #for all of the years get the maximum and minimum values, the grade of the recording, and when it occured
    results = []
    for yr in unique_years:
        max = df.loc[df['timestamp'].dt.year == yr].max()
        max_year = max.timestamp.year
        max_value = max.value
        max_grade = max.grade
        results.append((max_year, max_value, max_grade))

    #convert to dataframe
    df_r = pd.DataFrame(results, columns=['year', 'flow', 'grade'])
    print(df_r)

    #Plot the data year vs value with grade code for checking
    df_r.plot.bar(x='year', y='flow')
    plt.show()

    #Output the data 
    to_flike = pd.DataFrame({
                                'Number': df_r.index,
                                'Value': df_r['flow'],
                                'Year': df_r['year']
                            })
    to_flike.to_csv('../flike/peak_data.csv', index=False)


if __name__ == "__main__":
    main()