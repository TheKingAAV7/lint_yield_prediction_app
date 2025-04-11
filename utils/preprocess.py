import numpy as np

# List of feature names in the exact order used during model training
FEATURE_ORDER = [
    'Fertilizer_use',       # Fertilizer used (e.g., in kg/ha)
    'Area_Planted',         # Area planted (e.g., in hectares)
    'Irrigation_Level',     # Irrigation level (e.g., in %)
    'Rainfall',             # Rainfall amount (e.g., in mm)
    'Temperature'           # Temperature (e.g., in Celsius)
    # Add more features here if your model was trained on additional columns
]

def preprocess_input(form_data):
    """
    Processes form input data and returns a NumPy array formatted for prediction.
    
    Parameters:
        form_data (ImmutableMultiDict): The data dictionary from Flask's request.form.
    
    Returns:
        np.ndarray: Array with shape (1, n_features) ready for prediction.
    """
    try:
        features = []

        for key in FEATURE_ORDER:
            value = form_data.get(key)
            if value is None or value.strip() == '':
                raise ValueError(f"Missing or empty value for feature: {key}")
            features.append(float(value))

        return np.array(features).reshape(1, -1)

    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"Error in preprocessing input: {e}")
