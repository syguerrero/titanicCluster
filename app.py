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

# Rutas de la API
@app.route('/predict', methods=['POST'])
def predict():
    # Obtener los datos enviados en la solicitud
    content = request.get_json()

    # Crear un DataFrame para los datos del usuario
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

    # Realizar la predicción
    prediccion = clf.predict(usuario)[0]
    resultado = "Sobrevivió" if prediccion == 1 else "No sobrevivió"

    # Responder con el resultado
    return jsonify({'resultado': resultado})

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)
