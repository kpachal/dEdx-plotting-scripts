from art.morisot import Morisot
from art.morisot_2p0 import Morisot_2p0
import glob
import ROOT

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation
                          
myPainter.dodrawUsersText = False             

myPainter2 = Morisot_2p0()
myPainter2.setColourPalette("notSynthwave")

file = "../run/results_reprocessed1516_haddedAnn_{0}.root"
plotDir = "plots_bkgvalidation/"

for analysis in ["stable", "metastable"] :

  thisfile = file.format(analysis)
  open_file = ROOT.TFile.Open(thisfile,"READ")  

  for region in ["Nominal", "Validation"] :

    # Plot 1: data versus background estimate in SR. Blinded in data (should just be background estimate).
    mass_SR_est = open_file.Get("{0}/scaled_generated_mass_SR_{1}".format(region,region.upper()))
    mass_SR_est.SetDirectory(0)
    mass_SR = open_file.Get("{0}/data_mass_passcut_{1}".format(region,region.upper()))
    mass_SR.SetDirectory(0)
    name_list = ["Background estimate, SR","Data, SR"]
    outname = plotDir+region + "_"+analysis + "_dataVsBkg_SR"
    myPainter2.drawManyOverlaidHistograms([mass_SR_est],mass_SR,name_list,"Mass [GeV]","Events",outname,0,500,0,50,extraLegendLines = [region+" region"],doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")
    thisratio = myPainter.createRatio(mass_SR,[mass_SR_est])
    myPainter.drawDataAndFitOverSignificanceHist(mass_SR,mass_SR_est,thisratio,"Mass [GeV]","Events","Data/bkg",outname+"_withratio",-1,-1,-999,-999,firstBin=-1,lastBin=-1,doBumpLimits=False,extraLegendLines=[region+" region"],doLogX=False,doRectangular=False,)

#     # Plot 2: Same but with paper binning

#     # Plot 3: data versus background estimate, with estimated normalisation, in p-control region.
#     mass_pcontrol_est = open_file.Get("{0}/scaled_generated_mass_pcontrol_{1}".format(region,upper(region)))
#     mass_pcontrol = open_file.Get("{0}/data_mass_failcut_{1}".format(region,upper(region)))

#     # Plot 4: compare mass distribution of tracks in each control region, normalised to 1
#     # Include estimate in p-control region.

#     mass3 = open_file.Get("{0}/")

  open_file.Close()


# hist5 = open_file.Get("Background_dEdxControl_Nominal_MuInclusive/dEdx_p150_p250")
# hist6 = open_file.Get("Background_dEdxControl_Nominal_MuInclusive/dEdx_p250_inf")

# hist7 = open_file.Get("Background_pControl_Nominal_MuInclusive/p")

# fine_bin_dict = {}
# for p_string in ["none","p150_p250","p250_inf"] :
#   fine_bin_dict[p_string] = {}
#   for eta_string in ["below_eta0p10","eta0p10_eta1p00","eta1p00_eta1p50","eta1p50_eta1p75","eta1p75_eta2p00"] :
#     if p_string == "none" :
#       name = "Background_dEdxControl_Nominal_MuInclusive/dEdx_{0}".format(eta_string)
#     else :
#       name = "Background_dEdxControl_Nominal_MuInclusive/dEdx_{0}_{1}".format(p_string,eta_string)
#     print "Fetching",name,"..."
#     hist = open_file.Get(name)
#     hist.SetDirectory(0)  
#     fine_bin_dict[p_string][eta_string] = hist


# for p_string in ["none","p150_p250","p250_inf"] :

#   hist_list = []
#   name_list = []
#   for eta_string in ["below_eta0p10","eta0p10_eta1p00","eta1p00_eta1p50","eta1p50_eta1p75","eta1p75_eta2p00"] :
#     hist = fine_bin_dict[p_string][eta_string]

#     # Normalize
#     hist.Scale(1.0/hist.Integral())

#     hist_list.append(hist)
#     name_string = hist.GetName()
#     name_tokens = name_string.split("_")
#     eta_tokens = [name_tokens[-2],name_tokens[-1]]
#     name_new = "{0} < #eta < {1}"
#     for token in eta_tokens :
#       index = eta_tokens.index(token)
#       token = token.replace("eta","")
#       token = token.replace("p",".")
#       eta_tokens[index] = token
#     name_new = name_new.format(eta_tokens[0],eta_tokens[1])
#     name_list.append(name_new)

#   outname = "plots/eta_comparison_dEdx"
#   if "none" not in p_string :
#     outname = outname + "_"+p_string

#   myPainter.drawManyOverlaidHistograms(hist_list,name_list,"dE/dx","A.U.",outname,0.5,2.5,"automatic","automatic",doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")
#   myPainter.drawManyOverlaidHistograms(hist_list,name_list,"dE/dx","A.U.",outname+"_log",0.5,2.5,"automatic","automatic",doLogX=False,doLogY=True,doLegendLow=False,doATLASLabel="None")

# hist_list = []
# name_list = []
# for hist in [hist5, hist6] :
#   hist.SetDirectory(0)

#   # Normalize
#   hist.Scale(1.0/hist.Integral())

#   hist_list.append(hist)
#   name_string = hist.GetName()  
#   name_tokens = name_string.split("_")
#   p_tokens = [name_tokens[-2],name_tokens[-1]]
#   name_new = "{0} < momentum [GeV] < {1}"  
#   for token in p_tokens :
#     index = p_tokens.index(token)
#     token = token.replace("p","")
#     p_tokens[index] = token
#   name_new = name_new.format(p_tokens[0],p_tokens[1])
#   name_list.append(name_new)

# myPainter.drawManyOverlaidHistograms(hist_list,name_list,"dE/dx","A.U.","plots/p_comparison_dEdx",0.5,2.5,"automatic","automatic",doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")
# myPainter.drawManyOverlaidHistograms(hist_list,name_list,"dE/dx","A.U.","plots/p_comparison_dEdx_log",0.5,2.5,"automatic","automatic",doLogX=False,doLogY=True,doLegendLow=False,doATLASLabel="None")

# hist7.SetDirectory(0)
# hist7.Scale(1.0/hist7.Integral())
# myPainter.drawManyOverlaidHistograms([hist7],["Momentum from high-MET CR"],"Momentum [GeV]","A.U.","plots/p",-1000,1000,"automatic","automatic",doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")
# myPainter.drawManyOverlaidHistograms([hist7],["Momentum from high-MET CR"],"Momentum [GeV]","A.U.","plots/p_log",-1000,1000,"automatic","automatic",doLogX=False,doLogY=True,doLegendLow=False,doATLASLabel="None")
