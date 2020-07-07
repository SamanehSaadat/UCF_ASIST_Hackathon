class Building:
    def __init__(self, bname, trials=None, zones_file=None, victims_file=None, sizes=None, limits=None):
        self.bname = bname
        self.trials = trials
        self.zones_file = zones_file
        self.victims_file = victims_file
        self.sizes = sizes
        self.limits = limits
