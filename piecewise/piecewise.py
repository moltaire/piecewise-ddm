#!usr/bin/python

class Piece(object):
    
    def __init__(self, T, label=None):
        """A single piece of length T.
        
        Parameters
        ----------
        T : int
            Piece duration in time steps.
        label : str, optional
            Piece label.
        """
        self.label = label
        self.T = T