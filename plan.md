# Plano de Implementação: Pipeline ETL Batch E-commerce

Este documento detalha o plano técnico passo a passo para a implementação do pipeline DataOps definido no projeto.

## Proposed Changes

### 1. Preparação do Ambiente e Estrutura

Atualizaremos as dependências do projeto e criaremos a estrutura de pastas proposta.

#### [MODIFY] requirements.txt
Inclusão das bibliotecas:
- `duckdb` (Banco Analítico local)
- `pandera` (Validação de Schema)
- `pyarrow` (Suporte de I/O de dados otimizado entre Pandas/Polars e DuckDB)
- `tqdm` (Opcional, para barra de progresso no console se os scripts demorarem na geração)

#### Criação de Diretórios
- `data/raw`
- `data/trusted`
- `data/refined`
- `sql`
- `src/generators`
- `src/etl`
- `src/utils`

---

### 2. Utilitários (DataOps)

Construção dos módulos baseados nas premissas operacionais (observabilidade).

#### [NEW] src/utils/logger.py
Configuração do log estruturado que permitirá gravar eventos (início/fim, linhas processadas) com o módulo padrão `logging` em formato legível no console e persistindo em um arquivo `pipeline.log`.

---

### 3. Geração de Dados Sintéticos

#### [NEW] src/generators/generate_data.py
Script em Python utilizando `Faker`.
- Irá gerar de forma interconectada as 4 entidades: `customers` (3k), `products` (300), `orders` (10k) e `order_items` (20k).
- Irá persistir esses dados em arquivos CSV localizados no diretório `data/raw/`.

---

### 4. Validação de Contratos de Dados e Transformação (DataOps)

#### [NEW] src/utils/schemas.py
- Modelos usando a biblioteca `Pandera` (`DataFrameSchema`) para verificar se os dados que chegam do CSV bruto cumprem com os nossos padrões de tipagens.

---

### 5. Pipeline ETL e Banco DuckDB

#### [NEW] src/etl/pipeline.py
Este será o orquestrador do Pipeline de Carga Batch.
1. **Conexão:** Iniciará banco de dados local DuckDB (`ecommerce.duckdb`).
2. **Extração e Validação:** Fará carga CSV de `data/raw` e passará pelos schemas do `Pandera`.
3. **Carga Raw e Trusted:** Inserção ou substituição de dados raw e persistência da camada trusted corrigindo nulos e cast de colunas.
4. **Transformação Refined (One Big Table):** Usando SQL diretamente pelo DuckDB para calcular métricas (quantidade * preço) e fazer os joins entre as dimensões para a base consolidada.
5. **Idempotência:** O pipeline aceitará recargas consecutivas apagando/atualizando as tabelas DuckDB daquele processamento no fluxo full load.

---

### 6. Consultas Analíticas (Negócio)

#### [NEW] sql/queries.sql
Arquivo contendo 5 consultas SQL utilizando a OBT para as métricas solicitadas: Faturamento mensal, Faturamento por categoria, Volume por Estado, Ticket Médio e Top 10 Produtos.

#### [NEW] src/etl/analytics.py
Um script de suporte para executar os SQLs no DuckDB e apresentar os resultados formatados (DataFrame pandas) na tela do console, evidenciando o sucesso das análises.
