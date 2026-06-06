import requests
import sys
import json


def main():
    print("-" * 50)
    print("AETHER: Tactical HTTP Request Forger")
    print("-" * 50)

    # 1. The Target
    # httpbin.org/get echoes back the headers and cookies we send it
    target_url = "https://httpbin.org/get"

    # 2. The Payload (Custom Headers)
    # Spoofing the User-Agent is a classic way to bypass basic WAF blocks.
    # We can also inject custom headers to test for misconfigurations.
    custom_headers = {
        "User-Agent": "AETHER-Agent/v1.0 (Security Auditing)",
        "Accept": "application/json",
        "X-Forwarded-For": "127.0.0.1",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
    }# As we saw earlier that x-forwarded-for is a sec header that informs the server of the origin

    # 3. The Payload (Custom Cookies)
    # This is where one can inject a hijacked session ID or a forged JWT token
    custom_cookies = {
        "session_id": "super_secret_admin_token_999",
        "tracking_pref": "opt_out"
    }

    print(f"[*] Target URL: {target_url}")

    # We isolate ONLY the network transaction here to catch connection failures gracefully.
    try:
        # timeout=5 prevents the script from hanging infinitely if the server drops the connection
        response = requests.get(
            target_url,
            headers=custom_headers,
            cookies=custom_cookies,
            timeout=5
        )

    except requests.exceptions.RequestException as e:
        # This catches DNS failures, timeouts, and refused connections
        print(f"[-] ERROR: Network transmission failed. System says: {e}")
        sys.exit(1)


    else:
        print("-" * 50)
        print("SERVER RESPONSE")
        print("-" * 50)

        # Displaying the HTTP Status Code
        print(f"[>] Status Code : {response.status_code}")

        # Displaying the Server's Headers
        print(f"[>] Server Type : {response.headers.get('Server', 'Unknown')}")

        print("\n[>] Echoed Body Data:")
        print("-" * 45)

        # Parsing the JSON response to prove our data made it through
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=4))
        except ValueError:
            # Fallback if the server didn't return JSON
            print(response.text)


if __name__ == "__main__":
    main()

