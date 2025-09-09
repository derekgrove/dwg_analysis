#some efficiency tools and plotting tools for said efficiency tools

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import mplhep
import numpy as np
import awkward as ak

import hist.dask as dah



def init_plt():
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    import mplhep
    mplhep.style.use(mplhep.style.CMS)
    plt.figure()
    mplhep.style.use(mplhep.style.CMS)
    
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

    

def get_1d_pt_hist_v2(leps, name="default"):

    lep_pt = leps.pt
    
    ele_pt_bins = [2,3,4,5,7,8,10,15,20,30,45,60,75,500]
    
    hist = dah.Hist.new.Variable(ele_pt_bins, name=f"{name} ele $p_T$ (GeV").Double()
    
    hist.fill(ak.flatten(lep_pt))
    
    return hist

    
        
def get_2d_eta_pt_hist_v2(leps, name="default"): #This is the one I used with the plotting function

    ele_pt = leps.pt
    ele_eta = leps.eta

    #ele_pt_bins = [2,3,4,5,7,8,10,15,20,30,45,60,75,500]
    ele_pt_bins = [7,8,10,15,20]
    
    ele_eta_bins = [0, 0.8, 1.442, 2.8]
    
    hist = (
        dah.Hist.new
        .Variable(ele_pt_bins, name="ele_pt", label = "ele $p_T$ (GeV)")
        .Variable(ele_eta_bins, name="ele_eta", label = "ele |η|")
        .Double()
        )

    hist.fill(ele_eta=np.abs(ak.flatten(ele_eta)), ele_pt=ak.flatten(ele_pt))
    
    return hist


def make_1d_eff_plot_even_binning(eff_errs, pt_bins, label, title="Default title", ymin=-0.1, ymax=1.1):

    fig, ax = plt.subplots(figsize=(20, 12))


    """
    makes plot with even-spaced binning, doesn't matter where the real-space between bins is
    """
    
    
    #pt_bins = [2,3,4,5,7,8,10,15,20,30,45,60,75,500]
    
    str_names = [str(num) for num in range(len(pt_bins))]
    
    all_colors = [
    'black', 'red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive',
    'cyan', 'magenta', 'lime', 'teal', 'navy', 'maroon', 'coral', 'gold', 'indigo', 'violet',
    'turquoise', 'crimson', 'chocolate', 'darkgreen', 'darkblue', 'darkred', 'darkorange',
    'darkviolet', 'darkcyan', 'darkmagenta', 'darkgray', 'lightgray', 'lightblue', 'lightgreen',
    'lightcoral', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightsteelblue',
    'mediumblue', 'mediumseagreen', 'mediumslateblue', 'mediumturquoise', 'mediumvioletred',
    'midnightblue', 'orangered', 'orchid', 'palegreen', 'paleturquoise', 'palevioletred',
    'peru', 'plum', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
    'seagreen', 'sienna', 'skyblue', 'slateblue', 'springgreen', 'steelblue', 'tan', 'tomato'
    ]

    colors = ['darkmagenta','darkblue','lightsteelblue','sienna', 'plum', 'darkcyan']
    #x = np.arange(len(data)) #literally don't see the advantage to using this, range works just fine


    for i, eff_err in enumerate(eff_errs):
        data = eff_err[0]
        errs = eff_err[1]
        #xs = range(len(data))
        xs = np.arange(len(data))
        
        ax.errorbar(
            xs, data,
            xerr=0.5,
            fmt='o',
            #capsize=10,
            elinewidth=3,
            color=colors[i],
            label=labels[i]
        )
    
        ax.errorbar(
            xs, data,
            yerr=errs,
            fmt='none', #if you would like no point, just the error bar
            capsize=10,
            elinewidth=3,
            color=colors[i]
        )
    
    edge_ticks = np.arange(-0.5, len(data)+0.5)
    #ax.set_xticks([i + 1 for i in x]) #no longer needed for step if I use where='mid'
    ax.set_xticks(edge_ticks)
    ax.set_xticklabels([str(n) for n in pt_bins])
    ax.set_title(title, pad=20, fontweight="bold")
    
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    
    ax.xaxis.grid(True, which='major', linestyle='--', alpha=0.5)
    ax.legend()
    
    ax.set_xlabel("$p_T$ (GeV)")
    ax.set_ylabel("Efficiency")

    ax.axhline(y=0, linewidth=1, linestyle='--', color='0.5')  # dashed grey
    ax.axhline(y=1, linewidth=1, linestyle='--', color='0.5')  # dashed grey

    ax.set_ylim(ymin, ymax)
    #ax.set_xlim(ymin, ymax)
    
    fig.show()

def make_1d_eff_plot_even_test(
    eff_errs,
    pt_bins,
    title="Default title",
    labels=None,
    ymin=-0.1,
    ymax=1.1,
    fig=None,
    ax=None,
):
    """
    Makes a plot with even-spaced binning. If fig/ax are passed, reuse them;
    otherwise create a new figure.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Create fig/ax if not provided
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(20, 12))

    if labels is None:
        labels = [f"Series {i}" for i in range(len(eff_errs))]

    colors = [
        'darkmagenta', 'darkblue', 'lightsteelblue',
        'sienna', 'plum', 'darkcyan'
    ]

    for i, eff_err in enumerate(eff_errs):
        data = eff_err[0]
        errs = eff_err[1]
        xs = np.arange(len(data))

        ax.errorbar(
            xs, data,
            xerr=0.5,
            fmt='o',
            elinewidth=3,
            color=colors[i % len(colors)],
            label=labels[i]
        )
        ax.errorbar(
            xs, data,
            yerr=errs,
            fmt='none',
            capsize=10,
            elinewidth=3,
            color=colors[i % len(colors)]
        )

    # Configure only once (otherwise it gets re-set each call)
    if ax.get_title() == "":
        edge_ticks = np.arange(-0.5, len(pt_bins) + 0.5)
        ax.set_xticks(edge_ticks)
        ax.set_xticklabels([str(n) for n in pt_bins])
        ax.set_title(title, pad=20, fontweight="bold")
        ax.tick_params(axis='x', labelsize=30)
        ax.tick_params(axis='y', labelsize=30)
        ax.xaxis.grid(True, which='major', linestyle='--', alpha=0.5)
        ax.set_xlabel("$p_T$ (GeV)")
        ax.set_ylabel("Efficiency")
        ax.axhline(y=0, linewidth=1, linestyle='--', color='0.5')
        ax.axhline(y=1, linewidth=1, linestyle='--', color='0.5')
        ax.set_ylim(ymin, ymax)

    return fig, ax


"""
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
"""
    