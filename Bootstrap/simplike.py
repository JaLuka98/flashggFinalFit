# -*- python -*-

from __future__ import division
import numpy as np

"""
Calculation of Simplified Likelihood parameters

Accompanying code implementation for the paper
  "The Simplified Likelihood framework", arXiv:1809.05548
  https://arxiv.org/abs/1809.05548
by A. Buckley, M. Citron, S. Fichet, S. Kraml, W. Waltenberger and N. Wardle

The expected backgrounds in terms of the combined nuisance parameters
are parameterized as n_I = a_I + b_I theta_I + c_I theta_I^2
where the nuisances, theta_I, are distributed as a multivariate normal.

This reference code includes functions to calculate the coefficients a_I,
b_I, c_I, and rho_IJ from provided moments m_1,I, m_2,IJ and m_3,I,
cf. eqs.(2.9)-(2.12) in the paper. It also includes an SLParams class
which computes these and higher-level statistics such as profile likelihoods,
log likelihood-ratios, and related limit-setting measures computed
using observed and expected signal yields.

**Note:** this code has been written with reverse engineering and
comprehensibility of the calculations explicitly in mind. While it computes
likelihood statistics on a reasonable timescale, further (but less readable)
optimisations can be added for production code.
"""

def getCoeffCi_fast(m2ii, m3iii):
    "Compute c_i from the minimal necessary moment data"
    if not m3iii:
        return 0.0
    rtn = -np.sign(m3iii) * np.sqrt(2*m2ii)
    arg = 8 * m2ii**3 / m3iii**2 - 1
    if arg < 0:
        raise Exception("Negative sqrt term in c_III coeff extraction!")
    rtn *= np.cos(4*np.pi/3 + np.arctan(np.sqrt(arg))/3)
    return rtn

def getCoeffBi_fast(m2ii, ci):
    "Compute b_i from the second-order moment data and a precomputed c_i"
    return np.sqrt(m2ii - 2*ci**2)

def getCoeffAi_fast(m1i, ci):
    "Compute a_i from the first-order moment data and a precomputed c_i"
    return m1i - ci


def getCoeffCi(m1i, m2ii, m3iii):
    "Get c_i from a uniform interface of all moment data"
    return getCoeffCi_fast(m2ii, m3iii)

def getCoeffBi(m1i, m2ii, m3iii):
    "Get b_i from a uniform interface of all moment data (internally recomputes c_i)"
    return getCoeffBi_fast(m2ii, getCoeffCi_fast(m2ii, m3iii))

def getCoeffAi(m1i, m2ii, m3iii):
    "Get a_i from a uniform interface of all moment data (internally recomputes c_i)"
    return getCoeffAi_fast(m1i, getCoeffCi_fast(m2ii, m3iii))


def getCoeffsABCi(m1i, m2ii, m3iii, skew=True):
    "Efficiently compute all three SL coefficients for bin i"
    ci = getCoeffCi_fast(m2ii, m3iii) if skew else 0.0
    return getCoeffAi_fast(m1i, ci), getCoeffBi_fast(m2ii, ci), ci


def getCoeffsABC(m1, m2, m3=None, skew=True):
    "Efficiently compute all three SL coefficients for all bins"
    As, Bs, Cs = [], [], []
    if m3 is not None:
        if m1.ndim > 0:
            assert len(m1) == len(m3)
    if m1.ndim > 0:
        assert m2.shape == tuple([len(m1), len(m1)])
    for i in range(len(m1)):
        A, B, C = getCoeffsABCi(m1[i], m2[i][i], m3[i] if m3 is not None else None, skew)
        As.append(A)
        Bs.append(B)
        Cs.append(C)
    return np.array(As), np.array(Bs), np.array(Cs)


def getRhoIJ(m1i, m2ii, m3iii, m1j, m2jj, m3jjj, m2ij, skew=True):
    "Compute the SL correlation matrix element rho_ij"
    if skew and (m3iii or m3jjj):
        epsilon = 1e-5
        ci = getCoeffCi_fast(m2ii, m3iii)
        cj = getCoeffCi_fast(m2jj, m3jjj)
        ci += epsilon if ci >= 0 else -epsilon
        cj += epsilon if cj >= 0 else -epsilon
        cicj = ci*cj
        #
        bi = getCoeffBi_fast(m2ii, ci)
        bj = getCoeffBi_fast(m2jj, cj)
        bibj = bi*bj
        #
        discr1 = bibj**2
        discr2 = 8*cicj*m2ij
        discr = discr1 + discr2
        #
        rtn = (np.sqrt(abs(discr)) - bibj) / 4 / cicj
    else:
        rtn = m2ij / np.sqrt(m2ii*m2jj)
    return rtn

