from django import forms
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ('title', 'introduction', 'site_link', 'avater_image')

        labels = {
            'title': '肩書き',
            'introduction': 'どんなひと？',
            'site_link': 'ウェブサイト',
            'avater_image': 'プロフィール画像'
        }

        help_texts = {
            'title': '自分を表すタイトルを20文字以内で入力',
            'introduction': 'プロフィール文を120文字以内で入力',
            'site_link': 'SNSや自分のブログのURLを入力',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'プログラマー、社長、愛妻家'}),
            'introduction': forms.Textarea(attrs={
                'placeholder': 'プロフィール紹介文',
                'size': 50}),
            'site_link': forms.TextInput(attrs={'placeholder': 'https://twitter.com/xxxxxxxxx'}),
            'avater_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }