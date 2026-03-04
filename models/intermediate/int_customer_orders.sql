{{ config(materialized='view') }}

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.signup_date,
    o.order_id,
    o.order_date,
    o.status
from {{ ref('stg_customers') }} c
inner join {{ ref('stg_orders') }} o
    on c.customer_id = o.customer_id
