# Speech_Recognition_app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from model_inference import load_trained_model, preprocess_audio, predict_emotion
import os
import numpy as np

app = Flask(__name__)

# Load the trained model during initialization
model = load_trained_model('entire_trained-model.h5')

emotion_labels = ['fear', 'angry', 'disgust', 'neutral', 'sad', 'surprise', 'happy', 'calm']

def process_audio_file(audio_file):
    # Preprocess the audio file
    audio_features = preprocess_audio(audio_file)

    # Print the preprocessed audio features for debugging
    print("Preprocessed Audio Features:", audio_features)

    # Perform model inference
    prediction = predict_emotion(model, audio_features)

    # Print the raw prediction for debugging
    print("Raw Prediction:", prediction)

    return prediction

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the uploaded audio file
        audio_file = request.files['audio_file']
        if audio_file:
            # Save the audio file temporarily
            temp_path = 'temp_audio.wav'
            audio_file.save(temp_path)

            # Process the audio file and get the prediction
            result = process_audio_file(temp_path)

            # Remove the temporary audio file
            os.remove(temp_path)

            # Assuming 'result' is your prediction result
            predicted_emotion = emotion_labels[np.argmax(result)]

            return render_template('result.html', predicted_emotion=predicted_emotion)
        else:
            return redirect(url_for('home'))

@app.route('/predict_audio', methods=['POST'])
def predict_audio():
    audio_file = request.files['audio']
    temp_path = 'temp_audio.wav'
    audio_file.save(temp_path)

    audio_features = preprocess_audio(temp_path)
    prediction = predict_emotion(model, audio_features)
    predicted_emotion = emotion_labels[np.argmax(prediction)]

    os.remove(temp_path)

    return jsonify({'predicted_emotion': predicted_emotion})

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
