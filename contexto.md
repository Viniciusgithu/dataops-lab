# Projeto DataOps Lab: Pipeline ETL Batch E-commerce

## 1. Visão Geral do Projeto

- **Objetivo:** Simular o processamento de dados de um e-commerce gerando bases sintéticas, processando-as em batch e carregando em uma base analítica local.
- **Foco do Estudo:** Engenharia de Dados e práticas de DataOps.

---

## 2. Arquitetura e Stack Tecnológica

- **Linguagem:** Python.
- **Geração de Dados:** Biblioteca `Faker`.
- **Banco de Dados Analítico:** `DuckDB` (local).

### Estrutura de Diretórios Recomendada

```text
dataops-lab/
├── data/
│   ├── raw/          # Dados brutos (CSVs gerados pelo Faker)
│   ├── trusted/      # Dados padronizados e limpos
│   └── refined/      # Dados prontos para análise (One Big Table)
├── sql/              # Queries de criação de tabelas e consultas de análise
├── src/
│   ├── generators/   # Scripts de geração de dados sintéticos
│   ├── etl/          # Scripts do pipeline (extração, transformação e carga)
│   └── utils/        # Reusáveis de log e validação
├── contexto.md       # Este documento
└── README.md         # Informações do repositório
```

---

## 3. Dicionário de Dados e Volumetria (Geração)

### 3.1. `customers.csv`
**Volume:** 3.000 registros

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `customer_id` | String | Identificador único do cliente |
| `customer_name`| String | Nome completo |
| `city` | String | Cidade |
| `state` | String | Estado |
| `signup_date` | Date/Time | Data de cadastro |

### 3.2. `products.csv`
**Volume:** 300 registros

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `product_id` | String | Identificador do produto |
| `product_name` | String | Nome do produto |
| `category` | String | Categoria do produto |
| `price` | Float | Preço unitário original do produto |

### 3.3. `orders.csv`
**Volume:** 10.000 registros

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `order_id` | String | Identificador único do pedido |
| `customer_id` | String | Relacionado a `customers.csv` |
| `order_date` | Date/Time | Data e hora em que ocorreu a compra |
| `status` | String | Status do pedido (ex: Processando, Concluído) |

### 3.4. `order_items.csv`
**Volume:** 20.000 registros

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `order_item_id` | String | Identificador do registro do item específico no pedido |
| `order_id` | String | Relacionado a `orders.csv` |
| `product_id` | String | Relacionado a `products.csv` |
| `quantity` | Integer | Quantidade do produto no pedido |
| `unit_price` | Float | Preço efetivado no momento da venda |

---

## 4. Pipeline ETL (Etapas)

O fluxo de processamento de dados percorrerá as seguintes etapas lógicas:

1. **Extração:** Leitura dos CSVs situados na camada `data/raw/`.
2. **Transformação:**
   - Ajuste de tipagem (cast) de colunas de texto para numéricos ou data, e tratamento de nulos.
   - Cálculo da métrica `valor_total` nos itens do pedido (quantity * unit_price).
   - Realização das junções/JOINs necessários mesclando transações (`orders`, `order_items`) com dimensões (`customers`, `products`).
   - Geração de uma estrutura denormalizada (*One Big Table*).
3. **Carga (DuckDB):** Persistência no banco de dados distribuído pelas seguintes frentes físicas/views:
   - Tabela bruta (Raw).
   - Tabela tratada (Trusted).
   - Tabela analítica consolidada (Refined).

---

## 5. Requisitos de Negócio (Consultas Analíticas)

O modelo consolidado na fase refinada deve simplificar análises em SQL, permitindo as seguintes extrações analíticas com máxima facilidade:

- O Faturamento total mês a mês.
- Faturamento consolidado por categoria de produtos.
- Distribuição de volume (quantidade de pedidos) por estado do consumidor.
- O ticket médio por cliente nas compras realizadas.
- O ranking dos Top 10 produtos mais vendidos no e-commerce.

---

## 6. Práticas de DataOps (Desafios Avançados)

Para evidenciar maturidade em Engenharia de Dados, o pipeline adotará abordagens focadas em DataOps:

- **Logs Estruturados de Execução:** Abandono do `print` básico; o processo emitirá logs formatados contendo tempo de início/término, identificadores da etapa (extração, carga) e numeração de linhas processadas.
- **Validação de Schema:** Aplicação de contratos de dados (utilitários como `Pandera` ou `Pydantic`) que impeçam a ingestão de registros com colunas incompatíveis à etapa *trusted*.
- **Particionamento de Dados por Data:** Escrita inteligente utilizando diretórios (`year=YYYY/month=MM/day=DD`) simulando fluxos transacionais.
- **Idempotência no pipeline de carga:** Design de arquitetura que permite reexecutar o mesmo bloco de datas N vezes de modo seguro, sem risco de dados duplicados nas métricas analíticas.
- **Estratégia de reprocessamento (backfill):** Código modular suportando o passe de blocos temporais (datas específicas parametrizadas) para preencher a base de maneira orquestrável sem interferência manual via código base.

---

## 7. Entregáveis Esperados

O projeto será encerrado quando os seguintes itens puderem ser encontrados no repositório final:

- [ ] Arquivos CSV de origem de acordo com o dicionário de dados localizados.
- [ ] Scripts Python cobrindo as funções de geração de dados e execução de ETL.
- [ ] Evidências demonstrativas como logs estruturados de execução e prints de queries sendo respondidas na base final.
- [ ] Controle de versão atualizado no Git.
