# Jenkins Pipeline Configuration for Santa iOS Enterprise Framework

```groovy
pipeline {
    agent {
        label 'macos' // Run on macOS agent with Xcode
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
    }

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression', 'ntp', 'api'],
            description: 'Select test suite to run'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: true,
            description: 'Enable parallel test execution'
        )
        string(
            name: 'NUM_WORKERS',
            defaultValue: '2',
            description: 'Number of parallel workers'
        )
    }

    environment {
        PYTHON_VERSION = '3.11'
        APPIUM_HOST = '127.0.0.1'
        APPIUM_PORT = '4723'
        VENV_PATH = "${WORKSPACE}/.venv"
        REPORTS_PATH = "${WORKSPACE}/reports"
        PATH = "${VENV_PATH}/bin:${PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    echo "🔄 Repository checked out successfully"
                    echo "Workspace: ${WORKSPACE}"
                }
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    echo "📦 Setting up Python environment"
                    sh '''
                        # Check Python version
                        python3 --version
                        
                        # Create virtual environment
                        python3 -m venv ${VENV_PATH}
                        source ${VENV_PATH}/bin/activate
                        
                        # Upgrade pip and install tools
                        pip install --upgrade pip setuptools wheel
                        
                        echo "✅ Virtual environment created"
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo "📥 Installing dependencies from requirements.txt"
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        pip install -r requirements.txt
                        pip list
                        echo "✅ All dependencies installed"
                    '''
                }
            }
        }

        stage('Verify Xcode & Appium') {
            steps {
                script {
                    echo "🔍 Verifying Xcode and development tools"
                    sh '''
                        xcode-select --version
                        xcodebuild -version
                        
                        # Check if Appium is available
                        if ! command -v appium &> /dev/null; then
                            echo "Installing Appium..."
                            npm install -g appium
                        fi
                        
                        appium --version
                        echo "✅ Development tools verified"
                    '''
                }
            }
        }

        stage('Start Appium Server') {
            steps {
                script {
                    echo "🚀 Starting Appium server on ${APPIUM_HOST}:${APPIUM_PORT}"
                    sh '''
                        # Kill any existing Appium processes
                        pkill -f "appium" || true
                        sleep 2
                        
                        # Start Appium in background
                        appium --port ${APPIUM_PORT} > ${REPORTS_PATH}/appium.log 2>&1 &
                        APPIUM_PID=$!
                        echo $APPIUM_PID > ${REPORTS_PATH}/appium.pid
                        
                        # Wait for server to start
                        for i in {1..30}; do
                            if curl -s http://${APPIUM_HOST}:${APPIUM_PORT}/status > /dev/null 2>&1; then
                                echo "✅ Appium server is ready (PID: $APPIUM_PID)"
                                exit 0
                            fi
                            echo "⏳ Waiting for Appium server... ($i/30)"
                            sleep 2
                        done
                        
                        echo "❌ Failed to connect to Appium server"
                        exit 1
                    '''
                }
            }
        }

        stage('Prepare Test Environment') {
            steps {
                script {
                    echo "📋 Preparing test environment"
                    sh '''
                        # Create report directories
                        mkdir -p ${REPORTS_PATH}/screenshots
                        mkdir -p ${REPORTS_PATH}/logs
                        
                        # Clear old logs
                        rm -f ${REPORTS_PATH}/logs/test.log
                        
                        echo "✅ Test environment prepared"
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "🧪 Running tests - Suite: ${params.TEST_SUITE}"
                    
                    def pytestCmd = "pytest"
                    def testPath = "tests/"
                    def markerOption = ""
                    
                    // Select test suite
                    switch(params.TEST_SUITE) {
                        case 'smoke':
                            markerOption = "-m smoke"
                            break
                        case 'regression':
                            markerOption = "-m 'not skip'"
                            break
                        case 'ntp':
                            testPath = "tests/ntp/"
                            break
                        case 'api':
                            testPath = "tests/api/"
                            break
                        default:
                            markerOption = "-m 'not skip'"
                    }
                    
                    // Add parallel options if enabled
                    def parallelOption = ""
                    if (params.PARALLEL_EXECUTION) {
                        parallelOption = "-n ${params.NUM_WORKERS}"
                    }
                    
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        
                        echo "Test command: ${pytestCmd} ${testPath} \\
                            -v \\
                            --tb=short \\
                            --html=${REPORTS_PATH}/report.html \\
                            --self-contained-html \\
                            --junit-xml=${REPORTS_PATH}/junit.xml \\
                            ${parallelOption} \\
                            ${markerOption}"
                        
                        ${pytestCmd} ${testPath} \
                            -v \
                            --tb=short \
                            --html=${REPORTS_PATH}/report.html \
                            --self-contained-html \
                            --junit-xml=${REPORTS_PATH}/junit.xml \
                            ${parallelOption} \
                            ${markerOption} || true
                        
                        echo "✅ Tests completed"
                    '''
                }
            }
        }

        stage('Generate Reports') {
            steps {
                script {
                    echo "📊 Generating test reports"
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        
                        # Check if reports were generated
                        if [ -f ${REPORTS_PATH}/report.html ]; then
                            echo "✅ HTML report generated"
                            ls -lh ${REPORTS_PATH}/report.html
                        else
                            echo "⚠️  HTML report not found"
                        fi
                        
                        if [ -f ${REPORTS_PATH}/junit.xml ]; then
                            echo "✅ JUnit XML report generated"
                            ls -lh ${REPORTS_PATH}/junit.xml
                        else
                            echo "⚠️  JUnit XML report not found"
                        fi
                        
                        # List screenshots
                        SCREENSHOT_COUNT=$(find ${REPORTS_PATH}/screenshots -type f -name "*.png" 2>/dev/null | wc -l)
                        echo "📸 Screenshots captured: $SCREENSHOT_COUNT"
                    '''
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                script {
                    echo "📤 Publishing test results"
                    
                    // Publish JUnit XML results
                    junit(
                        allowEmptyResults: true,
                        testResults: "${REPORTS_PATH}/junit.xml"
                    )
                    
                    // Publish HTML report
                    publishHTML(
                        reportDir: REPORTS_PATH,
                        reportFiles: 'report.html',
                        reportName: 'pytest HTML Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    )
                    
                    echo "✅ Test results published"
                }
            }
        }
    }

    post {
        always {
            script {
                echo "🧹 Cleaning up"
                sh '''
                    # Stop Appium server
                    if [ -f ${REPORTS_PATH}/appium.pid ]; then
                        APPIUM_PID=$(cat ${REPORTS_PATH}/appium.pid)
                        kill $APPIUM_PID 2>/dev/null || true
                    fi
                    pkill -f "appium" || true
                    
                    echo "✅ Cleanup completed"
                '''
            }

            // Archive artifacts
            archiveArtifacts(
                artifacts: 'reports/**/*',
                allowEmptyArchive: true,
                onlyIfSuccessful: false
            )
        }

        success {
            script {
                echo "✅ Pipeline completed successfully"
                // Optional: Send success notification
                // emailext subject: 'Tests Passed',
                //          body: 'All tests passed. View report at ${BUILD_URL}pytest_HTML_Report/'
            }
        }

        failure {
            script {
                echo "❌ Pipeline failed"
                // Optional: Send failure notification
                // emailext subject: 'Tests Failed',
                //          body: 'Some tests failed. Check report at ${BUILD_URL}pytest_HTML_Report/'
            }
        }

        unstable {
            script {
                echo "⚠️  Pipeline unstable - some tests may have failed"
            }
        }
    }
}
```

