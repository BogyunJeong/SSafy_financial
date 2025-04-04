from django import forms
from .models import Crawling

class CrawlingForm(forms.ModelForm):
    class Meta:
        model = Crawling
        fields = '__all__'

        # 위젯
        widget= {
            'company_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요'}),
        }
