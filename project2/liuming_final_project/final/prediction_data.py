"""
MPCS 51042 Project 2

Part 2

Ming Liu
"""

import numpy as np
import pathlib
import matplotlib.pyplot as plt

class PredictionData:
    def __init__(self, filePath: str):
        """
        Constructor for the PredictionData class, taking in CSV of the prediction data and 
        building a list of lists out of it.
        Note: This one assumes you have headers as the first row. If you don't, it will chop 
        off the first row of data.

        Parameters:
        filePath: string with the file's relative or absolute path - works regardless of OS.

        Returns:
        nothing (constructor)
        """
        try:
            # use pathlib to make it agnostic to OS and relative/absolute issues
            filePath = pathlib.Path(filePath)
            filePath = pathlib.Path.absolute(filePath)
            self.data = []
            with open(str(filePath), newline="") as read:
                for row in read:
                    # clean up the rows and columns
                    self.data.append(list(row.strip().split(",")))
            # get the header (column titles) and the lead
            self.header = self.data[0]
            self.data = self.data[1:]
            # remove unneeded whitespace
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.data[i][j] = self.data[i][j].strip()
            self.data = np.array(self.data)
            self.header = np.atleast_2d(self.header)
        except:
            print("Could not find the file specified by ", str(filePath))
        
    def cleanup_column(self, col : int):
        """
        Removes a column from the data set.

        Parameters:
        col: int of the index in a list of lists that you want removed.

        Returns:
        none (in-place deletion)
        """
        self.data = np.delete(self.data, col, axis=1)
        self.header = np.delete(self.header, col, axis=1)

    def cleanup_row(self, col: int, target: str):
        """
        Removes rows based on the value of a particular cell in the row.
        Use 'target' to specify which rows you want to keep.

        Parameters:
        col: int of the index in the array (which column you are looking at)
        target: str indicating the target parameter you want to match
        """
        match = []
        for row in self.data:
            if row[col] == target:
                match.append(row)
        self.data = np.array(match)

    def graph(self, x : list, y : list):
        """
        Scatterplots the data. In an attempt to generalize this function as much as possible, no 
        parameters are specified, and between calling graph() and show_graph() you will 
        need to specify them yourself, unless you trust matplotlib's default settings.
        Call show_graph() when you've finished specifying your plot parameters.

        Parameters:
        x: iterable object of things you want on the x axis
        y: iterable object of things you want on the y axis
        color: string of the color used by matplotlib (optional)
        x and y must be the same length, or else it won't work.

        Returns:
        none (creates a matplotlib plot object)
        """
        plt.scatter(x, y, alpha=0.5)

    def show_graph(self):
        """
        Shows the plot you've created. Calling this before calling graph() will 
        probably show you nothing, or an error.

        Parameters:
        none

        Returns:
        none (opens a window with your new plot)
        """
        plt.show()

    def close_graph(self):
        """
        Closes the current graph so that you can show a new one.

        Parameters:
        none

        Returns:
        none
        """
        plt.close()
        
    def standardize(self, data : np.array):
        """
        Creates a new array in the class, self.standard, that standardizes by column.
        If your input array has things that aren't numbers, won't work.

        Parameters:
        none

        Returns:
        none
        """
        self.standard = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

    def least_squares(self, x : np.array, y : np.array):
        """
        Calculate the least-squares regression for x and y.
        
        Parameters:
        x: np.array object, preferably of two dimensions with each row being [x 1] 
        if an intercept is desired, or [x 0] if not
        y: np.array object of y (the dependent variable)

        Returns:
        m: float of the slope
        c: float of the intercept
        """
        m, c = np.linalg.lstsq(x, y, rcond=-1)[0]
        return m, c

    def residuals(self, x : list, y : list, m : float, c : float):
        """
        Calculate the least-squares residuals.

        Parameters:
        x: list object of the independent variables
        y: list object of the actual dependent variable for x
        m: predicted slope
        c: predicted intercept

        Returns:
        resid: float of the square of the residuals
        """
        resid = 0
        for i in range(len(x)):
            resid += (y[i] - (m*x[i]+c))**2
            i += 1
        return float(resid)
    
    def molar_mass(self, steel : list):
        """
        Calculate the molar mass of a steel from a list of its elements.

        Parameters:
        steel: a list of elemental composition of a steel, in the following order:
            - carbon
            - silicon
            - manganese
            - phosphorus
            - sulfur
            - nickel
            - chromium
            - molybdenum
            - copper
            - vanadium
            - aluminum
            - nitrogen
        The rest is assumed to be iron.
        """
        iron_balance = 100.0
        mass_table = [12.01, 28.09, 54.94, 30.97, 
                      32.06, 58.69, 52.00, 95.95, 
                      63.55, 50.94, 26.98, 14.01]
        mass = 0.0
        for u in range(len(steel)):
            mass += mass_table[u] * steel[u]
            iron_balance -= steel[u]
        mass += iron_balance * 55.85
        return (mass / 100)

def main():
    # import the data
    alloys = PredictionData("data/Alloys.csv")
    # get rid of the temperatures we don't care about
    alloys.cleanup_row(15, "27")
    # eliminate alloys that have been tested for carbon equivalent (don't care)
    alloys.cleanup_row(13, "0")
    # eliminate alloys that have niobium or tantalum content (too expensive)
    alloys.cleanup_row(14, "0")
    print(np.shape(alloys.data))

if __name__ == "__main__":
    main()