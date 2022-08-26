import pandas as pd
from prophet.serialize import model_from_json
import json
import valohai

def load_data():
    # print(valohai.inputs('periods').path())
    
    return 1

def load_model():
    path = valohai.inputs('model').path()

    with open(path, 'r') as file:
        model = model_from_json(file.read())
    return model

def predict(model, periods):
    future = model.make_future_dataframe(periods=periods, freq='1d')
    forecast = model.predict(future)
    print(forecast)
    forecast = forecast.set_index('ds')
    forecast = forecast['yhat'].iloc[-periods:]
    return forecast.to_json()

def save_predictions(predictions):
    path = valohai.outputs().path('predictions.json')
    with open(path, 'w') as file:
        json.dump(predictions, file, default=lambda v: str(v))

def main():
    periods = load_data()
    model = load_model()
    predictions = predict(model, periods)
    save_predictions(predictions)

if __name__ == "__main__":
    main()
