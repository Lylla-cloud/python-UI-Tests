import uuid
import time
import threading
from datetime import datetime
from typing import Dict, Any, List
from flask import Flask, render_template, request, jsonify

from core.driver_factory import DriverFactory
from pages.generic_page import GenericWebPage

app = Flask(__name__)

# In-memory test run registry
TEST_RUNS: Dict[str, Dict[str, Any]] = {}

def run_test_job(test_id: str, payload: Dict[str, Any]):
    run_info = TEST_RUNS[test_id]
    run_info["status"] = "RUNNING"
    start_time = time.time()
    
    target_url = payload.get("targetUrl", "https://example.com")
    browser = payload.get("browser", "chrome")
    headless = payload.get("headless", True)
    timeout = payload.get("timeoutSeconds", 10)
    selected_suites = payload.get("suites", ["smoke", "link_crawler", "form_tester", "page_audit"])
    
    def log(level: str, msg: str, screenshot_b64: str = None, suite: str = None):
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "level": level,
            "message": msg,
            "suite": suite,
            "screenshotBase64": screenshot_b64
        }
        run_info["logs"].append(entry)
        
    log("INFO", f"Initializing Selenium WebDriver [{browser.upper()}, Headless={headless}]...")
    driver = None
    
    try:
        driver = DriverFactory.create_driver(browser=browser, headless=headless, timeout_seconds=timeout)
        log("SUCCESS", "WebDriver session established.")
        page = GenericWebPage(driver, timeout_seconds=timeout)
        
        passed_count = 0
        failed_count = 0
        
        for suite_key in selected_suites:
            suite_start = time.time()
            suite_result = {
                "suiteKey": suite_key,
                "status": "RUNNING",
                "logs": [],
                "summary": "",
                "durationMs": 0
            }
            run_info["suiteResults"].append(suite_result)
            
            try:
                if suite_key == "smoke":
                    suite_result["suiteName"] = "Smoke & Reachability"
                    log("INFO", f"Navigating to: {target_url}", suite="Smoke")
                    page.navigate_to(target_url)
                    title = page.get_title()
                    current_url = page.get_current_url()
                    screenshot = page.capture_screenshot_base64()
                    
                    log("SUCCESS", f"Loaded page. Title: '{title}' | URL: {current_url}", screenshot_b64=screenshot, suite="Smoke")
                    suite_result["status"] = "PASSED"
                    suite_result["summary"] = f"Site online. Title: '{title}'"
                    passed_count += 1
                    
                elif suite_key == "link_crawler":
                    suite_result["suiteName"] = "Link Crawler & 404 Audit"
                    log("INFO", f"Scanning links on page: {target_url}", suite="Link Crawler")
                    links = page.get_all_href_links()
                    log("INFO", f"Found {len(links)} total links. Auditing top 10 unique links...", suite="Link Crawler")
                    
                    import requests
                    unique_links = list(dict.fromkeys(links))[:10]
                    broken = 0
                    for u in unique_links:
                        try:
                            resp = requests.head(u, timeout=5, headers={"User-Agent": "Mozilla/5.0 Audit"})
                            if resp.status_code >= 400:
                                broken += 1
                                log("WARN", f"Broken link: {u} [HTTP {resp.status_code}]", suite="Link Crawler")
                        except Exception as e:
                            broken += 1
                            log("WARN", f"Unreachable link: {u} ({str(e)})", suite="Link Crawler")
                            
                    if broken == 0:
                        suite_result["status"] = "PASSED"
                        suite_result["summary"] = f"Audited {len(unique_links)} links. All healthy!"
                        log("SUCCESS", f"Audited {len(unique_links)} links successfully.", suite="Link Crawler")
                    else:
                        suite_result["status"] = "FAILED"
                        suite_result["summary"] = f"Found {broken} broken/unreachable links."
                    passed_count += 1 if broken == 0 else 0
                    failed_count += 1 if broken > 0 else 0
                    
                elif suite_key == "form_tester":
                    suite_result["suiteName"] = "Form & Input Field Audit"
                    log("INFO", "Scanning page forms and text fields...", suite="Form Audit")
                    forms = page.get_forms_info()
                    log("INFO", f"Found {len(forms)} form(s) on page.", suite="Form Audit")
                    screenshot = page.capture_screenshot_base64()
                    log("SUCCESS", f"Discovered {len(forms)} forms.", screenshot_b64=screenshot, suite="Form Audit")
                    suite_result["status"] = "PASSED"
                    suite_result["summary"] = f"Discovered {len(forms)} forms and input fields."
                    passed_count += 1
                    
                elif suite_key == "page_audit":
                    suite_result["suiteName"] = "Performance & Accessibility Audit"
                    log("INFO", "Auditing page load timing, headers, and images...", suite="Page Audit")
                    imgs = page.get_images_audit()
                    load_ms = page.get_page_load_time_ms()
                    missing_alt = [img for img in imgs if not img.get("hasAlt")]
                    
                    log("INFO", f"Page load time: {load_ms}ms | Images: {len(imgs)} ({len(missing_alt)} missing alt text)", suite="Page Audit")
                    suite_result["status"] = "PASSED"
                    suite_result["summary"] = f"Load time: {load_ms}ms. Images: {len(imgs)} ({len(missing_alt)} missing alt)."
                    passed_count += 1
                    
            except Exception as e:
                suite_result["status"] = "FAILED"
                suite_result["summary"] = f"Suite error: {str(e)}"
                log("ERROR", f"Exception in suite [{suite_key}]: {str(e)}", suite=suite_key)
                failed_count += 1
            finally:
                suite_result["durationMs"] = int((time.time() - suite_start) * 1000)
                
        # Final screenshot capture
        try:
            run_info["finalScreenshotBase64"] = page.capture_screenshot_base64()
        except Exception:
            pass
            
        run_info["passedSuites"] = passed_count
        run_info["failedSuites"] = failed_count
        run_info["status"] = "COMPLETED" if failed_count == 0 else "COMPLETED_WITH_FAILURES"
        log("SUCCESS", f"Execution finished. Passed: {passed_count}, Failed: {failed_count}")
        
    except Exception as e:
        run_info["status"] = "FAILED"
        log("ERROR", f"Critical test execution error: {str(e)}")
    finally:
        if driver:
            try:
                log("INFO", "Closing WebDriver session...")
                driver.quit()
            except Exception:
                pass
        run_info["totalDurationMs"] = int((time.time() - start_time) * 1000)
        run_info["endTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tests/run", methods=["POST"])
