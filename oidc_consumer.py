import requests
import jwt
from jwt import PyJWKClient

ISSUER = "http://localhost:8000"
AUDIENCE = "my-demo-app"

# 1. Read the OIDC discovery document
discovery_url = f"{ISSUER}/.well-known/openid-configuration"

print("Fetching discovery document...")
discovery = requests.get(discovery_url).json()

print("Discovery document:")
print(discovery)

# 2. Get the JWKS URI from the discovery document
jwks_uri = discovery["jwks_uri"]

print("\nJWKS endpoint found:")
print(jwks_uri)

# 3. Request an ID token from the issuer
print("\nRequesting ID token...")
token_response = requests.get(f"{ISSUER}/token").json()
id_token = token_response["id_token"]

print("\nReceived JWT:")
print(id_token)

# 4. Use the JWKS endpoint to find the public key for this token
print("\nFetching public key from JWKS endpoint...")
jwk_client = PyJWKClient(jwks_uri)
signing_key = jwk_client.get_signing_key_from_jwt(id_token)

# 5. Validate the token
print("\nValidating token signature and claims...")

claims = jwt.decode(
    id_token,
    signing_key.key,
    algorithms=["RS256"],
    audience=AUDIENCE,
    issuer=ISSUER
)

print("\nToken is valid.")
print("Trusted claims:")
print(claims)
