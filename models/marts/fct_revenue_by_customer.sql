{{ config(materialized='table') }}

select
    cs.customer_id,
    cs.first_name,
    cs.last_name,
    cs.total_orders,
    cs.total_spent,
    cs.total_spent / nullif(cs.completed_orders, 0) as avg_order_value,
    dr.total_revenue_on_last_order_day
from {{ ref('fct_customer_summary') }} cs
left join (
    select
        order_date,
        daily_revenue as total_revenue_on_last_order_day
    from {{ ref('int_daily_revenue') }}
) dr
    on cs.last_order_date = dr.order_date
