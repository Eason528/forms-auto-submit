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
        # ====== 无头模式（GitHub Actions 必需） ======
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--window-size=1920,1080")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-blink-features=AutomationControlled")
        firefox_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        # ==========================================
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.wait = WebDriverWait(self.driver, 30)

    def open_and_start(self):
        """打开问卷并点击'立即开始'按钮"""
        print("正在打开问卷...")
        self.driver.get(self.form_url)
        time.sleep(8)

        print("正在查找'立即开始'按钮...")
        try:
            start_btn = self.driver.find_element(By.XPATH, "//div[text()='立即开始']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", start_btn)
            print("✓ 已进入问卷")
            time.sleep(5)
            return True
        except Exception as e:
            print(f"❌ 点击开始按钮失败: {e}")
            # 尝试备用方法
            try:
                start_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), '开始')]")
                self.driver.execute_script("arguments[0].click();", start_btn)
                print("✓ 已进入问卷 (备用方法)")
                time.sleep(5)
                return True
            except:
                return False

    def fill_questions(self):
        """完整填写问卷"""
        print("开始填写问卷...")
        time.sleep(3)

        def click_label(label_text):
            """通过标签文本点击单选按钮"""
            try:
                label = self.driver.find_element(By.XPATH, f"//label[normalize-space(.)='{label_text}']")
                self.driver.execute_script("arguments[0].click();", label)
                print(f"✓ 选择: {label_text}")
                return True
            except Exception as e:
                print(f"✗ 选择 '{label_text}' 失败: {e}")
                return False

        # ====== 第1题：发现日期 ======
        try:
            date_input = self.driver.find_element(By.ID, "DatePicker0-label")
            today = datetime.now().strftime("%Y/%m/%d")
            date_input.clear()
            date_input.send_keys(today)
            print(f"✓ 第1题 (发现日期): {today}")
        except Exception as e:
            print(f"✗ 第1题失败: {e}")

        # ====== 第2题：发现项 - ABBS ======
        click_label("ABBS")

        # ====== 第3题：发现人（通过 Tab 定位） ======
        try:
            for _ in range(1):
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(0.3)
            active = self.driver.switch_to.active_element
            active.clear()
            active.send_keys("Yi Wang")
            print("✓ 第3题 (发现人): Yi Wang")
        except Exception as e:
            print(f"✗ 第3题失败: {e}")

        # ====== 第4题：发现工位 ======
        try:
            dropdown = self.driver.find_element(By.XPATH, 
                "//div[contains(@class, 'dropdown') or contains(@role, 'combobox') or contains(@aria-haspopup, 'listbox')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            time.sleep(0.5)
            dropdown.click()
            time.sleep(1)
            options = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'item') or contains(@role, 'option')]"))
            )
            if options:
                random_index = random.randint(1, len(options) - 1) if len(options) > 1 else 0
                options[random_index].click()
                print("✓ 第4题 (发现工位): 随机选择了一个选项")
            else:
                print("✗ 第4题: 没有找到下拉选项")
        except Exception as e:
            print(f"✗ 第4题填写失败: {e}")

        # ====== 第5题：安全状态 - 安全 ======
        click_label("安全")

        # ====== 第6题：问题描述（通过 Tab 定位） ======
        try:
            for _ in range(1):
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(0.3)
            active = self.driver.switch_to.active_element
            active.send_keys("无问题")
            print("✓ 第6题 (问题描述): 无问题")
        except Exception as e:
            print(f"✗ 第6题失败: {e}")

        # ====== 第7题：是否沟通 - 是 ======
        try:
            inputs = self.driver.find_elements(By.XPATH, "//input[not(ancestor::div[@aria-hidden='true'])]")
            if len(inputs) > 8:
                self.driver.execute_script("arguments[0].click();", inputs[8])
                print("✓ 第7题 (是否沟通): 是")
            else:
                click_label("是")
        except Exception as e:
            try:
                click_label("是")
            except:
                print(f"✗ 第7题失败: {e}")

        # ====== 第8题：是否卡特员工 - 是 ======
        try:
            inputs = self.driver.find_elements(By.XPATH, "//input[not(ancestor::div[@aria-hidden='true'])]")
            if len(inputs) > 10:
                self.driver.execute_script("arguments[0].click();", inputs[10])
                print("✓ 第8题 (是否卡特员工): 是")
            else:
                all_yes = self.driver.find_elements(By.XPATH, "//label[normalize-space(.)='是']")
                if len(all_yes) >= 3:
                    all_yes[2].click()
                    print("✓ 第8题 (是否卡特员工): 是")
                else:
                    click_label("是")
        except Exception as e:
            try:
                all_yes = self.driver.find_elements(By.XPATH, "//label[normalize-space(.)='是']")
                if len(all_yes) >= 3:
                    all_yes[2].click()
                    print("✓ 第8题 (是否卡特员工): 是")
                else:
                    print(f"✗ 第8题失败: {e}")
            except:
                print(f"✗ 第8题失败: {e}")

        # ====== 第9题：非卡特员工类型 - 不填写 ======
        print("○ 第9题: 不填写")

        print("\n" + "="*60)
        print("✅ 所有题目已填写完成！")
        print("="*60 + "\n")

    def submit_form(self):
        """自动提交问卷"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            submit_btn = self.driver.find_element(By.XPATH, 
                "//button[@type='submit'] | //button[contains(text(), '提交')] | //button[contains(text(), 'Submit')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            submit_btn.click()
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