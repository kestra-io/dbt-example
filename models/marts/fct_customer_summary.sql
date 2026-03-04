{{ config(materialized='table') }}

select
    co.customer_id,
    co.first_name,
    co.last_name,
    co.signup_date,
    count(distinct co.order_id) as total_orders,
    sum(case when co.status = 'completed' then 1 else 0 end) as completed_orders,
    sum(case when co.status = 'returned' then 1 else 0 end) as returned_orders,
    coalesce(sum(op.amount), 0) as total_spent,
    min(co.order_date) as first_order_date,
    max(co.order_date) as last_order_date
from {{ ref('int_customer_orders') }} co
left join {{ ref('int_order_payments') }} op
    on co.order_id = op.order_id
group by
    co.customer_id,
    co.first_name,
    co.last_name,
    co.signup_date
