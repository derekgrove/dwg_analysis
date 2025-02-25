import matplotlib.pyplot as plt
import mplhep
import hist
from hist import Hist
import numpy as np

"""
I give up on making automatic plots for now, I learned about the .plot() function that just does everything automatically, essentially what I was trying to do. 
"""

def bug_call():

    #have to call this a second time to get proper scaling, a known bug
    
    mplhep.style.use(mplhep.style.CMS)
    plt.figure()
    mplhep.style.use(mplhep.style.CMS)

def plot_1d(hist_obj, title = "Title", save = False):
    
    #bug_call()
    plt.figure()
    fig, ax = plt.subplots(figsize=(10, 6))
    hist_obj.plot1d(ax=ax, label="test")
    plt.xlabel(hist_obj.axes.name)
    plt.ylabel("Counts")
    plt.title(title, pad=25)  # Adjust title position
    mplhep.cms.label(loc=0, fontsize=15)  # Move CMS label to a different position
    plt.legend()
    

    if save:
        plt.savefig(f"pt_plot_TEST", dpi=120)
    plt.show()


#axis_names = [axis.name for axis in ele_pt_eta_dist.axes]




#def plot_2d(hist_obj):