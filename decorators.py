import timeit, cProfile, pstats, io
import time



def what_time(func):
    def timed(*args, **kwargs):

        cost, best_route = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        return cost, best_route, elapsed_time
    return timed


def profile(func):
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        results = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return results
    return inner
