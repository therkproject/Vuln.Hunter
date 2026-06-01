import requests
from urllib.parse import urljoin

# Common test payloads for SQLi and XSS
payloads = {
    "sql_injection": ["'", "' OR '1'='1", "\" OR \"1\"=\"1"],
    "xss": ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
}

# Common vulnerable endpoints to test
endpoints = [
    "/login",
    "/search",
    "/product?id=1",
    "/comment",
    "/profile"
]

def test_endpoint(url):
    findings = []
    for endpoint in endpoints:
        full_url = urljoin(url, endpoint)
        for vuln_type, tests in payloads.items():
            for test in tests:
                try:
                    # Sending payload as GET param 'q'
                    r = requests.get(full_url, params={"q": test}, timeout=5)
                    if test in r.text:
                        findings.append((full_url, vuln_type, test))
                except requests.RequestException:
                    continue
    return findings

def main():

        banner = r"""
╦  ╦ ╦ ╦
╚╗╔╝ ╠═╣
 ╚╝  ╩ ╩

Vuln.Hunter v1.0
"""

print(banner)
    target = input("Enter target URL (e.g., https://example.com): ").strip()
    print(f"Scanning {target} ...")
    results = test_endpoint(target)
    if results:
        print("Potential vulnerabilities found:")
        for url, vuln, payload in results:
            print(f"[!] {vuln.upper()} at {url} with payload: {payload}")
    else:
        print("No obvious vulnerabilities detected.")

if __name__ == "__main__":
    main()
