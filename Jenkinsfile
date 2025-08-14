def remote = [:]

pipeline {
    agent any

        environment {
            host = credentials('demeter_llm_host')
        }

    stages {
        stage('Ssh to connect Melisa server') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'bbb872a0-f1a9-4d1c-a6ff-49a54fbe4985', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        try {
                            remote.user = USER
                            remote.password = PASS
                            remote.host = host
                            remote.name = host
                            remote.allowAnyHosts = true

                            sshCommand remote: remote, command: "echo 'Connection successful!'"
                        } catch (Exception e) {
                            echo "SSH Connection Error: ${e.message}"
                            error("Failed to establish SSH connection: ${e.message}")
                        }
                    }
                }
            }
        }
        stage('Update API code') {
            steps {
                script {
                    try {
                        sshCommand remote: remote, command: """
                            cd /var/www/melisa/demeter_llm/
                            git checkout main
                            git pull origin main
                            conda activate /home/scalderon/.conda/envs/demeter_llm_api
                            pip install -r requirements.txt
                        """
                    } catch (Exception e) {
                        echo "Git Pull Error: ${e.message}"
                        error("Failed to update code: ${e.message}")
                    }
                }
            }
        }
        stage('Restart API service') {
            steps {
                script {
                    try {
                        sshCommand remote: remote, command: """
                            conda activate /home/scalderon/.conda/envs/demeter_llm_api
                            fuser -k 3001/tcp || true
                            nohup uvicorn src.api:app --host 0.0.0.0 --port 3001 > api.log 2>&1 &
                        """
                    } catch (Exception e) {
                        echo "API Restart Error: ${e.message}"
                        error("Failed to restart API: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                echo "Pipeline failed"
            }
        }
        success {
            script {
                echo 'API deployed successfully!'
            }
        }
    }
}
