import pickle

# Load your model from the .pkl file
with open('videomodel.pkl', 'rb') as f:
    model = pickle.load(f)
    import tensorflow as tf



# Save the TensorFlow model in SavedModel format
export_path = 'C:\labedc\ParkinSeen-master\static'  # Replace with desired export path
tf.saved_model.save(model, export_path)

