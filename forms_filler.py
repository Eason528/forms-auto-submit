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
        try:
            active = self.driver.switch_to.active_element
            active.clear()
            active.send_keys(text)
            print(f"✓ 输入: {text}")
            return True
        except Exception as e:
            print(f"✗ 输入失败: {e}")
            return False

    def select_focused_option(self, expected_text):
        """在当前焦点选择与期望文本匹配的选项"""
        try:
            active = self.driver.switch_to.active_element
            if active.text and expected_text in active.text:
                active.click()
                print(f"✓ 选择: {expected_text}")
                return True
        except:
            pass
        
        # 如果当前焦点不匹配，尝试按 Tab 查找
        for _ in range(3):
            self.press_tab(1)
            active = self.driver.switch_to.active_element
            if active.text and expected_text in active.text:
                active.click()
                print(f"✓ 选择: {expected_text}")
                return True
        
        print(f"✗ 未找到选项: {expected_text}")
        return False

    def open_and_start(self):
        """打开问卷并点击'立即开始'按钮（按2次Tab定位）"""
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
        
        # 按2次Tab定位到"立即开始"按钮
        self.press_tab(2)
        
        # 点击当前焦点（应该是"Start now"按钮）
        try:
            active = self.driver.switch_to.active_element
            if active.text in ["Start now", "立即开始"] or (active.tag_name == "button" and "Start" in active.text):
                active.click()
                print("✓ 已点击'Start now'按钮")
                time.sleep(3)
                
                # 验证是否进入问卷
                try:
                    self.driver.find_element(By.ID, "DatePicker0-label")
                    print("✓ 成功进入问卷")
                    return True
                except:
                    print("⚠️ 未进入问卷，尝试备用方法...")
                    # 备用：再按 Tab 寻找
                    for i in range(3):
                        self.press_tab(1)
                        active = self.driver.switch_to.active_element
                        if active.text and ("开始" in active.text or "Start" in active.text):
                            active.click()
                            print("✓ 备用方法点击成功")
                            time.sleep(3)
                            return True
        except Exception as e:
            print(f"❌ 点击开始按钮失败: {e}")
        
        print("❌ 无法进入问卷")
        return False

    def fill_questions(self):
        """按顺序填写所有题目"""
        print("开始填写问卷...")
        time.sleep(2)

        # 第1题：发现日期（按1次Tab到日期输入框）
        self.press_tab(1)
        today = datetime.now().strftime("%Y/%m/%d")
        self.fill_focused_input(today)

        # 第2题：发现项 - ABBS（按1次Tab到ABBS选项）
        self.press_tab(1)
        self.select_focused_option("ABBS")

        # 第3题：发现人（按1次Tab到姓名输入框）
        self.press_tab(1)
        self.fill_focused_input("Yi Wang")

        # 第4题：发现工位（按1次Tab到工位下拉菜单）
        self.press_tab(1)
        # 点击下拉菜单展开选项
        active = self.driver.switch_to.active_element
        active.click()
        time.sleep(0.5)
        # 按1次Tab选择第一个选项
        self.press_tab(1)
        # 按Enter确认
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        print("✓ 第4题 (发现工位): 随机选择了一个选项")
        time.sleep(0.5)

        # 第5题：安全状态 - 安全（按1次Tab）
        self.press_tab(1)
        self.select_focused_option("安全")

        # 第6题：问题描述（按1次Tab）
        self.press_tab(1)
        self.fill_focused_input("无问题")

        # 第7题：是否沟通 - 是（按1次Tab）
        self.press_tab(1)
        self.select_focused_option("是")

        # 第8题：是否卡特员工 - 是（按1次Tab）
        self.press_tab(1)
        self.select_focused_option("是")

        # 第9题：非卡特员工类型 - 不填写（跳过）

        # 按2次Tab到提交按钮
        self.press_tab(2)

        print("\n" + "="*60)
        print("✅ 所有题目已填写完成！")
        print("="*60 + "\n")

    def submit_form(self):
        """提交问卷"""
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