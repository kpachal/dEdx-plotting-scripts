import ROOT
from art.morisot import Morisot
import math

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

for analysis in ["stable","metastable"] :

  print "Beginning analysis of",analysis,"histogram."

  infile = ROOT.TFile.Open("histos_reprocessed1516_haddedAnn_{0}.root".format(analysis),"READ")
  hist1 = infile.Get("Background_dEdxControl_Validation_MuInclusive/dEdx_vs_met")
  hist1.SetDirectory(0)
  hist2 = infile.Get("Background_pControl_Validation_MuInclusive/dEdx_vs_met")
  hist2.SetDirectory(0)
  hist3 = infile.Get("SignalRegion_Validation_MuInclusive/dEdx_vs_met")
  hist3.SetDirectory(0)

  hist1.Add(hist2)
  hist1.Add(hist3)

  # Calculate correlation
  lowXbin = 1
  highXbin = 30
  factor = hist1.GetCorrelationFactor()
  print "Correlation factor is", factor
  print "Looking at fraction of events above dEdx",hist1.GetXaxis().GetBinLowEdge(highXbin+1)
  # conclusion: not very useful because this is looking for linear correlation. Only shows slight anticorrelation.

  # Check another way: percentage of events to left and right of a vertical line.
  # Put the line at 1.8, which is bottom of bin #31.
  for i in range(12) :
    lowYbin = 1+i*5
#    highYbin = 1+i*5+4
    highYbin = hist1.GetNbinsY()
    number_low = hist1.Integral(lowXbin,highXbin,lowYbin,highYbin)
    number_all = hist1.Integral(1,hist1.GetNbinsX(),lowYbin,highYbin)
    if number_all < 1 : continue
    frac_high = 1. - number_low/number_all
    uncert_on_ratio = frac_high * math.sqrt(1./number_low + 1./number_all)

#    print "\tFrac at high dEdx, {0} < MET < {1}:".format(hist1.GetYaxis().GetBinLowEdge(lowYbin),hist1.GetYaxis().GetBinLowEdge(highYbin+1)), round(frac_high,3)
    print "\tFrac at high dEdx, {0} < MET:".format(hist1.GetYaxis().GetBinLowEdge(lowYbin)), round(frac_high,4), " +/- ", round(uncert_on_ratio,4)

  myPainter.draw2DHist(hist1,"dEdx_vs_met_{0}".format(analysis),"dE/dx",0,6,"MET",0,1000,"Events",luminosity=-1,CME=-1,doRectangular=False,makeCanvas=True)