def getRho(m1, m2, m3, skew=True):
    "Compute the SL correlation matrix rho"
    rho = np.ones(m2.shape)
    for i in range(m2.shape[0]):
        for j in range(m2.shape[1]):
            rhoij = getRhoIJ(m1[i], m2[i,i], m3[i] if m3 is not None else 0.0,
                             m1[j], m2[j,j], m3[j] if m3 is not None else 0.0,
                             m2[i,j], skew)
            rho[i,j] = rhoij
            if i != j:
                rho[j,i] = rhoij
    return rho


class SLParams(object):
    """Unified container for SL background moments, observed data, signal
    prediction, computed coefficients, and statistical functions"""

    def __init__(self, bg_m1, bg_m2, bg_m3=None, obs=None, sig=None, skew=True):
        import scipy.stats as st
        self.bg_m1 = np.array(bg_m1)
        # self.bg_m2 = np.array(bg_m2).reshape([self.size,self.size])
        self.bg_m2 = np.array(bg_m2)
        self.bg_m3 = np.array(bg_m3) if bg_m3 is not None else None
        self.obs = np.array(obs) if obs is not None else None
        self.sig = np.array(sig) if sig is not None else None
        #
        self.aparams, self.bparams, self.cparams = getCoeffsABC(self.bg_m1, self.bg_m2, self.bg_m3, skew=skew)
        self.rhoparams = getRho(self.bg_m1, self.bg_m2, self.bg_m3, skew=skew)
        self.rhoinvparams = np.linalg.inv(self.rhoparams)
        self.thetadbn = st.multivariate_normal(np.zeros(self.size), self.rhoparams)
        #
        self.llmax = None #< for caching of unconditional max LL
        self.llnosig = None #< for caching of no-signal LL

    @property
    def size(self):
        "Number of bins / signal regions"
        if (self.bg_m1).ndim > 0:
            return len((self.bg_m1))
        else:
            return self.bg_m1

    def expbi(self, i, theta_i):
        "Expected background rate in bin i, for SL nuisance component theta_i"
        return self.aparams[i] + self.bparams[i]*theta_i + self.cparams[i]*theta_i**2

    def expbs(self, thetas):
        "Expected background rates in all bins, for SL nuisance vector thetas"
        thetas = np.array(thetas)
        bs = np.array([self.expbi(i, th) for (i, th) in enumerate(thetas)])
        bs[bs <= 0] = 1e-3 #< force any negatives to ~0
        return bs

    def expsi(self, i, mu):
        "Expected signal rate in bin i, for signal strength mu"
        return mu*self.sig[i]

    def expss(self, mu):
        "Expected signal rates in all bins, for signal strength mu"
        return mu*self.sig

    def expsbi(self, i, mu, theta_i):
        "Expected s+b rate in bin i, for signal strength mu and SL nuisance theta_i"
        return self.expsi(i, mu) + self.expbi(i, theta_i)

    def expsbs(self, mu, thetas):
        "Expected s+b rates in all bins, for signal strength mu and SL nuisance vector thetas"
        thetas = np.array(thetas)
        return self.expss(mu) + self.expbs(thetas)

    def sampleth(self, nsamp):
        "Draw nsamp theta vectors from the SL distribution"
        return self.thetadbn.rvs(nsamp)

    def sampleb(self, nsamp):
        "Draw nsamp background arrays from the SL distribution and parametrisation"
        ths = self.thetadbn.rvs(nsamp)
        bs = np.zeros_like(ths)
        for n in range(nsamp):
            bs_n = self.expbgs(ths[n,:])
            bs[n,:] = bs_n
        return bs

    def samplesb(self, mu, nsamp):
        "Draw nsamp s+b arrays from the SL distribution and parametrisation, with signal strength mu"
        bs = self.sampleb(nsamp)
        sbs = mu*self.sig + bs
        return sbs

    def loglike(self, mu, thetas):
        "Calculate the simplified log-likelihood for the given (mu, {theta}) params"
        thetas = np.array(thetas)
        import scipy.stats as st
        assert self.obs is not None
        assert mu == 0 or self.sig is not None
        ll_th = self.thetadbn.logpdf(thetas)
        counts = self.expsbs(mu, thetas)
        lls_poiss = st.poisson.logpmf(self.obs, counts)
        ll_poiss = np.sum(lls_poiss)
        ll_tot = ll_th + ll_poiss
        return ll_tot

    def dloglike(self, mu, thetas):
        "Calculate the gradient vector of the simplified log-likelihood for the given (mu, {theta}) params"
        thetas = np.array(thetas)
        grad = np.zeros(self.size+1)
        ## mu direction first:
        dlldmus = (self.obs/self.expsbs(mu, thetas) - 1) * self.expss(1.0) #< mu*s -> s in derivative
        grad[0] = np.sum(dlldmus)
        ## Now the thetas
        dlldths = (self.obs/self.expsbs(mu, thetas) - 1) * (self.bparams + 2*self.cparams*thetas) \
                  - np.sum(self.rhoinvparams*thetas, axis=1)
        grad[1:] = dlldths
        return grad

    def maxloglike(self, mu=None, rtnparams=False):
        """Calculate the conditional or unconditional maximum log likelihood

        If mu=None, the unconditional (i.e. absolute) maximum LL will be computed
        over (mu, {theta}). Otherwise, the likelihood conditional on mu wil be
        computed over {theta}.
        """
        from scipy.optimize import minimize
        if mu is None:
            if self.llmax is not None: #< return cached value if available
                minres, llopt = self.llmax
            else:
                def calc_optll_unconditional(mu_thetas):
                    return -self.loglike(mu_thetas[0], mu_thetas[1:])
                def calc_gradll_unconditional(mu_thetas):
                    return -self.dloglike(mu_thetas[0], mu_thetas[1:])
                minres = minimize(calc_optll_unconditional, [0 for _ in range(self.size+1)],
                                  jac=calc_gradll_unconditional)
                llopt = -calc_optll_unconditional(minres.x)
                self.llmax = (minres, llopt)
        else:
            if mu == 0 and self.llnosig is not None:
                minres, llopt = self.llnosig #< use mu=0 cache
            else:
                def calc_optll_conditional(thetas, mu): #< capture mu?
                    return -self.loglike(mu, thetas)
                def calc_gradll_conditional(thetas, mu):
                    return -self.dloglike(mu, thetas)[1:]
                minres = minimize(calc_optll_conditional, np.zeros(self.size),
                                  jac=calc_gradll_conditional, args=(mu,))
                llopt = -calc_optll_conditional(minres.x, mu)
                if mu == 0:
                    self.llnosig = (minres, llopt) #< mu=0 caching
        if rtnparams:
            return llopt, minres.x
        else:
            return llopt

    def deltaloglike(self, mu, wrtnosig=False):
        """Calculate profile likelihood log-likelihood difference, ln lambda_mu.

        If wrtnosig is True, calculate the delta with respect to the no-signal mu=0
        profile likelihood rather than the unconditional max likelihood.
        """
        ll_mu = self.maxloglike(mu)
        ll_0 = self.maxloglike(0 if wrtnosig else None) #< NB. use of cached maxLLs
        return ll_mu - ll_0

    def tmu(self, mu, wrtnosig=False):
        """Calculate profile likelihood chi2-distributed test statistic, t_mu = -2 ln lambda_mu"""
        return -2 * self.deltaloglike(mu, wrtnosig)


