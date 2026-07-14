from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
import time
from datetime import datetime

class HydraulicsFormsFiller:
    def __init__(self, form_url):
        self.form_url = form_url
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--window-size=1920,1080")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-blink-features=AutomationControlled")
        firefox_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.wait = WebDriverWait(self.driver, 30)

    def press_tab(self, times=1):
        for _ in range(times):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(0.3)

    def log_focus(self, step_name=""):
        active = self.driver.switch_to.active_element
        tag = active.tag_name
        text = active.text.strip() if active.text else ""
        input_type = active.get_attribute("type") if tag == "input" else ""
        print(f"  [{step_name}] 焦点: tag={tag}, type={input_type}, text='{text[:30]}'")
        return active

    def open_and_start(self):
        print("正在打开问卷...")
        self.driver.get(self.form_url)
        
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(3)
        print("页面加载完成")
        
        try:
            self.driver.find_element(By.ID, "DatePicker0-label")
            print("✓ 已直接进入问卷")
            return True
        except:
            pass
        
        print("正在定位'立即开始'按钮...")
        
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5)
        
        for i in range(10):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            active = self.driver.switch_to.active_element
            text = active.text.strip() if active.text else ""
            print(f"  按了 {i+1} 次 Tab，当前: {active.tag_name}, text='{text[:30]}'")
            
            if text in ["立即开始", "Start now"] or (active.tag_name == "button" and "开始" in text):
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", active)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", active)
                print(f"✓ 已点击'{text}'按钮")
                time.sleep(3)
                
                try:
                    self.driver.find_element(By.ID, "DatePicker0-label")
                    print("✓ 成功进入问卷")
                    return True
                except:
                    print("⚠️ 点击后未进入问卷，继续尝试...")
                    continue
        
        try:
            start_btn = self.driver.find_element(By.XPATH, "//div[text()='立即开始']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_btn)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", start_btn)
            print("✓ 已点击'立即开始'按钮 (XPath)")
            time.sleep(3)
            return True
        except:
            pass
        
        print("❌ 无法进入问卷")
        return False

    def fill_questions(self):
        print("开始填写问卷...")
        time.sleep(2)

        # 第1题：日期
        for _ in range(10):
            self.press_tab(1)
            active = self.log_focus("第1题")
            if active.tag_name == "input" and active.get_attribute("type") in ["text", "date", None]:
                today = datetime.now().strftime("%Y/%m/%d")
                active.clear()
                active.send_keys(today)
                print(f"✓ 第1题 (发现日期): {today}")
                break
        else:
            print("✗ 第1题失败")
            return

        # 第2题：ABBS
        for _ in range(5):
            self.press_tab(1)
            active = self.log_focus("第2题")
            if active.text and "ABBS" in active.text:
                active.click()
                print("✓ 第2题: ABBS")
                break
        else:
            print("✗ 第2题失败: 未找到 ABBS")
            # 不 return，继续尝试后续题目

        # 第3题：姓名
        for _ in range(5):
            self.press_tab(1)
            active = self.log_focus("第3题")
            if active.tag_name == "input":
                active.clear()
                active.send_keys("Yi Wang")
                print("✓ 第3题 (发现人): Yi Wang")
                break
        else:
            print("✗ 第3题失败")

        # 第4题：工位
        self.press_tab(1)
        active = self.log_focus("第4题-下拉")
        active.click()
        time.sleep(0.5)
        self.press_tab(1)
        active = self.log_focus("第4题-选项")
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        print("✓ 第4题: 选择工位")

        # 第5题：安全
        for _ in range(5):
            self.press_tab(1)
            active = self.log_focus("第5题")
            if active.text and "安全" in active.text:
                active.click()
                print("✓ 第5题: 安全")
                break
        else:
            print("✗ 第5题失败")

        # 第6题：问题描述
        for _ in range(5):
            self.press_tab(1)
            active = self.log_focus("第6题")
            if active.tag_name == "input":
                active.clear()
                active.send_keys("无问题")
                print("✓ 第6题 (问题描述): 无问题")
                break
        else:
            print("✗ 第6题失败")

        # 第7题：是
        for _ in range(5):
            self.press_tab(1)
            active = self.log_focus("第7题")
            if active.text and "是" in active.text:
                active.click()
                print("✓ 第7题: 是")
                break
        else:
            print("✗ 第7题失败")

        # 第8题：是
        for _ in range(5):
            self.press_tab(1)
            active = self.log_focus("第8题")
            if active.text and "是" in active.text:
                active.click()
                print("✓ 第8题: 是")
                break
        else:
            print("✗ 第8题失败")

        # 提交
        self.press_tab(2)
        active = self.log_focus("提交")
        if active.tag_name == "button":
            active.click()
            print("✅ 问卷已自动提交！")
        else:
            print(f"⚠️ 当前焦点在 {active.tag_name}，尝试继续按 Tab...")
            for _ in range(5):
                self.press_tab(1)
                active = self.log_focus("提交-继续")
                if active.tag_name == "button":
                    active.click()
                    print("✅ 问卷已自动提交！")
                    break

        print("\n" + "="*60)
        print("✅ 所有题目已填写完成！")
        print("="*60 + "\n")

    def close(self):
        time.sleep(3)
        self.driver.quit()
        print("浏览器已关闭。")


def main():
    url = "https://forms.office.com/Pages/ResponsePage.aspx?id=v3exzjsBq0mKnEq84yr8HuHJUQiSLitLk4NbBlTNB51UQlpTQUs4RE5XTlZOQTFPSTZJUkk4MjJIMC4u&origin=QRCode"
    
    filler = HydraulicsFormsFiller(url)
    try:
        if filler.open_and_start():
            filler.fill_questions()
        else:
            print("❌ 无法进入问卷，请手动检查")
    except Exception as e:
        print(f"程序出错: {e}")
    finally:
        filler.close()


if __name__ == "__main__":
    main()