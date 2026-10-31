"""D.5 oracle-criterion probe (suite finding S-1, 2026-10-31). Synthetic data only.
Usage: python scripts/tests/probe_oracle_criterion.py A phi reps
AR(1) noise, 20,000 per-step obs, 10 events, linear ramp L=100 of amplitude A x stationary SD;
thresholds matched on the noisy series (P-FA top scan), applied to the same series with noise x 1e-3."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'analysis'))
import pipeline
def ar1(rng,n,phi):
    e=rng.standard_normal(n)*np.sqrt(1-phi**2); x=np.empty(n); x[0]=rng.standard_normal()
    for i in range(1,n): x[i]=phi*x[i-1]+e[i]
    return x
A=float(sys.argv[1]); phi=float(sys.argv[2]); reps=int(sys.argv[3])
n=20000; L=100; nev=10
res=[]
for r in range(reps):
    rng=np.random.default_rng([20261030,999,r])
    x=ar1(rng,n,phi)
    ts=np.linspace(2500,19000,nev).astype(int)
    ev=[{"t_e":int(t),"eligible":True} for t in ts]
    ramp=np.zeros(n)
    for t in ts: ramp[t-L+1:t+1]=A*np.linspace(0,1,L+1)[1:]
    y=x+ramp; a=pipeline.run([{"first_step":0,"y":y,"g":np.exp(y)}],ev,grid=1,scan=128,resample=False,coverage_stop=None)
    y0=1e-3*x+ramp; o=pipeline.run([{"first_step":0,"y":y0,"g":np.exp(y0)}],ev,grid=1,scan=128,resample=False,coverage_stop=None,thetas=a["thetas"])
    res.append(([a["per_detector"][d]["mean_lead"] for d in pipeline.DET],[o["per_detector"][d]["mean_lead"] for d in pipeline.DET],a["C_min"],o["C_min"]))
R=np.array([x[0] for x in res]); O=np.array([x[1] for x in res])
print("A",A,"phi",phi,"n*",a["nstar"])
print("det      ", pipeline.DET)
print("rec mean ", np.round(R.mean(0),1)); print("orc mean ", np.round(O.mean(0),1))
print("per-rep |diff|<=8 frac", np.round((np.abs(R-O)<=8).mean(0),2))
print("Cmin sign agree", np.mean([np.sign(x[2])==np.sign(x[3]) for x in res]))
