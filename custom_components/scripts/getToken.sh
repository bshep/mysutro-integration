USERNAME='YOUR_USERNAME_HERE'
PASSWORD='YOUR_PASSWORD_HERE'

if ! command -v jq &> /dev/null; then
    echo '"jq" command not installed'
    exit -1
fi

curl -s -H 'Content-Type: application/json' -H 'Connection: keep-alive' -H 'Accept: */*' -H 'User-Agent: Sutro/348 CFNetwork/1333.0.4 Darwin/21.5.0' -H 'Accept-Language: en-US,en;q=0.9' --compressed -X POST https://api.mysutro.com/graphql -d '{"operationName":null,"variables":{"email":"'$USERNAME'","password":"'$PASSWORD'","focusedInput":"","loading":false},"query":"mutation ($email: String!, $password: String!) {\n  login(email: $email, password: $password) {\n    user {\n      firstName\n      lastName\n      email\n      phone\n      releaseGroup\n      __typename\n    }\n    token\n    __typename\n  }\n}\n"}' | jq -r .data.login.token
