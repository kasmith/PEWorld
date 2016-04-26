from __future__ import division
import numpy as np
import copy

def SPSA(fnc, initparams, a_par = 1e-6, c_par = .01, args = (), \
         bounds = None, param_tol = None, ftol = 1e-8, maxiter = 10000,
         alpha = .602, gamma = .101,print_iters = 100.):

    def calc(ps): return fnc(ps, *args)

    big_a = maxiter / 10.

    n_iter = 0
    initparams = np.array(initparams)
    n_params = initparams.shape[0]

    p = initparams
    old_val = calc(p)
    saved_p = p*100.

    if bounds is not None:
        if len(bounds) != n_params: raise Exception('Malformed bounds')
        minvals = [x[0] for x in bounds]
        maxvals = [x[1] for x in bounds]
    else:
        minvals = None
        maxvals = None


    while (np.linalg.norm(saved_p - p) / np.linalg.norm(saved_p)) > ftol and n_iter < maxiter:
        saved_p = copy.copy(p)
        ak = a_par / (n_iter + 1 + big_a)**alpha
        ck = c_par / (n_iter + 1)**gamma

        delta = (np.random.randint(0,2,n_params) * 2 - 1)
        p_plus = p + ck*delta
        p_minus = p - ck*delta
        if maxvals:
            p_plus = np.minimum(p_plus,maxvals)
            p_minus = np.minimum(p_minus,maxvals)
        if minvals:
            p_plus = np.maximum(p_plus,minvals)
            p_minus = np.maximum(p_minus,minvals)

        try:
            grad = (calc(p_plus) - calc(p_minus)) / (2.*ck*delta)
        except:
            print p_plus, p_minus, ck, delta
            raise Exception('Stopping')

        # Scale parameter movement
        this_ak = np.ones(n_params)*ak
        new_ps = p
        running = True
        while running:
            ntry = new_ps - this_ak*grad
            oob = np.where(np.logical_or(ntry > maxvals, ntry < minvals))[0]
            new_ps = p - this_ak*grad
            if len(oob) == 0:
                p -= this_ak*grad
                running = False
            else:
                this_ak[oob] = this_ak[oob]/2.

        new_val = calc(p)
        old_val = new_val
        if n_iter % print_iters == 0:
            print "\tIter %05d" % n_iter, new_val, ak, ck, p

        if param_tol is not None:
            pdiff = np.abs(p - saved_p)
            if not np.all(pdiff < param_tol):
                p = saved_p
                continue
        n_iter += 1

    return (p, new_val,n_iter)

