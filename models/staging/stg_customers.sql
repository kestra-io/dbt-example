{{ config(materialized='table') }}

with customers as (
    select 1 as customer_id, 'Alice' as first_name, 'Anderson' as last_name, '2024-01-10' as signup_date union all
    select 2, 'Bob', 'Baker', '2024-02-15' union all
    select 3, 'Charlie', 'Clark', '2024-03-20' union all
    select 4, 'Diana', 'Davis', '2024-04-05' union all
    select 5, 'Eve', 'Evans', '2024-05-12'
)

select
    customer_id,
    first_name,
    last_name,
    cast(signup_date as date) as signup_date
from customers
