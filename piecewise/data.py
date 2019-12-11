#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt


class Data(object):
    def __init__(self, kind=None, responses=None, fpts=None, X=None, thresholds=None):
        self.type = kind
        self.responses = responses
        self.fpts = fpts
        self.X = X
        self.thresholds = thresholds

    def plot(self, bins=None):

        if bins is None:
            bins = np.linspace(0, self.X.shape[1], 21)

        fig, axs = plt.subplots(
            3, 1, gridspec_kw={"height_ratios": [1, 2, 1]}, sharex=True
        )

        # Remove data post threshold crossing
        for r in range(self.X.shape[0]):
            if np.isfinite(self.fpts[r]):
                self.X[r, int(self.fpts[r]) :] = np.nan

        # Plot trajectories
        axs[1].plot(self.X.T, color="k", alpha=(5 / self.X.shape[0]))
        mean = np.nanmean(self.X, axis=0)  # mean of remaining paths
        axs[1].plot(mean)
        std = np.nanstd(self.X, axis=0)  # std of remaining paths
        axs[1].fill_between(
            np.arange(self.X.shape[1]),
            y1=mean - std,
            y2=mean + std,
            alpha=0.1,
            zorder=0,
        )

        # Plot thresholds
        for threshold in self.thresholds:
            axs[1].axhline(threshold, c="k", linewidth=0.75)
        axs[1].set_ylim(self.thresholds)

        # Plot FPT histogram for upper threshold
        axs[0].hist(
            self.fpts[self.responses == 1], bins=bins, color="darkgray", linewidth=1,
        )
        # Plot FPT histogram for lower threshold
        axs[2].hist(
            self.fpts[self.responses == 0], bins=bins, color="darkgray", linewidth=1,
        )

        # Adjust limits
        hist1y = axs[0].get_ylim()[1]
        hist0y = axs[2].get_ylim()[1]
        histymax = np.max([hist1y, hist0y])
        axs[0].set_ylim(0, histymax)
        axs[2].set_ylim(histymax, 0)
        axs[1].set_xlim(0, self.X.shape[1])

        # Set labels
        axs[1].set_ylabel("X")
        axs[2].set_xlabel("t")
        for ax in [axs[0], axs[2]]:
            ax.set_ylabel("Freq.")

        fig.tight_layout()

        return fig, axs
