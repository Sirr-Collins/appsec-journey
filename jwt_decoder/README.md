# AETHER: Tactical JWT Claims Extractor

A robust, dependency-free Python tool developed to dismantle and inspect JSON Web Tokens (JWT) directly via the command line. 

This utility acts as a local security auditing mechanism to analyze user sessions, privilege vectors, and identity claims without transmitting sensitive authentication tokens over public third-party testing sites like jwt.io.

## Features
* **Zero Dependencies:** Relies strictly on standard core Python components (`base64`, `json`), minimizing attack surface and dependencies.
* **Padding Deficit Resolution:** Implements an automated mathematical correction function (`len(data) % 4`) to restore URL-safe Base64 strings to standard cryptographic layouts.
* **Fault-Isolated Execution:** Separates binary parsing errors from JSON rendering faults via atomic exception handling to pinpoint corrupt tokens instantly.


## Proof of Concept (PoC)
* Below is the PoC for this tool which is a simple .gif of my local implementation VS a sample from jwt.io using the same jwt token
![AETHER JWT Decoder Demonstration](docs/jwt_demo.gif)



## Installation & Usage

1. **Navigate to the tool's folder:**
   ```bash
   cd jwt_decoder
   
2. **Execute the script**
    ```bash
    python jwt_decoder.py

3. **Provide Input Data**

    Paste your intercepted authorization header or cookie token when prompted to retrieve the raw structured text. (sample jwt from jwt.io below)
    ```bash
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30

## Under the Hood

JWTs segment information using dots (.) to map components structurally:
[Header].[Payload].[Signature]

Because signatures cannot be verified without access to the environment's signing key, this utility isolates and bypasses the signature verification engine to fulfill a purely forensic role—inspecting internal claims elements like user authorization scopes, expiration timestamps (exp), and issuance contexts (iat).





