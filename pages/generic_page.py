from typing import Dict, List, Any
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class GenericWebPage(BasePage):
    def get_meta_tags(self) -> Dict[str, str]:
        meta_dict = {}
        metas = self.driver.find_elements(By.TAG_NAME, "meta")
        for meta in metas:
            try:
                name = meta.get_attribute("name") or meta.get_attribute("property")
                content = meta.get_attribute("content")
                if name and content:
                    meta_dict[name.lower()] = content
            except Exception:
                pass
        return meta_dict

    def get_forms_info(self) -> List[Dict[str, str]]:
        forms_list = []
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        for idx, form in enumerate(forms, 1):
            try:
                inputs = form.find_elements(By.CSS_SELECTOR, "input, textarea, select, button")
                forms_list.append({
                    "formIndex": str(idx),
                    "action": form.get_attribute("action") or "",
                    "method": form.get_attribute("method") or "",
                    "id": form.get_attribute("id") or "",
                    "inputCount": str(len(inputs))
                })
            except Exception:
                pass
        return forms_list

    def get_images_audit(self) -> List[Dict[str, Any]]:
        images_list = []
        images = self.driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            try:
                src = img.get_attribute("src") or ""
                alt = img.get_attribute("alt") or ""
                images_list.append({
                    "src": src,
                    "alt": alt,
                    "hasAlt": bool(alt.strip())
                })
            except Exception:
                pass
        return images_list

    def get_page_load_time_ms(self) -> int:
        try:
            perf_script = (
                "var perf = window.performance.timing; "
                "return (perf.loadEventEnd > 0 && perf.navigationStart > 0) ? (perf.loadEventEnd - perf.navigationStart) : 0;"
            )
            val = self.execute_script(perf_script)
            return int(val) if val else 0
        except Exception:
            return 0
