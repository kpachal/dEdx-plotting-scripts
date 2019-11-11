import ROOT

# Stable
sets_obs_expected_err = [
[7,5.3,0.1],
[38,38.4,0.016],
[33,43.3,0.012],
[3,2.85,0.25],
[22,27.9,0.034],
[8.,17.6,0.026]
]

# Metastable
sets_obs_expected_err = [
[7,6.3,.125],
[48,53.4,.020],
[23,35.0,0.014]
]

for sets in sets_obs_expected_err :

  obs = sets[0]
  exp = sets[1]
  err = sets[2]

  if (obs >= exp) :
    pval = ROOT.RooStats.NumberCountingUtils.BinomialObsP(obs,exp,err)
  else :
    pval = 1.0 - ROOT.RooStats.NumberCountingUtils.BinomialObsP(obs+1,exp,err)

  zval = ROOT.RooStats.PValueToSignificance(pval/2.)
  print obs,exp,":\t",pval,"\t",zval
