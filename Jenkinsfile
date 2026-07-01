pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Instalando dependencias...'
                sh 'apt-get update -qq && apt-get install -y python3 python3-pip -qq'
                sh 'pip3 install flask --quiet --break-system-packages'
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
        stage('Analyze') {
            steps {
                echo 'Analizando codigo con SonarQube...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        pip3 install sonar-scanner --quiet --break-system-packages || true
                        sonar-scanner \
                        -Dsonar.projectKey=proyecto-jenkins \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://172.17.0.1:9000 \
                        || true
                    '''
                }
            }
        }
        stage('Security Test') {
            steps {
                echo 'Ejecutando OWASP Dependency-Check...'
                dependencyCheck additionalArguments: '--scan ./ --format HTML --format XML', odcInstallation: 'OWASP-DC'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'

                echo 'Ejecutando OWASP ZAP...'
                sh '''
                    python3 -m flask run --host=0.0.0.0 --port=5000 &
                    sleep 5
                    docker run --rm --network host \
                        ghcr.io/zaproxy/zaproxy:stable \
                        zap-baseline.py -t http://localhost:5000 \
                        -r zap-report.html || true
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Desplegando aplicacion...'
                sh 'python3 app.py &'
                sh 'sleep 2'
                echo 'Deploy completado.'
            }
        }
    }
}
