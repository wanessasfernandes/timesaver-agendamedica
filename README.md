# TimeSaver - Agenda Médica 

Aplicação web de agenda médica desenvolvida como desafio técnico para o processo seletivo de Estágio em Desenvolvimento de Software da TimeSaver. Permite login de usuário autenticado, exibição de agendamentos médicos em formato de tabela interativa, e busca/filtro por paciente, CPF ou médico. 

## Descrição da solução

A aplicação foi contruida como um serviço Flask único, responsável por três frentes: 

1. **Autenticação** - tela de login que valida credenciais contra um banco SQLite, usando sessão de servidor para manter o usuário autenticando entre requisições.
2. **API interna de agendamentos** - endpoint HTTP (`/api/agendamentos`) que consulta o banco de dados e retorna os agendamentos em formato JSON, simulando o comportamento de uma API de agendamentos real.
3. **Frontend da agenda** - página que consome esse endpoint via `fetch` e exibe os dados usando a biblioteca Tabulador, com busca em tempo real por paciente, CPF ou médico. 

## Tecnologias utilizadas 

- **Python 3.12** +  **Flask** - framework web e roteamento 
- **Flask-SQLAlchemy** — ORM para acesso ao banco de dados
- **SQLite** — banco de dados relacional
- **Werkzeug (security)** — hash e verificação de senhas
- **Tabulator.js** — renderização da tabela de agendamentos no frontend
- **pytest** — testes automatizados
- **python-dotenv** — carregamento de variáveis de ambiente em desenvolvimento
- **Docker / Docker Compose** — containerização da aplicação

## Como executar com Docker 

Pré-requisitórios: Docker e Docker Compose instalador. 

1.Clone o repositório:
``` 
    git clone <https://github.com/wanessasfernandes/timesaver-agendamedica.git>
    cd timesaver-agendamedica
```

2. Crie o arquivo `.env` na raiz do projeto e preencha a `SECRET_KEY`: 
```
    SECRET_KEY: uma-chave-secreta
```

3. Suba a aplicação: 
    docker compose up --build

4. Acesse `http://localhost:5000` no navegador.

Ao subir, o container executa automaticamente o script de seed, criando o usuário de teste e populando o banco com agendamentos de exemplo (o script é idempotente — pode ser executado múltiplas vezes sem gerar duplicatas).

**Observação sobre o banco de dados no Docker**: como o banco utilizado é SQLite (um arquivo, não um serviço de rede), o `docker-compose.yml` não define um serviço separado de banco de dados. O arquivo `agenda.db` é persistido através de um volume (`./instance:/app/instance`), garantindo que os dados não sejam perdidos ao recriar o container. Isso atende ao requisito de "iniciar a aplicação e o banco de dados com um único comando", já que ambos sobem juntos através do único serviço definido.

### Executando sem Docker (desenvolvimento local)
```
python -m venv venv
venv\Script\active 

pip install -r requirements.txt

python seed.py

python run.py
```

## Credenciais do usuário de teste

| Campo    | Valor      |
|----------|------------|
| Usuário  | `teste`    |
| Senha    | `teste123` |

## Exemplos de uso

1. Acesse `/login` e entre com as credenciais acima.
2. Após o login, você é redirecionado para `/agenda`, onde a tabela de agendamentos é carregada automaticamente via `/api/agendamentos`.
3. Digite um nome de paciente, CPF (completo ou parcial) ou nome de médico no campo de busca — a tabela filtra os resultados automaticamente.
4. Uma busca sem correspondência exibe a mensagem "Nenhum agendamento encontrado", sem gerar erro.
5. Clique em "Sair" para encerrar a sessão e retornar ao login.

## Executando os testes

`pytest -v`

Os testes cobrem: login com credenciais válidas e inválidas, campos vazios, proteção de rotas autenticadas, busca de agendamento com e sem resultado, e a resposta do endpoint interno de agendamentos. Os testes utilizam um banco SQLite em memória, isolado do banco de desenvolvimento.

## Decisões técnicas

