*** Variables ***
${URL_LOGIN}                http://127.0.0.1:3008/
${URL_SIGNUP}               http://127.0.0.1:3008/signup
${BROWSER}                  Chrome

${VALID_EMAIL}        thao@gmail.com
${INVALID_EMAIL_1}    thaogmail.com
${INVALID_EMAIL_2}    thao@ gmail.com
${INVALID_EMAIL_3}    thao@g.c
${INVALID_EMAIL_4}    
${INVALID_EMAIL_5}    thao1234567891234567891234567891234567891@gmail.com
${INVALID_EMAIL_6}    thu@gmail.com


${VALID_PASSWORD}      123456
${INVALID_PASSWORD_1}  123455
${INVALID_PASSWORD_2}  123456789012345678901
${INVALID_PASSWORD_3}  123 123
${INVALID_PASSWORD_4}  12345 
${INVALID_PASSWORD_5}   
${INVALID_PASSWORD_6}  123@@@123