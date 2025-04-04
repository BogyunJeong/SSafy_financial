import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from .models import Crawling

def crawl_toss_comments(company_name):
    """
    토스증권에서 종목명을 검색하고, 커뮤니티 탭에서 댓글을 무한스크롤로 수집 후 DB에 저장합니다.
    """

    options = webdriver.ChromeOptions()
    # options.add_argument("headless")  # 디버깅 시 주석처리
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 ... Chrome/90.0.4430.93 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Toss 접속
        driver.get("https://tossinvest.com/")
        print("✅ [1] Toss 메인 접속 완료")
        time.sleep(2)

        # 2. 검색창 클릭
        search_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#tossinvest_global_navigation_bar > nav > div._9x1lao0 > div > button')))
        search_button.click()
        print("✅ [2] 검색창 열기 완료")

        # 3. 종목명 입력
        search_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='검색어를 입력해주세요']")))
        search_input.send_keys(company_name)
        print(f"✅ [3] 종목명 입력: {company_name}")
        time.sleep(1.5)

        # 4. 자동완성 → 첫 번째 종목 클릭
        first_result = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'button[data-selectable-item]:not([data-selectable-item="news"]):not([data-selectable-item="category"])'
        )))
        first_result.click()
        print("✅ [4] 첫 종목 클릭 완료")
        time.sleep(2)

        # 5. 종목코드 추출
        current_url = driver.current_url
        stock_code = current_url.split("/stocks/")[-1].split("/")[0]
        print(f"✅ [5] 종목코드 추출: {stock_code}")

        # 6. 커뮤니티 탭 클릭
        community_tab = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[id*="trigger-community"]')))
        community_tab.click()
        print("✅ [6] 커뮤니티 탭 클릭 완료")
        time.sleep(2)


        # ✅ 7. 댓글 수집
        comment_elements = driver.find_elements(By.CSS_SELECTOR,
        '#stock-content article a > span:nth-child(2) > span')
        comments = [el.text.strip() for el in comment_elements if el.text.strip()]
        print(f"✅ [7] 댓글 수집 완료: {len(comments)}개")

        # ✅ 8. DB 저장
        saved_comments = [
            Crawling(
                company_name=company_name,
                stock_code=stock_code,
                comment=comment_text,
                save_at=datetime.now()
            )
            for comment_text in comments
        ]
        print(f"✅ [8] DB 저장")
        Crawling.objects.bulk_create(saved_comments)

        return {
            "success": True,
            "saved_count": len(saved_comments),
            "company_name": company_name,
            "stock_code": stock_code,
            "comments": comments,
        }

    except Exception as e:
        import traceback
        print("⛔ 오류 발생:")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
        }

    finally:
        driver.quit()

