import shapefile as sf
import pandas as pd
import os
import math
import numpy as np

def main():
    dirname = os.path.dirname(__file__)
    sentinal = "LINE_COLOUR"
    _12d_data = "./channel_xs.dat"
    gis_name = "skinners"

    headers = ["easting", "northing", "level", 'id']
    df = pd.read_csv(os.path.join(dirname, _12d_data), names=headers, sep="\s+", usecols=[0, 1, 2, 3], encoding="UTF-16")
    df = df[df["easting"] != sentinal]
    df['easting'] = df['easting'].astype(float)
    df['northing'] = df['northing'].astype(float)
    
    sections_names = df.id.unique()

    xs_read = sf.Reader(os.path.join(dirname, '1d_xs_empty_L'))
    xs_write = sf.Writer(os.path.join(dirname, '1d_xs_{}_L'.format(gis_name)))
    for field in xs_read.fields[1:]:
        xs_write.field(*field)

    for sn in sections_names:     
        df_temp = df[df["id"] == sn]
        df_temp["X"] = (((df_temp["easting"].iloc[0] - df_temp["easting"]) ** 2 + (df_temp["northing"].iloc[0] - df_temp["northing"]) ** 2).apply(math.sqrt))
        df_temp["Z"] = df_temp["level"]

        #create the shape file
        p1 = [df_temp.iloc[0].easting, df_temp.iloc[0].northing]
        p2 = [df_temp.iloc[-1].easting, df_temp.iloc[-1].northing]
        xs_write.line([[p1, p2]])
        xs_write.record(Source='../xs/xs_{}.csv'.format(df_temp.iloc[0].id), Type='xz')

        #create the csv files
        df_temp.to_csv(index=False, columns=["X", "Z"], path_or_buf=os.path.join(dirname, "out", "xs_{}.csv".format(df_temp.id.iloc[0])))
    
    xs_write.close()

if __name__ == "__main__":
    main() 