import valohai
import pandas as pd

my_data = {
    'myinput': 'datum://0182b0ad-0cee-a0a0-a4f8-ec01b8421bb3'
}
 

valohai.prepare(
    step='preprocess-dataset',
    image='python:3.9',
    default_inputs= my_data
)

#read csv with pandas
df = pd.read_csv(valohai.inputs("myinput").path())


#Conversão dos dtypes

df["time"] = pd.to_datetime(df["time"])

#Agrupamento e aplicação da transformação na base toda

df['entries_diff'] = df.groupby(['ca', 'scp', 'station', 'linename'])['entries'].transform(pd.Series.diff)

idx_outliers = df.groupby(['ca', 'scp', 'station', 'linename']).apply(
    lambda x: outlier_boxplot(x['entries_diff'])
)

x_total_outliers = []
for i in idx_outliers:
    idx_total_outliers.extend(i)
df.loc[idx_total_outliers, 'entries_diff'] = 0


#saving output to valohai

output_path = valohai.outputs().path('datum://0182b0ad-0cee-a0a0-a4f8-ec01b8421bb3')
