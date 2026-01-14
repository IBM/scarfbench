import requests
import sys
import time
import argparse


def wait_for_server(url, timeout=60, interval=2):
    """Wait for the server to be ready"""
    print(f"Waiting for server at {url}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, allow_redirects=False, timeout=5)
            if response.status_code in [200, 302, 401, 403]:
                print(f"Server is ready! Status: {response.status_code}")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(interval)

    print(f"Server failed to start within {timeout} seconds")
    return False


def test_app_deployed():
    """Test that the application is deployed and accessible"""
    url = "http://localhost:9080/servlet"

    try:
        # Just check if the server responds (even if it's 401/403 for auth required)
        response = requests.get(url, allow_redirects=False, timeout=10)
        print(f"GET {url} - Status: {response.status_code}")

        # Application is deployed if we get any valid HTTP response
        if response.status_code in [200, 401, 403]:
            print("✓ Application is deployed and servlet endpoint exists")
            return True
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Failed to access application: {e}")
        return False


def test_servlet_requires_auth():
    """Test that servlet endpoint requires authentication"""
    url = "http://localhost:9080/servlet"

    try:
        # Try without authentication - should fail with 401 or 403
        response = requests.get(url, allow_redirects=False, timeout=10)
        print(f"GET {url} (no auth) - Status: {response.status_code}")

        if response.status_code in [401, 403]:
            print("✓ Servlet requires authentication")
            return True
        else:
            print(f"✗ Expected 401/403, got: {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Servlet authentication test failed: {e}")
        return False


def test_authentication_with_valid_credentials():
    """Test authentication with valid credentials (Joe/secret1)"""
    url = "http://localhost:9080/servlet"

    try:
        # Try with valid credentials
        response = requests.get(url, auth=("Joe", "secret1"), timeout=10)
        print(f"GET {url} (Joe/secret1) - Status: {response.status_code}")

        if response.status_code == 200:
            # Check response content
            content = response.text
            print(f"Response content:\n{content}")

            # Verify expected content
            if (
                "web username: Joe" in content
                and 'web user has role "foo": true' in content
            ):
                print("✓ Authentication successful and roles verified")
                return True
            else:
                print("✗ Response content doesn't match expected output")
                return False
        else:
            print(f"✗ Authentication failed with status: {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        return False


def test_authentication_with_invalid_credentials():
    """Test that invalid credentials are rejected"""
    url = "http://localhost:9080/servlet"

    try:
        # Try with invalid credentials
        response = requests.get(
            url, auth=("invalid", "wrong"), allow_redirects=False, timeout=10
        )
        print(f"GET {url} (invalid/wrong) - Status: {response.status_code}")

        if response.status_code in [401, 403]:
            print("✓ Invalid credentials correctly rejected")
            return True
        else:
            print(
                f"✗ Expected 401/403 for invalid credentials, got: {response.status_code}"
            )
            return False

    except Exception as e:
        print(f"✗ Invalid credentials test failed: {e}")
        return False


def run_smoke_tests():
    """Run all smoke tests"""
    print("=" * 50)
    print("Starting Smoke Tests for Custom Identity Store")
    print("=" * 50)

    # Wait for server to be ready
    if not wait_for_server("http://localhost:9080/servlet"):
        print("\n✗ SMOKE TESTS FAILED - Server not ready")
        sys.exit(1)

    print("\nRunning tests...\n")

    tests = [
        ("Application Deployment", test_app_deployed),
        ("Servlet Requires Authentication", test_servlet_requires_auth),
        (
            "Valid Credentials Authentication",
            test_authentication_with_valid_credentials,
        ),
        ("Invalid Credentials Rejection", test_authentication_with_invalid_credentials),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))

    # Summary
    print("\n" + "=" * 50)
    print("SMOKE TEST SUMMARY")
    print("=" * 50)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    failed_tests = [name for name, result in results if not result]

    if failed_tests:
        print(f"\n✗ {len(failed_tests)} test(s) failed")
        sys.exit(1)
    else:
        print("\n✓ All smoke tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    run_smoke_tests()