### Serviço único em vez de API separada
O desafio permitia simular a API de agendamentos como um serviço separado ou como um endpoint interno na mesma aplicação. Optei por uma aplicação Flask única com endpoint interno (`/api/agendamentos`) simulando a API de agendamentos, priorizando organização de código e tratamento de erros dentro do prazo disponível. A estratégia adotada foi: os agendamentos (mockados) são persistidos na tabela `Agendamento` do próprio banco SQLite; o endpoint `/api/agendamentos` executa uma consulta (`Agendamento.query.all()`), serializa os resultados usando o método `to_dict()` de cada registro, e retorna a resposta em JSON; o frontend consome esse endpoint via `fetch`, exatamente como consumiria uma API externa. Essa abordagem atende ao requisito de "requisição HTTP para buscar os dados dos agendamentos" descrito no desafio, com a vantagem de reduzir a complexidade de orquestração dado o prazo disponível.

### `config.py` dentro do pacote `app/`
Optei por manter `config.py` dentro do pacote `app/`, tratando a configuração como parte integrante da aplicação, em vez de deixá-lo solto na raiz do projeto. Essa escolha mantém coerência com o restante da estrutura (models, routes, services e templates também residem dentro de `app/`), e evita misturar arquivos Python de aplicação com os arquivos de infraestrutura do projeto (Dockerfile, docker-compose, README) que ficam na raiz.

### Campo `horario` como `String` em vez de `Time`
O campo `horario` do modelo `Agendamento` foi definido como `String` em vez do tipo `Time` do SQLAlchemy. Essa decisão simplifica a serialização para JSON (não é necessário converter um objeto `time` para string a cada resposta da API) e evita ambiguidade de fuso horário ou formatação — o valor já nasce no formato `"HH:MM"` esperado pelo frontend. A limitação conhecida dessa abordagem é que o banco não valida nativamente se o valor é um horário bem formado; essa validação, se necessária, ficaria a cargo da camada de aplicação.

### Lógica de senha dentro do próprio modelo `Usuario`
Os métodos `set_senha()` e `verificar_senha()` foram implementados diretamente na classe `Usuario`, em vez de ficarem soltos em `services.py`. Essa escolha segue o padrão conhecido como "fat model, thin controller": a entidade é responsável por cuidar da própria regra de negócio relacionada a ela mesma (nesse caso, gerar e validar o hash da senha), mantendo `services.py`/`routes.py` mais enxutos e focados em orquestração.

### Controle de versão em branch única
O desenvolvimento foi conduzido diretamente na branch `main`, sem uso de feature branches. Dado que o projeto foi desenvolvido individualmente e sob prazo reduzido, essa abordagem evitou o overhead de criação e merge de branches, mantendo o foco na entrega funcional. O histórico de commits foi organizado por bloco funcional (estrutura inicial, modelos, autenticação, API, frontend, testes, Docker), com mensagens seguindo o padrão Conventional Commits (`feat:`, `fix:`, `test:`, `chore:`), garantindo rastreabilidade da evolução do projeto mesmo sem uso de branches.

### Testes com banco SQLite em memória
Os testes automatizados utilizam um banco SQLite em memória (`sqlite:///:memory:`), isolado do banco de desenvolvimento (`instance/agenda.db`). Isso garante que a suíte de testes seja rápida, isolada e repetível — cada execução parte de um estado limpo e conhecido, sem depender ou interferir nos dados reais da aplicação.

### Seed idempotente
O script `seed/seed.py` verifica a existência de dados antes de inserir novos registros, tornando-o seguro para execução repetida (tanto manualmente quanto automaticamente, a cada subida do container Docker), sem gerar erros de duplicidade ou violação de unicidade.

### Tratamento de erros e logging
Todas as rotas que acessam o banco de dados estão envolvidas em blocos `try/except`, capturando `SQLAlchemyError` e retornando mensagens amigáveis ao usuário, sem expor stack traces técnicos. Eventos relevantes (tentativas de login inválidas, erros de conexão, buscas sem resultado) são registrados via módulo `logging` padrão do Python, facilitando o diagnóstico de problemas em ambiente real.

## Limitações conhecidas

- O Tabulator (biblioteca da tabela) e a fonte do frontend (Google Fonts) são carregados via CDN. Em ambientes sem acesso à internet, o frontend perde a estilização/renderização da tabela, ainda que o backend continue funcional.
- A "API de agendamentos" é simulada internamente através de dados persistidos no próprio banco SQLite da aplicação, e não como um serviço HTTP externo real.
- O campo `horario` não possui validação de formato a nível de banco de dados (ver decisão técnica acima).
- Não há paginação implementada na tabela de agendamentos; para o volume de dados do desafio (poucos registros mockados), isso não impacta a experiência de uso.