{{ config(materialized='table') }}

with orders as (
    select 101 as order_id, 1 as customer_id, '2024-03-01' as order_date, 'completed' as status union all
    select 102, 2, '2024-03-05', 'completed' union all
    select 103, 1, '2024-03-10', 'completed' union all
    select 104, 3, '2024-04-01', 'returned' union all
    select 105, 2, '2024-04-15', 'completed' union all
    select 106, 4, '2024-05-01', 'completed' union all
    select 107, 1, '2024-05-20', 'completed' union all
    select 108, 5, '2024-06-01', 'completed' union all
    select 109, 3, '2024-06-15', 'completed' union all
    select 110, 4, '2024-07-01', 'returned'
)

select
    order_id,
    customer_id,
    cast(order_date as date) as order_date,
    status
from orders
