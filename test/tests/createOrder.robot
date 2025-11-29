*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

*** Test Cases ***


[Module 3-1]Create Order With Valid Data
	[Tags]    CreateOrder    valid

	Open Browser To Login Page
	Enter Login Info Correct
	Go To    http://127.0.0.1:3008/dss/orders/create
	Wait Until Element Is Visible    css=h1.section-title    10s
	Wait For Service Options    15s
    Select From List By Index    css=select[data-qa="service-select"]    1
    Set Number Input Value    css=input[data-qa="area-input"]    100
    Execute JavaScript    var s = '2025-12-04T10:00'; var el = document.querySelector('input[data-qa="start-input"]'); el.value = s; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));
    Execute JavaScript    var e = '2025-12-04T13:00'; var el2 = document.querySelector('input[data-qa="end-input"]'); el2.value = e; el2.dispatchEvent(new Event('input',{bubbles:true})); el2.dispatchEvent(new Event('change',{bubbles:true}));
    Input Text    css=textarea[data-qa="note-input"]    Test order from Robot Framework
    Wait Until Keyword Succeeds    15s    1s    Execute JavaScript    if (!(document.querySelector('input[data-qa="start-input"]').value && document.querySelector('input[data-qa="end-input"]').value && document.querySelectorAll('.form-errors .error-item').length===0 && document.querySelectorAll('.error-message').length===0)) { throw 'Form not valid yet'; } else { return true; }
    Execute JavaScript    var d = document.querySelector('nuxt-devtools-frame'); if (d) d.style.display='none'; document.querySelector('button[data-qa="create-order-cta"]').disabled = false; document.querySelector('button[data-qa="create-order-cta"]').click();
	
	Close Browser


[Module 3-2]Create Order With Negative Area
	[Tags]    CreateOrder    valid

	Open Browser To Login Page
	Enter Login Info Correct
	Go To    http://127.0.0.1:3008/dss/orders/create
	Wait Until Element Is Visible    css=h1.section-title    10s

	Wait For Service Options    15s
    Select From List By Index    css=select[data-qa="service-select"]    1

    # Fill area (number input)
    Set Number Input Value    css=input[data-qa="area-input"]    -1

    Should See Negative Area Error
	Close Browser

[Module 3-3]Create Order With Zero Area
	[Tags]    CreateOrder    valid

	Open Browser To Login Page
	Enter Login Info Correct
	Go To    http://127.0.0.1:3008/dss/orders/create
	Wait Until Element Is Visible    css=h1.section-title    10s

	Wait For Service Options    15s
    Select From List By Index    css=select[data-qa="service-select"]    1

    # Fill area (number input)
    Set Number Input Value    css=input[data-qa="area-input"]    0

    Should See Area Zero Error
	Close Browser

[Module 3-4]Create Order With Text Area
	[Tags]    CreateOrder    valid

	Open Browser To Login Page
	Enter Login Info Correct
	Go To    http://127.0.0.1:3008/dss/orders/create
	Wait Until Element Is Visible    css=h1.section-title    10s

	Wait For Service Options    15s
    Select From List By Index    css=select[data-qa="service-select"]    1

    # Fill area (number input)
    Set Number Input Value    css=input[data-qa="area-input"]    abc

    Should See Area Text Error
	Close Browser
