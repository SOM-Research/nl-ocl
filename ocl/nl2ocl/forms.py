from django import forms

class NewQuestionForm(forms.Form):
    question = forms.CharField(min_length=10, required=True)
    translation = forms.CharField( widget=forms.Textarea, required=True )

class ReportQuestionForm(forms.Form):
    reason = forms.CharField( widget=forms.Textarea, required=True )