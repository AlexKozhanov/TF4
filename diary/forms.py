from django.forms import ModelForm, BooleanField
from django.core.exceptions import ValidationError

from diary.models import Diary, DiaryEntries

cuss = [
    'казино', 'криптовалюта', 'крипта',
    'биржа', 'дешево', 'бесплатно',
    'обман', 'полиция', 'радар'
]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class DiaryForm(ModelForm):
    """
    Класс-форма Личный Дневник
    """

    class Meta:
        model = Diary
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.fields['head'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название Заголовка'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Содержимое дневника, кратко и если нужно'
        })
        self.fields['owner'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Владелец'
        })

    def clean(self):
        cleaned_data = super().clean()
        head = cleaned_data.get('head')
        content = cleaned_data.get('content')

        if head and content and head == content:
            self.add_error(field='name', error='Имя и описание не могут иметь одинаковое значение')


class DiaryEntriesForm(ModelForm):
    """
    Класс-форма Записи в Дневнике
    """

    class Meta:
        model = DiaryEntries
        fields = ('head', 'content', 'owner_entries', 'diary', 'publication_status',)

    def __init__(self, *args, **kwargs):
        super(DiaryEntriesForm, self).__init__(*args, **kwargs)
        self.fields['head'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название Заголовок'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Содержимое дневника, кратко и если нужно'
        })
        self.fields['owner_entries'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Владелец'
        })
        self.fields['diary'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Дневник'
        })
        self.fields['publication_status'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите Статус публикации'
        })

    def clean(self):
        cleaned_data = super().clean()
        head = cleaned_data.get('head')
        content = cleaned_data.get('content')

        if head and content and head == content:
            self.add_error(field='name', error='Заголовок и Содержимое не могут иметь одинаковое значение')

    def clean_name(self):
        head = self.cleaned_data.get('head')
        lowered = head.lower()
        for word in cuss:
            if word in lowered:
                raise ValidationError('Имя Заголовок запрещено')
        return head
