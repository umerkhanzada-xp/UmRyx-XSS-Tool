import requests
import time
import sys

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

# Function to animate loading text
def animate_loading(text):
    for _ in range(3):
        for dot in ['.', '..', '...']:
            sys.stdout.write(f'\r{text}{dot}')
            sys.stdout.flush()
            time.sleep(0.5)
    sys.stdout.write('\r')  # Clear loading line

# Function to validate if a URL is well-formed
def validate_url(url):
    return url.startswith('http://') or url.startswith('https://')

# Function to load payloads from a file
def load_payloads():
    with open('payloads.txt', 'r') as file:
        return [payload.strip() for payload in file.readlines()]

# Function to load URLs from a file
def load_urls():
    with open('final.txt', 'r') as file:
        return [url.strip() for url in file.readlines()]

# Function to generate the HTML report with the specified changes
def generate_html_report(vulnerable_urls, non_vulnerable_urls, output_file="vulnerable_report.html"):
    with open(output_file, "w") as html_file:
        html_file.write("<html>")
        html_file.write("<head><title>UmRyx XSS Report</title><style>")
        html_file.write("""
        body {
            background-image: url('https://wallpapercave.com/wp/wp1810653.jpg');
            background-size: cover;
            color: #ff0000;
            font-family: 'Courier New', monospace;
        }
        h1 {
            color: #ff0000;
            text-align: center;
            font-size: 3em;
            text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000;
            animation: glow 2s infinite;
        }
        h2 {
            color: #ffff00;
            text-align: center;
            text-shadow: 0 0 5px #ffff00;
        }
        marquee {
            font-size: 1.5em;
            color: #ffff00;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ff0000;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #550000;
            color: #ffff00;
        }
        td.vulnerable {
            background-color: #550000;
            color: #ffff00;
        }
        td.non-vulnerable {
            background-color: #550000;
            color: #ff0000;
        }
        a {
            color: #ffff00;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        @keyframes glow {
            0% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000; }
            50% { text-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000; }
            100% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000; }
        }
        </style></head>
        """)
        html_file.write("<body>")
        html_file.write("""
        <marquee>Developed by <a href='https://github.com/umerkhanzada-xp' target='_blank'>Umer Khanzada</a></marquee>
        <h1>UmRyx XSS Report</h1>
        <h2>Vulnerability Analysis Results</h2>
        """)

        # Vulnerable URLs
        html_file.write("<table><tr><th>#</th><th>Vulnerable URL</th></tr>")
        for count, url in enumerate(vulnerable_urls, 1):
            html_file.write(f"<tr><td>{count}</td><td class='vulnerable'><a href='{url}' target='_blank'>{url}</a></td></tr>")
        html_file.write("</table>")

        # Non-Vulnerable URLs
        html_file.write("<h2>Non-Vulnerable URLs</h2>")
        html_file.write("<table><tr><th>#</th><th>Non-Vulnerable URL</th></tr>")
        for count, url in enumerate(non_vulnerable_urls, 1):
            html_file.write(f"<tr><td>{count}</td><td class='non-vulnerable'><a href='{url}' target='_blank'>{url}</a></td></tr>")
        html_file.write("</table>")

        html_file.write("</body></html>")

    print(f"[+] HTML report generated: {output_file}")

# Main function to scan for XSS vulnerabilities
def scan_xss():
    # Load URLs and payloads
    urls = load_urls()
    payloads = load_payloads()

    # Lists to store vulnerable and non-vulnerable URLs
    vulnerable_urls = []
    non_vulnerable_urls = []

    # Scan each URL with each payload
    for url in urls:
        if not validate_url(url):
            print(f"{RED}[!] Invalid URL: {url}{RESET}")
            non_vulnerable_urls.append(url)
            continue

        print(f"Scanning {url} for XSS vulnerabilities...")
        animate_loading("Scanning")

        for payload in payloads:
            test_url = f"{url}{payload}"
            try:
                response = requests.get(test_url, timeout=5)
                if payload in response.text:
                    print(f"{GREEN}[+] Vulnerable: {test_url}{RESET}")
                    vulnerable_urls.append(test_url)
                else:
                    print(f"{RED}[X] Not Vulnerable: {test_url}{RESET}")
            except requests.exceptions.RequestException as e:
                print(f"{RED}[!] Error testing {test_url}: {e}{RESET}")

    # Generate HTML report
    generate_html_report(vulnerable_urls, non_vulnerable_urls)

# Run the scanner
if __name__ == "__main__":
    scan_xss()
