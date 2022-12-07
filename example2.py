## Importing required functions --------------------------------
import io
import base64

import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template


## Flask constructor ------------------------------------------
app = Flask(__name__)

## Generate a scatter plot and returns the figure --------------
def get_plot():
    data = {
        'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)
    }
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

    plt.scatter('a', 'b', c='c', s='d', data=data)
    plt.xlabel('X label')
    plt.ylabel('Y label')
    return plt

## Root URL ----------------------------------------------------
@app.get('/')
def single_converter():
    ## Create a new buffered I/O -------------------------------
    base_string = io.BytesIO()

    ## Get the matplotlib plot ---------------------------------
    plot = get_plot()

    ## Save the figure as Base64 format ------------------------
    plot.savefig(base_string, format='png', bbox_inches="tight")

    ## Close the figure to avoid overwriting -------------------
    plot.close()

    ## Encode the base64 string in desired format --------------
    base_string = base64.b64encode(base_string.getvalue()) \
        .decode("utf-8") \
        .replace("\n", "")

    return render_template('matplotlib-plot2.html', s = base_string)


## Main Driver Function ----------------------------------------
if __name__ == '__main__':
    ## Run the application on the local development server ##
    app.run(debug=True)
