*** Settings ***
Documentation    Test Cases cho luồng tạo đơn hàng - Negative Scenarios
...              Test tất cả các trường hợp validation lỗi theo yêu cầu
Library          SeleniumLibrary
Library          DateTime
Library          String
Resource         ../resources/common.robot
Resource         ../resources/create_order_keywords.robot
Suite Setup      Open Browser To Create Order Page
Suite Teardown   Close Browser
Test Setup       Reset Form


*** Variables ***
${CREATE_ORDER_URL}    ${BASE_URL}/dss/orders/create
${SERVICE_SELECTOR}    css:select[name="service_type"]
${AREA_INPUT}          css:input[v-model="order.area_m2"]
${START_TIME_INPUT}    css:input[v-model="order.preferred_start_time"]
${END_TIME_INPUT}      css:input[v-model="order.preferred_end_time"]
${NOTE_INPUT}          css:textarea[v-model="order.note"]
${SUBMIT_BUTTON}       css:.featured-cta
${ERROR_MESSAGE}       css:.error-message
${FORM_ERRORS}         css:.form-errors


*** Test Cases ***
#=============================================================================
# TEST CASES - DỊCH VỤ (Service Type)
#=============================================================================

TC_SERVICE_001 - Không chọn dịch vụ
    [Documentation]    Kiểm tra validation khi không chọn dịch vụ
    [Tags]    negative    service    required
    
    # Bỏ qua trường dịch vụ, nhập các trường khác
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    # Thử submit
    Click Submit Button
    
    # Verify lỗi
    Wait Until Element Is Visible    ${FORM_ERRORS}
    Element Should Contain    ${FORM_ERRORS}    Vui lòng chọn loại dịch vụ


TC_SERVICE_002 - Kiểm tra danh sách dịch vụ từ hệ thống
    [Documentation]    Verify hệ thống load đúng list dịch vụ từ API
    [Tags]    positive    service    api
    
    Wait Until Element Is Visible    ${SERVICE_SELECTOR}
    ${service_count}=    Get Element Count    ${SERVICE_SELECTOR} option
    
    # Phải có ít nhất 1 option placeholder + các dịch vụ
    Should Be True    ${service_count} > 1
    
    # Verify có các dịch vụ mong đợi
    Page Should Contain Element    xpath=//option[contains(text(), 'Regular Cleaning')]
    Page Should Contain Element    xpath=//option[contains(text(), 'Deep Cleaning')]


#=============================================================================
# TEST CASES - TIỀN (Price)
#=============================================================================

TC_PRICE_001 - Tự động tính giá khi chọn dịch vụ Regular Cleaning
    [Documentation]    Kiểm tra giá được tự động generate theo dịch vụ
    [Tags]    positive    price    calculation
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    
    # Verify giá per m2 hiển thị
    Wait Until Element Is Visible    css:.form-input.price-display
    ${price_text}=    Get Element Attribute    css:.form-input.price-display    value
    Should Not Be Empty    ${price_text}
    Should Contain    ${price_text}    VNĐ


TC_PRICE_002 - Tự động tính giá khi chọn dịch vụ Deep Cleaning
    [Documentation]    Kiểm tra giá được tự động generate theo dịch vụ Deep Cleaning
    [Tags]    positive    price    calculation
    
    Select Service Type    Deep Cleaning
    Input Valid Area    50
    
    # Verify giá per m2 hiển thị
    Wait Until Element Is Visible    css:.form-input.price-display
    ${price_text}=    Get Element Attribute    css:.form-input.price-display    value
    Should Not Be Empty    ${price_text}
    Should Contain    ${price_text}    VNĐ


