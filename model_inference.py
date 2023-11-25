# model_inference.py

import numpy as np
import librosa
from keras.models import load_model

def load_trained_model(model_file):
    return load_model(model_file)

def preprocess_audio(audio_file):
    data, _ = librosa.load(audio_file, duration=3, offset=0.5)
    # You may need to adjust the feature extraction logic based on your training
    mfccs = librosa.feature.mfcc(y=data, sr=22050, n_mfcc=58)
    mfccs_processed = np.mean(mfccs.T, axis=0)
    return np.array(mfccs_processed)

def predict_emotion(model, audio_features):
    prediction = model.predict(np.expand_dims(audio_features, axis=0).reshape(1, -1, 1))
    return prediction
