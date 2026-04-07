import duckdb
import pandas as pd
from pathlib import Path
import sys

# Ajuste do path para os utilitários
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import get_logger

logger = get_logger("analytics_reports")

BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR / "ecommerce.duckdb"
SQL_PATH = BASE_DIR / "sql" / "queries.sql"

def main():
    logger.info("INÍCIO - Relatórios Analíticos Baseados em SQL")
    
    if not DB_PATH.exists():
        logger.error("DuckDB database não encontrado! Rode src/etl/pipeline.py antes.")
        sys.exit(1)

    logger.info(f"Conectando ao banco {DB_PATH.name}...")
    conn = duckdb.connect(str(DB_PATH))
    
    # Busca todas formatadas
    queries = SQL_PATH.read_text(encoding='utf-8').split(';')
    queries = [q.strip() for q in queries if len(q.strip()) > 5]
    
    titulos = [
        "1. Faturamento Total por Mês",
        "2. Faturamento por Categoria",
        "3. Quantidade de Pedidos por Estado",
        "4. Ticket Médio por Cliente (Amostra Top 20)",
        "5. Top 10 Produtos Mais Vendidos"
    ]
    
    print("\n================== RELATÓRIO DE NEGÓCIOS [DUCKDB] ==================\n")
    for idx, query in enumerate(queries):
        titulo = titulos[idx] if idx < len(titulos) else f"Query Extra #{idx+1}"
        logger.info(f"Executando >> {titulo}")
        
        # Executa no duckDB e exporta para Pandas DataFrame apenas para 'printar' bonito na tela
        df = conn.execute(query).df()
        
        # Configurar opções de exibição para facilitar a leitura no console
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        
        print(f"\n--- {titulo} ---")
        print(df)
        print("-" * 60)
        
    logger.info("FIM - Execução das Queries finalizadas.")
    conn.close()

if __name__ == "__main__":
    main()
