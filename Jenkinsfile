pipeline {

     agent any

    //agent any
 
   environment {
        REMOTE_CONN = 'demeter_llm@192.168.199.91'  // Reemplaza con tu usuario y host del servidor remoto
       REMOTE_HOST = '192.168.199.91'
        FOLDER_NAME = '/var/www/melisa/demeter_llm/'
         REPO_URL = 'https://github.com/CIAT-DAPA/demeter_llm'
        
    }
 
    stages {
        

        stage('Check directory and content') {
        steps {
                script {
                    DIRECTORIO = sh(script: 'ssh ${REMOTE_CONN} "[ -d ${FOLDER_NAME} ] && echo 1 || echo 0"', returnStdout: true).trim()
                    CONTENIDO = sh(script: '''
                        ssh ${REMOTE_CONN} '
                        if [ "$(ls -A ${FOLDER_NAME})" ]; then
                            echo "1"
                        else
                            echo "0"
                        fi'
                    ''', returnStdout: true).trim()
                
                
                }
        echo "El resultado del comando es: ${DIRECTORIO}"
        echo "Resultado: ${CONTENIDO}"             
        
            }
                
        }

    }
}
