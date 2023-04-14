import pandas as pd

siheng_input = 'results/noise/total_corners_detected.csv'
tartan_input = 'results/noise/tartan_results.csv'
output = 'results/merged_results.csv'

detectors = ['Deltille','AT3','Kaess-AT3','ArUco','TartanCalib']

siheng_df = pd.read_csv(siheng_input)
tartan_df = pd.read_csv(tartan_input)

merged_df = siheng_df.assign(TartanCalib=0.0)

for idx, row in merged_df.iterrows():
    # print(row)

    id = row['File'].split('/')[-1]
    
    # find tartan row with 'bag' entry similar to file 
    tartan_row = tartan_df.loc[tartan_df['bag'].str.contains(id)]
    tartan_detections = max(tartan_row['Tartan Train Features'].values)
    merged_df['TartanCalib'][idx] = int(tartan_detections)

# remove all rows that has at least one zero
# merged_df = merged_df[(merged_df.T != 0).all()]
# save merged results
merged_df.to_csv(output)