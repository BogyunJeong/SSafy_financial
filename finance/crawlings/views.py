from django.shortcuts import render,redirect
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
            comments = Crawling.objects.filter(company_name=company_name).order_by('-pk')[:8]
            context = {
                'company_name': result['company_name'],
                'stock_code': result['stock_code'],
                'comments': comments,
                'saved_count': result['saved_count'],  # 추가됨
                'save_at': datetime.now()
            }
            return render(request, 'crawlings/stock_debate.html', context)

    context = {
        'success': False,
        'error': '현재 조회된 기업 정보가 없습니다. 기업 정보를 입력시켜주세요.'
    }
    return render(request, 'crawlings/stock_debate.html', context)

def delete(request, pk):
    crawling = Crawling.objects.get(pk=pk)
    company_name = crawling.company_name  # 삭제 전에 회사명 저장
    crawling.delete()  # 삭제 실행

    # 삭제 후 남은 댓글들 조회
    comments = Crawling.objects.filter(company_name=company_name)

    # 댓글이 없다면 초기화 화면으로
    if not comments.exists():
        context = {
            'success': False,
            'error': '현재 조회된 기업 정보가 없습니다. 기업 정보를 입력시켜주세요.'
        }
        return render(request, 'crawlings/stock_debate.html', context)

    # 댓글이 존재하면 그대로 렌더링
    stock_code = comments.first().stock_code  # 이 시점엔 first()가 절대 None 아님

    context = {
        'company_name': company_name,
        'stock_code': stock_code,
        'comments': comments,
    }

    return render(request, 'crawlings/stock_debate.html', context)