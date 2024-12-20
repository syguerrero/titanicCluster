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
        # Obtener los datos JSON enviados al servidor
        content = request.get_json()
        app.logger.info(f"Datos recibidos: {content}")

        # Validar campos obligatorios
        required_fields = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
        for field in required_fields:
            if field not in content:
                app.logger.error(f"Campo faltante: {field}")
                return jsonify({'error': f"Missing field: {field}"}), 400

        # Validar valores de los campos
        if content['Pclass'] not in [1, 2, 3]:
            app.logger.error(f"Valor inválido para Pclass: {content['Pclass']}")
            return jsonify({'error': "Invalid value for Pclass"}), 400
        if content['Sex'] not in ['male', 'female']:
            app.logger.error(f"Valor inválido para Sex: {content['Sex']}")
            return jsonify({'error': "Invalid value for Sex"}), 400
        if content['Embarked'] not in ['C', 'Q', 'S']:
            app.logger.error(f"Valor inválido para Embarked: {content['Embarked']}")
            return jsonify({'error': "Invalid value for Embarked"}), 400

        # Crear DataFrame para predicción
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
        app.logger.info(f"Datos preparados para predicción: {usuario}")

        # Realizar predicción
        prediccion = model.predict(usuario)[0]
        resultado = "Sobrevivió" if prediccion == 1 else "No sobrevivió"
        app.logger.info(f"Resultado de la predicción: {resultado}")
        return jsonify({'resultado': resultado})

    except Exception as e:
        app.logger.error(f"Error durante la predicción: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)
