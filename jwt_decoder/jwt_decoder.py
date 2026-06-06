
import base64
import json
import sys


def pad_base64(data):
    """Restores the trailing padding required by standard cryptographic libraries."""
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return data


def decode_segment(segment_name, raw_segment):
    """Handles the transformation from a URL-safe Base64 string to a structured dictionary."""
    # AIM: To Isolate the cryptographic decoding process
    try:
        padded_segment = pad_base64(raw_segment)
        decoded_bytes = base64.urlsafe_b64decode(padded_segment.encode("utf-8"))
    except Exception as e:
        print(
            f"[-] ERROR: Failed to Base64URL decode the {segment_name}. Code: {e}"
        )
        return None

    # Here, We Isolate the JSON string parsing mechanism
    else:
        try:
            return json.loads(decoded_bytes.decode("utf-8"))
        except json.JSONDecodeError:
            print(
                f"[-] ERROR: Successfully decoded {segment_name} bytes, but failed to parse valid JSON."
            )
            return None


def main():
    print("-" * 50)
    print("AETHER: Tactical JWT Claims Extractor")
    print("-" * 50)

    # Prompting user for the raw JSON Web Token string and striping away leading and trailing spaces (if any)
    raw_jwt = input("[*] Enter target JWT string:\n> ").strip()
    print("\n" + "-" * 50)

    # Validate structural integrity (A valid JWT must contain Header, Payload, and Signature)
    segments = raw_jwt.split(".")
    if len(segments) != 3:
        print("[-] ERROR: Invalid token structure.")
        print("[!] A valid JWT must consist of exactly 3 parts separated by dots.")
        sys.exit(1)

    raw_header, raw_payload, _ = segments

    # Process Header
    header_json = decode_segment("HEADER", raw_header)

    # Process Payload
    payload_json = decode_segment("PAYLOAD", raw_payload)

    # Display Extracted Intelligence
    if header_json and payload_json:
        print(" EXTRACTED HEADER (Metadata)")
        print("-" * 45)
        for key, val in header_json.items():
            print(f"{key:<15} : {val}")

        print("\n EXTRACTED PAYLOAD (Claims Data)")
        print("-" * 45)
        for key, val in payload_json.items():
            # Format nested objects cleanly if encountered
            if isinstance(val, (dict, list)):
                print(f"{key:<15} : {json.dumps(val, indent=4)}")
            else:
                print(f"{key:<15} : {val}")
    else:
        print("\n[-] Extraction failed due to payload corruption.")

    print("-" * 50)


if __name__ == "__main__":
    main()




































