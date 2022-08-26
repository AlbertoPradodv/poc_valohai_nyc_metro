from fastapi import FastAPI
 
app = FastAPI()
 
model_path = 'model-prophet'
loaded_model = None
 
@app.post("{full_path:path}")
async def pred(periods):
    print(periods)
    
    global loaded_model
    # Check if model is already loaded
 
    # if not loaded_model:
    #     loaded_model = tf.keras.models.load_model(model_path)
 
    # Predict with the model
    # prediction = loaded_model.predict_classes(image_data)
    
    return f'Predicted_Digit: {periods}'