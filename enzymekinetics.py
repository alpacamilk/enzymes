#!/usr/bin/env python

# coding: utf-8



# In[1]:





import scipy

import numpy as np

import pylab as plt

import plotly.express as px

import plotly.graph_objects as go



x = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,1])

n = len(x)

sd=0.1



def model(x, Vm, Km):

    return Vm*x / (x + Km)



y=np.array([5.14E-06, 1.06E-05, 1.64E-05, 2.25E-05, 2.90E-05, 3.21E-05, 3.44E-05])


initialGuess = [1,1]

err = np.full(n, sd)

err[0] = 1e-6

y = y + err

parameters, covar = scipy.optimize.curve_fit(model, x, y, absolute_sigma = True, p0 = initialGuess)

vM_guess = parameters[0]

kM_guess = parameters[1]



xMax = x.max()

t = np.linspace(0, xMax + 0.5*xMax)

tY = model(t, vM_guess, kM_guess)

lineFig = go.Figure(data=go.Scatter(x=t, y=tY))

scatterFig = px.scatter(x=x, y=y)

combinedFig = go.Figure(data=scatterFig.data + lineFig.data)

combinedFig.add_hline(y=vM_guess)

combinedFig.show()
