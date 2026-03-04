{{ config(materialized='table') }}

with payments as (
    select 1001 as payment_id, 101 as order_id, 50.00 as amount, 'credit_card' as payment_method union all
    select 1002, 102, 75.50, 'bank_transfer' union all
    select 1003, 103, 30.00, 'credit_card' union all
    select 1004, 104, 120.00, 'credit_card' union all
    select 1005, 105, 45.00, 'paypal' union all
    select 1006, 106, 200.00, 'bank_transfer' union all
    select 1007, 107, 15.00, 'credit_card' union all
    select 1008, 108, 90.00, 'paypal' union all
    select 1009, 109, 60.00, 'credit_card' union all
    select 1010, 110, 35.00, 'bank_transfer'
)

select
    payment_id,
    order_id,
    amount,
    payment_method
from payments
