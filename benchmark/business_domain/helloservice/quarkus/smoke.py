import os
import sys
import urllib.request
import urllib.error

PAYLOAD = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:hel="http://ejb.helloservice.tutorial.jakarta/">
   <soapenv:Header/>
   <soapenv:Body>
      <hel:sayHello>
         <arg0>John</arg0>
      </hel:sayHello>
   </soapenv:Body>
</soapenv:Envelope>
"""


def main():
    HELLO_SERVICE_URL = os.getenv(
        "HELLO_SERVICE_URL",
        "http://localhost:8080/helloservice/HelloServiceBean",
    )

    # Prepare the request
    req = urllib.request.Request(
        HELLO_SERVICE_URL,
        data=bytes(PAYLOAD, "utf-8"),
        headers={"Content-Type": "text/xml"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            response_text = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP error {e.code}: {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Connection error: {e.reason}")
        sys.exit(1)

    if "Hello, John." in response_text:
        print("✅ Validation passed: 'Hello, John.' found in response.")
    else:
        print("❌ Validation failed: 'Hello, John.' not found in response.")
        sys.exit(1)


if __name__ == "__main__":
    main()
