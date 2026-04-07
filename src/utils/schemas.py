import pandera as pa
from pandera.typing import Series
from typing import Optional

class CustomerSchema(pa.DataFrameModel):
    customer_id: Series[str] = pa.Field(nullable=False)
    customer_name: Series[str] = pa.Field(nullable=False)
    city: Series[str] = pa.Field(nullable=False)
    state: Series[str] = pa.Field(nullable=False)
    # O arquivo bruto salva data como string ISO
    signup_date: Series[str] = pa.Field(nullable=False)

class ProductSchema(pa.DataFrameModel):
    product_id: Series[str] = pa.Field(nullable=False)
    product_name: Series[str] = pa.Field(nullable=False)
    category: Series[str] = pa.Field(nullable=False)
    price: Series[float] = pa.Field(nullable=False, ge=0)

class OrderSchema(pa.DataFrameModel):
    order_id: Series[str] = pa.Field(nullable=False)
    customer_id: Series[str] = pa.Field(nullable=False)
    order_date: Series[str] = pa.Field(nullable=False)
    status: Series[str] = pa.Field(isin=['Pendente', 'Cancelado', 'Enviado', 'Entregue'], nullable=False)

class OrderItemSchema(pa.DataFrameModel):
    order_item_id: Series[str] = pa.Field(nullable=False)
    order_id: Series[str] = pa.Field(nullable=False)
    product_id: Series[str] = pa.Field(nullable=False)
    quantity: Series[int] = pa.Field(nullable=False, ge=1)
    unit_price: Series[float] = pa.Field(nullable=False, ge=0)

def validate_raw_data(customers_df, products_df, orders_df, items_df):
    """
    Função utilitária para chamar a validação em todos os DataFrames.
    Levantará erro do pandera caso não atenda aos requisitos de DataOps.
    """
    CustomerSchema.validate(customers_df)
    ProductSchema.validate(products_df)
    OrderSchema.validate(orders_df)
    OrderItemSchema.validate(items_df)
    return True
