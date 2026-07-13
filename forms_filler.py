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
import random
from datetime import datetime

class HydraulicsFormsFiller:
    def __init__(self, form_url):
        self.form_url = form_url
        firefox_options = Options()
        # 无头模式（GitHub Actions 必需）
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

    def open_and_start(self):
        """打开问卷，通过 Tab 键定位并点击'立即开始'按钮"""
        print("正在打开问卷...")
        self.driver.get(self.form_url)
        
        # 等待页面加载完成
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(3)
        print("页面加载完成")
        
        # 检查是否已经直接进入问卷
        try:
            self.driver.find_element(By.ID, "DatePicker0-label")
            print("✓ 已直接进入问卷，无需点击开始按钮")
            return True
        except:
            pass
        
        print("正在通过 Tab 键定位'立即开始'按钮...")
        
        # 先点击页面主体，确保焦点在页面内
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.click()
        time.sleep(0.5)
        
        # 按 Tab 直到找到"立即开始"按钮
        for i in range(5):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            active = self.driver.switch_to.active_element
            print(f"  按了 {i+1} 次 Tab，当前: {active.tag_name}, text='{active.text[:30] if active.text else ''}'")
            
            if active.text and "开始" in active.text:
                active.click()
                print("✓ 已点击'立即开始'按钮")
                time.sleep(3)
                
                # 验证是否进入问卷
                try:
                    self.driver.find_element(By.ID, "DatePicker0-label")
                    print("✓ 成功进入问卷")
                    return True
                except:
                    print("⚠️ 点击后未进入问卷，继续尝试...")
                    continue
        
        # 备用：通过文本扫描
        try:
            all_elems = self.driver.find_elements(By.XPATH, "//*")
            for elem in all_elems:
                if elem.text and "立即开始" in elem.text and elem.is_displayed() and elem.is_enabled():
                    elem.click()
                    print("✓ 已点击'立即开始'按钮 (备用)")
                    time.sleep(3)
                    return True
        except:
            pass
        
        print("❌ 无法进入问卷")
        return False

    def fill_questions(self):
        """使用 Tab 键顺序定位所有题目"""
        print("开始填写问卷...")
        time.sleep(2)

        def press_tab(times=1):
            """按指定次数的 Tab 键"""
            for _ in range(times):
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(0.3)

        def select_option_by_text(expected_text):
            """
            通过 Tab 键定位到当前选项，选择期望的文本。
            如果当前焦点元素文本匹配，则选择；否则继续按 Tab。
            """
            for _ in range(3):  # 最多尝试 3 次
                active = self.driver.switch_to.active_element
                if active.text and expected_text in active.text:
                    active.click()
                    print(f"✓ 选择: {expected_text}")
                    return True
                press_tab(1)
            print(f"✗ 未找到选项: {expected_text}")
            return False

        def fill_input(text):
            """在焦点输入框中填入文本"""
            try:
                active = self.driver.switch_to.active_element
                active.clear()
                active.send_keys(text)
                print(f"✓ 输入: {text}")
                return True
            except Exception as e:
                print(f"✗ 输入失败: {e}")
                return False

        # ============================================================
        # 按照你描述的顺序执行
        # ============================================================

        # 第1题：发现日期（从问卷开头按 1 次 Tab）
        press_tab(1)
        fill_input(datetime.now().strftime("%Y/%m/%d"))

        # 第2题：发现项 - ABBS（按 1 次 Tab 到第2题，然后选择 ABBS）
        press_tab(1)
        select_option_by_text("ABBS")

        # 第3题：发现人（按 1 次 Tab 到第3题，然后输入姓名）
        press_tab(1)
        fill_input("Yi Wang")

        # 第4题：发现工位（按 1 次 Tab 到第4题，然后随机选择一个选项）
        press_tab(1)
        # 按 Tab 进入下拉菜单，随机选择一项
        press_tab(1)
        # 等待下拉选项加载
        time.sleep(1)
        # 选择第 2 个选项（索引 1）
        for _ in range(2):
            press_tab(1)
        # 按 Enter 确认选择
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        print("✓ 第4题 (发现工位): 随机选择了一个选项")
        time.sleep(0.5)

        # 第5题：安全状态 - 安全（按 1 次 Tab 到第5题）
        press_tab(1)
        select_option_by_text("安全")

        # 第6题：问题描述（按 1 次 Tab 到第6题，然后输入）
        press_tab(1)
        fill_input("无问题")

        # 第7题：是否沟通 - 是（按 1 次 Tab 到第7题）
        press_tab(1)
        select_option_by_text("是")

        # 第8题：是否卡特员工 - 是（按 1 次 Tab 到第8题）
        press_tab(1)
        select_option_by_text("是")

        # 第9题：非卡特员工类型 - 不填写（跳过）

        # 按 2 次 Tab 到提交按钮
        press_tab(2)
        
        print("\n" + "="*60)
        print("✅ 所有题目已填写完成！")
        print("="*60 + "\n")

    def submit_form(self):
        """提交问卷（当前焦点应在提交按钮上）"""
        try:
            active = self.driver.switch_to.active_element
            active.click()
            print("✅ 问卷已自动提交！")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"✗ 自动提交失败: {e}")
            return False

    def close(self):
        time.sleep(2)
        self.driver.quit()
        print("浏览器已关闭。")


def main():
    url = "https://forms.office.com/Pages/ResponsePage.aspx?id=v3exzjsBq0mKnEq84yr8HuHJUQiSLitLk4NbBlTNB51UQlpTQUs4RE5XTlZOQTFPSTZJUkk4MjJIMC4u&origin=QRCode"
    
    filler = HydraulicsFormsFiller(url)
    try:
        if filler.open_and_start():
            filler.fill_questions()
            filler.submit_form()
        else:
            print("❌ 无法进入问卷，请手动检查")
    except Exception as e:
        print(f"程序出错: {e}")
    finally:
        filler.close()


if __name__ == "__main__":
    main()