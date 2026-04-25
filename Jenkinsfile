pipeline {
    agent any

    stages {

        stage('Verify Docker') {
            steps {
                echo "🔍 Checking Docker..."
                sh 'docker --version'
                sh 'docker-compose --version'
            }
        }

        stage('Build & Deploy') {
            steps {
                echo "🚀 Running Docker Compose..."

                sh '''
                cd $WORKSPACE

                docker-compose down || true
                docker-compose up --build -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 10
                curl -f http://localhost:8000/health || exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD Pipeline Successful"
        }
        failure {
            echo "❌ CI/CD Pipeline Failed"
        }
    }
}
