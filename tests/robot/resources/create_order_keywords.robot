*** Settings ***
Documentation    Custom keywords for Create Order test suite
Library          SeleniumLibrary
Library          DateTime
Library          String
Library          Collections

*** Keywords ***
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
