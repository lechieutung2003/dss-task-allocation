*** Settings ***
Documentation    Common variables and configurations for all test suites

*** Variables ***
# Base URL - Thay đổi theo môi trường
${BASE_URL}          http://localhost:3000
${BROWSER}           Chrome
${SELENIUM_SPEED}    0.3

# Timeouts
${TIMEOUT_SHORT}     5s
${TIMEOUT_MEDIUM}    10s
${TIMEOUT_LONG}      30s

# Common Selectors
${LOADING_SPINNER}    css:.loading
${SUCCESS_MESSAGE}    css:.el-message--success
${ERROR_MESSAGE}      css:.el-message--error

# User credentials (nếu cần login)
${VALID_USERNAME}     test@example.com
${VALID_PASSWORD}     password123
