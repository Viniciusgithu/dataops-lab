# DataOps Mini Lab

Pipeline de dados local para ingestão de pedidos CSV em um banco analítico DuckDB — base para evolução com práticas de DataOps.


## Estrutura do Projeto

```
dataops-mini-lab/
├── data/
│   ├── raw/                 # Dados brutos (CSV de entrada)
│   │   └── orders_2026_03_23.csv
│   └── curated/             # Dados tratados (uso futuro)
├── ingestion/
│   └── load_orders.py       # Script de ingestão e carga
├── docs/                    # Documentação complementar
├── warehouse/               # Banco de dados DuckDB
├── .gitignore
└── readme.md
```


## Como Configurar o Ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/Viniciusgithu/dataops-lab.git
cd dataops-lab
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Atualizar o pip

```bash
python -m pip install --upgrade pip
```

### 4. Instalar as dependências

```bash
pip install pandas duckdb
```

## Como Executar o Pipeline

Com o ambiente virtual ativado, execute:

```bash
python ingestion/load_orders.py
```

### Saída esperada

O script irá:

1. **Exibir uma prévia dos dados brutos** do CSV
2. **Criar a tabela `raw_orders`** no banco `warehouse/local.duckdb`
3. **Exibir uma agregação por status** com total de pedidos e valor total

Exemplo de saída:

```
Preview of raw data:
   order_id  customer_id             order_ts  amount     status
0         1         1001  2026-03-23 08:10:00   55.90  delivered
1         2         1002  2026-03-23 08:15:00   32.50  delivered
...

Table 'raw_orders' created successfully.

Aggregated result by status:
      status  total_orders  total_amount
0  delivered             6        314.59
1  cancelled             2        138.40
2  processing            2        105.00
```

## O que o Script Faz

1. Lê o arquivo CSV em `data/raw/orders_2026_03_23.csv`
2. Conecta (ou cria) o banco DuckDB em `warehouse/local.duckdb`
3. Cria a tabela `raw_orders` com tipagem explícita
4. Executa uma consulta agregada agrupando por `status`

## Reflexões

1. **Onde está o dado bruto?** — Na pasta `data/raw/`, no arquivo CSV de entrada.
2. **Qual é o papel do script Python?** — Ele é o orquestrador do pipeline: lê o CSV, carrega no DuckDB e executa a consulta agregada.
3. **O que aconteceria se uma coluna do CSV mudasse de nome?** — O script falharia com erro, pois os `CAST` referenciam colunas específicas. Isso evidencia a necessidade de contratos de dados.
4. **Por que o primeiro commit no Git é importante?** — Ele estabelece o ponto de partida do projeto, permitindo rastrear toda a evolução e, se necessário, reverter alterações.
5. **O pipeline funciona, mas ele já pode ser considerado confiável para produção?** — Não. Faltam validações, testes, tratamento de erros, logs estruturados e monitoramento — práticas que serão incorporadas nos próximos encontros.

## Licença

Projeto acadêmico — uso para fins de estudo e aprendizado.
