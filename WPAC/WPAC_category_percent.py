## This script reads in data from the JTWC that is saved in the 'data' directory.
## It creates a new df of information from 1965 to the most recent year (2014)
## which is used to create a climatology of how long storms spent at specific
## strengths in terms of percentages which are outputted at the end.


import numpy as np
import glob
import pandas as pd

## Creates main dataframe (DF) from data
count = 0
year = 1965 #choose start year here
DF = pd.DataFrame()
while(year<2015):
    storm_count = 1
    df1 = pd.DataFrame()
    while(storm_count<57):
        filename = glob.glob('/homes/metogra/kdoughe1/HWRF_Tool/WPAC/data/' + format(year) + 's-bwp-full/bwp' + format(storm_count,'02d') + format(year) + '.txt')
        try:
            file = open(filename[0],mode='r')
            
            lines = file.readlines()
            lines = list(map(str.strip,lines))
            wp_storms = {'data': lines}

            wp_dfs = []
            for storm_dict in wp_storms['data']:
                storm_dict=storm_dict.split(",")
                df = pd.DataFrame([storm_dict[:9]])
                wp_dfs.append(df)

            wp_storms = pd.concat(wp_dfs).reset_index()    

            wp_storms.columns = [
                "index",
                "Basin",
                "Storm Number",
                "Date",
                " ",
                "BEST",
                " ",
                "Latitude",
                "Longitude",
                "Maximum Sustained Wind Knots"
            ]  


            df1 = df1.append(wp_storms)
        except:
            pass
        storm_count = storm_count+1
    year = year+1
    DF = DF.append(df1)

## Creates a subdirectory of DF and counts how many lines were at a specific
## maximum sustained wind speed in knots. It prints table to break down each wind speed


sub_df = DF['Maximum Sustained Wind Knots'].value_counts().to_frame()
sub_df = sub_df.sort_index()
sub_df = sub_df.drop(sub_df.index[[-1,0,1,2,3,4,5]]) # hardcoded to eliminate storms less than 35 knots
sub_df = sub_df.reset_index()
sub_df['index'] = pd.to_numeric(sub_df['index'])

total = sub_df['Maximum Sustained Wind Knots'].sum()

ts = sub_df.loc[sub_df['index'] <= 60]
tot_ts = ts['Maximum Sustained Wind Knots'].sum()

c1 = sub_df.loc[(sub_df['index'] >= 65) & (sub_df['index'] <= 80)]
tot_c1 = c1['Maximum Sustained Wind Knots'].sum()

c2 = sub_df.loc[(sub_df['index'] >= 85) & (sub_df['index'] <= 95)]
tot_c2 = c2['Maximum Sustained Wind Knots'].sum()

c3 = sub_df.loc[(sub_df['index'] >= 100) & (sub_df['index'] <= 110)]
tot_c3 = c3['Maximum Sustained Wind Knots'].sum()

c4 = sub_df.loc[(sub_df['index'] >= 115) & (sub_df['index'] <= 135)]
tot_c4 = c4['Maximum Sustained Wind Knots'].sum()

c5 = sub_df.loc[(sub_df['index'] >= 140)]
tot_c5 = c5['Maximum Sustained Wind Knots'].sum()

print("Total storms: ", total)


ts = (tot_ts/total)*100
c1 = (tot_c1/total)*100
c2 = (tot_c2/total)*100
c3 = (tot_c3/total)*100
c4 = (tot_c4/total)*100
c5 = (tot_c5/total)*100

print('Percentages broken down by category:')
print('Tropical Storm: ', ts)
print('Cat 1: ', c1)
print('Cat 2: ', c2)
print('Cat 3: ', c3)
print('Cat 4: ', c4)
print('Cat 5: ', c5)
