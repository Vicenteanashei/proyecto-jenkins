pipeline {
    agent any
    environment {
        SONAR_AUTH_TOKEN = credentials('SONAR_AUTH_TOKEN')
    }
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
                sh '''
                    apt-get install -y unzip curl -qq
                    curl -sL https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip -o sonar-scanner.zip
                    unzip -o sonar-scanner.zip -d /opt/
                    /opt/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner \
                        -Dsonar.projectKey=proyecto-jenkins \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://172.17.0.1:9000 \
                        -Dsonar.token=$SONAR_AUTH_TOKEN \
                        || true
                '''
            }
        }
        stage('Security Test') {
            steps {
                echo 'Ejecutando OWASP Dependency-Check...'
                sh '''
                    apt-get install -y default-jdk -qq || true
                    curl -sL https://github.com/jeremylong/DependencyCheck/releases/download/v8.4.0/dependency-check-8.4.0-release.zip -o dc.zip
                    unzip -o dc.zip -d /opt/
                    /opt/dependency-check/bin/dependency-check.sh \
                        --scan ./ \
                        --format HTML \
                        --out ./dependency-check-report \
                        --nvdApiKey 0 \
                        || true
                '''
                echo 'Ejecutando OWASP ZAP...'
                sh '''
                    python3 -m flask run --host=0.0.0.0 --port=5000 &
                    sleep 5
                    docker run --rm --network host \
                        ghcr.io/zaproxy/zaproxy:stable \
                        zap-baseline.py -t http://localhost:5000 \
                        -r zap-report.html || true
                    pkill -f "flask run" || true
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Desplegando aplicacion...'
                sh 'nohup python3 app.py &'
                sh 'sleep 2'
                echo 'Deploy completado.'
            }
        }
    }
}
