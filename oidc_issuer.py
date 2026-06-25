from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

ISSUER = "http://localhost:8000"
AUDIENCE = "my-demo-app"
KEY_ID = "demo-key-1"

# Generate an RSA key pair.
# In real systems, the private key is stored securely and rotated carefully.
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()


def public_jwk():
    """
    Return the public key in JWKS format.
    This is what the consumer uses to verify the JWT signature.
    """
    jwk_json = jwt.algorithms.RSAAlgorithm.to_jwk(public_key)
    jwk = json.loads(jwk_json)

    jwk["kid"] = KEY_ID
    jwk["use"] = "sig"
    jwk["alg"] = "RS256"

    return jwk


def issue_token():
    """
    Create a signed JWT.
    This is our simple 'hall pass'.
    """
    now = int(time.time())

    claims = {
        "iss": ISSUER,
        "sub": "student:gayatri",
        "aud": AUDIENCE,
        "iat": now,
        "exp": now + 300,
        "name": "Gayatri"
    }

    token = jwt.encode(
        claims,
        private_key,
        algorithm="RS256",
        headers={"kid": KEY_ID}
    )

    return token


class OIDCHandler(BaseHTTPRequestHandler):
    def send_json(self, data):
        response = json.dumps(data, indent=2).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if self.path == "/.well-known/openid-configuration":
            self.send_json({
                "issuer": ISSUER,
                "jwks_uri": f"{ISSUER}/discovery/keys",
                "id_token_signing_alg_values_supported": ["RS256"],
                "claims_supported": [
                    "iss",
                    "sub",
                    "aud",
                    "iat",
                    "exp",
                    "name"
                ]
            })

        elif self.path == "/discovery/keys":
            self.send_json({
                "keys": [
                    public_jwk()
                ]
            })

        elif self.path == "/token":
            self.send_json({
                "id_token": issue_token()
            })

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), OIDCHandler)

    print("Simple OIDC issuer running at http://localhost:8000")
    print("Discovery document:")
    print("  http://localhost:8000/.well-known/openid-configuration")
    print("JWKS endpoint:")
    print("  http://localhost:8000/discovery/keys")
    print("Token endpoint:")
    print("  http://localhost:8000/token")

    server.serve_forever()
