from flask import Flask, render_template, request
import numpy as np
import joblib
import pickle  # ← add this

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    state_name = request.form['state']
    state_mapping = {
        'Alabama': 1,
        'Arizona': 2,
        'Arkansas': 3,
        'California': 4,
        'Georgia': 5,
        'Louisiana': 6,
        'Mississippi': 7,
        'Missouri': 8,
        'New Mexico': 9,
        'North Carolina': 10,
        'Oklahoma': 11,
        'South Carolina': 12,
        'Tennessee': 13,
        'Texas': 14,
    }
    state_code = state_mapping.get(state_name, -1)  # Fallback to -1 if state not found

    year = float(request.form['year'])
    n_percent = float(request.form['n_percent'])
    n_pounds = float(request.form['n_pounds'])
    p_percent = float(request.form['p_percent'])
    p_pounds = float(request.form['p_pounds'])
    k_percent = float(request.form['k_percent'])
    k_pounds = float(request.form['k_pounds'])
    area_planted = float(request.form['area_planted'])
    harvested_area = float(request.form['harvested_area'])

    # ✅ DO NOT overwrite state_code — just use the mapped value
    features = np.array([[state_code, year, n_percent, n_pounds, p_percent, p_pounds,
                          k_percent, k_pounds, area_planted, harvested_area]])

    

    with open('models/model_svr.pkl', 'rb') as f:
        model_svr = pickle.load(f)

    with open('models/model_knn.pkl', 'rb') as f:
        model_knn = pickle.load(f)

    # Make predictions
   
    pred_svr = model_svr.predict(features)[0]
    pred_knn = model_knn.predict(features)[0]

    # Show results
    return render_template('result.html', svr=pred_svr, knn=pred_knn)


if __name__ == '__main__':
    app.run(debug=True)
