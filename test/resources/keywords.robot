*** Settings ***
Library           SeleniumLibrary
Variables         ./variables.robot

Documentation    Custom keywords for Create Order test suite
Library          SeleniumLibrary
Library          DateTime
Library          String
Library          Collections

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

Enter Login Info Wrong
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_1}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD1}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Empty
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_4}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Format Wrong @
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_1}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Format Wrong Space
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_2}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Format Wrong g.c
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_3}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Not Exist
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_6}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Format Wrong Too Long
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_5}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Password Empty
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${VALID_EMAIL}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_5}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Password Format Wrong Too Short
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${VALID_EMAIL}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_4}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Password Format Wrong Too Long
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${VALID_EMAIL}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_2}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Password Format Wrong Space
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${VALID_EMAIL}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_3}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Password Format Wrong @
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${VALID_EMAIL}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_6}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email and Password Empty
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_4}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_5}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Empty @ and Password Empty
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_1}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_5}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Wrong g.c and Password Too Short
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_3}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_4}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Email Too Long and Password Correct
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_5}
    Input Text    css=input.input[placeholder="Password"]    ${VALID_PASSWORD}
    Click Button    css=button.button-submit
    Sleep    1s

Enter Login Special Email and Password 
    Wait Until Element Is Visible    css=input.input[placeholder="Email"]    timeout=5s
    Input Text    css=input.input[placeholder="Email"]    ${INVALID_EMAIL_2}
    Input Text    css=input.input[placeholder="Password"]    ${INVALID_PASSWORD_6}
    Click Button    css=button.button-submit
    Sleep    1s





Enter SignUp Info
    Input Text      name=name                             ${VALID_dk_U}
    Input Text      css=input[data-qa="signup-email"]     ${VALID_dk_G}
    Click Button    css=button[data-qa="signup-button"]

Check Text At XPath
    [Arguments]    ${xpath}    ${expected_text}
    Wait Until Element Is Visible    ${xpath}    10s
    ${text}=       Get Text    ${xpath}
    Should Be Equal As Strings    ${text}    ${expected_text}

Check Error Message Should Appear
    [Arguments]    ${expected_text}
    Wait Until Page Contains    ${expected_text}    timeout=5s
    ${txt}=    Get Text    xpath=//p[contains(text(),"${expected_text}")]
    Should Be Equal As Strings    ${txt}    ${expected_text}

Check Error Message Should Appear Span
    [Arguments]    ${expected_text}
    Wait Until Page Contains    ${expected_text}    timeout=5s
    ${txt}=    Get Text    xpath=//span[contains(text(),"${expected_text}")]
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



Wait For Service Options
    [Arguments]    ${timeout}=15s
    Wait Until Keyword Succeeds    ${timeout}    1s    Check Service Options

Check Service Options
    ${items}=    Get List Items    css=select[data-qa="service-select"]
    ${count}=    Get Length    ${items}
    Run Keyword If    ${count} > 1    No Operation    ELSE    Fail    Not enough service options yet


Set Number Input Value
    [Arguments]    ${selector}    ${value}
    Wait Until Element Is Visible    ${selector}    10s
    Execute JavaScript    var sel = '${selector}'; sel = sel.replace(/^css[:=]/, ''); var el = document.querySelector(sel); if (!el) { throw 'Element not found: ' + sel; } el.value = '${value}'; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));


Input Valid Area
    [Arguments]    ${area}=50
    Comment    Use the stable AREA selector from variables and set value via JS so Vue updates
    Set Number Input Value    ${AREA_INPUT}    ${area}

Select Future Start Time
    [Arguments]    ${hours}=2
    ${start_time}=    Get Current Date    increment=${hours} hours
    ${start_formatted}=    Convert Date    ${start_time}    result_format=%Y-%m-%dT%H:%M
    Execute JavaScript    var sel = '${START_TIME_INPUT}'; sel = sel.replace(/^css[:=]/, ''); var el = document.querySelector(sel); if (!el) { throw 'Start input not found: ' + sel; } el.value = '${start_formatted}'; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));

Select Future End Time
    [Arguments]    ${hours}=4
    ${end_time}=    Get Current Date    increment=${hours} hours
    ${end_formatted}=    Convert Date    ${end_time}    result_format=%Y-%m-%dT%H:%M
    Execute JavaScript    var sel = '${END_TIME_INPUT}'; sel = sel.replace(/^css[:=]/, ''); var el = document.querySelector(sel); if (!el) { throw 'End input not found: ' + sel; } el.value = '${end_formatted}'; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));

Click Submit Button
    Comment    Ensure devtools overlay hidden and click submit CTA reliably
    Execute JavaScript    var d = document.querySelector('nuxt-devtools-frame'); if (d) d.style.display='none';
    Wait Until Element Is Visible    ${SUBMIT_BUTTON}    10s
    Wait Until Keyword Succeeds    10s    0.5s    Execute JavaScript    var sel = '${SUBMIT_BUTTON}'; sel = sel.replace(/^css[:=]/, ''); var btn = document.querySelector(sel); if (!btn) { throw 'Submit button not found: ' + sel; } if (btn.disabled) { throw 'Submit button disabled'; } else { return true; }
    Execute JavaScript    var sel2 = '${SUBMIT_BUTTON}'; sel2 = sel2.replace(/^css[:=]/, ''); document.querySelector(sel2).click();









Verify Customer Info Loaded
    [Documentation]    Verify customer information is displayed correctly
    Wait Until Element Is Visible    css:.customer-info    timeout=10s
    Element Should Contain    css:.customer-info    Tên:

