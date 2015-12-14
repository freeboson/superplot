#########################################################################
#                                                                       #
#    P l o t O p t i o n s                                              #
#                                                                       #
#########################################################################
"""
A named tuple data type to represent the plot options as selected in the UI.
"""
from collections import namedtuple

plot_options = namedtuple("plot_options", (
    "xindex",       # Index of x axis data
    "yindex",       # Index of y axis data
    "zindex",       # Index of z axis data
    "xlabel",       # Label for x axis
    "ylabel",       # Label for y axis
    "zlabel",       # Label for z axis
    "plottitle",    # Title of plot
    "legtitle",     # Plot legend
    "plot_limits",  # Plot limits [xmin, xmax, ymin, ymax]
    "nbins",        # Number of bins
    "bin_limits"    # Bin limits [[xmin, xmax], [ymin, ymax]]
    ))