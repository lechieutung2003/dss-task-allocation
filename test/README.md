#  Robot Framework Test Project

---

## System requirements

- Python >= 3.10
- pip (Python package manager)
- Google Chrome (or other browsers if customized)
- [ChromeDriver](https://chromedriver.chromium.org/) compatible with the browser version *(if not using `webdriver-manager`)*

---

## Environment Setup

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate    #MacOS
venv\Scripts\activate       #Windows


Install necessary libraries
pip install -r requirements.txt
or
pip install robotframework robotframework-seleniumlibrary webdriver-manager


Folder structure

Project_RobotFramework/
├── tests/                     # Contains .robot files
│   ├── 
│
├── reports/                   # Contains test result files generated automatically
│   ├── 
│
├── resources/                 
│   ├── keywords.robot
│   └── variables.robot
│
├── requirements.txt
└── README.md

How to run tests

robot --outputdir reports tests/ # This will run all test suites in the tests/ directory
# To run individual .robot files, run the following commands one by one
robot --outputdir reports 
