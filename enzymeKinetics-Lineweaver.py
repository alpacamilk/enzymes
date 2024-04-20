# All of these packages will be necessary
import scipy
import numpy as np
import pylab as plt
import plotly.express as px
import plotly.graph_objects as go


x = np.array([75, 19, 4.7, 1.17, 0.29, 0.07, 0.02, 0])
y = np.array([2.27E-02, 1.8E-02, 1.17E-02, 4.00E-03, 1.04E-03, 2.70E-04, 9.60E-05, 0])

##This is what will need to be changed by the user to accurately calculate kCat
enzymeConcentration = 1

##The X array is the susbtrate concentration, should be user input

# x = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,1])

#Get length of user input
n = len(x)

##The y array is the reaction velocity, should be user input. Right now, the program will not run if 
#y and x are different lengths

# y=np.array([5.14E-06, 1.06E-05, 1.64E-05, 2.25E-05, 2.90E-05, 3.21E-05, 3.44E-05, 3.44E-05])

##The following variables all affect the visuals of the graph output:

fontFamily="Courier New"
fontColor="black"
titleFontFamily="Times New Roman"
titleFontColor="black"
legendTitleFontColor="black"

##sets the colors of the input scatter points and the curve
inputColor = "Blue"
curveColor = "Green"

sd=0.1

#this is the function of the curve which we will optimize for
def model(x, Vm, Km):
    return Vm*x / (x + Km)


##initial guess for where to start (could be optimized)
initialGuess = [1,1]
err = np.full(n, sd)
err[0] = 1e-6

##Optimizing the curve and assigning variables
parameters, covar = scipy.optimize.curve_fit(model, x, y, absolute_sigma = True, p0 = initialGuess)
vM_guess = parameters[0]
kM_guess = parameters[1]

##this is a bootstrap way of creating a line plot. Just map out a whole bunch of new x and y points using
#The estimated parameters
xMax = x.max()
t = np.linspace(0, xMax + 0.5*xMax)
tY = model(t, vM_guess, kM_guess)
#lineFig is the plotted curve
lineFig = go.Figure(data=go.Scatter(x=t, y=tY))
lineFig.update_layout(
    title=dict(text="Enzyme-Kinetics Curve", font=dict(size=50), yref='paper')
)

##scatterfig controls the user input points, not the curve
scatterFig = px.scatter(x=x, y=y)



##combining the line plot and the scatterplot
combinedFig = go.Figure(data=scatterFig.data + lineFig.data)
##This line adds the asymptote line for the vMax
combinedFig.add_hline(y=vM_guess, annotation_text=("vMax: " + str(round(vM_guess, 10))))


##update layout based on graphic variables
combinedFig.update_layout(
    font_family=fontFamily,
    font_color=fontColor,
    title_font_family=titleFontFamily,
    title_font_color=titleFontColor,
    legend_title_font_color=legendTitleFontColor
)

##Adding the legend with names for the scatter and line parts
combinedFig.data[0].name = 'Input Points'
equation = "v =(VMax * s)/(Km + S)"
combinedFig.data[1].name = equation

combinedFig.data[0].showlegend = True
combinedFig.data[1].showlegend = True


combinedFig.update_traces(marker=dict(color=inputColor), selector=dict(name="Input Points"), overwrite=True)
combinedFig.update_traces(marker=dict(color=curveColor), selector=dict(name=equation), overwrite=True)

combinedFig.update_layout(
    title=dict(text="Enzyme-Kinetics Curve", font=dict(size=50), yref='paper'),
    xaxis=dict(title="Substrate Concentration"),
    yaxis=dict(title="Velocity"),
    legend_title=dict(text="Legend")
)

combinedFig.add_annotation(x=x[0], y=y[0],
            text=("vMax: " + str(round(vM_guess,10))),
            showarrow=False,
            yshift=10, xshift = 150, font=dict(
            family=fontFamily,
            size=20,
            ))

combinedFig.add_annotation(x=x[0], y=y[0],
            text=("kM: " + str(round(kM_guess,10))),
            showarrow=False,
            yshift=30, xshift = 150, font=dict(
            family=fontFamily,
            size=20,
            ))


combinedFig.show()


##Lineweaver burk
def lineweaver(slope, x, intercept):
    return((slope * x + intercept))

#slope = Km / Vmax
#b = 1 / Vmax
slope = (kM_guess / vM_guess)
b = (1 / vM_guess)

xMax = x.max()
t = np.linspace(0, xMax + 0.5*xMax)
tY = lineweaver(slope, t, b)

lineFig = go.Figure(data=go.Scatter(x=t, y=tY))

scatterFig = px.scatter(x=newX, y=newY)
combinedBurk = go.Figure(data=scatterFig.data + lineFig.data)
combinedBurk.update_layout(
    title=dict(text="Lineweaver-Burk", font=dict(size=50), yref='paper'),
    xaxis=dict(title="1 / Substrate Concentration"),
    yaxis=dict(title="1 / Velocity")
)

combinedBurk.data[0].name = 'Input Points'
equation = "Lineweaver-Burk"
combinedBurk.data[1].name = equation

combinedBurk.data[0].showlegend = True
combinedBurk.data[1].showlegend = True
combinedBurk.update_traces(marker=dict(color=inputColor), selector=dict(name="Input Points"), overwrite=True)
combinedBurk.update_traces(marker=dict(color=curveColor), selector=dict(name=equation), overwrite=True)
combinedBurk.show()

newX = list()
newY = list()

for element in x:
    if element != 0:
        newX.append(1/element)
    else:
        newX.append(element)
print(len(newX))
for element in newX:
    print(element)

for element in y:
    if element != 0:
        newY.append(1/element)
    else:
        newY.append(element)


kCat = vM_guess / enzymeConcentration

print("slope: " + str(slope) + ' (kM / vM)')
print('intercept: ' + str(b) + ' (1 / vM)')
print('kCat: ' + str(kCat))
