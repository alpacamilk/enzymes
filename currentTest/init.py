from flask import Flask, render_template, request
import numpy as np
import scipy
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':

       x_values = list(map(float, request.form.getlist('x_values[]')))
       y_values = list(map(float, request.form.getlist('y_values[]')))
       x_axis = request.form.get('x1')
       y_axis = request.form.get('y1')
       g_name = request.form.get('g')

       n = len(x_values)
       sd = 0.1

       def model(x, Vm, Km):
           return Vm * x / (x + Km)

       initialGuess = [1, 1]
       err = np.full(n, sd)
       err[0] = 1e-6
       y_values = y_values + err
       parameters, covar = scipy.optimize.curve_fit(model, x_values, y_values, absolute_sigma=True, p0=initialGuess)
       vM_guess = parameters[0]
       kM_guess = parameters[1]

       xMax = max(x_values)
       t = np.linspace(0, xMax + 0.5 * xMax)
       tY = model(t, vM_guess, kM_guess)
       lineFig = go.Figure(data=go.Scatter(x=t, y=tY))
       scatterFig = px.scatter(x=x_values, y=y_values)
       combinedFig = go.Figure(data=scatterFig.data + lineFig.data)
       combinedFig.add_hline(y=vM_guess)

       combinedFig.update_layout(
            xaxis=dict(range=[0, max(x_values)], tickmode='linear', tick0=0, dtick=0.5, title=x_axis, gridcolor='black'),
            yaxis=dict(range=[0, max(y_values)], tickmode='linear', tick0=0, dtick=0.5, title=y_axis, gridcolor='black'),
            title=dict(text=g_name, x=0.5),
            plot_bgcolor='white',  # Set plot background color to white
            paper_bgcolor='white'  # Set paper background color to white
        )
       return render_template('index.html', plot=combinedFig.to_html())
   else:
       return render_template('index.html', plot=None)
   
app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
if __name__ == "__main__":
   app.run('127.0.0.1', 5000, debug = True)
