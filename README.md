# DataOps Lab: Pipeline ETL Batch E-commerce

Pipeline de dados local (Batch) modelando dados sintéticos de um E-commerce utilizando práticas modernas de **Engenharia de Dados** e **DataOps**. O laboratório demonstra o fluxo ponta-a-ponta, desde a geração de milhões de registros até sua camada analítica no DuckDB, priorizando confiabilidade de schemas e observabilidade.

## 🚀 Arquitetura e Stack
- **Linguagem Orquestradora:** Python
- **Gerador de Dados Sensíveis/Sintéticos:** `Faker` gerando as tabelas (clientes, produtos, pedidos e itens do pedido).
- **Contrato de Dados (Validação):** `Pandera` efetuando o controle de qualidade do schema (tipos, nulos e limites).
- **Banco de Dados Analítico:** `DuckDB` servindo como Data Warehouse Local com processamento vetorial rápido.
- **Modelagem de Dados:** Camadas Raw, Trusted e Refined (consolidada em uma *One Big Table* — OBT).

## 📁 Estrutura do Projeto

```text
dataops-lab/
├── data/
│   ├── raw/          # Arquivos CSV brutos gerados pelo pipeline
│   ├── trusted/      # Referência à camada tratada
│   └── refined/      # Referência à camada agregada e pronta para BI
├── sql/
│   └── queries.sql   # Requisitos Analíticos (Faturamento, Top 10 Produtos, Ticket Médio)
├── src/
│   ├── generators/
│   │   └── generate_data.py  # Cria bases sintéticas integrando relacionamentos (FKs)
│   ├── etl/
│   │   ├── pipeline.py       # Extrai CSVs, valida (Pandera), transforma e carrega no DuckDB
│   │   └── analytics.py      # Executa e exibe as perguntas do negócio com Pandas em tela
│   └── utils/
│       ├── logger.py         # Configuração comum de logs (Console + arquivo pipeline.log)
│       └── schemas.py        # Modelos Pandas (Pandera) para a validação dos contratos
├── contexto.md       # Descritivo conceitual extenso da arquitetura
├── plan.md           # Log do planejamento da implementação final
├── requirements.txt  # Bibliotecas Python (duckdb, pandera, pyarrow, etc)
└── README.md         # Instruções de setup (este arquivo)
```

---

## ⚙️ Executar o Pipeline Passo-a-Passo

Este projeto foi dividido em instâncias independentes para simular ferramentas que comumente rodam isoladas. Execute na **raiz do projeto**:

### 1. Carga Bruta do Domínio (Geração Sintética de CSV)
Este script gera toda a volumetria inicial para `data/raw/*.csv` simulando um dump de produção de E-commerce. São cerca de >30 Mil registros gerados coerentemente (com datatempos corretos pós-cadastro):
```bash
python src/generators/generate_data.py
```

### 2. O Pipeline ETL Core (Filtro e Modelagem OBT)
Este é o orquestrador ETL que faz todo o processamento massivo. O processo de "Idempotência" foi configurado como um Full Drop/Replace nesse cenário de laboratório:
```bash
python src/etl/pipeline.py
```
> **O que acontece aqui?** 
> 1. Ele lê a pasta RAW.
> 2. Dispara a checagem do *Pandera*, matando o processo se houver dados fora do schema.
> 3. Abre/cria o `ecommerce.duckdb` na raiz da pasta.
> 4. Limpa e recria todas as views e features em instâncias Trusted e entrega uma *One Big Table* enriquecida (`refined_obt`).

### 3. Extração Visual (Métricas de Negócio)
Confirme e veja as respostas aos requisitos de negócios, direto na tela do seu console conectando no Banco DuckDB recém criado:
```bash
python src/etl/analytics.py
```

## 📋 Práticas de DataOps Implementadas

- **Observabilidade Total (Logs Estruturados):** Todos os módulos mandam os relatórios de execução, erro e falhas simultaneamente para o Console e para um arquivo perpétuo (`pipeline.log`) no root, abandonando `prints` inseguros do passado.
- **Data Contracts e Schema Validation:** Garantia que lixo transacional nunca passe para suas tabelas de análise via Pandera.
- **Idempotência Garantida:** Você pode rodar dezenas de vezes o `pipeline.py` sem criar valores repetidos ou impactar os analistas do final da esteira.
- **Modularização Limpa:** A regra de negócios está onde deveria estar (SQL) enquanto o código Python apenas acopla o encadeamento e orquestra a lógica robusta.

## Licença

Projeto acadêmico e conceitual — uso para fins de estudo de DataOps e Engenharia de Dados.
