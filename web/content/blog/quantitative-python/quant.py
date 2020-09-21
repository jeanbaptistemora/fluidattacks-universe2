#!/usr/bin/env python
# coding: utf-8

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def event_happens(occurrence_probability):
    """ An event happens if a randomly chosen number
        falls bellow the given occurrence probability """
    return np.random.rand() < occurrence_probability

def lognormal_event_result(lower, upper):
    """ Draws a number from the lognormal distribution
        with given lower and upper bounds for confidence interval """'
    mean = (np.log(upper) + np.log(lower))/2.0
    stdv = (np.log(upper) - np.log(lower))/3.29
    return np.random.lognormal(mean,stdv)

def simulate_scenario(events):
    """ If an event from the input list happens, add the losses due to it """
    total_loss = 0
    for _, event in events.iterrows():
        if event_happens(event['Probability']):
            total_loss += lognormal_event_result(event['Lower'],event['Upper'])
    return total_loss

# Read in the basic events table and test scenario simulation
events_basic = pd.read_csv('events.csv')
simulate_scenario(events_basic)

def monte_carlo(events, rounds):
    """ Simulate many scenarios, returns the results as simple List """
    list_losses = []
    for i in range(rounds):
        loss_result = simulate_scenario(events)
        list_losses.append(loss_result)
    return list_losses

# To test Monte Carlo execution time for some number of iterations
start_time = time.time()
monte_carlo(events_basic, 1000)
print(time.time() - start_time)

# This time run for real, save the results as pandas Series and as numpy parray
results = monte_carlo(events_basic, 1000)
results_series = pd.Series(results)
results_nparray = np.array(results)
results_series.describe()

# Plot the results in the order they came out
results_series.plot()
plt.ticklabel_format(axis='y', style='sci', scilimits=(6,6))
plt.xlabel('Iteration')
plt.ylabel('Loss (millions)')
plt.title('Monte-Carlo simulation results')
plt.savefig('results-raw.png')

# Aggregate and plot them as a histogram
results_series.hist(bins=15)
plt.xlabel('Loss (millions)')
plt.ylabel('Frequency (count)')
plt.ticklabel_format(axis='x',style='sci',scilimits=(6,6))
plt.title('Aggregated simulation results')
plt.savefig('results-hist.png')

def plot_lec(results_nparray, label):
    """ Plots the loss exceedance curve from
        an nparray of Monte Carlo results """
    hist, edges = np.histogram(results_nparray, bins=40)
    cumrev = np.cumsum(hist[::-1]*100/len(results_nparray))[::-1]
    plt.plot(edges[:-1], cumrev, label=label)
    plt.xlabel('Loss (millions)')
    plt.ylabel('Chance of loss or greater (%)')
    plt.ticklabel_format(axis='x',style='sci',scilimits=(6,6))
    plt.title('Loss Exceedance Curve')
    plt.grid()
    #plt.xscale('log') # opt make x axis logarithmic

# Obtain the residual risk curve
events_redux = pd.read_csv('events_redux.csv')
results_redux = monte_carlo(events_redux, 100)

arr_redux = np.array(results_redux)
plot_lec(arr_redux, 'Residual risk')
plot_lec(results_nparray, 'Inherent risk')
plt.xscale('log')
plt.xlabel('Loss')
plt.grid()

# Interpolate the risk tolerance curve
xs = np.array([1,2,3,7,9])*(1e6)
tols = np.array([100,60,10,2,1])

plt.plot(xs, tols, 'o')
xint = np.linspace(min(xs), max(xs))
yint = interpolate.interp1d(xs, tols, kind='slinear')
plt.plot(xint, yint(xint))
plt.xscale('log')
plt.legend()

def get_vars(array):
    """ Computes the 5% VaR and tVar from an nparray of Monte Carlo results """
    var  = np.percentile(array, 95)
    tvar = np.average(array[array >= var])
    return var, tvar

def gen_random_events():
    """ Simulates read input data """
    probability_column = np.random.random_sample(30)*0.1
    lower_ci_column    = np.random.random_sample(30)*(1e6)
    upper_ci_column    = np.random.random_sample(30)*(9e6)+1e6
    dicc = {'Probability' : probability_column,
            'Lower' : lower_ci_column,
            'Upper': upper_ci_column}
    events_rand = pd.DataFrame(dicc)
    return events_rand

def simulate_daily_vars(num_days):
    """ Runs Monte-Carlo over a number of days with simulated inputs """
    vars, tvars = [], []
    for i in range(num_days):
        events = gen_random_events()
        results = monte_carlo(events, 100)
        results_nparray = np.array(results)
        var, tvar = get_vars(results_nparray)
        vars.append(var)
        tvars.append(tvar)
    return vars, tvars

# Simulate t/Var monitoring
days = 30
vars, tvars = simulate_daily_vars(days)
t = np.arange(1, days + 1)

plt.plot(t, vars, label='VaR')
plt.plot(t, tvars, label='tVaR')
plt.title('Evolution of daily VaR in month')
plt.ticklabel_format(axis='y', style='sci', scilimits=(6,6))
plt.ylabel('t/VaR (millions)')
plt.xlabel('Day of the month')
plt.legend()
plt.savefig('monitor-var-time.png')
