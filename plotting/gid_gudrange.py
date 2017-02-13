def git_gudrange(sample, varname=None, frac=1):
    '''
    get_goodrange(sample, varname=None, frac=1)

    Inputs:
    sample : root TTree where the variable is saved (root ttree)
             can also be an 1d array to be plotted as histogram (1d-array like)
    varname : the name of the variable to get the range of (string)
              not optional if sample is a root TTree
    frac : how much percent should be covered by the plot, trying to set in an intelligent way when set to 0.
            using 0 uses quite a lot of computing time, dont use this too often

    Outputs:
    plot_range : a range to plot the variable with
    '''

    if(hasattr(sample, "Draw")):
        #use a root numpy function to get the varname entries as an array
        brancharr = root_numpy.tree2array(sample, varname)
    else:
        brancharr = sample
    length = len(brancharr)
    brancharr.sort()
    maxrange = [brancharr[0], brancharr[-1]]
    if frac==1:
        return maxrange
    if frac!=0:
        nEvts = int(np.ceil(length*frac))
        diff_array=np.zeros(length-nEvts+1) 
        for i in range(length-nEvts+1):
            diff_array[i] = brancharr[i+nEvts-1]-brancharr[i]
        minrange_arg = np.argmin(diff_array)
        return [brancharr[minrange_arg], brancharr[minrange_arg+nEvts-1]]
    else: #frac == 0
        test_fracs = np.arange(0.9, 1.,0.01)
        minrange_arg_array = np.zeros(len(test_fracs))
        minrange_array = np.zeros(len(test_fracs))
        for x in range(len(test_fracs)):
            nEvts = int(np.ceil(length*test_fracs[x]))
            diff_array = np.zeros(length-nEvts+1)
            for i in range(length-nEvts+1):
                diff_array[i] = brancharr[i+nEvts-1]-brancharr[i]
            minrange_arg_array[x] = np.argmin(diff_array)
            minrange_array[x] = np.amin(diff_array)
        #trying to set a figure of merit to choose the best range
        fom = [_plot_fom(k,l) for k,l in zip(test_fracs, minrange_array)]
        #calc fom with frac ==1
        fom = np.append(fom, _plot_fom(1,(brancharr[-1]-brancharr[0])))
        minrange_arg_array = np.append(minrange_arg_array,0)
        test_fracs = np.append(test_fracs, 1)
        if(varname != None):
            print("displayed fraction for "+ varname + ": " + str(test_fracs[np.argmax(fom)]))
        else:
            print("displayed fraction: " + str(test_fracs[np.argmax(fom)]))
        return [brancharr[int(minrange_arg_array[np.argmax(fom)])], brancharr[int(minrange_arg_array[np.argmax(fom)])+int(np.ceil(test_fracs[np.argmax(fom)]*nEvts-1))]]


def _plot_fom(frac, length):
    return (1000*frac**7/length**.8)
