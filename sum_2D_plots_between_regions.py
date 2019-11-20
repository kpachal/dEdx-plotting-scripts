import ROOT
from art.morisot import Morisot
import math
from analysisScripts.generalfunctions import *

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(2) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

filename = "../run/histograms_complex_all1.8_{0}.root"

plot_dict = {
  "dEdx_vs_met" : {"labels" : ["dE/dx","MET"], "range" : [0,6,0,1000]},
  "dPhi_vs_met" : {"labels" : ["#Delta#phi","MET"], "range" : [-3.2,3.2,0,1000]}}

for analysis in ["stable","metastable"] :

  print "Beginning analysis of",analysis,"histograms."

  infile = ROOT.TFile.Open(filename.format(analysis),"READ")
  keys = infile.GetKeyNames("Validation/")  

  for plot in plot_dict.keys() :

    hist_storage = {}
    for [keyname,keytype] in keys :
      hist = infile.Get("Validation/{0}/{1}".format(keyname,plot))
      hist.SetDirectory(0)
      keyname_tokens = keyname.split("_")
      region_name = keyname_tokens[-2] + "_" + keyname_tokens[-1]
      if not region_name in hist_storage.keys() :
        hist_storage[region_name] = []
      hist_storage[region_name].append(hist)

    for region_name in hist_storage.keys() :

      plot_name = "plots_correlationchecks/{0}_{1}_{2}".format(plot,analysis,region_name)

      main_hist = hist_storage[region_name][0]
      main_hist.Add(hist_storage[region_name][1])
      main_hist.Add(hist_storage[region_name][2])

      # Calculate correlation
      if "dEdx_vs_met" in plot_name :
        lowXbin = 1
        highXbin = 30
        factor = main_hist.GetCorrelationFactor()
        print "Correlation factor is", factor
        print "Looking at fraction of events above dEdx",main_hist.GetXaxis().GetBinLowEdge(highXbin+1)

        # Check another way: percentage of events to left and right of a vertical line.
        # Put the line at 1.8, which is bottom of bin #31.
        for i in range(18) :
          lowYbin = 1+i*5
          highYbin = main_hist.GetNbinsY()
          number_low = main_hist.Integral(lowXbin,highXbin,lowYbin,highYbin)
          number_all = main_hist.Integral(1,main_hist.GetNbinsX(),lowYbin,highYbin)
          if number_all < 1 : continue
          frac_high = 1. - number_low/number_all
          if number_low < 1 : 
            uncert_on_ratio = 1
          else : 
            uncert_on_ratio = frac_high * math.sqrt(1./number_low + 1./number_all)

          print "\tFrac at high dEdx, {0} < MET:".format(main_hist.GetYaxis().GetBinLowEdge(lowYbin)), round(frac_high,4), " +/- ", round(uncert_on_ratio,4)

      labels = plot_dict[plot]["labels"]
      ranges = plot_dict[plot]["range"]
      myPainter.draw2DHist(main_hist,plot_name,labels[0],ranges[0],ranges[1],labels[1],ranges[2],ranges[3],"Events",luminosity=-1,CME=-1,doRectangular=False,makeCanvas=True)
