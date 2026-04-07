-- 1. Faturamento total por mês
SELECT 
    DATE_TRUNC('month', order_date) AS mes_competencia,
    SUM(valor_total) AS faturamento_total_mensal
FROM refined_obt
WHERE status != 'Cancelado'
GROUP BY 1
ORDER BY 1 DESC;

-- 2. Faturamento por categoria (Todos os tempos)
SELECT 
    category AS categoria,
    SUM(valor_total) AS faturamento_por_categoria
FROM refined_obt
WHERE status != 'Cancelado'
GROUP BY 1
ORDER BY 2 DESC;

-- 3. Quantidade de pedidos por estado
SELECT 
    state AS estado,
    COUNT(DISTINCT order_id) AS total_de_pedidos
FROM refined_obt
GROUP BY 1
ORDER BY 2 DESC;

-- 4. Ticket médio geral por cliente (Exibindo Top 20 como amostra)
SELECT 
    customer_id,
    customer_name AS nome_cliente,
    SUM(valor_total) / COUNT(DISTINCT order_id) AS ticket_medio_historico
FROM refined_obt
WHERE status != 'Cancelado'
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 20;

-- 5. Top 10 produtos mais vendidos (por Relevância e Volume Real)
SELECT 
    product_name,
    category AS categoria,
    SUM(quantity) AS qtde_max_vendida,
    SUM(valor_total) AS total_receita
FROM refined_obt
WHERE status != 'Cancelado'
GROUP BY 1, 2
ORDER BY 3 DESC, 4 DESC
LIMIT 10;
