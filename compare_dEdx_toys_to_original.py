from art.morisot import Morisot
import glob
import ROOT

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

file = "../run/results_complex_all1.8_stable.root"
open_file = ROOT.TFile.Open(file,"READ")
dir_name = "Validation"

namemap = {
  "momentum" : "p", "eta" : "eta", "ionisation" : "dEdx"
}
rangemap = {
  "momentum" : [50,200],"eta" : [-3,3],"ionisation" : [0.5,2.5]
}

for mu_status in ["IsMu","IsNotMu"] :
  for nUsedHits in ["IBLOverflow","NoIBLNUsed2","NoIBLNUsed3Plus"] :

    for distribution in ["momentum","eta","ionisation"] :

      plotnameval = namemap[distribution]

      hist_generated_name = dir_name+"/generated_{2}_{0}_{1}VALIDATION".format(mu_status,nUsedHits,distribution)
      hist_generated = open_file.Get(hist_generated_name)
      hist_generated.SetDirectory(0)

      hist_dEdxControl_name = dir_name+"/InputDistributions/background_dEdxControl/Validation_Background_dEdxControl_{0}_{1}_{2}".format(mu_status,nUsedHits,plotnameval)
      hist_dEdxControl = open_file.Get(hist_dEdxControl_name)
      hist_dEdxControl.SetDirectory(0)

      hist_pControl_name = dir_name+"/InputDistributions/background_pControl/Validation_Background_pControl_{0}_{1}_{2}".format(mu_status,nUsedHits,plotnameval)
      hist_pControl = open_file.Get(hist_pControl_name)
      hist_pControl.SetDirectory(0)

      # Normalize all to 1
      hist_generated.Scale(1.0/hist_generated.Integral())
      hist_dEdxControl.Scale(1.0/hist_dEdxControl.Integral())
      hist_pControl.Scale(1.0/hist_pControl.Integral())

      if "dEdx" in plotnameval :

        # Integral above 1.8
        for bin in range(2,hist_dEdxControl.GetNbinsX()) :
          if hist_dEdxControl.GetBinCenter(bin-1) < 1.8 and hist_dEdxControl.GetBinCenter(bin) > 1.8 : break

        ratio_highdEdx_generated = hist_generated.Integral(bin,hist_generated.GetNbinsX())/hist_generated.Integral()
        ratio_highdEdx_original = hist_dEdxControl.Integral(bin,hist_dEdxControl.GetNbinsX())/hist_dEdxControl.Integral()
        print "In region",mu_status,nUsedHits,":"
        print "found original fraction at high dEdx =",round(ratio_highdEdx_original,4)
        print "and generated fraction =",round(ratio_highdEdx_generated,4)

        hist_list = [hist_dEdxControl,hist_generated]

      else :
        hist_list = [hist_pControl,hist_generated]

      name_list = ["Original","Generated"]
    
      line_1 = "{0}, {1}".format(mu_status,nUsedHits)
      extraLegendLines = [line_1]

      outname = "plots/{2}_generatedToReal_{0}_{1}".format(mu_status,nUsedHits,plotnameval)

      ranges = rangemap[distribution]

      # Compare template and generated
      myPainter.drawManyOverlaidHistograms(hist_list,name_list,plotnameval,"A.U.",outname,ranges[0],ranges[1],"automatic","automatic",doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None",extraLegendLines=extraLegendLines)

      hist_list = [hist_pControl,hist_dEdxControl,hist_generated]
      name_list = ["p-control region","dEdx control region","Generated"]

      # Compare both control regions to generated
      myPainter.drawManyOverlaidHistograms(hist_list,name_list,plotnameval,"A.U.",outname+"_allRegions",ranges[0],ranges[1],"automatic","automatic",doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None",extraLegendLines=extraLegendLines)

open_file.Close()