def start_test_run():
    payload = request.get_json() or {}
    target_url = payload.get("targetUrl")
    if not target_url:
        return jsonify({"error": "targetUrl is required"}), 400
        
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url.strip()
        payload["targetUrl"] = target_url
        
    test_id = "PYRUN-" + uuid.uuid4().hex[:8].upper()
    run_data = {
        "id": test_id,
        "targetUrl": target_url,
        "browser": payload.get("browser", "chrome"),
        "headless": payload.get("headless", True),
        "status": "QUEUED",
        "startTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totalDurationMs": 0,
        "totalSuites": len(payload.get("suites", ["smoke", "link_crawler", "form_tester", "page_audit"])),
        "passedSuites": 0,
        "failedSuites": 0,
        "suiteResults": [],
        "logs": [],
        "finalScreenshotBase64": None
    }
    
    TEST_RUNS[test_id] = run_data
    
    thread = threading.Thread(target=run_test_job, args=(test_id, payload))
    thread.daemon = True
    thread.start()
    
    return jsonify(run_data)

@app.route("/api/tests/<test_id>", methods=["GET"])
def get_test_status(test_id):
    run_data = TEST_RUNS.get(test_id)
    if not run_data:
        return jsonify({"error": "Test run not found"}), 404
    return jsonify(run_data)

@app.route("/api/tests/history", methods=["GET"])
def get_test_history():
    runs = list(TEST_RUNS.values())
    runs.sort(key=lambda r: r.get("startTime", ""), reverse=True)
    return jsonify(runs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
