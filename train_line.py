from ast import Return
from json import load
import pandas as pd
import prophet
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import valohai

def load_data():
    path = valohai.inputs('sample').path()
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

def data_separation(df_ts):
    df_ts = df_ts.reset_index()
    df_ts.columns = ['ds', 'y']
    train, test = train_test_split(df_ts, test_size=0.2, shuffle=False)
    
    return train, test

def train_model(X):
    model = prophet.Prophet()
    model.fit(X)
    
    return model

def predict(model, periods, freq):
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    return forecast

def plot_predictions(test, forecast):
    idx_plot = test.index
    ax = test.loc[idx_plot].plot(x='ds', y='y', figsize=(14,7))
    forecast.loc[idx_plot].plot(x='ds', y='yhat', ax=ax)
    plt.savefig(valohai.outputs().path("plot_forecast_result.png"))

def evaluate_forecast(y_test, pred):
    r2 = r2_score(y_test, pred)
    rmse = mean_squared_error(y_test, pred, squared=False)
    print('R2: {:.2f}'.format(r2))
    print('RMSE: {:.2f}'.format(rmse))

    return r2, rmse

def log_result(r2, rmse):
    with valohai.logger() as logger:
        logger.log('R2', r2)
        logger.log('RMSE', rmse)

def main():
    df = load_data()
    df = adjust_dtype(df)
    
    df_ts = create_daily_forecast_data(df)
    train, test = data_separation(df_ts)
    model = train_model(train)
    forecast = predict(model, test.shape[0], '1d')

    plot_predictions(test, forecast)
    r2, rmse = evaluate_forecast(test['y'], forecast.loc[test.index]['yhat'])
    log_result(r2, rmse)

if __name__ == "__main__":
    main()