TC_PRICE_003 - Tính tổng tiền với VAT 10%
    [Documentation]    Verify tổng tiền bao gồm VAT 10%
    [Tags]    positive    price    calculation
    
    Select Service Type    Regular Cleaning
    Input Valid Area    100
    Select Future Start Time    hours=2
    Select Future End Time    hours=5
    
    # Verify estimated price hiển thị với VAT
    Wait Until Element Is Visible    css:.form-input.price-estimated
    ${price_text}=    Get Element Attribute    css:.form-input.price-estimated    value
    Should Contain    ${price_text}    VNĐ
    
    # Verify price explanation chứa thông tin VAT
    Wait Until Element Contains    css:.form-hint    VAT 10%


TC_PRICE_004 - Áp dụng hệ số khi thời gian yêu cầu < thời gian ước tính
    [Documentation]    Verify áp dụng hệ số phạt khi requested_hours < estimated_hours
    [Tags]    positive    price    calculation    penalty
    
    Select Service Type    Regular Cleaning
    Input Valid Area    100
    
    # Tính: 100m2 / 40 m2/h = 2.5h ước tính
    # Chọn thời gian yêu cầu < 2.5h để trigger hệ số
    Select Future Start Time    hours=2
    Select Future End Time    hours=3.5
    # requested = 1.5h, estimated = 2.5h, diff = 1h → hệ số 1.2
    
    # Verify có thông báo áp dụng hệ số
    Wait Until Element Contains    css:.form-hint    hệ số


#=============================================================================
# TEST CASES - THỜI GIAN BẮT ĐẦU (Start Time)
#=============================================================================

TC_STARTTIME_001 - Không nhập thời gian bắt đầu
    [Documentation]    Kiểm tra validation khi không nhập thời gian bắt đầu
    [Tags]    negative    starttime    required
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    # Bỏ qua start time
    Select Future End Time    hours=4
    
    Click Submit Button
    
    Wait Until Element Is Visible    ${FORM_ERRORS}
    Element Should Contain    ${FORM_ERRORS}    Vui lòng chọn thời gian bắt đầu


TC_STARTTIME_002 - Thời gian bắt đầu trước hiện tại đúng 1 tiếng
    [Documentation]    Thời gian bắt đầu phải sau hiện tại ít nhất 1 tiếng
    [Tags]    negative    starttime    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    
    # Chọn thời gian hiện tại + 59 phút (< 1 tiếng)
    ${invalid_time}=    Get Time In Future    minutes=59
    Input Text    ${START_TIME_INPUT}    ${invalid_time}
    
    Select Future End Time    hours=4
    
    # Trigger validation
    Click Element    ${AREA_INPUT}
    
    # Verify lỗi validation
    Wait Until Element Is Visible    css:.error-message
    Element Should Contain    css:.error-message    phải cách thời điểm hiện tại ít nhất 1 tiếng


TC_STARTTIME_003 - Thời gian bắt đầu chính xác sau 1 tiếng (Boundary Value)
    [Documentation]    Test boundary value - đúng 1 tiếng sau hiện tại
    [Tags]    positive    starttime    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    
    # Chọn thời gian hiện tại + đúng 60 phút
    ${valid_time}=    Get Time In Future    minutes=60
    Input Text    ${START_TIME_INPUT}    ${valid_time}
    
    Select Future End Time    hours=4
    
    # Không có lỗi
    Element Should Not Be Visible    xpath=//div[contains(@class, 'error-message') and contains(text(), 'thời gian bắt đầu')]


TC_STARTTIME_004 - Thời gian bắt đầu trong quá khứ
    [Documentation]    Thời gian bắt đầu là thời điểm đã qua
    [Tags]    negative    starttime    validation
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    
    # Chọn thời gian trong quá khứ
    ${past_time}=    Get Time In Past    hours=2
    Input Text    ${START_TIME_INPUT}    ${past_time}
    
    Select Future End Time    hours=4
    
    # Trigger validation
    Click Element    ${AREA_INPUT}
    
    # Verify lỗi validation
    Wait Until Element Is Visible    css:.error-message
    Element Should Contain    css:.error-message    phải cách thời điểm hiện tại ít nhất 1 tiếng


#=============================================================================
# TEST CASES - THỜI GIAN KẾT THÚC (End Time)
#=============================================================================

