import requests
import time
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse
from colorama import Fore, Style
from colorama import init

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
        print(Fore.YELLOW + f"[*] Testing: {full_url}" + Style.RESET_ALL)
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
    init()

    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("VulnHunter 2026 v1.2")
        return
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
VulnHunter 2026

Usage:
 vulnhunter

 Options:
 --help   contact on github.com/therkproject
 --version  Show version information
 """)
        return
    
    banner = r"""
██╗   ██╗██╗   ██╗██╗     ███╗   ██╗
██║   ██║██║   ██║██║     ████╗  ██║
██║   ██║██║   ██║██║     ██╔██╗ ██║
╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║
 ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║
  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝

██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗
██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

                     2026

        Advanced Web Vulnerability Scanner

Author  : The RK Project
Version : v1.2
"""

    print(Fore.CYAN + banner + Style.RESET_ALL)
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    else:
        target = input("Enter Target URL (e.g.. https://example.com): ").strip()
    parsed = urlparse(target)

    if not parsed.scheme or not parsed.netloc:
        print(Fore.MAGENTA + "[!] Invalid URL!" + Style.RESET_ALL)
        return
    
    print(f"[V.H] Target: {target}")
    print("[V.H] testing endpoints...")
    print("[V.H] Scan Started...")
    start_time = time.time()
    results = test_endpoint(target)
    end_time = time.time()
    with open("report.txt","w", encoding="utf-8")as report:
        report.write(f"Target: {target}\n")
        report.write(f"Findings: {len(results)}\n\n")

        for url, vuln, payload in results:
            report.write(
                f"{vuln.upper()} at {url} with payload: {payload}\n"
                )
            
    print(Fore.GREEN + "\n[+] Scan Complete" + Style.RESET_ALL)
    print(f"[+] Findings: {len(results)}")
    print(f"[+] Report saved to report.txt")
    print(f"[+] Time Taken: {round(end_time - start_time, 2)} seconds")
    if results:
        print("Potential vulnerabilities found:")
        for url, vuln, payload in results:
            print(Fore.RED + f"[!] {vuln.upper()} at {url} with payload: {payload}" + Style.RESET_ALL)
    else:
        print("No obvious vulnerabilities detected.")

if __name__ == "__main__":
    main()
