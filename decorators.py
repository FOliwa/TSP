import timeit, cProfile, pstats, io


# TODO: USE timeit IN DIFRENT WAY
def what_time(func):
    def timed(*args, **kwargs):
        start_time = timeit.default_timer()
        cost, best_route = func(*args, **kwargs)
        return cost, best_route, (timeit.default_timer() - start_time)
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
