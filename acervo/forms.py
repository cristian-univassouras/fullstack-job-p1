from django import forms
from .models import Livro, Autor, Exemplar, Membro, Emprestimo, Reserva


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano', 'tipo_acervo', 'categoria']


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome']


class ExemplarForm(forms.ModelForm):
    class Meta:
        model = Exemplar
        fields = ['livro', 'codigo_patrimonio', 'estado']


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


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['livro', 'membro']
