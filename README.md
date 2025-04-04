여기서 시작합시다.

생성될 프로젝트

financial

앱 이름

1. crawlings 
   
   stock_finder.html -> base.html 역할
   
   index -> 접속시 사용자가 회사 정보 얻음.
   
   검색시 회사 종목명을 받아 크롤링 수행 -> selenium으로 토스증권에서 사용자가 입력한 종목의 토론 데이터 수집

        -> 내용 수집

    table

    회사 이름 - text

    종목코드 - text

    댓글 내용 - text

저장 일자 - datetime

필요한게

index -> 인덱스 창에서 크롤링 한걸 업데이트 하도록

create

update

delete

  

도전 -> 크롤링 데이터를 기준으로 gpt한테 입력시켜서 감정 분석 시키기

역할 분담.

1. 꾸미는거랑 crud 구현할 사람 나눈다.
   
   꾸미는거 1 , crud 2 -> 알아서 할건데 

프론트 -> 승재형 -> html

저희가 views, url, form

    모델

    회사 이름 - text 변수 company_title

    종목코드 - text -> stock_code

    댓글 내용 - text -> comment

   저장 일자 - datetime -> save_date

인덱스 -> 소개화면 (소개만 적혀있음)

stock_discussion -> 검색 후 회사의 댓글을 가져옴 

## 변수명 정리

#### 모델 이름

    회사 이름 - text 변수 company_title

    종목코드 - text -> stock_code

    댓글 내용 - text -> comment

   저장 일자 - datetime -> save_date
