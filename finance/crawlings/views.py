from django.shortcuts import render
from .models import Crawling
from .crawl import crawl_toss_comments

# Create your views here.
def index(request):
    return render(request,'crawlings/index.html')

def stock_debate(request): # 기본 화면 보여줌
    if request.method == 'POST': # POST 요청이 있을 경우( 즉 종목 정보를 받아와야하는 경우 )
        company_name = request.POST.get('company_name')     # stock_debate 에서 입력한 회사 이름
        result = crawl_toss_comments(company_name)      # crawl.py 의 함수 이름

        if result.get('success'): # 만약 가져오는데 성공 했다면
            context = {
                'success': True,
                'company_name': result['company_name'],
                'stock_code': result['stock_code'],
                'save_at': result['save_at']
            } # 회사명, 주식 종목, 저장일 가져와서서
            return render(request, 'crawlings/stock_debate.html', context) # 출력한다.

    context = {
    'success': False,
    'error': '오류임'
    }
    return render(request, 'crawlings/stock_debate.html', context)




def delete_comment(request):
    pass