TC_ENDTIME_001 - Không nhập thời gian kết thúc
    [Documentation]    Kiểm tra validation khi không nhập thời gian kết thúc
    [Tags]    negative    endtime    required
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    # Bỏ qua end time
    
    Click Submit Button
    
    Wait Until Element Is Visible    ${FORM_ERRORS}
    Element Should Contain    ${FORM_ERRORS}    Vui lòng chọn thời gian kết thúc


TC_ENDTIME_002 - Thời gian kết thúc bằng thời gian bắt đầu
    [Documentation]    End time = Start time (không hợp lệ)
    [Tags]    negative    endtime    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    
    ${start_time}=    Get Time In Future    hours=2
    Input Text    ${START_TIME_INPUT}    ${start_time}
    Input Text    ${END_TIME_INPUT}    ${start_time}
    
    # Trigger validation
    Click Element    ${AREA_INPUT}
    
    Wait Until Element Contains    ${ERROR_MESSAGE}    Thời gian kết thúc phải sau thời gian bắt đầu


TC_ENDTIME_003 - Thời gian kết thúc trước thời gian bắt đầu
    [Documentation]    End time < Start time
    [Tags]    negative    endtime    validation
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    
    ${start_time}=    Get Time In Future    hours=4
    ${end_time}=    Get Time In Future    hours=3
    
    Input Text    ${START_TIME_INPUT}    ${start_time}
    Input Text    ${END_TIME_INPUT}    ${end_time}
    
    # Trigger validation
    Click Element    ${AREA_INPUT}
    
    Wait Until Element Contains    ${ERROR_MESSAGE}    Thời gian kết thúc phải sau thời gian bắt đầu


TC_ENDTIME_004 - Thời gian kết thúc sau bắt đầu 1 phút (Boundary Value)
    [Documentation]    End time = Start time + 1 phút (hợp lệ)
    [Tags]    positive    endtime    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    
    ${start_time}=    Get Time In Future    hours=2
    ${end_time}=    Add Time To Date    ${start_time}    1 minute
    
    Input Text    ${START_TIME_INPUT}    ${start_time}
    Input Text    ${END_TIME_INPUT}    ${end_time}
    
    # Không có lỗi
    Element Should Not Be Visible    xpath=//div[contains(@class, 'error-message') and contains(text(), 'kết thúc')]


TC_ENDTIME_005 - Thời gian làm việc < 60% thời gian ước tính
    [Documentation]    Requested hours < 60% estimated hours
    [Tags]    negative    endtime    validation    business_rule
    
    Select Service Type    Regular Cleaning
    Input Valid Area    100
    # Estimated: 100/40 = 2.5h
    # Min required: 2.5 * 0.6 = 1.5h
    
    ${start_time}=    Get Time In Future    hours=2
    ${end_time}=    Add Time To Date    ${start_time}    1 hour
    # Requested: 1h < 1.5h min required
    
    Input Text    ${START_TIME_INPUT}    ${start_time}
    Input Text    ${END_TIME_INPUT}    ${end_time}
    
    Click Submit Button
    
    # Verify lỗi về thời gian tối thiểu
    Wait Until Element Is Visible    css:.error-message
    Element Should Contain    css:.error-message    60%


#=============================================================================
# TEST CASES - SỐ M2 (Area)
#=============================================================================

TC_AREA_001 - Không nhập diện tích
    [Documentation]    Kiểm tra validation khi không nhập diện tích
    [Tags]    negative    area    required
    
    Select Service Type    Regular Cleaning
    # Bỏ qua area
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    Click Submit Button
    
    Wait Until Element Is Visible    ${FORM_ERRORS}
    Element Should Contain    ${FORM_ERRORS}    Vui lòng nhập diện tích hợp lệ


TC_AREA_002 - Nhập diện tích = 0
    [Documentation]    Diện tích bằng 0 không hợp lệ
    [Tags]    negative    area    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Text    ${AREA_INPUT}    0
    
    # Trigger validation
    Press Keys    ${AREA_INPUT}    TAB
    
    Wait Until Element Contains    ${ERROR_MESSAGE}    Diện tích phải lớn hơn 0


