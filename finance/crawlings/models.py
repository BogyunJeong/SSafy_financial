from django.db import models

# Create your models here.
class Crawling(models.Model):
    company_title = models.CharField(max_length= 50) # 회사이름 
    stock_code = models.TextField() # 종목코드
    comment = models.TextField() # 댓글
    save_at = models.DateField() # 저장일자