#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 23:01:08 2020

@author: krushan
"""



annual_salary_initial = float(input("Enter your annual salary: "))
portion_saved = 0.0
total_cost = 1000000
semi_annual_raise = 0.07
portion_down_payment = 0.25
total_down_payment_cost = total_cost*portion_down_payment
current_savings_initial = 0.0
rate = 0.04
number_of_months = 36
number_of_steps = 0
current_savings = current_savings_initial
annual_salary = annual_salary_initial

low = 0
high = 10000

while(low < high):
    mid = int((low + high)/2)
    # print("Low = ", low)
    # print("Mid = ", mid)
    # print("High = ", high)
    # print()
    portion_saved = mid/10000
    annual_salary = annual_salary_initial
    current_savings = current_savings_initial
    for i in range(1, number_of_months+1):
        current_savings += current_savings*rate/12
        current_savings += annual_salary*portion_saved/12
        if i%6 == 0:
            annual_salary += annual_salary*semi_annual_raise
    if(current_savings >= total_down_payment_cost):
        high = mid - 1
    else:
        low = mid + 1
    number_of_steps += 1
    if abs(current_savings-total_down_payment_cost)<100:
        break
if low == high:
    print("It is not possible to pay the down payment in three years.")
else:
    print("Best savings rate =", mid/10000)
    print("Steps in bisection search =", number_of_steps)