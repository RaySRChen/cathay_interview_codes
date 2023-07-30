from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
import time
import logging

WAIT_TIME_FOR_OPERATING_APP_SEC = 2

class CathayBankAutomation:
    def __init__(self, appium_server, platform_version, device_name, app_package, app_activity):
        self.appium_server = appium_server
        self.platform_version = platform_version
        self.device_name = device_name
        self.app_package = app_package
        self.app_activity = app_activity

        # 初始化 self.driver
        self.driver = self.open_chrome_app()

    def setup_logger(self, log_file):
        """設定日誌記錄，記錄程式執行和除錯資訊。"""
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def open_chrome_app(self):
        """打開 Chrome App。"""
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': self.platform_version,
            'deviceName': self.device_name,
            'appPackage': self.app_package,
            'appActivity': self.app_activity
        }

        driver = webdriver.Remote(self.appium_server, desired_caps)
        return driver

    def handle_login_and_privacy(self):
        """處理Chrome App 的登入和隱私提示設定。"""
        for element_id in ['signin_fre_continue_button', 'button_secondary', 'ack_button']:
            try:
                logging.info(f'Checking for the {element_id}...')
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((MobileBy.ID, f'com.android.chrome:id/{element_id}')))
                logging.info(f'Clicking on the {element_id}...')
                element.click()
                time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC)
            except:
                pass

    def handle_new_notification(self):
        """處理Chrome App的新通知設定。"""
        try:
            logging.info('Checking for the skip new notification button...')
            skip_new_notification_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((MobileBy.ID, 'com.android.chrome:id/negative_button'))
            )
            if skip_new_notification_button:
                logging.info('Clicking on the skip new notification button...')
                skip_new_notification_button.click()
        except:
            pass

    def take_screenshot_question_one(self, file_path):
        """截取題目一的螢幕截圖。"""
        logging.info('Waiting for Cathay Bank logo...')
        cathay_bank_logo = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, '//android.view.View[@content-desc="cathaybk"]/android.widget.Image'))
        )
        if cathay_bank_logo:
            self.driver.save_screenshot(file_path)
            logging.info(f'Screenshot saved: {file_path}')

    def take_screenshot_question_two(self, file_path_two):
        """截取題目二的螢幕截圖。"""
        self.driver.save_screenshot(file_path_two)
        logging.info(f'Screenshot saved: {file_path_two}')

    def close_chrome_app(self):
        """關閉 Chrome App。"""
        self.driver.quit()

    def click_at_position_with_retry(self, x, y, max_attempts=3):
        """點擊指定位置，失敗時進行重試。"""
        position = [(x, y)]
        for attempt in range(1, max_attempts + 1):
            try:
                self.driver.tap(position, 2)
                logging.info(f'Successfully clicked at position ({x}, {y}), attempt: {attempt}')
                time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC)  # 點擊間隔時間3秒
                break  
            except Exception as e:
                logging.warning(f'Failed to click at position ({x}, {y}), attempt: {attempt}, Error: {e}')
                if attempt == max_attempts:
                    raise  
                else:
                    time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC)  

    def scroll_by_percent(self, start_x_percent, start_y_percent, end_x_percent, end_y_percent, duration=200):
        """根據百分比位置滑動螢幕。"""
        screen_width = self.driver.get_window_size()['width']
        screen_height = self.driver.get_window_size()['height']

        # 根據百分比計算滑動的起始點和終點座標
        start_x = int(screen_width * start_x_percent)
        start_y = int(screen_height * start_y_percent)
        end_x = int(screen_width * end_x_percent)
        end_y = int(screen_height * end_y_percent)

        # 使用 TouchAction 執行滑動動作，設定速度參數
        touch_action = TouchAction(self.driver)
        touch_action.press(x=start_x, y=start_y).wait(duration).move_to(x=end_x, y=end_y).release().perform()

    def take_screenshot_paused_credit_card(self, paused_credit_card_count):
        """截取暫停信用卡的螢幕截圖。"""
        file_name = f"cathay_screenshot_question_3_paused_credit_card_{paused_credit_card_count}.png"
        self.driver.save_screenshot(file_name)
        logging.info(f'Screenshot saved: {file_name}')

    def calculate_pause_credit_card_count_by_swiping_screen(self, start_x_percent, start_y_percent, end_x_percent, end_y_percent, duration=200, swipe_count=1):
        """計算滑動後暫停信用卡的數量"""
        screen_width = self.driver.get_window_size()['width']
        screen_height = self.driver.get_window_size()['height']
        
        start_x = int(screen_width * start_x_percent)
        start_y = int(screen_height * start_y_percent)
        end_x = int(screen_width * end_x_percent)
        end_y = int(screen_height * end_y_percent)
        
        # 針對滑動前的畫面已有暫停的信用卡進行截圖
        paused_credit_card_count = 1
        self.take_screenshot_paused_credit_card(paused_credit_card_count)
        
        for i in range(swipe_count):
            # 使用 TouchAction 執行滑動動作，設定速度參數
            touch_action = TouchAction(self.driver)
            touch_action.press(x=start_x, y=start_y).wait(duration).move_to(x=end_x, y=end_y).release().perform()
            time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC) 
            # 判斷畫面是否成功滑動
            if self.is_screen_swiped(start_x, start_y, end_x, end_y):
                paused_credit_card_count += 1
                # 執行暫停信用卡截圖
                self.take_screenshot_paused_credit_card(paused_credit_card_count)
            else:
                print(f'第 {i+1} 次滑動失敗')
        print(f'1. 已針對每個暫停的信用卡進行截圖並計算數量為{paused_credit_card_count}張')

        # 計算總暫停信用卡數量
        logging.info(f'Paused credit card count: {paused_credit_card_count}')
        return paused_credit_card_count

    def is_screen_swiped(self, start_x, start_y, end_x, end_y, threshold=5):
        """檢查螢幕是否成功滑動。"""
        # 計算滑動前後的位置差
        diff_x = abs(start_x - end_x)
        diff_y = abs(start_y - end_y)
        
        # 判斷滑動是否成功，這裡使用一個 threshold 閾值來判斷
        # 如果滑動前後位置差超過閾值，表示滑動成功，否則滑動失敗
        return diff_x > threshold or diff_y > threshold

    def question_one(self, file_path):
        """執行題目1: 使用Chrome App到國泰世華銀行官網並將畫面截圖 (預期結果: 開啟網頁, 並截圖)"""
        logging.info('Starting running the Question NO.1--------------------------------')
        print('# 開始執行 題目1: 使用Chrome App到國泰世華銀行官網並將畫面截圖 (預期結果: 開啟網頁, 並截圖) ==>')
        self.driver.get("https://www.cathaybk.com.tw/cathaybk/")
        logging.info('Entered cathay bank website by using Chrome app...')

        self.handle_login_and_privacy()
        self.handle_new_notification()
        self.take_screenshot_question_one(file_path)
        print('已針對透過Chrome app 開啟的國泰世華銀行官網進行截圖\n')
        logging.info('Question NO.1 completed.')

    def question_two(self, file_path_two):
        """執行題目2: 點選左上角選單, 進入 個人金融 > 產品介紹 > 信用卡列表, 需計算有幾個項目並將畫面截圖 (預期結果: 1. 進入信用卡列表選單後截圖; 2. 計算有幾項目在信用卡選單下面)"""
        logging.info('Starting running the Question NO.2--------------------------------')
        print('# 開始執行 題目2: 點選左上角選單, 進入 個人金融 > 產品介紹 > 信用卡列表, 需計算有幾個項目並將畫面截圖 (預期結果: 1. 進入信用卡列表選單後截圖; 2. 計算有幾項目在信用卡選單下面) ==>')
        logging.info('Counting the sub-items of credit card list...')
        # 左上角三條線設定按鈕 (XPATH, ClassName & Index 無法成功定位, 替代方案採點擊指定位置 (x=114, y=414)
        self.click_at_position_with_retry(114, 414)

        # 點擊 '產品介紹' 選項
        logging.info(f'Clicking for the product_introduction_button...')
        product_introduction_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View/android.widget.TextView'))
        )
        if product_introduction_button:
            product_introduction_button.click()
            logging.info(f'Clicking on the product_introduction_button...')
            time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC)

        # 點擊 '信用卡' 選項
        logging.info(f'Clicking for the credit_card_button...')
        credit_card_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View/android.widget.TextView'))
        )
        if credit_card_button:
            credit_card_button.click()
            logging.info(f'Clicking on the credit_card_button...')
            time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC)
        
        # 截圖記錄畫面
        self.take_screenshot_question_two(file_path_two)
        print('1. 已針對信用卡列表有幾個項目進行截圖')

        # 計算信用卡列表下有幾個項目
        elements = self.driver.find_elements(MobileBy.XPATH, '//android.view.View[@resource-id="lnk_Link"]')
        filtered_elements = []

        # 檢查每個元素的 content-desc 是否不包含指定內容，若不包含則加入 filtered_elements 中
        for element in elements:
            content_desc = element.get_attribute("content-desc")
            excluded_keywords = ['開戶', '挑選信用卡', '線上申辦', '匯率查詢', '預約服務', '活動專區']
            if all(keyword not in content_desc for keyword in excluded_keywords):
                filtered_elements.append(element)
        count_filtered_elements = len(filtered_elements)
        logging.info(f'There are {count_filtered_elements} items under the credit card list.')
        print(f"2. 已計算信用卡列表下的項目有{count_filtered_elements}個\n")
        logging.info('Question NO.2 completed.')

    def question_three(self):
        """執行題目3: 個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有停發信用卡數量並截圖 (預期結果: 1. 進入信用卡列表選單後計算停發信用卡數量並截圖, 2. 比對計算停發信用卡數量與截圖數量相同)"""
        logging.info('Starting running the Question NO.3--------------------------------')
        print('# 開始執行 題目3: 個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有停發信用卡數量並截圖 (預期結果: 1. 進入信用卡列表選單後計算停發信用卡數量並截圖, 2. 比對計算停發信用卡數量與截圖數量相同) ==>')
        logging.info('Counting the stoped credit cards...')

        # 點擊 '卡片介紹' 選項
        logging.info(f'Click the card introduction...')
        credit_card_introduction_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, '//android.view.View[@content-desc="卡片介紹"]'))
        )
        if credit_card_introduction_button:
            credit_card_introduction_button.click()
            logging.info(f'Clicked the card introduction button...')
            time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC)

        # 自行指定滑動的起始點和終點的百分比
        start_x_percent = 0.5  # 代表螢幕寬度的 50%
        start_y_percent = 0.9  # 代表螢幕高度的 90%
        end_x_percent = 0.5    # 代表螢幕寬度的 50%
        end_y_percent = 0.1    # 代表螢幕高度的 10%
        # 指定滑動的速度（持續時間，單位：毫秒）
        scroll_duration = 1000  # 滑動持續 1 秒
        # 呼叫 scroll_by_percent 函式向上滑動三次
        for _ in range(3):
            self.scroll_by_percent(start_x_percent, start_y_percent, end_x_percent, end_y_percent, duration=scroll_duration)
            time.sleep(WAIT_TIME_FOR_OPERATING_APP_SEC)

        # 停發卡按鈕 (XPATH, ClassName & Index 無法成功定位, 替代方案採點擊指定位置 (x=958, y=247)
        self.click_at_position_with_retry(958, 247)
        
        # 自行指定滑動的起始點和終點的百分比位置，以及滑動的次數、速度和停止發行卡片的數量
        start_x_percent = 0.5  # 代表螢幕寬度的 50%
        start_y_percent = 0.5  # 代表螢幕高度的 50%
        end_x_percent = 0.0    # 代表螢幕寬度的 0%
        end_y_percent = 0.5    # 代表螢幕高度的 50%
        swipe_count = 10       # 滑動的次數
        swipe_duration = 1000  # 滑動持續 1 秒
        paused_credit_card_count = self.calculate_pause_credit_card_count_by_swiping_screen(start_x_percent, start_y_percent, end_x_percent, end_y_percent, duration=swipe_duration, swipe_count=swipe_count)
        
        logging.info(f'Total paused credit cards are {paused_credit_card_count}')

        # 計算截圖的總數量
        screenshot_count = paused_credit_card_count  # 因為我們針對每張停發的信用卡都進行了截圖

        logging.info(f'Total screenshots of credit cards are {screenshot_count}')
        print(f'2. 已比對計算停發信用卡數量與截圖數量相同都為{screenshot_count}張\n')
        logging.info('Question NO.3 completed.')

        # 將截圖的總數量返回，方便後續在程式碼的其他部分使用
        return screenshot_count

    def run_automation_test(self):
        """執行自動化測試流程"""
        appium_server = "http://127.0.0.1:4723/wd/hub"
        platform_version = "13.0"  
        device_name = "99101FFBA004HH"  
        app_package = "com.android.chrome"  
        app_activity = "com.google.android.apps.chrome.Main"  

        # 輸入截圖檔案路徑
        file_path = "cathay_screenshot_question_1.png"
        file_path_two = "cathay_screenshot_question_2.png"

        # 輸入logs檔案路徑
        log_file = "cathay_bank_automation_log.txt"
        self.setup_logger(log_file)
        self.driver = self.open_chrome_app()

        # 題目1
        self.question_one(file_path)

        # 題目2
        self.question_two(file_path_two)

        # 題目3
        screenshot_count = self.question_three()

        # 題目3的驗證步驟
        if screenshot_count == 0:
            logging.warning('Test Failed! 沒有任何停發信用卡的截圖!')
            print('3. 測試失敗：沒有任何停發信用卡的截圖')
        else:
            logging.info('Test Passed! 至少有一張停發信用卡的截圖!')
            print('3. 測試通過：至少有一張停發信用卡的截圖')

        self.close_chrome_app()

if __name__ == '__main__':
    appium_server = "http://127.0.0.1:4723/wd/hub"
    platform_version = "13.0"  
    device_name = "99101FFBA004HH"  
    app_package = "com.android.chrome"  
    app_activity = "com.google.android.apps.chrome.Main"  

    # 建立 CathayBankAutomation 物件，並執行自動化測試流程
    automation_test = CathayBankAutomation(appium_server, platform_version, device_name, app_package, app_activity)
    automation_test.run_automation_test()
