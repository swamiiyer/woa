# This script can be used to plot an animation of the lattice structure 
# as it evolves over a given time interval [start, end). The color of 
# each cell in the lattice indicates the strength of the trait value the 
# player at that cell. The trait values and step size for the animation 
# are obtained from the results file specified as the first command-line 
# argument to the program. The next two arguments specifiy the start and 
# end values for the time interval for the animation.
#
# Usage: python plot_trait_structure.py <fname> <start> <end>

import numpy, pickle, pylab, sys
from continuous import *

def main(argv):
    """
    Entry point.
    """

    if len(argv) != 3:
        print "Usage: python plot_trait_structure.py <fname> <start> <end>"
        sys.exit(0)

    plot(argv[0], int(argv[1]), int(argv[2]))
    
def plot(fname, start, end):
    """
    Given the results file (fname) from running the game on an nxn 
    lattice, plot an animation of the lattice structure as it evolves 
    over time given by the interval [start, end) in steps of report_freq. 
    The color of each cell in the lattice indicates the strength of the 
    trait value the player at that cell.
    """

    fh = open(fname, "r")
    params = pickle.load(fh)
    population = pickle.load(fh)
    fh.close()
    pylab.ion()
    pylab.hold(False)
    for generation in range(start, end, params["report_freq"]):
        print "Generation %d" %(generation)
        trait_list = []
        for p in population:
            trait_list.append(p.get_trait_list()[generation / \
                                                     params["report_freq"]])
        colormap = {}
        n_bins = 100
        delta = params["max_trait"] / n_bins
        for trait in trait_list:
            a = 0.0
            b = a + delta
            for i in range(0, n_bins):
                if trait >= a and trait < b:
                    colormap[trait] = i
                    break
                a = b
                b += delta
        mat = []
        if params["network_topology"] == "Grid_2D":
            m = params["network_params"]["m"]
            n = params["network_params"]["n"]
        else:
            m = n = params["network_params"]["n"]
        for i in range(0, m):
            r = []
            for j in range(0, n):
                r.append(colormap[trait_list[i * n + j]])
            mat.append(r)
        mm = pylab.imshow(mat, interpolation = "nearest", 
                          extent = [0, n - 1, m - 1, 0], 
                          vmin = 0, vmax = n_bins)
        if generation == start:
            cb = pylab.colorbar(mm, ticks = [0, n_bins / 2, n_bins])
            cb.ax.set_yticklabels([0.0, params["max_trait"] / 2, 
                                               params["max_trait"]])
            cb.set_label(r"$x$")
        pylab.draw()

    # Keep the final plot window around until the user shuts it.
    pylab.show() 

if __name__ == "__main__":
    main(sys.argv[1:])
