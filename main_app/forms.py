from django import forms
from .models import Post

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ('title', 'tags', 'content', 'site_link')

        labels = {
            'title': 'タイトル',
            'tags': 'タグ',
            'content': '極意の詳細',
            'site_link': '関連サイトリンク',
        }

        help_texts = {
            'title': '極意のタイトルを20文字以内で入力',
            'tags': 'タイトルのタグを,(カンマ)区切りで入力',
            'content': '極意の内容を100文字以内で入力',
            'site_link': '詳細サイトのURLなどを入力',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '極意タイトル'}),
            'content': forms.Textarea(attrs={
                'placeholder': '極意の内容',
                'size': 50}),
            'site_link': forms.TextInput(attrs={'placeholder': 'https://twitter.com/xxxxxxxxx'}),
        }