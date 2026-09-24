# Sistema de Gerenciamento de Biblioteca

Projeto da P1 de Laboratório de Programação Full Stack (Universidade de Vassouras).
É um sistema web em Django para gerenciar o acervo de uma biblioteca: livros, autores,
exemplares, membros, empréstimos e reservas.

## Funcionalidades

- **Acervo de livros:** cadastro com título, autor, ano, tipo (físico ou digital),
  categoria pela classificação Dewey e imagem de capa.
- **Busca e filtro:** busca por texto em todas as listagens. Na de livros, também dá
  para filtrar por tipo e categoria, juntos ou separados, numa única consulta com `Q()`.
- **Exemplares:** cada cópia tem código de patrimônio e estado (disponível, emprestado
  ou em manutenção).
- **Empréstimos:** prazo de devolução sugerido de 14 dias e cálculo automático dos dias
  de atraso e da multa.
- **Reservas:** fila por livro. Na devolução de um exemplar, a reserva mais antiga
  daquele livro é marcada como atendida.
- **Validação:** o ano de publicação de um livro não pode ser um ano futuro.

## Tecnologias

- Python 3
- Django 6.1
- SQLite
- HTML e CSS (templates do Django)

## Como rodar

```bash
git clone https://github.com/cristian-univassouras/fullstack-job-p1.git
cd fullstack-job-p1

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000/. O banco `db.sqlite3` já vem com registros de exemplo.

Para usar o painel administrativo em http://127.0.0.1:8000/admin/, crie um usuário com
`python manage.py createsuperuser`.

## Estrutura

```
biblioteca/     configurações do projeto Django (settings, urls)
acervo/         app principal
  models.py     Autor, Livro, Exemplar, Membro, Emprestimo, Reserva
  forms.py      ModelForms e validações
  views.py      listagens com busca, CRUD, empréstimo e devolução
  templates/    páginas HTML
  static/       CSS
relatorio.txt   relatório da entrega P1
```
