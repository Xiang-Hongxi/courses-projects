import numpy as np

def color_histogram(xmin, ymin, xmax, ymax, frame, hist_bin):
    # frame: (m,n,3) numpy.array
    hist_bin_interval = 256/hist_bin
    R = frame[ymin:ymax,xmin:xmax,0] # 2d numpy.array
    G = frame[ymin:ymax,xmin:xmax,1] # 2d numpy.array
    B = frame[ymin:ymax,xmin:xmax,2] # 2d numpy.array

    method = 1

    if method == 1:
        # use three 1-D hist
        R_count = []
        G_count = []
        B_count = []

        for i in range(hist_bin):
            R_count.append(len(np.where((R>=(i*hist_bin_interval)) & (R<(i+1)*hist_bin_interval))[0]))
            G_count.append(len(np.where((G>=(i*hist_bin_interval)) & (G<(i+1)*hist_bin_interval))[0]))
            B_count.append(len(np.where((B>=(i*hist_bin_interval)) & (B<(i+1)*hist_bin_interval))[0]))
        
        unnormalized_color_histogram = np.asarray(R_count + G_count + B_count)
        hist = unnormalized_color_histogram/(np.sum(unnormalized_color_histogram))
        return hist

    elif method == 2:
        # use one 3-D hist
        unnormalized_color_histogram = np.zeros((hist_bin, hist_bin, hist_bin), dtype=np.int32)
        for i in range(R.shape[0]):
            for j in range(R.shape[1]):
                R_interval_index = np.int32(np.floor((R[i][j])/hist_bin_interval))
                G_interval_index = np.int32(np.floor((G[i][j])/hist_bin_interval))
                B_interval_index = np.int32(np.floor((B[i][j])/hist_bin_interval))
                unnormalized_color_histogram[R_interval_index][G_interval_index][B_interval_index]+=1

        hist = unnormalized_color_histogram/(np.sum(unnormalized_color_histogram))

        return hist
