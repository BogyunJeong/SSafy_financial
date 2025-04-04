import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime

from bs4 import BeautifulSoup
from .models import Crawling

def crawl_toss_comments(company_name):
    """
    토스증권에서 종목명을 검색하고, 커뮤니티 탭에서 댓글을 수집하여 DB에 저장합니다.
    """

    # 브라우저 설정
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 화면 없이 실행 (디버깅할 땐 주석처리해도 OK)
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 ... Chrome/90.0.4430.93 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 크롬 드라이버 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 1. 토스 메인 페이지 접속
        driver.get("https://tossinvest.com/")
        time.sleep(2)

        # 2. 종목명 검색
        search_input = driver.find_element(By.CLASS_NAME, 'input_txt1vpj6')
        search_input.send_keys(company_name)
        time.sleep(1)
        search_input.send_keys('\n')
        time.sleep(3)

        # 3. 자동완성 리스트 중 첫 번째 종목 클릭
        first_result = driver.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(1) a')
        first_result.click()
        time.sleep(3)

        # 4. 종목 코드 얻기
        stock_url = driver.current_url
        stock_code = stock_url.split('/')[-2] if "community" in stock_url else stock_url.split('/')[-1]

        # 5. 커뮤니티 탭 클릭
        community_button = driver.find_element(By.XPATH, '//button[contains(text(), "커뮤니티")]')
        community_button.click()
        time.sleep(3)

        # 6. 댓글 수집 (tw-1r5dc8g0 클래스 포함하는 span)
        comment_elements = driver.find_elements(By.CSS_SELECTOR, 'span.tw-1r5dc8g0')
        comments = [el.text.strip() for el in comment_elements if el.text.strip()]

        # 7. DB 저장
        saved_comments = []
        for comment_text in comments:
            saved_comments.append(Crawling(
                company_title=company_name,
                stock_code=stock_code,
                comment=comment_text,
                save_at=datetime.now()
            ))

        Crawling.objects.bulk_create(saved_comments)

        return {
            "success": True,
            "saved_count": len(saved_comments),
            "company_name": company_name,
            "stock_code": stock_code,
            "comments": comments,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

    finally:
        driver.quit()