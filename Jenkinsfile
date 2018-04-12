pipeline {
  agent any
  stages {
    stage('Cleanup workspace') {
      steps {
        deleteDir()
      }
    }
    stage('Get source code') {
      steps {
        dir(path: 'cgat-core') {
          git(url: 'https://github.com/cgat-developers/cgat-core.git', changelog: true, poll: true)
        }
        dir(path: 'cgat-apps') {
          git(url: 'https://github.com/cgat-developers/cgat-apps.git', changelog: true, poll: true)
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
}
