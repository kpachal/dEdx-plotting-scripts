from art.morisot import Morisot
import glob
import ROOT
from analysisScripts.generalfunctions import *

## Every 1D plot for the same analysis selection, compared 
## between the different control regions, normalised to unity and overlaid.

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

tag = "20p7_"

plotsDir = "plots_compareAcrossRegions/"
#filename = "../run/histograms_complex_all1.8_{0}.root"
filename = "../run/histograms_release20.7_{0}.root"

regions = ["Background_dEdxControl","Background_pControl","SignalRegion"]
map_plot_name_type = {}

for analysis in ["stable","metastable"] :

  print "Beginning analysis of",analysis,"histograms."

  infile = ROOT.TFile.Open(filename.format(analysis),"READ")
  keys = infile.GetKeyNames("Validation/")  

  # Loop over each region+analysis selection and get histograms
  hist_storage = {}
  for [keyname,keytype] in keys :

    if not "TDirectory" in keytype : continue

    # Region name and analysis bin name
    for region_option in regions :
      if region_option in keyname :
        region_name = region_option
        bin_name = keyname.replace(region_option+"_","")

    print "Got region name and bin name",region_name,bin_name

    # Make location in hist_storage for this analysis bin
    if not bin_name in hist_storage.keys() :
      hist_storage[bin_name] = {}

    # Make sub-dictionary for each plot existing in the region
    plots_list = infile.GetKeyNames("Validation/{0}".format(keyname))
    for [plotname,plottype] in plots_list :

      if not plotname in hist_storage[bin_name].keys() :
        hist_storage[bin_name][plotname] = {}

      store_name = plotname.replace("Validation_{0}_{1}_".format(region_name,bin_name),"")

      # Time to get the plot and store with appropriate label
      hist = infile.Get("Validation/{0}/{1}".format(keyname,plotname))
      hist.SetDirectory(0)
      hist_storage[bin_name][store_name][region_name] = hist

      # And note what type this plot is for later
      map_plot_name_type[store_name] = plottype

  # Drawing time!
  for bin_name in hist_storage.keys() :

    print "Making overlaid plots for bin",bin_name

    for plot in hist_storage[bin_name].keys() :

      if "TH1" in map_plot_name_type[plot] :

        histsToDraw = hist_storage[bin_name][plot]

        histList = []
        labelList = []
        for region_name in histsToDraw.keys() :
          if "Signal" in region_name : continue
          thishist = histsToDraw[region_name]
          if thishist.Integral() != 0 :
            thishist.Scale(1.0/thishist.Integral())
          histList.append(thishist)
          labelList.append(region_name)

        plotName = plotsDir+"/{3}{0}_{1}_{2}".format(analysis,bin_name,plot,tag)
        myPainter.drawManyOverlaidHistograms(histList,labelList,plot,"A.U.",plotName,"automatic","automatic","automatic","automatic",doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")

      else :
        print "TH2, currently skipping"

  infile.Close()

