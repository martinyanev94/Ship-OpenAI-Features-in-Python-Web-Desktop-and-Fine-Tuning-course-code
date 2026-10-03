from django import forms

class QuizGenerationForm(forms.Form):
    source_material = forms.CharField(
        label="Study material",
        widget=forms.Textarea(attrs={"rows": 8, "class": "form-control"}),
        min_length=20,
    )
