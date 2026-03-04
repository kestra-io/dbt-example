{{ config(materialized='view') }}

select
    o.order_date,
    count(distinct o.order_id) as total_orders,
    sum(p.amount) as daily_revenue,
    count(distinct o.customer_id) as unique_customers
from {{ ref('stg_orders') }} o
inner join {{ ref('stg_payments') }} p
    on o.order_id = p.order_id
where o.status = 'completed'
group by o.order_date
