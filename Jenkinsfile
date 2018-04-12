pipeline {
  agent any
  stages {
    stage('Get source code') {
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
}
