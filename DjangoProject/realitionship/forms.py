from django import forms

class Anketa(forms.Form):
    GENDERS = [[("female","Женского"), ("male","Мужского")]]
    gender = forms.ChoiceField(
        choices=GENDERS,
        widget=forms.Select,
        required=True
    )
    age = forms.IntegerField(
        required=True
    )
    FIND_GENDERS = [("female", "Женского"), ("male", "Мужского"), ("both", "Без разницы")]
    find_gender = forms.ChoiceField(
        choices=FIND_GENDERS,
        widget=forms.Select,
        required=True
    )