TC_AREA_003 - Nhập diện tích âm
    [Documentation]    Diện tích âm không hợp lệ
    [Tags]    negative    area    validation
    
    Select Service Type    Regular Cleaning
    Input Text    ${AREA_INPUT}    -50
    
    # Trigger validation
    Press Keys    ${AREA_INPUT}    TAB
    
    Wait Until Element Contains    ${ERROR_MESSAGE}    Diện tích không được âm


TC_AREA_004 - Nhập diện tích không phải số (text)
    [Documentation]    Input text thay vì số
    [Tags]    negative    area    validation    datatype
    
    Select Service Type    Regular Cleaning
    
    # Thử nhập text
    Input Text    ${AREA_INPUT}    abc
    
    # HTML5 input type="number" sẽ không cho nhập text
    ${value}=    Get Value    ${AREA_INPUT}
    Should Be Equal    ${value}    ${EMPTY}


TC_AREA_005 - Nhập diện tích không phải số (ký tự đặc biệt)
    [Documentation]    Input ký tự đặc biệt
    [Tags]    negative    area    validation    datatype
    
    Select Service Type    Regular Cleaning
    
    Input Text    ${AREA_INPUT}    @#$%
    
    ${value}=    Get Value    ${AREA_INPUT}
    Should Be Equal    ${value}    ${EMPTY}


TC_AREA_006 - Nhập diện tích rất lớn (boundary)
    [Documentation]    Test với giá trị rất lớn
    [Tags]    negative    area    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Text    ${AREA_INPUT}    999999999
    
    Select Future Start Time    hours=2
    Select Future End Time    hours=100
    
    # Có thể có lỗi business logic hoặc chấp nhận
    # Kiểm tra hệ thống xử lý như thế nào
    ${submit_enabled}=    Run Keyword And Return Status    Element Should Be Enabled    ${SUBMIT_BUTTON}
    Log    Submit button enabled: ${submit_enabled}


TC_AREA_007 - Nhập diện tích nhỏ nhất (0.01)
    [Documentation]    Test với giá trị nhỏ nhất có thể (boundary)
    [Tags]    positive    area    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Text    ${AREA_INPUT}    0.01
    
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    # Không có lỗi validation
    Element Should Not Be Visible    xpath=//div[contains(@class, 'error-message') and contains(text(), 'Diện tích')]


TC_AREA_008 - Nhập diện tích số thập phân
    [Documentation]    Test với số thập phân hợp lệ
    [Tags]    positive    area    validation
    
    Select Service Type    Regular Cleaning
    Input Text    ${AREA_INPUT}    45.75
    
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    # Không có lỗi validation
    Element Should Not Be Visible    xpath=//div[contains(@class, 'error-message') and contains(text(), 'Diện tích')]


TC_AREA_009 - Nhập diện tích với nhiều dấu chấm
    [Documentation]    Test với format số không hợp lệ
    [Tags]    negative    area    validation    datatype
    
    Select Service Type    Regular Cleaning
    Input Text    ${AREA_INPUT}    12.34.56
    
    # HTML5 validation hoặc JS validation sẽ catch
    ${value}=    Get Value    ${AREA_INPUT}
    Should Not Contain    ${value}    ..


#=============================================================================
# TEST CASES - GHI CHÚ (Note)
#=============================================================================

TC_NOTE_001 - Không nhập ghi chú (optional field)
    [Documentation]    Ghi chú là trường không bắt buộc
    [Tags]    positive    note    optional
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    # Bỏ qua note
    
    Click Submit Button
    
    # Không có lỗi, modal payment hiển thị
    Wait Until Element Is Visible    css:.modal-overlay


