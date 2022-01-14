"""
MPCS 51042 Project 2

Part 1

Ming Liu
"""

import numpy as np
import datetime
import pathlib
import matplotlib.pyplot as plt


class TimeSeries:
    def __init__(self, filePath: str):
        """
        Constructor for the TimeSeries class, taking in CSV of the time series data and 
        building a NumPy array out of it.
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
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.data[i][j] = self.data[i][j].strip()
            self.data = np.array(self.data)
        except:
            print("Could not find the file specified by ", str(filePath))

    def cleanup_wifi(self):
        """
        This one is honestly a hack for *one* dataset in particular: the 
        Chicago Libraries WiFi usage set.
        Converts the list of lists to a NumPy array, and cleans up the data 
        set by adding a column of datetime objects to better get the data and time.
        However, if your data uses the same format, it could still work.
        This function also appends your headers accordingly, adding a 'DATE_TIME' column.

        Assumptions:
        NO HEADERS (since headers are probably str objects, trying to force them to 
        datetime will probably fail)
        FIRST COLUMN (index 0) is month data
        SECOND COLUMN (index 1) is year data

        Parameters:
        none

        Returns:
        none (modify in place)
        """
        self.dates = []
        for row in self.data:
            self.dates.append(datetime.datetime.strptime(
                row[0] + " " + row[1], "%B %Y"))
        self.dates = np.array(self.dates)
        self.data = np.hstack((np.atleast_2d(self.dates).T, self.data))
        self.header.insert(0, "DATE_TIME")
        self.header = np.atleast_2d(np.array(self.header))
        self.data = np.vstack((self.header, self.data))

    def graph(self, x : list, y : list, color : str = 'r'):
        """
        Graphs the data. In an attempt to generalize this function as much as possible, no 
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
        plt.plot(x, y, color)

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

    def moving_average(self, data: list, window: int):
        """
        Calculates the moving average with a specified window size.
        If you put in an odd number, it increments your input and informs you.

        Parameters:
        data: list (maybe works with other iterables) of input data
        window: int denoting the desired window size

        Returns:
        list of moving averages
        """
        try:
            window = int(window)
            if window % 2 == 0:
                print(
                    "The moving average window input should be odd, adjusting your input window to " + str(window+1))
                window += 1
            i = window // 2
            sma = []
            while i < len(data) - window // 2:
                current = data[i - window // 2: i + window // 2 + 1]
                bucket = sum(current) / window
                sma.append(bucket)
                i += 1
            return [sma, window]
        except:
            print("Invalid input for moving average.")
    
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
        m, c = np.linalg.lstsq(x, y, rcond=None)[0]
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

"""
Debug code
"""


def main():
    wifi = TimeSeries("data/Libraries_WiFi.csv")
    wifi.cleanup_wifi()
    window = 3
    usage = wifi.data[1:, 3].astype(int)
    data = wifi.moving_average(usage, window)
    movingAverage = data[0]
    window = data[1]
    dates = wifi.data[(1 + window // 2):(len(usage) - (window // 2) + 1), 0]

    wifi.graph(wifi.data[1:, 0], wifi.data[1:, 3].astype(int))
    wifi.graph(dates, movingAverage, 'b')
    plt.locator_params(axis='y', nbins=6)
    plt.xticks(rotation=45)
    plt.ticklabel_format(axis='y', style="plain")
    plt.title("City of Chicago Library WiFi usage data")
    plt.xlabel("Year and month")
    plt.ylabel("Library WiFi sessions/month")
    plt.gca().legend(("Actual data", (str(window) + "-month moving average")))
    wifi.show_graph()


if __name__ == "__main__":
    main()
