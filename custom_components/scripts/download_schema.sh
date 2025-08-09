#!/bin/bash
# Download the latest GraphQL schema from the Sutro API
# Usage: ./download_schema.sh <API_URL> <AUTH_TOKEN>

API_URL=${1:-"https://api.mysutro.com/graphql"}
AUTH_TOKEN=${2:-""}

OUTPUT_FILE="schema.graphql"

if [ -z "$AUTH_TOKEN" ]; then
  echo "Usage: $0 <API_URL> <AUTH_TOKEN>"
  echo "Example: $0 https://api.mysutro.com/graphql <your_token>"
  exit 1
fi

# # Download the schema using introspection
# echo "Downloading schema from $API_URL..."
# curl -s -H "Authorization: Bearer $AUTH_TOKEN" \
#      -H "Content-Type: application/json" \
#      --data '{"query": "query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description locations args { ...InputValue } } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }"}' \
#      "$API_URL" > introspection.json
  
echo "Attempting Node.js conversion from introspection.json..."
# Create a Node.js script to convert introspection.json to schema.graphql
cat > introspection_to_sdl.js <<'EOF'
const fs = require('fs');
const { printSchema, buildClientSchema } = require('graphql');
const introspection = JSON.parse(fs.readFileSync('introspection.json', 'utf8'));
const schema = buildClientSchema(introspection.data ? introspection.data : introspection);
const sdl = printSchema(schema);
fs.writeFileSync('schema.graphql', sdl);
console.log('schema.graphql written from introspection.json');
EOF
if command -v npm >/dev/null 2>&1; then
    npm install graphql >/dev/null 2>&1
    node introspection_to_sdl.js && echo "Schema written to schema.graphql using Node.js."
else
    echo "npm not found. Please install Node.js and npm, or use an online tool to convert introspection.json to SDL."
fi

