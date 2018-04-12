pipeline {
  agent any
  environment {
    TERM = 'xterm'
  }
  options {
    checkoutToSubdirectory('cgat-apps')
  }
  stages {
    stage('Clean up') {
      deleteDir()
    }
    stage('Get cgat-apps') {
      checkout scm
    }
    stage('Get cgat-core') {
      steps {
        dir(path: 'cgat-core') {
          git(url: 'https://github.com/cgat-developers/cgat-core.git', changelog: true, poll: true)
        }
      }
    }
    stage('Run tests') {
      steps {
        catchError() {
          sh 'xvfb-run bash install-CGAT-tools.sh --jenkins'
        }

      }
    }
  }
  post {
    failure {
      mail to: 'sebastian.lunavalero@imm.ox.ac.uk', subject: 'Failed testing of cgat-app', body: 'Please visit https://jenkins for more details'
    }
  }
}
