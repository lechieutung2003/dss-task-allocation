*** Settings ***
Library           SeleniumLibrary
Variables         ./variables.robot

*** Keywords ***
Open Browser To Login Page
    Open Browser        ${URL_LOGIN}      ${BROWSER}

Open Browser To SignUp Page
    Open Browser        ${URL_SIGNUP}      ${BROWSER}

Enter Login Info Correct
    # Wait for the real email input (uses class "input" and placeholder)
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${VALID_EMAIL}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s


Enter SignUp Info
    Input Text      name=name                             ${VALID_dk_U}
    Input Text      css=input[data-qa="signup-email"]     ${VALID_dk_G}
    Click Button    css=button[data-qa="signup-button"]


Enter Login Info Wrong
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_1}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD1}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Wrong
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_1}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit

Check Text At XPath
    [Arguments]    ${xpath}    ${expected_text}
    Wait Until Element Is Visible    ${xpath}    10s
    ${text}=       Get Text    ${xpath}
    Should Be Equal As Strings    ${text}    ${expected_text}

Check Error Message Should Appear
    [Arguments]    ${expected_text}
    Wait Until Page Contains    ${expected_text}    timeout=10s
    ${txt}=    Get Text    xpath=//p[contains(text(),"${expected_text}")]
    Should Be Equal As Strings    ${txt}    ${expected_text}
    
Check Logo Is Displayed
    Wait Until Element Is Visible    css=h1.logo-text    timeout=10s
    ${text}=    Get Text    css=h1.logo-text
    Should Be Equal As Strings    ${text}    Clean Go


Fill Account Information
    Input Text    id=password        ${VALID_dk_P}
    Input Text    id=first_name      ${VALID_dk_F}
    Input Text    id=last_name       ${VALID_dk_L}
    Input Text    id=company         ${VALID_dk_C}
    Input Text    id=address1        ${VALID_dk_A1}
    Input Text    id=address2        ${VALID_dk_A2}
    Input Text    id=state           ${VALID_dk_S}
    Input Text    id=city            ${VALID_dk_Ci}
    Input Text    id=zipcode         ${VALID_dk_Z}
    Input Text    id=mobile_number   ${VALID_dk_M}

Click Create Account Button
    Wait Until Element Is Visible    css=button[data-qa="create-account"]    15s
    Scroll Element Into View         css=button[data-qa="create-account"]
    Sleep    2s
    Click Button                     css=button[data-qa="create-account"]
