#!usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from piecewise import Data


class PieceWiseDDM(object):
    def __init__(self, ds, σs, Ts, thresholds=[-1, 1], x0=0):
        assert len(Ts) == len(ds) == len(σs), "Inputs have varying lengths!"
        assert len(thresholds) == 2, "Thresholds must be of length 2."
        self.ds = ds
        self.σs = σs
        self.Ts = Ts
        self.thresholds = thresholds
        self.x0 = x0

    def simulate(self, repetitions=1):
        """Simulate evidence accumulation paths.
        
        Parameters
        ----------
        repetitions : int, optional
            Number of repetitions, by default 1
        """

        X = np.zeros((repetitions, np.sum(self.Ts) + 1))
        X[:, 0] = self.x0

        t = 0  # time across pieces

        for d, σ, T in zip(self.ds, self.σs, self.Ts):

            ε = np.random.normal(loc=0, scale=σ, size=(repetitions, T))

            for pt in range(T):
                X[:, t + 1] = X[:, t] + d + ε[:, pt]
                t += 1

        # Find FPTs and responses
        # https://stackoverflow.com/a/16244044
        fpts_lower = np.argmax(X < self.thresholds[0], axis=1)
        fpts_upper = np.argmax(X > self.thresholds[1], axis=1)
        fpts_both = np.stack([fpts_lower, fpts_upper], axis=-1)
        ## replace 0s with np.nan (if fpt is 0, threshold is actually not crossed)
        fpts_both = np.where(fpts_both == 0, np.inf, fpts_both)
        responses = np.argmin(fpts_both, axis=1)
        fpts = np.min(fpts_both, axis=1)

        self.data = Data(
            kind="binary",
            responses=responses,
            fpts=fpts,
            X=X,
            thresholds=self.thresholds,
        )

        return self.data

