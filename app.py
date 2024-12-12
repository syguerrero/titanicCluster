from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Inicializar Flask
app = Flask(__name__)

# Entrenar el modelo (utilizando tu código)
file_path = 'Titanic-Dataset.csv'
data = pd.read_csv(file_path)

# Preprocesamiento de datos
data['Age'].fillna(data['Age'].median(), inplace=True)
data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)
data['Fare'].fillna(data['Fare'].median(), inplace=True)
data = pd.get_dummies(data, columns=['Sex', 'Embarked'], drop_first=True)
data.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)

X = data.drop('Survived', axis=1)
y = data['Survived']

# Dividir y entrenar el modelo
clf = RandomForestClassifier(random_state=42)
clf.fit(X, y)

@app.route('/')
def home():
    return "Welcome to the Titanic Prediction API. Use the /predict endpoint to send predictions."


# Rutas de la API
@app.route('/predict', methods=['POST'])
def predict():
    try:
        content = request.get_json()

        # Validar campos obligatorios
        required_fields = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
        for field in required_fields:
            if field not in content:
                return jsonify({'error': f"Missing field: {field}"}), 400

        # Validar datos individuales
        if content['Pclass'] not in [1, 2, 3]:
            return jsonify({'error': "Invalid value for Pclass"}), 400
        if content['Sex'] not in ['male', 'female']:
            return jsonify({'error': "Invalid value for Sex"}), 400
        if content['Embarked'] not in ['C', 'Q', 'S']:
            return jsonify({'error': "Invalid value for Embarked"}), 400

        # Preparar los datos para el modelo
        usuario = pd.DataFrame({
            'Pclass': [content['Pclass']],
            'Age': [content['Age']],
            'SibSp': [content['SibSp']],
            'Parch': [content['Parch']],
            'Fare': [content['Fare']],
            'Sex_male': [1 if content['Sex'] == 'male' else 0],
            'Embarked_Q': [1 if content['Embarked'] == 'Q' else 0],
            'Embarked_S': [1 if content['Embarked'] == 'S' else 0]
        })
        # SOLUCIÓN TEMPORAL: Ignorar columnas no numéricas
        usuario = usuario.apply(pd.to_numeric, errors='coerce')  # Convierte a numérico o NaN si no es posible
        if usuario.isnull().any().any():  # Si hay valores NaN después de la conversión, devolver error
            return jsonify({'error': 'Invalid data in input'}), 400

        # Realizar predicción
        prediccion = model.predict(usuario)[0]
        resultado = "Sobrevivió" if prediccion == 1 else "No sobrevivió"
        return jsonify({'resultado': resultado})

    except Exception as e:
        app.logger.error(f"Error during prediction: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)
