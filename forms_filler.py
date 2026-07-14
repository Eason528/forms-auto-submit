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

    def press_tab(self, times=1):
        """按指定次数的 Tab 键"""
        for _ in range(times):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(0.3)

    def fill_focused_input(self, text):
        """在当前焦点输入框中填写文本"""
        try:
            active = self.driver.switch_to.active_element
            active.clear()
            active.send_keys(text)
            print(f"✓ 输入: {text}")
        except Exception as e:
            print(f"✗ 输入失败: {e}")

    def click_focused(self):
        """点击当前焦点元素"""
        try:
            active = self.driver.switch_to.active_element
            active.click()
            print(f"✓ 点击: {active.tag_name}")
        except Exception as e:
            print(f"✗ 点击失败: {e}")

    def select_focused_option(self, expected_text):
        """选择与期望文本匹配的选项（焦点在选项上时）"""
        try:
            active = self.driver.switch_to.active_element
            if active.text and expected_text in active.text:
                active.click()
                print(f"✓ 选择: {expected_text}")
                return True
        except:
            pass
        print(f"✗ 未找到选项: {expected_text}")
        return False

    def open_and_start(self):
        """打开问卷并点击'立即开始'按钮（Tab 2 次定位）"""
        print("正在打开问卷...")
        self.driver.get(self.form_url)
        
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(3)
        print("页面加载完成")
        
        # 检查是否已进入问卷
        try:
            self.driver.find_element(By.ID, "DatePicker0-label")
            print("✓ 已直接进入问卷")
            return True
        except:
            pass
        
        print("正在通过 Tab 键定位'立即开始'按钮...")
        
        # 点击页面主体获取焦点
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5)
        
        # 按 2 次 Tab 定位到"立即开始"按钮
        self.press_tab(2)
        
        # 点击当前焦点元素
        active = self.driver.switch_to.active_element
        print(f"  当前焦点: tag={active.tag_name}, text='{active.text[:20] if active.text else ''}'")
        
        if active.is_enabled() and active.is_displayed():
            active.click()
            print("✓ 已点击'立即开始'按钮")
            time.sleep(3)
            
            # 验证是否进入问卷
            try:
                self.driver.find_element(By.ID, "DatePicker0-label")
                print("✓ 成功进入问卷")
                return True
            except:
                print("⚠️ 点击后未进入问卷")
                return False
        else:
            print("❌ 当前焦点元素不可点击")
            return False

    def fill_questions(self):
        """按顺序填写所有题目"""
        print("开始填写问卷...")
        time.sleep(2)

        # ====== 按 2 次 Tab 到第1题 ======
        self.press_tab(2)
        today = datetime.now().strftime("%Y/%m/%d")
        self.fill_focused_input(today)

        # ====== 按 1 次 Tab 到第2题 ======
        self.press_tab(1)
        self.select_focused_option("ABBS")

        # ====== 按 1 次 Tab 到第3题 ======
        self.press_tab(1)
        self.fill_focused_input("Yi Wang")

        # ====== 按 1 次 Tab 到第4题 ======
        self.press_tab(1)
        # 点击展开下拉菜单
        active = self.driver.switch_to.active_element
        active.click()
        time.sleep(0.5)
        # 按 1 次 Tab 选择第一个选项
        self.press_tab(1)
        # 按 Enter 确认
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        print("✓ 第4题 (发现工位): 选择工位")

        # ====== 按 1 次 Tab 到第5题 ======
        self.press_tab(1)
        self.select_focused_option("安全")

        # ====== 按 1 次 Tab 到第6题 ======
        self.press_tab(1)
        self.fill_focused_input("无问题")

        # ====== 按 1 次 Tab 到第7题 ======
        self.press_tab(1)
        self.select_focused_option("是")

        # ====== 按 1 次 Tab 到第8题 ======
        self.press_tab(1)
        self.select_focused_option("是")

        # ====== 按 2 次 Tab 到提交按钮 ======
        self.press_tab(2)
        self.click_focused()
        print("✅ 问卷已自动提交！")

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