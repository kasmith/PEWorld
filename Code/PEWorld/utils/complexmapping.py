import dill
from multiprocessing import Pool, cpu_count

# From http://stackoverflow.com/questions/8804830/python-multiprocessing-pickling-error
def run_dill_encoded(what):
    fun, args = dill.loads(what)
    return fun(*args)

def apply_async(pool, fun, args):
    return pool.apply_async(run_dill_encoded, (dill.dumps((fun, args)),))

def async_map(fun,args,ncpu = cpu_count()):
    P = Pool(ncpu)
    jobs = [apply_async(P,fun, (a,) ) for a in args]
    P.close()
    r = [j.get() for j in jobs]
    P.join()
    return r
