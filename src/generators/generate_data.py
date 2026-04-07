import csv
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path
from tqdm import tqdm
import sys

# Adiciona a raiz do projeto ao sys.path para conseguirmos importar src.utils
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import get_logger

logger = get_logger("data_generator")
fake = Faker('pt_BR')

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"

def generate_customers(num_records=3000):
    logger.info(f"Gerando dados de {num_records} clientes...")
    data = []
    for _ in tqdm(range(num_records)):
        data.append({
            "customer_id": str(uuid.uuid4()),
            "customer_name": fake.name(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "signup_date": fake.date_time_between(start_date="-2y", end_date="now").isoformat()
        })
    return data

def generate_products(num_records=300):
    logger.info(f"Gerando dados de {num_records} produtos...")
    categories = ['Eletrônicos', 'Móveis', 'Roupas', 'Brinquedos', 'Alimentos', 'Livros', 'Esportes']
    data = []
    for _ in tqdm(range(num_records)):
        data.append({
            "product_id": str(uuid.uuid4()),
            "product_name": fake.catch_phrase(),
            "category": random.choice(categories),
            "price": round(random.uniform(10.0, 5000.0), 2)
        })
    return data

def generate_orders(customers, num_records=10000):
    logger.info(f"Gerando dados de {num_records} pedidos...")
    data = []
    statuses = ['Pendente', 'Cancelado', 'Enviado', 'Entregue']
    for _ in tqdm(range(num_records)):
        customer = random.choice(customers)
        # O pedido não pode ter sido feito antes do cadastro do cliente
        signup_date = datetime.fromisoformat(customer["signup_date"].replace("Z", "+00:00"))
        # Garantir tz-naive para consistência do Faker ou converte
        signup_date = signup_date.replace(tzinfo=None)
        
        data.append({
            "order_id": str(uuid.uuid4()),
            "customer_id": customer["customer_id"],
            "order_date": fake.date_time_between(start_date=signup_date, end_date="now").isoformat(),
            "status": random.choices(statuses, weights=[10, 5, 25, 60])[0]
        })
    return data

def generate_order_items(orders, products, num_records=20000):
    logger.info(f"Gerando {num_records} itens de pedidos (relacionamentos)...")
    data = []
    for _ in tqdm(range(num_records)):
        order = random.choice(orders)
        product = random.choice(products)
        data.append({
            "order_item_id": str(uuid.uuid4()),
            "order_id": order["order_id"],
            "product_id": product["product_id"],
            "quantity": random.randint(1, 10),
            "unit_price": product["price"] # Simula o preço histórico e pode sofrer impacto se quisermos add desconto
        })
    return data

def save_csv(data, filename):
    filepath = DATA_DIR / filename
    if not data:
        return
    keys = data[0].keys()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    logger.info(f"Salvo arquivo: {filename} em {filepath}")

def main():
    logger.info("INÍCIO - Geração de Dados Sintéticos")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    customers = generate_customers(3000)
    save_csv(customers, "customers.csv")
    
    products = generate_products(300)
    save_csv(products, "products.csv")
    
    orders = generate_orders(customers, 10000)
    save_csv(orders, "orders.csv")
    
    order_items = generate_order_items(orders, products, 20000)
    save_csv(order_items, "order_items.csv")
    
    logger.info("FIM - Geração de Dados Sintéticos concluída com sucesso.")

if __name__ == "__main__":
    main()