TC_NOTE_002 - Nhập ghi chú đúng 50 từ (boundary)
    [Documentation]    Boundary value - đúng max 50 từ
    [Tags]    positive    note    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    ${note_50_words}=    Generate Words    50
    Input Text    ${NOTE_INPUT}    ${note_50_words}
    
    # Trigger validation
    Press Keys    ${NOTE_INPUT}    TAB
    
    # Không có lỗi
    Element Should Not Be Visible    xpath=//div[contains(@class, 'error-message') and contains(text(), 'Ghi chú')]


TC_NOTE_003 - Nhập ghi chú 51 từ (vượt quá giới hạn)
    [Documentation]    Vượt quá max 50 từ
    [Tags]    negative    note    validation    boundary
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    ${note_51_words}=    Generate Words    51
    Input Text    ${NOTE_INPUT}    ${note_51_words}
    
    # Trigger validation
    Press Keys    ${NOTE_INPUT}    TAB
    
    Wait Until Element Contains    ${ERROR_MESSAGE}    Ghi chú chỉ được tối đa 50 từ


TC_NOTE_004 - Nhập ghi chú 100 từ
    [Documentation]    Nhập ghi chú nhiều hơn nhiều
    [Tags]    negative    note    validation
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    ${note_100_words}=    Generate Words    100
    Input Text    ${NOTE_INPUT}    ${note_100_words}
    
    Press Keys    ${NOTE_INPUT}    TAB
    
    Wait Until Element Contains    ${ERROR_MESSAGE}    hiện tại: 100 từ


TC_NOTE_005 - Nhập ghi chú với ký tự đặc biệt
    [Documentation]    Test với ký tự đặc biệt, emoji
    [Tags]    positive    note    validation    special_chars
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    Input Text    ${NOTE_INPUT}    Ghi chú với @#$% & ký tự đặc biệt 😊 emoji
    
    # Chấp nhận ký tự đặc biệt nếu không vượt quá 50 từ
    Element Should Not Be Visible    xpath=//div[contains(@class, 'error-message') and contains(text(), 'Ghi chú')]


TC_NOTE_006 - Nhập ghi chú chỉ có khoảng trắng
    [Documentation]    Ghi chú chỉ toàn space
    [Tags]    negative    note    validation    edge_case
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    
    Input Text    ${NOTE_INPUT}    ${SPACE * 20}
    
    Press Keys    ${NOTE_INPUT}    TAB
    
    # Hệ thống tính word count = 0 (không có từ thực sự)
    Element Should Not Be Visible    xpath=//div[contains(@class, 'error-message') and contains(text(), 'Ghi chú')]


#=============================================================================
# TEST CASES - TỔNG HỢP (Multiple Fields)
#=============================================================================

TC_COMBINED_001 - Tất cả các trường đều để trống
    [Documentation]    Test khi submit form hoàn toàn trống
    [Tags]    negative    combined    required
    
    Click Submit Button
    
    Wait Until Element Is Visible    ${FORM_ERRORS}
    
    # Verify tất cả lỗi bắt buộc
    Element Should Contain    ${FORM_ERRORS}    Vui lòng chọn loại dịch vụ
    Element Should Contain    ${FORM_ERRORS}    Vui lòng nhập diện tích hợp lệ
    Element Should Contain    ${FORM_ERRORS}    Vui lòng chọn thời gian bắt đầu
    Element Should Contain    ${FORM_ERRORS}    Vui lòng chọn thời gian kết thúc


TC_COMBINED_002 - Tất cả các trường hợp lệ - Happy path
    [Documentation]    Test case thành công với tất cả input hợp lệ
    [Tags]    positive    combined    happy_path
    
    Select Service Type    Regular Cleaning
    Input Valid Area    50
    Select Future Start Time    hours=2
    Select Future End Time    hours=4
    Input Text    ${NOTE_INPUT}    Đây là ghi chú hợp lệ
    
    Click Submit Button
    
    # Payment modal xuất hiện
    Wait Until Element Is Visible    css:.modal-overlay
    Element Should Contain    css:.modal-content    Chọn phương thức thanh toán


