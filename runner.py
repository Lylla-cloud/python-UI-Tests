import sys
import argparse
import pytest
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Reno Python Selenium Test Runner")
    parser.add_argument("--url", default="https://example.com", help="Target URL to test")
    parser.add_argument("--browser", default="chrome", choices=["chrome", "firefox"], help="Browser engine")
    parser.add_argument("--headless", action="store_true", default=True, help="Run browser headless")
    parser.add_argument("--headed", action="store_false", dest="headless", help="Run browser headed")
    parser.add_argument("--suite", default="all", help="Suite to run (smoke, links, forms, audit, all)")

    args = parser.parse_args()

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / "report.html"

    pytest_args = [
        f"--target-url={args.url}",
        f"--browser={args.browser}",
        f"--html={str(report_file)}",
        "--self-contained-html",
        "-v"
    ]

    if args.headless:
        pytest_args.append("--headless")

    if args.suite != "all":
        pytest_args.append(f"tests/test_{args.suite}.py")
    else:
        pytest_args.append("tests")

    print(f"🚀 Launching Pytest with args: {pytest_args}")
    exit_code = pytest.main(pytest_args)
    print(f"✅ Execution finished with exit code {exit_code}. HTML Report generated at: {report_file.resolve()}")
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
