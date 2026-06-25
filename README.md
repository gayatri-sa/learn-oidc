# Simple OIDC Demo

This is a small, beginner-friendly demo that shows how the main OIDC pieces fit together.

It is not a production OIDC implementation. It is only meant to explain the flow between:

- an OIDC issuer
- a discovery document
- a JWKS endpoint
- a signed JWT token
- an OIDC consumer / receiver

## Files

```text
oidc_issuer.py
oidc_consumer.py
README.md
```

## What This Demo Shows

This demo shows the basic OIDC flow in a very small setup.

```text
OIDC issuer
  ├─ publishes a discovery document
  ├─ publishes public keys through a JWKS endpoint
  └─ issues a signed JWT token

OIDC consumer
  ├─ reads the discovery document
  ├─ finds the jwks_uri
  ├─ fetches the public key from the JWKS endpoint
  ├─ validates the JWT signature
  └─ trusts the claims only after validation
```

In the school/treehouse analogy:

```text
OIDC issuer        = the school
JWT token          = the signed hall pass
JWKS endpoint      = the public noticeboard with the signature
OIDC consumer      = the treehouse guard
Temporary access   = entry into the treehouse for a short time
```

## Requirements

Install the required Python packages:

```bash
pip install pyjwt cryptography requests
```

## 1. Start the OIDC Issuer

Run the issuer in one terminal:

```bash
python oidc_issuer.py
```

The issuer starts at:

```text
http://localhost:8000
```

It exposes three simple endpoints.

### Discovery document

```text
http://localhost:8000/.well-known/openid-configuration
```

This is where the consumer learns basic information about the OIDC provider.

It includes values like:

```text
issuer
jwks_uri
supported signing algorithms
supported claims
```

### JWKS endpoint

```text
http://localhost:8000/discovery/keys
```

This endpoint publishes the public key.

The public key is used by the consumer to verify the JWT signature.

### Token endpoint

```text
http://localhost:8000/token
```

This endpoint returns a signed JWT token.

In a real system, token issuance would involve proper authentication and authorization. In this demo, it is hardcoded to keep the flow easy to understand.

## 2. Run the OIDC Consumer

Open another terminal and run:

```bash
python oidc_consumer.py
```

The consumer will:

1. Fetch the discovery document.
2. Read the `jwks_uri`.
3. Request an ID token.
4. Fetch the public key from the JWKS endpoint.
5. Validate the token signature.
6. Validate important claims like `issuer` and `audience`.
7. Print the trusted claims only after validation succeeds.

## Expected Output

You should see output similar to this:

```text
Fetching discovery document...

JWKS endpoint found:
http://localhost:8000/discovery/keys

Requesting ID token...

Fetching public key from JWKS endpoint...

Validating token signature and claims...

Token is valid.
Trusted claims:
{
  'iss': 'http://localhost:8000',
  'sub': 'student:gayatri',
  'aud': 'my-demo-app',
  'iat': 1234567890,
  'exp': 1234568190,
  'name': 'Gayatri'
}
```

The exact `iat` and `exp` values will be different each time because they are based on the current time.

## Important Concepts in the Demo

### Issuer

The issuer is the system that creates and signs the token.

In this demo:

```text
http://localhost:8000
```

### Discovery Document

The discovery document tells the consumer where to find OIDC metadata.

In this demo:

```text
http://localhost:8000/.well-known/openid-configuration
```

### JWKS Endpoint

The JWKS endpoint publishes the public keys.

In this demo:

```text
http://localhost:8000/discovery/keys
```

### JWT Token

The JWT is the signed token.

It contains claims such as:

```text
iss - issuer
sub - subject
aud - audience
iat - issued at
exp - expiry
name - sample user/workload name
```

### Signature Validation

The consumer uses the public key from the JWKS endpoint to verify that the JWT was really signed by the issuer.

### Claim Validation

The consumer also checks that the token has the expected:

```text
issuer
audience
expiry
```

A token should not be trusted just because it can be decoded. It should only be trusted after the signature and important claims are validated.

## What This Demo Does Not Show

This demo intentionally skips many production-level details, including:

- user login
- consent screens
- authorization code flow
- refresh tokens
- key rotation
- TLS certificates
- scopes and permissions
- real access control policies
- secure private key storage
- production-grade OIDC provider behavior

Those details matter in real systems, but they would make this beginner demo harder to follow.

## Why This Demo Is Useful

This demo helps make OIDC less abstract.

Instead of only reading about terms like `issuer`, `jwks_uri`, `JWT`, and `claims`, you can see them working together in a small local example.

The main idea is:

```text
The issuer signs a token.
The consumer discovers the public keys.
The consumer verifies the token.
Only then does the consumer trust the claims.
```

That is the core of the OIDC trust model.

