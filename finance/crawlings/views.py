from django.shortcuts import render
from .models import Crawling
from .crawl import crawl_toss_comments
from datetime import datetime

# Create your views here.
def index(request):
    return render(request,'crawlings/index.html')

def stock_debate(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        result = crawl_toss_comments(company_name)

        if result.get('success'):
            context = {
                'success': True,
                'company_name': result['company_name'],
                'stock_code': result['stock_code'],
                'saved_count': result['saved_count'],  # 추가됨
                'save_at': datetime.now()
            }
            return render(request, 'crawlings/stock_debate.html', context)

    context = {
        'success': False,
        'error': '크롤링 실패 또는 유효하지 않은 종목명입니다.'
    }
    return render(request, 'crawlings/stock_debate.html', context)





def delete_comment(request):
    pass


