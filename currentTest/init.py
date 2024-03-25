# All of these packages will be necessary
from flask import Flask, render_template, request
import scipy
import numpy as np
import pylab as plt
import plotly.express as px
import plotly.graph_objects as go


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
        g_name = request.form.get('g')
        x_name = request.form.get('x1')
        y_name = request.form.get('y1')
        
        # Retrieve user input for x values
        x_values = list(map(float, request.form.getlist('x_values[]')))
        
        # Retrieve user input for y values
        y_values = list(map(float, request.form.getlist('y_values[]')))
        
        # Assuming user inputs the same number of x and y values
        n = len(x_values)
        
        # Assuming x units are always in M
        x = np.array(x_values)
        
        # Assuming y units are always in A
        y = np.array(y_values)

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
            title=dict(text=g_name, font=dict(size=50), yref='paper', x=0.5)
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
            title=dict(text=g_name, font=dict(size=50), yref='paper',x=0.5),
            xaxis=dict(title=x_name, gridcolor='black'),
            yaxis=dict(title=y_name, gridcolor='black'),
            legend_title=dict(text="Legend"),
            plot_bgcolor='white',
            paper_bgcolor='white'
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
        return render_template('index.html', plot=combinedFig.to_html())
   else:
        return render_template('index.html', plot='')
   
   

app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
if __name__ == "__main__":
   app.run('127.0.0.1', 5000, debug = True)
