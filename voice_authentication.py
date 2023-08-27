from speaker_recognition import extract_features, train_speaker_model, predict_speaker

# Extract features from the audio samples
features = extract_features(["sample1.wav", "sample2.wav", "sample3.wav"])

# Train a speaker model using the extracted features
model = train_speaker_model(features, ["user1", "user2", "user3"])

# Predict the speaker of a new audio sample
prediction = predict_speaker("unknown.wav", model)

print("The predicted speaker is: ", prediction)