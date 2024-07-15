# Projeto Django - Gerenciamento de Gerentes e Abastecimentos

Este é um projeto Django para gerenciar informações de abastecimento de um posto de combustível. O projeto permite criar, atualizar, listar e excluir registros de gerentes e abastecimentos. Além disso, é possível gerar relatórios em PDF dos abastecimentos realizados por um determinado gerente.

## Deploy

Você pode acessar o projeto em funcionamento no seguinte link: [Gerenciamento de Abastecimentos](https://beatriz888.pythonanywhere.com/gerentes/)

## Funcionalidades

- **Cadastrar Gerente**: Permite cadastrar um novo gerente junto com seus abastecimentos.
- **Atualizar Gerente**: Atualiza as informações de um gerente existente.
- **Excluir Abastecimento**: Exclui um abastecimento associado a um gerente.
- **Atualizar Abastecimento**: Atualiza os detalhes de um abastecimento existente.
- **Gerar PDF de Abastecimentos**: Gera um relatório em PDF dos abastecimentos de um gerente com base no CPF fornecido.

## Como usar

### Clonar o repositório

Primeiro, clone o repositório para sua máquina local:

```bash

git clone https://github.com/Beatrizfernan/Posto-ABC.git {nome do seu repositorio}

```

### Configurar o ambiente virtual

Navegue até o diretório do projeto e crie um ambiente virtual:

```bash
cd seu-repositorio
python -m venv venv

```

Ative o ambiente virtual:

- No Windows:

```bash
venv\Scripts\activate

```

- No macOS/Linux:

```bash

source venv/bin/activate

```

### Instalar as dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt

```

### Executar as migrações

Antes de executar o servidor, aplique as migrações do banco de dados:

```bash
python manage.py makemigrations
python manage.py migrate

```

### Iniciar o servidor

Finalmente, inicie o servidor de desenvolvimento Django:

```bash
python manage.py runserver

```