TC_COMBINED_003 - Nhiều lỗi validation cùng lúc
    [Documentation]    Test hiển thị nhiều lỗi khi có nhiều field invalid
    [Tags]    negative    combined
    
    Select Service Type    Regular Cleaning
    Input Text    ${AREA_INPUT}    -10
    
    ${past_time}=    Get Time In Past    hours=1
    Input Text    ${START_TIME_INPUT}    ${past_time}
    Input Text    ${END_TIME_INPUT}    ${past_time}
    
    ${note_100_words}=    Generate Words    100
    Input Text    ${NOTE_INPUT}    ${note_100_words}
    
    Click Submit Button
    
    # Verify có nhiều lỗi
    Wait Until Element Is Visible    ${FORM_ERRORS}
    ${error_count}=    Get Element Count    ${FORM_ERRORS} li
    Should Be True    ${error_count} > 1


TC_COMBINED_004 - Button disable khi form invalid
    [Documentation]    Verify button bị disable khi form không hợp lệ
    [Tags]    negative    combined    ui
    
    # Form chưa điền đầy đủ
    Select Service Type    Regular Cleaning
    
    # Button nên bị disable hoặc hiển thị text báo lỗi
    ${button_text}=    Get Text    ${SUBMIT_BUTTON}
    Should Not Be Equal    ${button_text}    Tạo đơn hàng
    
    # Hoặc kiểm tra disabled attribute
    ${is_disabled}=    Get Element Attribute    ${SUBMIT_BUTTON}    disabled
    Should Not Be Empty    ${is_disabled}


*** Keywords ***
Open Browser To Create Order Page
    Open Browser    ${CREATE_ORDER_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.3
    Wait Until Page Contains    Tạo đơn hàng mới    timeout=10s
    Wait Until Element Is Visible    ${SERVICE_SELECTOR}    timeout=10s

Reset Form
    Reload Page
    Wait Until Element Is Visible    ${SERVICE_SELECTOR}    timeout=10s

Select Service Type
    [Arguments]    ${service_name}
    Wait Until Element Is Visible    ${SERVICE_SELECTOR}
    Select From List By Label    ${SERVICE_SELECTOR}    ${service_name}
    Sleep    0.5s    # Wait for calculations

Input Valid Area
    [Arguments]    ${area}
    Wait Until Element Is Visible    ${AREA_INPUT}
    Input Text    ${AREA_INPUT}    ${area}
    Sleep    0.3s    # Wait for calculations

Select Future Start Time
    [Arguments]    ${hours}=2
    ${time}=    Get Time In Future    hours=${hours}
    Input Text    ${START_TIME_INPUT}    ${time}
    Sleep    0.3s

Select Future End Time
    [Arguments]    ${hours}=4
    ${time}=    Get Time In Future    hours=${hours}
    Input Text    ${END_TIME_INPUT}    ${time}
    Sleep    0.3s

Click Submit Button
    Wait Until Element Is Enabled    ${SUBMIT_BUTTON}
    Click Element    ${SUBMIT_BUTTON}
    Sleep    0.5s

Get Time In Future
    [Arguments]    ${hours}=0    ${minutes}=0
    ${current}=    Get Current Date
    ${future}=    Add Time To Date    ${current}    ${hours} hour ${minutes} minutes
    ${formatted}=    Convert Date    ${future}    result_format=%Y-%m-%dT%H:%M
    [Return]    ${formatted}

Get Time In Past
    [Arguments]    ${hours}=0    ${minutes}=0
    ${current}=    Get Current Date
    ${past}=    Subtract Time From Date    ${current}    ${hours} hour ${minutes} minutes
    ${formatted}=    Convert Date    ${past}    result_format=%Y-%m-%dT%H:%M
    [Return]    ${formatted}

Generate Words
    [Arguments]    ${count}
    ${words}=    Create List
    FOR    ${i}    IN RANGE    ${count}
        Append To List    ${words}    word${i}
    END
    ${text}=    Catenate    SEPARATOR=${SPACE}    @{words}
    [Return]    ${text}
