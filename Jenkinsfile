pipeline {
    agent any
        stages {
            stage ('Checkout') {
                steps {
                    git branch:'master', url: 'https://github.com/vianiecetan/ssdlabquiz.git'
                }
            }
            stage('OWASP DependencyCheck') {
			    steps {
				    dependencyCheck additionalArguments: '-n --noupdate --format HTML --format XML', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
			    }
		    }
            stage('Code Quality Check via SonarQube') {
                steps {
                    script {
                        def scannerHome = tool 'SonarQube';
                        withSonarQubeEnv('SonarQube') {
                            sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=labquiz -Dsonar.sources=."
                        }
                    }
                }
            }
            stage('Integration UI Test') {
            parallel {
                stage('Deploy') {
                    agent any
                    steps {
                        sh './jenkins/scripts/deploy.sh'
                        input message: 'Finished using the web site? (Click "Proceed" to continue)'
                        sh './jenkins/scripts/kill.sh'
                    }
                }
                stage('Headless Browser Test') {
                    agent {
                        docker {
                            image 'python:3.9-slim' // Use a Python image
                            args '-v /root/.cache:/root/.cache' // Caching for pip
                        }
                    }
                    steps {
                        sh 'pip install -r requirements.txt'
                        sh 'pytest tests/test_ui.py --headless' // Running the tests
                    }
                    post {
                        always {
                            junit 'reports/*.xml' // Adjust path to test reports
                        }
                    }
                }
            }
        }
            
    }
    post {
        always {
            recordIssues enabledForFailure: true, tool: sonarQube()
        }
        success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
    }
}
