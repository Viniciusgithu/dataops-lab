import duckdb
import pandas as pd
from pathlib import Path
import sys

# Adiciona o diretório raiz ao sys.path para imports do projeto
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import get_logger
from src.utils.schemas import validate_raw_data

logger = get_logger("etl_pipeline")

DATA_DIR = Path(__file__).parent.parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
DB_PATH = Path(__file__).parent.parent.parent / "ecommerce.duckdb"

def extract_and_validate():
    logger.info("Extraindo dados da camada RAW (CSV)...")
    customers = pd.read_csv(RAW_DIR / "customers.csv")
    products = pd.read_csv(RAW_DIR / "products.csv")
    orders = pd.read_csv(RAW_DIR / "orders.csv")
    order_items = pd.read_csv(RAW_DIR / "order_items.csv")

    logger.info("Validando schema dos dados estruturados da camada Raw (via Pandera)...")
    validate_raw_data(customers, products, orders, order_items)
    logger.info("Validação do Contrato de Dados concluída com sucesso.")
    return customers, products, orders, order_items

def load_to_duckdb(conn, customers, products, orders, order_items):
    logger.info("Carregando para DuckDB camada Raw e Trusted...")
    
    # Registrando DataFrames no DuckDB (cria views virtuais para leitura rápida)
    conn.register("df_customers", customers)
    conn.register("df_products", products)
    conn.register("df_orders", orders)
    conn.register("df_order_items", order_items)

    # Abordagem de Idempotência "Drop and Replace"
    conn.execute("CREATE OR REPLACE TABLE raw_customers AS SELECT * FROM df_customers")
    conn.execute("CREATE OR REPLACE TABLE raw_products AS SELECT * FROM df_products")
    conn.execute("CREATE OR REPLACE TABLE raw_orders AS SELECT * FROM df_orders")
    conn.execute("CREATE OR REPLACE TABLE raw_order_items AS SELECT * FROM df_order_items")

    # Transformação: Criando Camada Trusted com Tipos rigorosos
    conn.execute("""
        CREATE OR REPLACE TABLE trusted_customers AS 
        SELECT 
            customer_id, 
            customer_name, 
            city, 
            state, 
            CAST(signup_date AS TIMESTAMP) AS signup_date 
        FROM raw_customers
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE trusted_orders AS 
        SELECT 
            order_id, 
            customer_id, 
            CAST(order_date AS TIMESTAMP) AS order_date, 
            status 
        FROM raw_orders
    """)
    
    # Preços e quantidades já mantem os formatos, recriamos na camada trusted
    conn.execute("CREATE OR REPLACE TABLE trusted_products AS SELECT * FROM raw_products")
    conn.execute("CREATE OR REPLACE TABLE trusted_order_items AS SELECT * FROM raw_order_items")

    logger.info("Tabelas RAW e TRUSTED carregadas com sucesso.")

def build_refined_obt(conn):
    logger.info("Transformando e cruzando dados para Camada Refined (One Big Table)...")
    
    # OBT contendo a regras de negócio e cálculo derivado de valor faturamento base.
    conn.execute("""
        CREATE OR REPLACE TABLE refined_obt AS 
        SELECT 
            o.order_id,
            o.order_date,
            o.status,
            c.customer_id,
            c.customer_name,
            c.state,
            c.city,
            p.product_id,
            p.product_name,
            p.category,
            oi.order_item_id,
            oi.quantity,
            oi.unit_price,
            (oi.quantity * oi.unit_price) AS valor_total
        FROM trusted_orders o
        JOIN trusted_customers c ON o.customer_id = c.customer_id
        JOIN trusted_order_items oi ON o.order_id = oi.order_id
        JOIN trusted_products p ON oi.product_id = p.product_id
    """)
    logger.info("Camada Refined OBT criada de forma otimizada com sucesso.")

def main():
    logger.info("INÍCIO - Processamento Pipeline ETL Batch")
    try:
        customers, products, orders, order_items = extract_and_validate()
        
        # Conexão no DuckDB persistente (cria o banco local se não existe)
        conn = duckdb.connect(str(DB_PATH))
        
        load_to_duckdb(conn, customers, products, orders, order_items)
        build_refined_obt(conn)
        
        # Verificando as integridades
        total_rows = conn.execute("SELECT COUNT(*) FROM refined_obt").fetchone()[0]
        logger.info(f"FIM - Pipeline ETL concluído com integridade. Total de {total_rows} linhas analíticas criadas (Refined OBT).")
        
        conn.close()
    except Exception as e:
        logger.error(f"FATAL ERROR - Pipeline interrompido: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
