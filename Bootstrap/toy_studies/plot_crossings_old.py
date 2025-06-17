import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep

def plot_cms_parameters(parameters, sm_value=1.0,
                        custom_fits_by_param=None, custom_label="", custom_xlim=None,
                        output_file="plot.png"):
    hep.style.use("CMS")
    num_params = len(parameters)
    y_pos = np.arange(num_params)

    fig, ax = plt.subplots(figsize=(8, 10))
    ax.axvline(x=sm_value, color='red', linestyle='-', label='SM expected')

    # # 95% and 68% CL error bars
    # ax.errorbar(best_fit, y_pos, xerr=ci_95, fmt='o', color='orange', label='95% CL',
    #             linestyle='none', markersize=6, markeredgewidth=2)
    # ax.errorbar(best_fit, y_pos, xerr=ci_68, fmt='o', color='blue', label='68% CL',
    #             linestyle='none', markersize=6, markeredgewidth=2)
    # ax.plot(best_fit, y_pos, 'o', color='white', markeredgecolor='black', label='Best-fit')

    # Plot custom fits per parameter
    if custom_fits_by_param:
        colors = ['green', 'darkmagenta', 'teal']
        markers = ['^', 's', 'v']
        labels_added = set()

        for i, fits in enumerate(custom_fits_by_param):
            for j, (label, val, (low, high)) in enumerate(fits):
                err = [[val - low], [high - val]]
                marker_label = label if label not in labels_added else None
                ax.errorbar(val, y_pos[i] + 0.10 * (j + 0), xerr=err,
                            fmt=markers[j % len(markers)], color=colors[j % len(colors)],
                            markersize=6, capsize=3, label=marker_label)
                labels_added.add(label)

    # Decorations
    ax.set_yticks(y_pos)
    ax.set_yticklabels(parameters)
    ax.set_xlabel('r')
    ax.invert_yaxis()
    
    if custom_xlim:
        ax.set_xlim(custom_xlim)
    
    hep.cms.label("Preliminary", rlabel='')
    if custom_label:
        ax.set_title(custom_label, fontsize=10)
    # fig.subplots_adjust(bottom=0.15)  # Increase bottom margin
    legend = ax.legend(title='No Discrete profiling\nNo Syst., 10k toys', loc='lower right', fontsize=15)
    legend.get_title().set_fontsize(16)
    plt.tight_layout()
    plt.savefig('./Plot/'+output_file+'.png', dpi=300)
    plt.savefig('./Plot/'+output_file+'.pdf', dpi=300)
    plt.show()


# Sample parameters, leave a space for the legend
# parameters = [r"$p_{T}^{\gamma\gamma}$", r"$N_{\text{Jets}}$", r"$p_{T,j0}$", ""]
PTH_parameters = [r"$r_{p_{T}^{\gamma\gamma} \in [0,15) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [15,30) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [30,45) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [45,80) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [80,120) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [120,200) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [200,350) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [350,+\infty) \text{ GeV}}$", "", "", ""]

NJ_parameters = [r"$r_{N_{\text{Jets}} \in [0,1)}$", r"$r_{N_{\text{Jets}} \in [1,2)}$", r"$r_{N_{\text{Jets}} \in [2,3)}$", r"$r_{N_{\text{Jets}} \in [3,+\infty)}$", "", ""]

PTJ0_parameters = [r"$r_{p_{T,j0} (N_{\text{Jets}} = 0)}$", r"$r_{p_{T,j0} \in [30,75) \text{ GeV}}$", r"$r_{p_{T,j0} \in [75,120) \text{ GeV}}$", r"$r_{p_{T,j0} \in [120,200) \text{ GeV}}$", r"$r_{p_{T,j0} \in [200,+\infty) \text{ GeV}}$", "", ""]

# Your custom fits per parameter
PTH_fits = [
    [  # Param 0
        ("SL Minimum", 0.996, [0.5636, 1.4230]),
        ("Hesse Minimum", 1.012, [0.5787, 1.4448]),
        ("Combine Minimum", 0.9990, [0.5656, 1.4270])
    ],
    [  # Param 1
        ("SL Minimum", 0.970, [0.5074, 1.4340]),
        ("Hesse Minimum", 1.032, [0.5629, 1.5013]),
        ("Combine Minimum", 0.9992, [0.5340, 1.4659])
    ],
    [  # Param 2
        ("SL Minimum", 1.024, [0.5110, 1.5483]),
        ("Hesse Minimum", 1.016, [0.4945, 1.5382]),
        ("Combine Minimum", 1.0001, [0.4852, 1.5269])
    ],
    [  # Param 3
        ("SL Minimum",0.999, [0.5765078184589209, 1.4231873293963317]),
        ("Hesse Minimum", 1.046, [0.6186049870814815, 1.4737967256436648]),
        ("Combine Minimum", 0.999081552028656, [0.57559324251913, 1.4239120870379651])
    ],
    [  # Param 4
        ("SL Minimum", 0.996, [0.541077015899777, 1.4591573691698794]),
        ("Hesse Minimum", 1.045, [0.5809984411088189, 1.509621506606495]),
        ("Combine Minimum", 0.9999997019767761, [0.5441462284393301, 1.4631688395188436])
    ],
    [  # Param 5
        ("SL Minimum", 0.997, [0.6260592117259924, 1.386936959422965]),
        ("Hesse Minimum", 0.974, [0.5878857299112944, 1.3607421425183994]),
        ("Combine Minimum", 0.9999923706054688, [0.6285753544775692, 1.390660775516218])
    ],
    [  # Param 6
        ("SL Minimum", 0.999, [0.560280631768897, 1.4657234498744678]),
        ("Hesse Minimum", 0.992, [0.5353361703168403, 1.448737823140978]),
        ("Combine Minimum", 0.9999897480010986, [0.5608108991961696, 1.4675031138983807])
    ],
    [  # Param 7
        ("SL Minimum", 1.008, [0.24724456752703114, 1.9515270638178581]),
        ("Hesse Minimum", 0.985, [0.13399799494076264, 1.8364501976568044]),
        ("Combine Minimum", 1.0000014305114746, [0.2409088508289295, 1.9422601185065291])
    ]
]

