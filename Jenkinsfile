pipeline {
  agent any
  environment {
    TERM = 'xterm'
  }
  triggers {
    pollSCM('H/15 * * * *')
  }
  stages {
    stage('Clean up') {
      steps {
        deleteDir()
      }
    }
    stage('Get cgat-apps') {
      steps {
        dir(path: 'cgat-apps') {
          checkout scm
        }
      }
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
          sh 'xvfb-run bash cgat-apps/install-CGAT-tools.sh --jenkins'
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
