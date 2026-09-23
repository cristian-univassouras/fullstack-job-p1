from datetime import date

from django import forms
from .models import Livro, Autor, Exemplar, Membro, Emprestimo, Reserva


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano', 'tipo_acervo', 'categoria', 'imagem_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['autor'].empty_label = 'Selecione um autor'

    def clean_ano(self):
        ano = self.cleaned_data.get('ano')
        ano_atual = date.today().year
        if ano and ano > ano_atual:
            raise forms.ValidationError('O ano de publicação não pode ser um ano futuro.')
        return ano


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome', 'imagem_url']


class ExemplarForm(forms.ModelForm):
    class Meta:
        model = Exemplar
        fields = ['livro', 'codigo_patrimonio', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['livro'].empty_label = 'Selecione um livro'


class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['nome', 'email']


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['exemplar', 'membro', 'data_prevista_devolucao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exemplar'].queryset = Exemplar.objects.filter(estado='disponivel')
        self.fields['exemplar'].empty_label = 'Selecione um exemplar disponível'
        self.fields['membro'].empty_label = 'Selecione um membro'


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['livro', 'membro']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['livro'].empty_label = 'Selecione um livro'
        self.fields['membro'].empty_label = 'Selecione um membro'