NJ_fits = [
    [  # Param 0
        ("SL Minimum", 0.994, [0.7252047378497378, 1.2303391987859427]),
        ("Hesse Minimum", 1.012, [0.7359830580105502, 1.2872812510276488]),
        ("Combine Minimum", 0.9992467761039734, [0.7159890519769962, 1.2472551214577385])
    ],
    [  # Param 1
        ("SL Minimum", 1.009, [0.6329733977256943, 1.394194056386589]),
        ("Hesse Minimum", 1.032, [0.6254985839660943, 1.438431280483314]),
        ("Combine Minimum", 0.9998127818107605, [0.5939198874321674, 1.417286999001917])
    ],
    [  # Param 2
        ("SL Minimum", 1.002, [0.22753087224801521, 1.790170086598359]),
        ("Hesse Minimum", 1.016, [0.22611499327711704, 1.8068207682218405]),
        ("Combine Minimum", 1.0000505447387695, [0.18014899826484201, 1.8341363448210681])
    ],
    [  # Param 3
        ("SL Minimum", 0.967, [-0.18214541768364811, 2.1455706234742458]),
        ("Hesse Minimum", 1.046, [-0.12694513382315295, 2.2195884253367058]),
        ("Combine Minimum", 1.000049352645874, [-0.18284812964698569, 2.2137617641912493])
    ]
]

PTJ0_fits = [
    [  # Param 0
        ("SL Minimum", 0.995, [0.767056642990043, 1.2388048931317586]),
        ("Hesse Minimum", 1.012, [0.7365080846639068, 1.2867099607435382]),
        ("Combine Minimum", 0.9994791746139526, [0.7574100076918154, 1.2594318994951363])
    ],
    [  # Param 1
        ("SL Minimum", 0.991, [0.5117979004812196, 1.4849671407986276]),
        ("Hesse Minimum", 1.032, [0.5297938202626314, 1.5341012665770937]),
        ("Combine Minimum", 0.9998571276664734, [0.46262184838886966, 1.554437818236537])
    ],
    [  # Param 2
        ("SL Minimum", 1.010, [0.3019780005406019, 1.7265519955315407]),
        ("Hesse Minimum", 1.016, [0.2867867700142045, 1.7462845876043025]),
        ("Combine Minimum", 1.0000598430633545, [0.21228607212590173, 1.79770666087395])
    ],
    [  # Param 3
        ("SL Minimum", 0.987, [0.29226508179017485, 1.7081028636909577]),
        ("Hesse Minimum", 1.046, [0.3208148055623336, 1.7717837922000228]),
        ("Combine Minimum", 0.9996008276939392, [0.25724079831532115, 1.7709927841059205])
    ],
    [  # Param 4
        ("SL Minimum", 0.991, [0.23094697900994765, 1.8130315902741079]),
        ("Hesse Minimum", 1.045, [0.2417292617698983, 1.8488136333817613]),
        ("Combine Minimum", 1.000063419342041, [0.2266877393630733, 1.8363361944116479])
    ]
]

# Call the function
plot_cms_parameters(
    parameters=PTH_parameters,
    sm_value=1.0,
    custom_fits_by_param=PTH_fits,
    custom_label="",
    output_file="PTH"
)

plot_cms_parameters(
    parameters=NJ_parameters,
    sm_value=1.0,
    custom_fits_by_param=NJ_fits,
    custom_label="",
    output_file="NJ"
)

plot_cms_parameters(
    parameters=PTJ0_parameters,
    sm_value=1.0,
    custom_fits_by_param=PTJ0_fits,
    custom_label="",
    output_file="PTJ0"
)

plot_cms_parameters(
    parameters=PTH_parameters[:-2]+NJ_parameters[:-1]+PTJ0_parameters[:-1]+["", "", "", "", "", ""],
    sm_value=1.0,
    custom_fits_by_param=PTH_fits+[[]]+NJ_fits+[[]]+PTJ0_fits+[[]],
    custom_label="",
    custom_xlim=(-0.4, 2.5),
    output_file="all"
)
