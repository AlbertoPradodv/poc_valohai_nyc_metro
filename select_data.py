from venv import create
import pandas as pd
import matplotlib.pyplot as plt
import valohai


def load_data():
    path = valohai.inputs('raw').path()
    df = pd.read_csv(path)
    print(df.shape)
    return df

def adjust_dtype(df):
    df["time"] = pd.to_datetime(df["time"])
    return df

def select_line(df):
    ca = 'R610'
    scp = '00-04-01'
    df_ca_scp_example = df[(df['ca'] == ca) & (df['scp'] == scp)]
    df_ca_scp_example = df_ca_scp_example.reset_index(drop=True)
    return df_ca_scp_example

def adjust_frequency(df):
    df = df.set_index('time')
    df = df.asfreq('4H')
    df = df.reset_index()
    
    return df

def create_diffs(df):
    df['time_diff'] = df['time'] - df.shift(1)['time']
    df['entries_diff'] = df['entries'] - df['entries'].shift(1)
    df['exits_diff'] = df['exits'] - df['exits'].shift(1)
    df.loc[448, 'entries_diff'] = df.loc[442, 'entries_diff']

    return df

def save_data(df):
    output_path = valohai.outputs().path('data_sample.csv')
    df.to_csv(output_path, index=False)

def plot_line(df):
    df.plot(x='time', y='entries_diff')
    plt.savefig(valohai.outputs().path("plot_line_complete.png"))

    df.head(100).plot(x='time', y='entries_diff', figsize=(10, 6))
    plt.savefig(valohai.outputs().path("plot_line_zoom.png"))

def fix_missing_data(df):
    idx_missing_entries_diff = df[df['entries_diff'].isnull()].index
    idx_last_week = idx_missing_entries_diff[1:] - 6
    df.loc[idx_missing_entries_diff[1:], 'entries_diff'] = df.loc[idx_last_week, 'entries_diff'].values
    return df

def main():
    df = load_data()
    df = adjust_dtype(df)
    df_line = select_line(df)
    df_line = adjust_frequency(df_line)
    df_line = create_diffs(df_line)
    df_line = fix_missing_data(df_line)
    plot_line(df_line)
    save_data(df_line)

if __name__ == "__main__":
    main()
