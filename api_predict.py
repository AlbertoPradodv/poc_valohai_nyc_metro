from fastapi import FastAPI
from prophet.serialize import model_from_json

app = FastAPI()
 
model_path = 'model-prophet'
model = None

def load_model():
    with open(model_path, 'r') as file:
        model = model_from_json(file.read())
    return model

def forecast(model, periods):
    future = model.make_future_dataframe(periods=periods, freq='1d')
    forecast = model.predict(future)
    print(forecast)
    forecast = forecast.set_index('ds')
    forecast = forecast['yhat'].iloc[-periods:]
    return forecast.to_json()

# def save_predictions(predictions):
#     path = valohai.outputs().path('predictions.json')
#     with open(path, 'w') as file:
#         json.dump(predictions, file, default=lambda v: str(v))
 

@app.post("{full_path:path}")
async def predict(periods):
    global model
    
    if not model:
        model = load_model() 
      
    predictions = forecast(model, int(periods))
    return str(predictions)
