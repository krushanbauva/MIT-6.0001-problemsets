#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 22:34:43 2020

@author: krushan
"""


annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
portion_down_payment = 0.25
current_savings = 0.0
rate = 0.04
number_of_months = 0
while(current_savings < total_cost*portion_down_payment):
    current_savings += current_savings*rate/12
    current_savings += annual_salary*portion_saved/12
    number_of_months += 1
print(number_of_months)