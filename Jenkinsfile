pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Compilando...'
                sh 'python3 --version'
            }
        }
        stage('Test') {
            steps {
                echo 'Ejecutando pruebas...'
                sh 'pip3 install pytest --quiet'
                sh 'pytest test_app.py -v'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Desplegando...'
                sh 'python3 app.py'
            }
        }
    }
}
