import pandas as pd
import prophet
from prophet.serialize import model_to_json
import valohai

def load_data():
    path = valohai.inputs('data').path()
    return pd.read_csv(path)

def adjust_dtype(df):
    df['time'] = pd.to_datetime(df['time'])
    return df

def create_daily_forecast_data(df):
    df_ts = df[['time', 'entries_diff']].copy()
    df_ts = df_ts.set_index('time')
    df_ts = df_ts.resample('d').sum()
    df_ts.columns = ['ts']
    
    return df_ts

def reset_index(df_ts):
    df_ts = df_ts.reset_index()
    df_ts.columns = ['ds', 'y']
    
    return df_ts
    
def load_params():
    param_growth = valohai.parameters('growth').value
    param_changepoint_prior_scale = valohai.parameters('changepoint_prior_scale').value

    params = {
        'growth': param_growth,
        'changepoint_prior_scale': param_changepoint_prior_scale
    }

    return params

def train_model(X, params=None):
    model = prophet.Prophet(**params)
    model.fit(X)
    
    return model

def save_model(model):
    path = valohai.outputs().path('model.json')
    with open(path, 'w') as file:
        file.write(model_to_json(model))


def main():
    df = load_data()
    df = adjust_dtype(df)
    
    df_ts = create_daily_forecast_data(df)
    df_ts = reset_index(df_ts)
    params = load_params()
    model = train_model(df_ts, params)
    save_model(model)

if __name__ == "__main__":
    main()