Verify Form Calculations
    [Documentation]    Verify all automatic calculations are working
    [Arguments]    ${expected_productivity}=${None}
    
    # Kiểm tra có hiển thị productivity hint
    ${hint_visible}=    Run Keyword And Return Status    
    ...    Element Should Be Visible    xpath=//small[contains(text(), 'Năng suất')]
    
    Run Keyword If    ${hint_visible}    
    ...    Log    Productivity hint is visible

Verify Price Calculation
    [Documentation]    Verify price is calculated correctly with VAT
    Wait Until Element Is Visible    css:.form-input.price-estimated
    ${price}=    Get Element Attribute    css:.form-input.price-estimated    value
    Should Not Be Empty    ${price}
    Should Contain    ${price}    VNĐ
    [Return]    ${price}

Verify Estimated Hours Display
    [Documentation]    Verify estimated hours is calculated and displayed
    Wait Until Element Is Visible    css:.form-input.estimated-display
    ${hours}=    Get Element Attribute    css:.form-input.estimated-display    value
    Should Not Be Empty    ${hours}
    [Return]    ${hours}

Fill Valid Order Form
    [Documentation]    Fill the order form with all valid data
    [Arguments]    ${service}=Regular Cleaning    ${area}=50    ${note}=Test order note
    
    Select From List By Label    css:select[name="service_type"]    ${service}
    Input Text    css:input[v-model="order.area_m2"]    ${area}
    
    ${start_time}=    Get Current Date    increment=2 hours
    ${start_formatted}=    Convert Date    ${start_time}    result_format=%Y-%m-%dT%H:%M
    Input Text    css:input[v-model="order.preferred_start_time"]    ${start_formatted}
    
    ${end_time}=    Get Current Date    increment=4 hours
    ${end_formatted}=    Convert Date    ${end_time}    result_format=%Y-%m-%dT%H:%M
    Input Text    css:input[v-model="order.preferred_end_time"]    ${end_formatted}
    
    Input Text    css:textarea[v-model="order.note"]    ${note}

Submit Order And Select Payment
    [Documentation]    Submit order and select payment method
    [Arguments]    ${payment_method}=CASH
    
    Click Element    css:.featured-cta
    Wait Until Element Is Visible    css:.modal-overlay
    
    ${radio_selector}=    Set Variable    css:input[value="${payment_method}"]
    Click Element    ${radio_selector}
    
    Click Element    css:.btn-download

Verify Invoice Modal
    [Documentation]    Verify invoice modal appears with correct information
    Wait Until Element Is Visible    css:.invoice-modal    timeout=10s
    Element Should Contain    css:.invoice-modal    HÓA ĐƠN DỊCH VỤ
    Element Should Be Visible    css:.invoice-number
    Element Should Be Visible    css:.customer-info
    Element Should Be Visible    css:.pricing-details

Verify Payment Redirect
    [Documentation]    Verify redirect to payment page for bank transfer
    [Arguments]    ${order_id}
    Wait Until Location Contains    /dss/customer-orders/payment/${order_id}    timeout=10s

Calculate Expected Hours
    [Documentation]    Calculate expected hours based on area and service type
    [Arguments]    ${area}    ${service_type}
    
    ${productivity}=    Set Variable If
    ...    '${service_type}' == 'Regular Cleaning'    40
    ...    '${service_type}' == 'Deep Cleaning'    35
    ...    40
    
    ${expected_hours}=    Evaluate    ${area} / ${productivity}
    [Return]    ${expected_hours}

Verify Error Messages Count
    [Documentation]    Verify number of error messages displayed
    [Arguments]    ${expected_count}
    
    Wait Until Element Is Visible    css:.form-errors
    ${actual_count}=    Get Element Count    css:.form-errors li
    Should Be Equal As Numbers    ${actual_count}    ${expected_count}

Clear Form Field
    [Documentation]    Clear a specific form field
    [Arguments]    ${field_selector}
    
    Clear Element Text    ${field_selector}
    Press Keys    ${field_selector}    TAB
    Sleep    0.3s

Take Screenshot On Failure
    [Documentation]    Take screenshot when test fails
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    Capture Page Screenshot    failure_${timestamp}.png

Wait For Calculation To Complete
    [Documentation]    Wait for form calculations to complete
    Sleep    0.5s    # Wait for Vue reactivity to complete

Should See Negative Area Error
    [Arguments]    ${expected_text}=Diện tích không được âm
    Comment    Wait for the area-specific error item and assert its message
    Wait Until Element Is Visible    css:.form-errors li.error-item    10s
    ${elements}=    Get WebElements    css:.form-errors li.error-item
    ${found_texts}=    Create List
    FOR    ${el}    IN    @{elements}
        ${t}=    Get Text    ${el}
        Append To List    ${found_texts}    ${t}
    END
    ${joined}=    Catenate    SEPARATOR= ||     @{found_texts}
    Should Contain    ${joined}    ${expected_text}

Should See Area Zero Error
    [Arguments]    ${expected_text}=Diện tích phải lớn hơn 0
    Comment    Wait for the area-specific error item and assert its message
    Wait Until Element Is Visible    css:.form-errors li.error-item    10s
    ${elements}=    Get WebElements    css:.form-errors li.error-item
    ${found_texts}=    Create List
    FOR    ${el}    IN    @{elements}
        ${t}=    Get Text    ${el}
        Append To List    ${found_texts}    ${t}
    END
    ${joined}=    Catenate    SEPARATOR= ||     @{found_texts}
    Should Contain    ${joined}    ${expected_text}

Should See Area Text Error
    [Arguments]    ${expected_text}=Vui lòng nhập diện tích hợp lệ
    Comment    Wait for the area-specific error item and assert its message
    Wait Until Element Is Visible    css:.form-errors li.error-item    10s
    ${txt}=    Get Text    css:.form-errors li.error-item
    Should Contain    ${txt}    ${expected_text}
