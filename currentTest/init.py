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
        
        # Retrieve the user input
        x_units = request.form.get('x-units')
        y_units = request.form.get('y-units')
        units_per = request.form.get('units-per')
        g_name = request.form.get('g')
        x_name = request.form.get('x1')
        y_name = request.form.get('y1')
        enzymeConcentration_str = request.form.get('e')
        if enzymeConcentration_str:
            enzymeConcentration = float(enzymeConcentration_str)
        else:
            enzymeConcentration = 0
            kCat = 0


        # Retrieve user input for number of pairs
        num_pairs = int(request.form.get('numPairs'))

        # Retrieve user input for x and y values
        x_values = [float(request.form.getlist('x_values[]')[i]) for i in range(num_pairs)]
        y_values = [float(request.form.getlist('y_values[]')[i]) for i in range(num_pairs)]
        
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
        inputColor = request.form.get('input-color')
        curveColor = request.form.get('curve-color')

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
            xaxis=dict(title=x_name, gridcolor='black', autorange=True),
            yaxis=dict(title=y_name, gridcolor='black', autorange=True),  
            legend_title=dict(text="Legend"),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        combinedFig.add_annotation(x=x[0], y=y[0],
                    text=("vMax: " + str(round(vM_guess,10))),
                    showarrow=False,
                    yshift=50, xshift = 150, font=dict(
                    family=fontFamily,
                    size=20,
                    ))

        combinedFig.add_annotation(x=x[0], y=y[0],
                    text=("kM: " + str(round(kM_guess,10))),
                    showarrow=False,
                    yshift=70, xshift = 150, font=dict(
                    family=fontFamily,
                    size=20,
                    ))
        
        miny = min(y)
        maxy = max(y)

        if miny >= 0 and maxy >= 0:
            y_range = [0, maxy]
        elif miny <= 0 and maxy <= 0:
            y_range = [miny, 0]
        else:
            y_range = [miny, maxy]

        combinedFig.update_yaxes(range=y_range)

 ##Lineweaver burk
        def lineweaver(slope, x, intercept):
            return((slope * x + intercept))
        
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
            title=dict(text="Lineweaver-Burk", font=dict(size=50), yref='paper',  x=0.5),
            xaxis=dict(title="1 / Substrate Concentration",gridcolor='black'),
            yaxis=dict(title="1 / Velocity",gridcolor='black'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            width = 775
        )

        combinedBurk.data[0].name = 'Input Points'
        equation = "Lineweaver-Burk"
        combinedBurk.data[1].name = equation

        combinedBurk.data[0].showlegend = True
        combinedBurk.data[1].showlegend = True
        combinedBurk.update_traces(marker=dict(color=inputColor), selector=dict(name="Input Points"), overwrite=True)
        combinedBurk.update_traces(marker=dict(color=curveColor), selector=dict(name=equation), overwrite=True)

      
        if enzymeConcentration is not None:
            kCat = vM_guess / enzymeConcentration
        else:
            kCat = 0
        
        return render_template('index.html', plot2 = combinedBurk.to_html(), plot=combinedFig.to_html(), g=g_name, x1=x_name, y1=y_name, input_color=inputColor, curve_color=curveColor, numPairs=num_pairs, x_values=x_values, y_values=y_values, vMax="{:.4g} {}{}".format(vM_guess, y_units, units_per), kM="{:.4g} {}{}".format(kM_guess, x_units, units_per), kCat="{:.3f}".format(kCat), e = enzymeConcentration)
   else:
        blank_plot = go.Figure()
        blank_plot.update_layout(
        title=dict(text='Graph Name', font=dict(size=50), yref='paper',x=0.5),
        xaxis=dict(title='X-axis Name', gridcolor='black', range=[0, 10]),
        yaxis=dict(title='Y-axis Name', gridcolor='black', range=[0, 10]),
        plot_bgcolor='white',
        paper_bgcolor='white'
        )
        return render_template('index.html', plot=blank_plot.to_html(), g="", x1="", y1="", input_color="#0000ff", curve_color="#ff0000", numPairs=0, vMax =0.0, kM=0.0,kCat=0.0)
   
   

app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
if __name__ == "__main__":
   app.run('127.0.0.1', 5000, debug = True)



