from datetime import date

from django.db import models


class Autor(models.Model):
    nome = models.CharField(max_length=150)
    imagem_url = models.URLField(blank=True, verbose_name='URL da imagem')

    def __str__(self):
        return self.nome


class Livro(models.Model):
    TIPO_ACERVO_CHOICES = [
        ('digital', 'Digital'),
        ('fisico', 'Físico'),
    ]

    CATEGORIA_CHOICES = [
        ('000', '000 – Generalidades e Informação'),
        ('100', '100 – Filosofia e Psicologia'),
        ('200', '200 – Religião e Teologia'),
        ('300', '300 – Ciências Sociais e Direito'),
        ('400', '400 – Linguística e Idiomas'),
        ('500', '500 – Ciências Puras (Exatas e Naturais)'),
        ('600', '600 – Ciências Aplicadas (Tecnologia)'),
        ('700', '700 – Artes e Recreação'),
        ('800', '800 – Literatura'),
        ('900', '900 – História e Geografia'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name='livros')
    ano = models.IntegerField()
    tipo_acervo = models.CharField(
        max_length=10, choices=TIPO_ACERVO_CHOICES, default='fisico'
    )
    categoria = models.CharField(
        max_length=3, choices=CATEGORIA_CHOICES, default='000'
    )
    imagem_url = models.URLField(blank=True, verbose_name='URL da imagem (capa)')

    def __str__(self):
        return self.titulo


class Exemplar(models.Model):
    ESTADO_CHOICES = [
        ('disponivel', 'Disponível'),
        ('emprestado', 'Emprestado'),
        ('manutencao', 'Em manutenção'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='exemplares')
    codigo_patrimonio = models.CharField(max_length=30, unique=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='disponivel')

    def __str__(self):
        return f'{self.livro.titulo} ({self.codigo_patrimonio})'


class Membro(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    exemplar = models.ForeignKey(Exemplar, on_delete=models.PROTECT, related_name='emprestimos')
    membro = models.ForeignKey(Membro, on_delete=models.PROTECT, related_name='emprestimos')
    data_emprestimo = models.DateField(auto_now_add=True)
    data_prevista_devolucao = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    valor_multa_diaria = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)

    @property
    def dias_atraso(self):
        fim = self.data_devolucao or date.today()
        atraso = (fim - self.data_prevista_devolucao).days
        return max(atraso, 0)

    @property
    def multa(self):
        return round(self.dias_atraso * float(self.valor_multa_diaria), 2)

    def __str__(self):
        return f'{self.exemplar} -> {self.membro}'


class Reserva(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='reservas')
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='reservas')
    data_reserva = models.DateTimeField(auto_now_add=True)
    atendida = models.BooleanField(default=False)

    class Meta:
        ordering = ['data_reserva']

    def __str__(self):
        return f'{self.membro} aguardando {self.livro}'
