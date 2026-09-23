from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Livro, Autor, Exemplar, Membro, Emprestimo, Reserva
from .forms import (
    LivroForm, AutorForm, ExemplarForm, MembroForm, EmprestimoForm, ReservaForm
)


def lista_livros(request):
    livros = Livro.objects.select_related('autor').all()

    nome = request.GET.get('nome', '')
    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')

    if nome:
        livros = livros.filter(Q(titulo__icontains=nome) | Q(autor__nome__icontains=nome))
    if tipo:
        livros = livros.filter(tipo_acervo=tipo)
    if categoria:
        livros = livros.filter(categoria=categoria)

    return render(
        request, 'acervo/lista.html',
        {
            'livros': livros,
            'tipos': Livro.TIPO_ACERVO_CHOICES,
            'categorias': Livro.CATEGORIA_CHOICES,
            'filtro_nome': nome,
            'filtro_tipo': tipo,
            'filtro_categoria': categoria,
        }
    )


def novo_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = LivroForm()
    return render(request, 'acervo/form.html', {'form': form})


def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'acervo/form.html', {'form': form})


def apagar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect('lista')
    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': livro})


def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'acervo/autores.html', {'autores': autores})


def novo_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_autores')
    else:
        form = AutorForm()
    return render(request, 'acervo/form.html', {'form': form})


def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('lista_autores')
    else:
        form = AutorForm(instance=autor)
    return render(request, 'acervo/form.html', {'form': form})


def apagar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        return redirect('lista_autores')
    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': autor})


def lista_exemplares(request):
    exemplares = Exemplar.objects.select_related('livro').all()
    return render(request, 'acervo/exemplares.html', {'exemplares': exemplares})


def novo_exemplar(request):
    if request.method == 'POST':
        form = ExemplarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_exemplares')
    else:
        form = ExemplarForm()
    return render(request, 'acervo/form.html', {'form': form})


def editar_exemplar(request, pk):
    exemplar = get_object_or_404(Exemplar, pk=pk)
    if request.method == 'POST':
        form = ExemplarForm(request.POST, instance=exemplar)
        if form.is_valid():
            form.save()
            return redirect('lista_exemplares')
    else:
        form = ExemplarForm(instance=exemplar)
    return render(request, 'acervo/form.html', {'form': form})


def apagar_exemplar(request, pk):
    exemplar = get_object_or_404(Exemplar, pk=pk)
    if request.method == 'POST':
        exemplar.delete()
        return redirect('lista_exemplares')
    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': exemplar})


def lista_membros(request):
    membros = Membro.objects.all()
    return render(request, 'acervo/membros.html', {'membros': membros})


def novo_membro(request):
    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_membros')
    else:
        form = MembroForm()
    return render(request, 'acervo/form.html', {'form': form})


def editar_membro(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            return redirect('lista_membros')
    else:
        form = MembroForm(instance=membro)
    return render(request, 'acervo/form.html', {'form': form})


def apagar_membro(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == 'POST':
        membro.delete()
        return redirect('lista_membros')
    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': membro})


def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.select_related('exemplar__livro', 'membro').all()
    return render(request, 'acervo/emprestimos.html', {'emprestimos': emprestimos})


def novo_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save()
            emprestimo.exemplar.estado = 'emprestado'
            emprestimo.exemplar.save()
            return redirect('lista_emprestimos')
    else:
        form = EmprestimoForm(initial={'data_prevista_devolucao': date.today() + timedelta(days=14)})
    return render(request, 'acervo/form.html', {'form': form})


def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        emprestimo.data_devolucao = date.today()
        emprestimo.save()

        exemplar = emprestimo.exemplar
        exemplar.estado = 'disponivel'
        exemplar.save()

        proxima_reserva = Reserva.objects.filter(livro=exemplar.livro, atendida=False).first()
        if proxima_reserva:
            proxima_reserva.atendida = True
            proxima_reserva.save()

    return redirect('lista_emprestimos')


def lista_reservas(request):
    reservas = Reserva.objects.select_related('livro', 'membro').all()
    return render(request, 'acervo/reservas.html', {'reservas': reservas})


def nova_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'acervo/form.html', {'form': form})


def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_reservas')
    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': reserva})
