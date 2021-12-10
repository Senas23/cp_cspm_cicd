pipeline {
  agent any
  parameters {
    string(name: 'CSPM_RULESET_ID', defaultValue: '', description: 'CSPM Ruleset ID')
    string(name: 'AWS_ACCOUNT_ID', defaultValue: '', description: 'AWS Account ID')
  }
  environment {
    DOME9_ACCESS_ID = credentials('jenkins-cspm-user-access-id')
    DOME9_SECRET_KEY = credentials('jenkins-cspm-user-secret-key')
  }
  stages {
    stage('Install Python3 Requirements') {
      steps {
        script {
          try {
            sh 'pip3 install -r requirements.txt'
          } catch (Exception e) {
            error "Could not install with pip3 python3 requirements"
          }
        }
      }
    }
    stage('CSPM Update Ruleset bundle') {   
      steps {
        script {
          try {
            sh 'python3 d9_update_rule_bundle.py --bundleId ${CSPM_RULESET_ID}'
           } catch (Exception e) {
             error "Could not update CSPM ruleset"
           }
        }
      }
    }
    stage('CSPM Run Assessment') {   
      steps {
        script {
          try {
            sh 'python3 d9_run_assessment.py --awsAccountNumber ${AWS_ACCOUNT_ID} --bundleId ${CSPM_RULESET_ID}'
           } catch (Exception e) {
             error "Could not run assessment"  
           }
        }
      }
    }
  }
}