## Jenkins Setup Instructions

### 1. Create New Pipeline Job

1. Go to Jenkins Dashboard
2. Click "New Item"
3. Enter job name: `santa-ios-automation`
4. Select "Pipeline"
5. Click "OK"

### 2. Configure Pipeline

In the Pipeline section:

**Option A: From SCM (Recommended)**
- Definition: Pipeline script from SCM
- SCM: Git
- Repository URL: `https://github.com/your-org/santa_ios_enterprise_framework.git`
- Script Path: `ci/Jenkinsfile`

**Option B: From Text**
- Copy the Groovy script above into the Pipeline text area

### 3. Configure Build Parameters

Go to Build with Parameters:
- TEST_SUITE: Allows selecting which tests to run
- PARALLEL_EXECUTION: Toggle parallel test running
- NUM_WORKERS: Number of concurrent workers

### 4. Set Up Build Triggers

**Poll SCM** (for scheduled builds):
```
H H(0-5) * * *  # Run between midnight and 5 AM daily
```

**GitHub Hook** (for webhook-based builds):
- Requires GitHub plugin
- Configure webhook in GitHub repo settings

**Build periodically** (for scheduled runs):
```
H H(2) * * *  # Run daily at 2 AM
```

### 5. Configure Notifications

In Post-build Actions, add:
- **Email Notification**: Notify on build failure
- **Slack Plugin**: Send results to Slack channel
- **Archive Artifacts**: Save reports

### 6. Agent Configuration

Ensure Jenkins agent has:
- macOS with Xcode installed
- Python 3.10+ available
- Appium installed (or via npm)
- Label: `macos`

### 7. Node.js Setup (for Appium)

```bash
brew install node
npm install -g appium
appium --version
```

## Local Testing with Jenkinsfile

To test the Jenkinsfile locally:

```bash
# Install Jenkins on macOS
brew install jenkins-lts

# Start Jenkins
jenkins-lts

# Or use Docker
docker run -d -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts

# Validate Groovy syntax
groovy -c ci/Jenkinsfile
```

## Environment Variables

Set in Jenkins credentials/configuration:

```
APPIUM_HOST=127.0.0.1
APPIUM_PORT=4723
DEVICE_UDID=<Your Device UDID>
BUNDLE_ID=com.brave.ios
```

## Troubleshooting

**Appium server fails to start:**
```bash
# Check if port is in use
lsof -i :4723

# Kill process using port
kill -9 <PID>
```

**Python virtual environment issues:**
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
```

**Xcode permissions:**
```bash
sudo xcode-select --reset
xcode-select --install
sudo xcodebuild -license accept
```
