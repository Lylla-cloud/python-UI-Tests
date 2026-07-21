import pytest
import requests
from pages.generic_page import GenericWebPage

def test_link_crawler_and_health(driver, target_url):
    page = GenericWebPage(driver)
    page.navigate_to(target_url)
    
    links = page.get_all_href_links()
    unique_links = list(dict.fromkeys(links))[:15] # Audit up to 15 unique links
    
    broken_links = []
    audited = 0
    
    headers = {"User-Agent": "Mozilla/5.0 (Python Selenium Auditor)"}
    
    for url in unique_links:
        audited += 1
        try:
            resp = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            if resp.status_code == 405: # Method not allowed, retry with GET
                resp = requests.get(url, headers=headers, timeout=5, stream=True)
            if resp.status_code >= 400:
                broken_links.append((url, resp.status_code))
        except Exception as e:
            broken_links.append((url, str(e)))
            
    print(f"\n[Link Crawler] Audited {audited}/{len(links)} links. Broken links found: {len(broken_links)}")
    assert len(broken_links) == 0, f"Found {len(broken_links)} broken link(s): {broken_links}"
