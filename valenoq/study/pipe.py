from pdb import set_trace as stop


class Pipe(object):

    def __init__(self, columns=None):
        self.columns = columns

def run_pipe(pipe_obj, start, end):
    # filter by start/end
    #
    # filter by pipe_obj.columns["sma_10"]["ts"].param ("close")
    #
    # apply callback (sma) iteratively
    pass
