pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Instalando Python...'
                sh 'apt-get update -qq && apt-get install -y python3 python3-pip -qq'
                echo 'Compilando...'
                sh 'python3 --version'
            }
        }
        stage('Test') {
            steps {
                echo 'Ejecutando pruebas...'
                sh 'pip3 install pytest --quiet --break-system-packages'
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
