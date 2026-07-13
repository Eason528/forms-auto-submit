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
        """按指定次数的 Tab 键"""
        for _ in range(times):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(0.3)

    def fill_focused_input(self, text):
        """在当前焦点输入框中填写文本"""
        active = self.driver.switch_to.active_element
        active.clear()
        active.send_keys(text)
        print(f"✓ 输入: {text}")

    def click_focused(self):
        """点击当前焦点元素"""
        active = self.driver.switch_to.active_element
        active.click()
        print(f"✓ 点击: {active.tag_name}")

    def open_and_start(self):
        """打开问卷并点击'立即开始'按钮"""
        print("正在打开问卷...")
        self.driver.get(self.form_url)
        time.sleep(5)
        print("页面加载完成")
        
        # 检查是否已进入问卷
        try:
            self.driver.find_element(By.ID, "DatePicker0-label")
            print("✓ 已直接进入问卷")
            return True
        except:
            pass
        
        print("正在定位'立即开始'按钮...")
        
        # 点击页面主体获取焦点
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5)
        
        # 按2次Tab定位到"立即开始"按钮
        self.press_tab(2)
        self.click_focused()
        print("✓ 已点击'立即开始'按钮")
        time.sleep(3)
        
        # 验证是否进入问卷
        try:
            self.driver.find_element(By.ID, "DatePicker0-label")
            print("✓ 成功进入问卷")
            return True
        except:
            print("❌ 未能进入问卷")
            return False

    def fill_questions(self):
        """按顺序填写所有题目"""
        print("开始填写问卷...")
        time.sleep(2)

        # ====== 第1题：发现日期 ======
        self.press_tab(1)
        today = datetime.now().strftime("%Y/%m/%d")
        self.fill_focused_input(today)

        # ====== 第2题：发现项 - ABBS ======
        self.press_tab(1)
        self.click_focused()  # 点击ABBS
        print("✓ 选择: ABBS")

        # ====== 第3题：发现人 ======
        self.press_tab(1)
        self.fill_focused_input("Yi Wang")

        # ====== 第4题：发现工位 ======
        self.press_tab(1)      # 跳转到工位下拉
        self.click_focused()   # 展开下拉
        time.sleep(0.5)
        self.press_tab(1)      # 选择第一个选项
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        print("✓ 第4题: 选择工位")

        # ====== 第5题：安全状态 - 安全 ======
        self.press_tab(1)
        self.click_focused()
        print("✓ 选择: 安全")

        # ====== 第6题：问题描述 ======
        self.press_tab(1)
        self.fill_focused_input("无问题")

        # ====== 第7题：是否沟通 - 是 ======
        self.press_tab(1)
        self.click_focused()
        print("✓ 选择: 是")

        # ====== 第8题：是否卡特员工 - 是 ======
        self.press_tab(1)
        self.click_focused()
        print("✓ 选择: 是")

        # 第9题跳过

        # ====== 提交 ======
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