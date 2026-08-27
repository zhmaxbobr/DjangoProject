from django import forms

class Anketa(forms.Form):
    GENDERS = [("female","Женского"), ("male","Мужского")]
    gender = forms.ChoiceField(
        label="Какого Вы пола:",
        choices=GENDERS,
        widget=forms.Select,
        required=True
    )
    age = forms.IntegerField(
        label="Нижняя планка возраста:",
        required=True
    )
    FIND_GENDERS = [("female", "Женского"), ("male", "Мужского"), ("both", "Без разницы")]
    find_gender = forms.ChoiceField(
        label="Какого пола ищем:",
        choices=FIND_GENDERS,
        widget=forms.Select,
        required=True
    )