if __name__ == "__main__":

    import numpy as np
    from scipy import stats as st

    # ## Load data sampled from elementary nuisances
    # bs_true = np.loadtxt("toy_trees.dat.gz")
    # BG_M1 = np.mean(bs_true, axis=0)
    # BG_M2 = np.cov(bs_true, rowvar=False)
    # BG_M3 = st.moment(bs_true, 3, axis=0)
    # SIGNAL = np.array([0.0, 0.8760676383972168, 1.6500988006591797, 2.3310067653656006, 2.9270126819610596, 3.4456961154937744, 3.894041061401367, 4.278481483459473, 4.6049394607543945, 4.878864765167236, 5.105268955230713, 5.28875732421875, 5.433560848236084, 5.543562412261963, 5.622325420379639, 5.67311429977417, 5.342737674713135, 5.0316009521484375, 4.738583087921143, 4.462629795074463, 4.202746391296387, 3.9579975605010986, 3.727501630783081, 3.5104289054870605, 3.305997371673584, 3.113471031188965, 2.932156562805176, 2.7614011764526367, 2.6005897521972656, 2.449143171310425, 0.0, 0.2255440205335617, 0.43775638937950134, 0.6372280716896057, 0.824526846408844, 1.0001980066299438, 1.1647652387619019, 1.318731427192688, 1.4625794887542725, 1.5967729091644287, 1.7217568159103394, 1.8379583358764648, 1.9457874298095703, 2.045637369155884, 2.137885808944702, 2.2228946685791016, 2.157198190689087, 2.0934433937072754, 2.0315728187561035, 1.971530795097351, 1.913263201713562, 1.856717824935913, 1.8018434047698975, 1.7485909461975098, 1.6969122886657715, 1.6467609405517578, 1.5980918407440186, 1.5508610010147095, 1.5050262212753296, 1.4605458974838257, 0.0, 0.12994906306266785, 0.2567979693412781, 0.38060224056243896, 0.5014163851737976, 0.6192941665649414, 0.7342885136604309, 0.8464512825012207, 0.9558337926864624, 1.0624864101409912, 1.1664586067199707, 1.2677992582321167, 1.3665562868118286, 1.4627768993377686, 1.5565075874328613, 1.6477940082550049, 1.6281386613845825, 1.6087177991867065, 1.5895285606384277, 1.5705682039260864, 1.551833987236023, 1.5333232879638672, 1.5150333642959595, 1.4969615936279297, 1.4791053533554077, 1.4614622592926025, 1.444029450416565, 1.4268046617507935, 1.409785270690918, 1.392969012260437])
    # DATA = np.array([281.0, 266.0, 205.0, 186.0, 171.0, 161.0, 116.0, 94.0, 89.0, 73.0, 67.0, 59.0, 54.0, 44.0, 37.0, 24.0, 30.0, 17.0, 20.0, 15.0, 16.0, 12.0, 10.0, 10.0, 9.0, 2.0, 6.0, 5.0, 4.0, 6.0, 59.0, 52.0, 33.0, 45.0, 31.0, 33.0, 18.0, 28.0, 33.0, 20.0, 20.0, 16.0, 10.0, 12.0, 19.0, 13.0, 11.0, 5.0, 12.0, 8.0, 10.0, 12.0, 12.0, 6.0, 7.0, 2.0, 7.0, 6.0, 3.0, 3.0, 4.0, 7.0, 4.0, 6.0, 2.0, 5.0, 5.0, 3.0, 7.0, 3.0, 4.0, 3.0, 3.0, 1.0, 0.0, 4.0, 4.0, 5.0, 1.0, 1.0, 5.0, 3.0, 4.0, 0.0, 3.0, 2.0, 5.0, 2.0, 1.0, 1.0])
    # NBINS = len(BG_M1)

    ## Load data from the model script
    exec(open("model-90_100000toys.py").read())
    NBINS = nbins
    BG_M1 = np.array(background)
    BG_M2 = np.array(covariance).reshape([NBINS,NBINS]) #!
    #print np.linalg.eigvals(BG_M2)
    BG_M3 = np.array(third_moment)
    SIGNAL = np.array(signal)
    DATA = np.array(data)

    ## Create the key SL params objects
    slp1 = SLParams(BG_M1, BG_M2, obs=DATA, sig=SIGNAL)
    slp2 = SLParams(BG_M1, BG_M2, BG_M3, obs=DATA, sig=SIGNAL)

    ## Calculate t_mu values for a range of mu values
    mus = np.linspace(0,1,30)
    tmus1 = [slp1.tmu(mu) for mu in mus]
    tmus2 = [slp2.tmu(mu) for mu in mus]

    ## Compare to true t_mu values computed from full likelihood
    mustrue = np.linspace(0,1,16+1)
    tmustrue = [0.0009691, 0.0411193, 0.1329959, 0.2649894, 0.4527930, 0.6973918, 0.9997511, 1.3608103, 1.7814781, 2.2626238, 2.8050761, 3.4096148, 4.0769662, 4.8079994, 5.6025722, 6.4611683, 7.3840528]

    ## Plot
    from matplotlib import pyplot as plt
    plt.figure()
    plt.axhline(st.chi2.ppf(0.68, 1), linestyle=":", color="gray")
    plt.annotate("68%", xy=(0.0, st.chi2.ppf(0.68,1)+0.2), color="gray")
    plt.axhline(st.chi2.ppf(0.95, 1), linestyle=":", color="gray")
    plt.annotate("95%", xy=(0.0, st.chi2.ppf(0.95,1)+0.2), color="gray")
    #
    plt.plot(mustrue, tmustrue, "-", color="black", label="Full likelihood")
    plt.plot(mus, tmus1, "--", color="red", label="Simplified likelihood (linear)")
    plt.plot(mus, tmus2, "--", color="green", label="Simplified likelihood (quadratic)")
    print("mus:", mus)
    print("t_mu (quadratic):", tmus2)
    plt.legend(loc="best")
    #
    plt.xlabel(r"Signal strength $\mu$")
    plt.ylabel(r"$t_\mu = -2 \Delta \ln L$")
    plt.tight_layout()
    plt.savefig("testtoy-tmuscan.pdf")
    plt.close()
