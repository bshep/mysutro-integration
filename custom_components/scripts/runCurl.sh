
if [[ ! -f authFile ]]; then
    echo 'Please create "authFile" with contents "Authorization: Bearer TOKEN_GOES_HERE"'
    exit 
fi

echo 'Getting Schema' 
curl -H 'Content-Type: application/json' --compressed -H @authFile -X POST https://api.mysutro.com/graphql -d @querySchema > ./data/schemaOut.txt
echo 'Go to https://ivangoncharov.github.io/graphql-voyager/ to visualize it'
echo '------------------------'
echo 'Getting Historical Data to data/historicalReadings.txt'
curl -H 'Content-Type: application/json' --compressed -H @authFile -X POST https://api.mysutro.com/graphql -d @querySchema > ./data/historicalReadings.txt
