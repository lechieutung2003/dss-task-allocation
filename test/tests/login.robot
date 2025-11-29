*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

*** Test Cases ***


[Module 2-1]Login with a email empty
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Empty
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    This is required field.
    Close Browser    


[Module 2-2]Login with a email wrong @
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Format Wrong @
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid email format.
    Close Browser   

[Module 2-3]Login with a email wrong space
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Format Wrong Space
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid email format.
    Close Browser  

[Module 2-4]Login with a email wrong g.c
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Format Wrong g.c
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid email format.
    Close Browser    


[Module 2-5]Login with a email too long
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Format Wrong Too Long
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Email too long
    Close Browser  

[Module 2-6]Login with a email not exist
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Not Exist
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear     The user does not exist.

    Close Browser  

[Module 2-7]Login with a password empty
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Password Empty
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    This is required field.
    Close Browser

[Module 2-8]Login with a password too short
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Password Format Wrong Too Short
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Password must be more than 6 characters
    Close Browser    

[Module 2-9]Login with a password too long
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Password Format Wrong Too Long
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Password too long
    Close Browser 

[Module 2-10]Login with a password too space
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Password Format Wrong Space
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid Password format.
    Close Browser  

[Module 2-11]Login with a password wrong @
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Password Format Wrong @
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid Password format.
    Close Browser    

[Module 2-12]Log in with a valid email and password
    [Tags]    Login    valid

    Open Browser To Login Page
    Enter Login Info Correct
    Check Logo Is Displayed
    Location Should Be     http://127.0.0.1:3008/dss/home
    Wait Until Element Is Visible    xpath=//h1[@class="hero-title"]    timeout=10s
    Check Text At XPath              //h1[@class="hero-title"]    Discover and Experience
    Wait Until Element Is Visible    xpath=//h2[@class="hero-subtitle"]    timeout=10s
    Check Text At XPath              //h2[@class="hero-subtitle"]    Professional Cleaning Services
    Wait Until Page Contains Element    xpath=//span[contains(text(),'About Us')]    10s
    Wait Until Page Contains Element    xpath=//span[contains(text(),'Services')]    10s
    Wait Until Page Contains Element    xpath=//span[contains(text(),'Contact')]    10s
    Wait Until Page Contains Element    xpath=//span[contains(text(),'Orders')]    10s
    Wait Until Page Contains Element    xpath=//span[contains(text(),'Create Order')]    10s
    Close Browser    

[Module 2-13]Login with email and password empty
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email and Password Empty
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    This is required field.
    Close Browser    

[Module 2-14]Login with email empty @ and password empty
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email and Password Empty
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid email format.
    Check Error Message Should Appear span    This is required field.
    Close Browser    

[Module 2-15]Login with email wrong g.c and password too short
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Wrong g.c and Password Too Short
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid Password format.
    Check Error Message Should Appear span    Password must be more than 6 characters
    Close Browser    

[Module 2-16]Login with email too long and password correct
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Email Too Long and Password Correct
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Email too long
    Close Browser 

[Module 2-17]Login with special email and password 
    [Tags]    Login    invalid

    Open Browser To Login Page
    Enter Login Special Email and Password 
    Location Should Be     http://127.0.0.1:3008/
    Check Error Message Should Appear span    Invalid Password format.
    Close Browser    
