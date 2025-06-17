import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import os

output_folder = "Plot"

def plot_cms_parameters(parameters, sm_value=1.0,
                        custom_fits_by_param=None, custom_label="", custom_xlim=None,
                        output_file="plot.png"):
    hep.style.use("CMS")
    num_params = len(parameters)
    y_pos = np.arange(num_params)
    
    if (not os.path.exists(f"./{output_folder}")):
        os.makedirs(f"./{output_folder}")

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
        colors = ['green', 'darkmagenta', 'teal', 'black']
        markers = ['^', 's', 'v', '*']
        labels_added = set()

        for i, fits in enumerate(custom_fits_by_param):
            for j, (label, val, (low, high)) in enumerate(fits):
                err = [[val - low], [high - val]]
                marker_label = label if label not in labels_added else None
                ax.errorbar(val, y_pos[i] + 0.2 * (j + 0), xerr=err,
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
    # legend = ax.legend(title='No Discrete profiling\nNo Syst., 10k toys', loc='lower right', fontsize=15)
    legend = ax.legend(title='Discrete profiling\n Syst., 10k toys', loc='lower right', fontsize=15)
    legend.get_title().set_fontsize(16)
    plt.tight_layout()
    plt.savefig(f'./{output_folder}/'+output_file+'.png', dpi=300)
    plt.savefig(f'./{output_folder}/'+output_file+'.pdf', dpi=300)
    plt.show()


# Sample parameters, leave a space for the legend
# parameters = [r"$p_{T}^{\gamma\gamma}$", r"$N_{\text{Jets}}$", r"$p_{T,j0}$", ""]
PTH_parameters = [r"$r_{p_{T}^{\gamma\gamma} \in [0,15) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [15,30) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [30,45) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [45,80) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [80,120) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [120,200) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [200,350) \text{ GeV}}$", r"$r_{p_{T}^{\gamma\gamma} \in [350,+\infty) \text{ GeV}}$", "", "", ""]

NJ_parameters = [r"$r_{N_{\text{Jets}} \in [0,1)}$", r"$r_{N_{\text{Jets}} \in [1,2)}$", r"$r_{N_{\text{Jets}} \in [2,3)}$", r"$r_{N_{\text{Jets}} \in [3,+\infty)}$", "", ""]

PTJ0_parameters = [r"$r_{p_{T,j0} (N_{\text{Jets}} = 0)}$", r"$r_{p_{T,j0} \in [30,75) \text{ GeV}}$", r"$r_{p_{T,j0} \in [75,120) \text{ GeV}}$", r"$r_{p_{T,j0} \in [120,200) \text{ GeV}}$", r"$r_{p_{T,j0} \in [200,+\infty) \text{ GeV}}$", "", ""]

# Your custom fits per parameter
PTH_fits = [
    [  # Param 0
        ("SL (Third Moments)", 1.031, [0.5828414434586644, 1.48859261108612]),
        ("SL (Crossing Method)", 1.031, [0.5983371650450394, 1.4656744322401265]),
        ("SL (Gaussian approx.)", 0.999, [0.5654091413742739, 1.4332776453302036]),
        ("Full likelihood", 0.9993274807929993, [0.5652149282828709, 1.4354208082569804])
    ],
    [  # Param 1
        ("SL (Third Moments)", 1.027, [0.5347843348658026, 1.5322223340328989]),
        ("SL (Crossing Method)", 1.027, [0.4857618350826215, 1.4886911065340425]),
        ("SL (Gaussian approx.)", 1.000, [0.5293519060757086, 1.4700607558902388]),
        ("Full likelihood", 0.9996972680091858, [0.45040548804458436, 1.467969816189522])
    ],
    [  # Param 2
        ("SL (Third Moments)", 1.045, [0.48445676619499495, 1.6110254401387303]),
        ("SL (Crossing Method)", 1.045, [0.5160597567223152, 1.580943032331861]),
        ("SL (Gaussian approx.)", 1.001, [0.4784981795121096, 1.5238834217682924]),
        ("Full likelihood", 1.0011966228485107, [0.4695311118167822, 1.5373420146922698])
    ],
    [  # Param 3
        ("SL (Third Moments)", 1.027, [0.5975794718525962, 1.4583191588048035]),
        ("SL (Crossing Method)", 1.027, [0.6274467118661978, 1.4332573734367526]),
        ("SL (Gaussian approx.)", 0.975, [0.5678786767861315, 1.3831479576416406]),
        ("Full likelihood", 0.9753729701042175, [0.5997806835208441, 1.406997132877828])
    ],
    [  # Param 4
        ("SL (Third Moments)", 1.047, [0.5685402134341644, 1.5310279132159017]),
        ("SL (Crossing Method)", 1.047, [0.5903770527281219, 1.5124248805798146]),
        ("SL (Gaussian approx.)", 1.000, [0.5340103753683565, 1.4653211133791442]),
        ("Full likelihood", 0.9996519684791565, [0.5438638761266688, 1.4654754562803765])
    ],
    [  # Param 5
        ("SL (Third Moments)", 0.989, [0.5974821472752663, 1.3870787040194412]),
        ("SL (Crossing Method)", 0.989, [0.6218371944746054, 1.377280583226367]),
        ("SL (Gaussian approx.)", 1.065, [0.6781393123145238, 1.4523365027737758]),
        ("Full likelihood", 1.0651988983154297, [0.6317362631893345, 1.3890054817404387])
    ],
    [  # Param 6
        ("SL (Third Moments)", 1.027, [0.5718709318223192, 1.4975021151774965]),
        ("SL (Crossing Method)", 1.027, [0.586597613900043, 1.4975241726983977]),
        ("SL (Gaussian approx.)", 1.000, [0.5427074495921682, 1.4574851584536852]),
        ("Full likelihood", 1.0000935792922974, [0.5606113049785546, 1.4689876917985607])
    ],
    [  # Param 7
        ("SL (Third Moments)", 0.998, [0.13725467450569453, 1.9097203471792052]),
        ("SL (Crossing Method)", 0.998, [0.23712057013295712, 1.9474370286973453]),
        ("SL (Gaussian approx.)", 1.000, [0.14830713303970214, 1.8521105843191685]),
        ("Full likelihood", 1.0002080202102661, [0.23802370408624599, 1.9496994763375086])
    ]
]

NJ_fits = [
    [  # Param 0
        ("SL (Third Moments)", 1.031, [0.7465557166950779, 1.3204708969699137]),
        ("SL (Crossing Method)", 1.031, [0.7573628478863342, 1.3052837171633325]),
        ("SL (Gaussian approx.)", 0.999, [0.7222516629020123, 1.2762827637868055]),
        ("Full likelihood", 0.9992518424987793, [0.7128422846296165, 1.2865275324191436])
    ],
    [  # Param 1
        ("SL (Third Moments)", 1.011, [0.5886868874280016, 1.4316605713701382]),
        ("SL (Crossing Method)", 1.011, [0.6107897089040378, 1.415124809873995]),
        ("SL (Gaussian approx.)", 1.000, [0.5908302101072167, 1.4087938608805937]),
        ("Full likelihood", 0.9998141527175903, [0.5697791427771177, 1.435858045722732])
    ],
    [  # Param 2
        ("SL (Third Moments)", 1.026, [0.19698020523753657, 1.8622445679667747]),
        ("SL (Crossing Method)", 1.026, [0.24192654812238076, 1.826316263829642]),
        ("SL (Gaussian approx.)", 1.000, [0.2058149361315563, 1.794277553313151]),
        ("Full likelihood", 1.0000476837158203, [0.16862606754076415, 1.8501355397238357])
    ],
    [  # Param 3
        ("SL (Third Moments)", 1.069, [-0.08552730756669644, 2.257258567516746]),
        ("SL (Crossing Method)", 0.967, [-0.18505602112413858, 2.150659040490559]),
        ("SL (Gaussian approx.)", 1.000, [-0.17529136198144815, 2.1753838535466667]),
        ("Full likelihood", 1.000045657157898, [-0.18595980719041205, 2.2224358031630493])
    ]
]

PTJ0_fits = [
    [  # Param 0
        ("SL (Third Moments)", 0.995, [0.71961337482708, 1.270712677085023]),
        ("SL (Crossing Method)", 0.995, [0.7251270782920407, 1.265288132151653]),
        ("SL (Gaussian approx.)", 0.999, [0.7246304897753222, 1.2743571408660155]),
        ("Full likelihood", 0.9994791746139526, [0.7129613418681073, 1.2860878258908288])
    ],
    [  # Param 1
        ("SL (Third Moments)", 0.991, [0.484986259756495, 1.499080416454804]),
        ("SL (Crossing Method)", 0.991, [0.5007189189193296, 1.486318188376778]),
        ("SL (Gaussian approx.)", 1.000, [0.49754046300636756, 1.5021637792243747]),
        ("Full likelihood", 0.9998571276664734, [0.4500053530789738, 1.5551358905726151])
    ],
    [  # Param 2
        ("SL (Third Moments)", 1.010, [0.27296057717985855, 1.7501599122949933]),
        ("SL (Crossing Method)", 1.010, [0.29530583620055384, 1.7383122088606426]),
        ("SL (Gaussian approx.)", 1.000, [0.2704989889882881, 1.729620851416547]),
        ("Full likelihood", 1.0000598430633545, [0.20541826497440774, 1.8109368132747843])
    ],
    [  # Param 3
        ("SL (Third Moments)", 0.987, [0.24098038827346846, 1.7428707569855555]),
        ("SL (Crossing Method)", 0.987, [0.2785756900310565, 1.7227472025487065]),
        ("SL (Gaussian approx.)", 1.000, [0.2741411250684508, 1.725062543131169]),
        ("Full likelihood", 0.9996008276939392, [0.2423639289421139, 1.786918791079557])
    ],
    [  # Param 4
        ("SL (Third Moments)", 0.991, [0.1808112509852206, 1.806184261883656]),
        ("SL (Crossing Method)", 0.991, [0.22101728253934289, 1.8213670498158843]),
        ("SL (Gaussian approx.)", 1.000, [0.196535532474331, 1.803590591522193]),
        ("Full likelihood", 1.000063419342041, [0.21670746265319316, 1.8446844691072988])
    ]
]

# Call the function
plot_cms_parameters(
    parameters=PTH_parameters+["", ""],
    sm_value=1.0,
    custom_fits_by_param=PTH_fits,
    custom_label="",
    output_file="PTH"
)

plot_cms_parameters(
    parameters=NJ_parameters+[""],
    sm_value=1.0,
    custom_fits_by_param=NJ_fits,
    custom_label="",
    output_file="NJ"
)

plot_cms_parameters(
    parameters=PTJ0_parameters+[""],
    sm_value=1.0,
    custom_fits_by_param=PTJ0_fits,
    custom_label="",
    output_file="PTJ0"
)

plot_cms_parameters(
    parameters=PTH_parameters[:-2]+NJ_parameters[:-1]+PTJ0_parameters[:-1]+["", "", "", "", "", "", "", ""],
    sm_value=1.0,
    custom_fits_by_param=PTH_fits+[[]]+NJ_fits+[[]]+PTJ0_fits+[[]],
    custom_label="",
    custom_xlim=(-0.4, 2.5),
    output_file="all"
)
