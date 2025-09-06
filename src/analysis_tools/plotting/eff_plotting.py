#some efficiency tools and plotting tools for said efficiency tools

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import mplhep
import numpy as np


def get_1d_pt_hist(lep_pt, name="default"):

    hist = dah.Hist.new.Regular(100, 0, 100, name=f"{name} lepton $p_T$").Double()

    hist.fill(ak.flatten(lep_pt))
    
    return hist



def get_1d_eta_hist(lep_eta, name="default"):

    hist = dah.Hist.new.Regular(50, -2.5, 2.5, name=f"{name} lepton η").Double()
    
    hist.fill(ak.flatten(lep_eta))
    
    return hist


def calc_eff_err(hist_1, hist_2): #hist_2 is the denominator of the efficiency

    
    num = hist_1.values()
    denom = hist_2.values()
    
    eff = num/denom
    err = np.sqrt(eff * (1 - eff)/ denom)
    
        
    return eff, err


def two_d_eff_err(h_num, h_denom): # h_num and h_denom must have same binning in both dimensions

    eff_h = h_num/h_denom # Creating a histogram
    
    err_h = np.sqrt(eff_h.values() * (1 - eff_h.values())/ h_denom.values())

    return eff_h, err_h


def make_1d_eff_plot(eff_err, pt_bins, title="Default title"): #pass this the tuple output of calc_eff_err
    fig, ax = plt.subplots(figsize=(20, 12))
    
    data = eff_err[0]
    errs = eff_err[1]
    
    #pt_bins = [2,3,4,5,7,8,10,15,20,30,45,60,75,500]
    
    str_names = [str(num) for num in range(len(pt_bins))]
    
    xs = range(len(data))
    #x = np.arange(len(data)) #literally don't see the advantage to using this, range works just fine
    
    ax.errorbar(
        xs, data,
        xerr=0.5,
        fmt='o',
        #capsize=10,
        elinewidth=2,
        color="black"
    )

    ax.errorbar(
        xs, data,
        yerr=errs,
        fmt='none', #if you would like no point, just the error bar
        capsize=10,
        elinewidth=2,
        color="black"
    )
    
    edge_ticks = np.arange(-0.5, len(data)+0.5)
    #ax.set_xticks([i + 1 for i in x]) #no longer needed for step if I use where='mid'
    ax.set_xticks(edge_ticks)
    ax.set_xticklabels([str(n) for n in pt_bins])
    ax.set_title(title, pad=20, fontweight="bold")
    
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    
    ax.xaxis.grid(True, which='major', linestyle='--', alpha=0.5)
    
    ax.set_xlabel("$p_T$ (GeV)")
    ax.set_ylabel("Efficiency")

    ax.axhline(y=0, linewidth=1, linestyle='--', color='0.5')  # dashed grey
    ax.axhline(y=1, linewidth=1, linestyle='--', color='0.5')  # dashed grey

    ax.set_ylim(-0.1, 1.1)
    
    #fig.show()
    
    return

    