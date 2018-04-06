#!/usr/bin/env python

import os, sys, ROOT
import numpy as np

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetNdivisions(405,"x");
ROOT.gStyle.SetEndErrorSize(0.)
ROOT.gStyle.SetErrorX(0.001)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

def getSJBTagEff(ptin, etain, fmap):
  etain = abs(etain)
  f = ROOT.TFile.Open(fmap)
  heff = f.Get('heff')
  for i in range(0, heff.GetNbinsX()+2):
    for j in range(0, heff.GetNbinsY()+01):
      pt       = heff.GetXaxis().GetBinLowEdge(i)
      eta      = heff.GetYaxis().GetBinLowEdge(j)
      ptwidth  = heff.GetXaxis().GetBinWidth(i)
      etawidth = heff.GetYaxis().GetBinWidth(j)
      if pt <= ptin < pt+ptwidth and eta <= etain < eta+etawidth:
        return heff.GetBinContent(i,j)
      else: continue
  return 0

def getHTagEff(ptin, etain):
  etain = abs(etain)
  f = ROOT.TFile.Open('heff.root')
  heff = f.Get('heff')
  for i in range(0, heff.GetNbinsX()+2):
    for j in range(0, heff.GetNbinsY()+01):
      pt       = heff.GetXaxis().GetBinLowEdge(i)
      eta      = heff.GetYaxis().GetBinLowEdge(j)
      ptwidth  = heff.GetXaxis().GetBinWidth(i)
      etawidth = heff.GetYaxis().GetBinWidth(j)
      if pt <= ptin < pt+ptwidth and eta <= etain < eta+etawidth:
        return heff.GetBinContent(i,j)
      else: continue
  return 0

import optparse

def main():

  options = optparse.OptionParser()
  
  options.add_option('-f', '--files',  
      dest="files", 
      default="VBF_M1500_W01_PU200.txt",
      type="string",
      )
  options.add_option('-n', '--maxEvts',  
      dest="maxEvts", 
      default=-1,
      type="int",
      )
  
  evtsel = optparse.OptionGroup(options, "Event selections",
                          "Caution: Do not change by hand")
                                              
  evtsel.add_option("--nak8min", 
      dest="nak8Min", 
      default=2,
      type="int",
      )
  
  evtsel.add_option("--ptak8_0_Min", 
      dest="ptak8_0_Min", 
      default=300.,
      type="float",
      )
  
  evtsel.add_option("--ptak8_1_Min", 
      dest="ptak8_1_Min", 
      default=300.,
      type="float",
      )
  
  evtsel.add_option("--etaak8_0_Max", 
      dest="etaak8_0_Max", 
      default=3.0,
      type="float",
      )
  
  evtsel.add_option("--etaak8_1_Max", 
      dest="etaak8_1_Max", 
      default=3.0,
      type="float",
      )
  
  evtsel.add_option("--detaak8Max", 
      dest="detaak8Max", 
      default=100.,
      type="float",
      )
  
  evtsel.add_option("--t21_0_Max", 
      dest="t21_0_Max", 
      default=0.60,
      type="float",
      )
  
  evtsel.add_option("--t21_1_Max", 
      dest="t21_1_Max", 
      default=0.60,
      type="float",
      )
  
  evtsel.add_option("--msd_0_Min", 
      dest="msd_0_Min", 
      default=80.,
      type="float",
      )
  
  evtsel.add_option("--msd_0_Max", 
      dest="msd_0_Max", 
      default=160.,
      type="float",
      )
  
  evtsel.add_option("--msd_1_Min", 
      dest="msd_1_Min", 
      default=60.,
      type="float",
      )
  
  evtsel.add_option("--msd_1_Max", 
      dest="msd_1_Max", 
      default=140.,
      type="float",
      )
  
  evtsel.add_option("--deepcsvMin", 
      dest="deepcsvMin", 
      default=0.1522, # deepcsvl=0.1522 deepcsvm=0.4941
      type="float",
      )
  
  evtsel.add_option("--ptak4Min", 
      dest="ptak4Min", 
      default=50., 
      type="float",
      )
  
  evtsel.add_option("--etaak4Max", 
      dest="etaak4Max", 
      default=5.0, 
      type="float",
      )
  
  evtsel.add_option("--detavbfMin", 
      dest="detavbfMin", 
      default=5.0, 
      type="float",
      )
  
  evtsel.add_option("--mjjvbfMin", 
      dest="mjjvbfMin", 
      default=300., 
      type="float",
      )
  
  options.add_option_group(evtsel)
  
  opt, remainder = options.parse_args()
  
  print opt
  
  fout = ROOT.TFile(opt.files.rstrip().replace('txt', 'root'), 'RECREATE')
  fout.cd()
  
  h2_msd0_npv                  = ROOT.TH2D("h2_msd0_npv"                  ,";n(PV);Soft dropped mass (leding AK8) [GeV];;"  , 200, 0., 200., 20, 0., 200.)
  h2_msd1_npv                  = ROOT.TH2D("h2_msd1_npv"                  ,";n(PV);Soft dropped mass (2nd AK8) [GeV];;"     , 200, 0., 200., 20, 0., 200.)
  
  h2_bFl_sjpt_sjeta            = ROOT.TH2D("h2_bFl_sjpt_sjeta"            ,";p_{T} (subjet) [GeV]; #eta (subjet);;", 200, 0., 2000, 50, -5, 5)
  h2_bFl_sjpt_sjeta_btagged    = ROOT.TH2D("h2_bFl_sjpt_sjeta_btagged"    ,";p_{T} (subjet) [GeV]; #eta (subjet);;", 200, 0., 2000, 50, -5, 5)
                                                   
  h2_cFl_sjpt_sjeta            = ROOT.TH2D("h2_cFl_sjpt_sjeta"            ,";p_{T} (subjet) [GeV]; #eta (subjet);;", 150, 0., 3000, 50, -5, 5)
  h2_cFl_sjpt_sjeta_btagged    = ROOT.TH2D("h2_cFl_sjpt_sjeta_btagged"    ,";p_{T} (subjet) [GeV]; #eta (subjet);;", 150, 0., 3000, 50, -5, 5)
                                                   
  h2_lFl_sjpt_sjeta            = ROOT.TH2D("h2_lFl_sjpt_sjeta"            ,";p_{T} (subjet) [GeV]; #eta (subjet);;", 150, 0., 3000, 50, -5, 5)
  h2_lFl_sjpt_sjeta_btagged    = ROOT.TH2D("h2_lFl_sjpt_sjeta_btagged"    ,";p_{T} (subjet) [GeV]; #eta (subjet);;", 150, 0., 3000, 50, -5, 5)
  
  h2_ak4pt_ak4eta              = ROOT.TH2D("h2_ak4pt_ak4eta"              ,";p_{T} (AK4) [GeV]; #eta (AK4);;", 150, 0., 3000, 50, -5, 5)
  
  h_genH_pt                    = ROOT.TH1D("h_genH_pt"                    ,"p_{T} (H) [GeV]; Events;;"     ,300  ,0.    ,3000)
  h_genH_eta                   = ROOT.TH1D("h_genH_eta"                   ,"#eta (H) [GeV]; Events;;"      ,200  ,-5    ,5)

  h_nak8                       = ROOT.TH1D("h_nak8"                       ,";N(AK8) [GeV]; Events;;"       ,11   ,-0.5  ,10.5 )
  h_nak4                       = ROOT.TH1D("h_nak4"                       ,";N(AK4) [GeV]; Events;;"       ,501  ,-0.5  ,501.5)
  
  h_ak80pt                     = ROOT.TH1D("h_ak80pt"                     ,";p_{T} [GeV]; Events;;"        ,300  ,0.    ,3000 )
  h_ak81pt                     = ROOT.TH1D("h_ak81pt"                     ,";p_{T} [GeV]; Events;;"        ,300  ,0.    ,3000 )
  h_ak80eta                    = ROOT.TH1D("h_ak80eta"                    ,";#eta;;"                       ,200  ,-5    ,5    )
  h_ak81eta                    = ROOT.TH1D("h_ak81eta"                    ,";#eta;;"                       ,200  ,-5    ,5    )
  h_ak80_tau2_tau1             = ROOT.TH1D("h_ak80_t2byt1"                ,";#tau_{2}/#tau_{1};;"          ,100  ,0     ,1    )
  h_ak81_tau2_tau1             = ROOT.TH1D("h_ak81_t2byt1"                ,";#tau_{2}/#tau_{1} ;;"         ,100  ,0     ,1    )
  h_sdmass_ak80                = ROOT.TH1D("h_sdmass_ak80"                ,";softdropped_mass[GeV];;"      ,100  ,0     ,1000 )
  h_sdmass_ak81                = ROOT.TH1D("h_sdmass_ak81"                ,";softdropped_mass[GeV];;"      ,100  ,0     ,1000 )
  
  h_nvbfpairs                  = ROOT.TH1D("h_nvbfpairs"                  ,";N(VBF pairs); Events;;"       ,201  ,-0.5  ,200.5 )
  h_vbf0pt                     = ROOT.TH1D("h_vbf0pt"                     ,";p_{T} (VBF) [GeV]; Events;;"  ,100  ,0.    ,1000 )
  h_vbf1pt                     = ROOT.TH1D("h_vbf1pt"                     ,";p_{T} (VBF) [GeV]; Events;;"  ,100  ,0.    ,1000 )
  h_vbf0eta                    = ROOT.TH1D("h_vbf0eta"                    ,";#eta (VBF); Events;"          ,200  ,-5    ,5    )
  h_vbf1eta                    = ROOT.TH1D("h_vbf1eta"                    ,";#eta (VBF); Events;"          ,200  ,-5    ,5    )
  h_deltaEta                   = ROOT.TH1D("h_deltaEta"                   ,";#delta#eta of VBF jets;;"     ,20   ,0     ,10   )
  h_mjjvbf                     = ROOT.TH1D("h_mjjvbf"                     ,";M(jj) (VBF) [GeV]; Events;"   ,200  ,0.    ,2000 )
  
  h_sj0_pts                    = ROOT.TH1D("h_sj0_pts"                    ,";p_{T} of subjet_1;;"          ,300   ,0     ,3000 )
  h_sj1_pts                    = ROOT.TH1D("h_sj1_pts"                    ,";p_{T} of subjet_2;;"          ,300   ,0     ,3000 )
  h_sj0_csvv2                  = ROOT.TH1D("h_sj0_csvv2"                  ,";CSVv2 of subjet_1;;"          ,100   ,0.    ,1.   )
  h_sj1_csvv2                  = ROOT.TH1D("h_sj1_csvv2"                  ,";CSVv2 of subjet_2;;"          ,100   ,0.    ,1.   )
  h_sj0_deepcsv                = ROOT.TH1D("h_sj0_deepcsv"                ,";DeepCSV of subjet_1;;"        ,100   ,0.    ,1.   )
  h_sj1_deepcsv                = ROOT.TH1D("h_sj1_deepcsv"                ,";DeepCSV of subjet_2;;"        ,100   ,0.    ,1.   )
  
  h_mjj_3b                     = ROOT.TH1D("h_mjj_3b"                     ,";M(jj) [GeV]; Events;"         ,400  ,500.   ,4500 )
  h_mjj_4b                     = ROOT.TH1D("h_mjj_4b"                     ,";M(jj) [GeV]; Events;"         ,400  ,500.   ,4500 )
  
  h_cutflow                    = ROOT.TH1D("h_cutflow"                    ,";;Events;"                     ,10   ,0.5    ,10.5 )
  
  h_cutflow.GetXaxis().SetBinLabel(1 ,"All evts") ; 
  h_cutflow.GetXaxis().SetBinLabel(2 ,"AK8 jets") ; 
  h_cutflow.GetXaxis().SetBinLabel(3 ,"p_{T}+#eta") ; 
  h_cutflow.GetXaxis().SetBinLabel(4 ,"#Delta#Eta(JJ)") ; 
  h_cutflow.GetXaxis().SetBinLabel(5 ,"#tau_{21}") ; 
  h_cutflow.GetXaxis().SetBinLabel(6 ,"M(J)") ; 
  h_cutflow.GetXaxis().SetBinLabel(7 ,"VBF") ; 
  h_cutflow.GetXaxis().SetBinLabel(8 ,"> 1 Subjet b") ; 
  h_cutflow.GetXaxis().SetBinLabel(9 ,"> 2 Subjet b") ; 
  h_cutflow.GetXaxis().SetBinLabel(10,"> 3 Subjet b") ; 
  
  fnames = [line.strip() for line in open(opt.files, 'r')]
  
  try: doqcdmaps = bool(sys.argv[2])
  except: doqcdmaps = False
  
  ievt = 0
  for fname in fnames:
    if opt.maxEvts > 0 and ievt > opt.maxEvts: break
    if ievt%100 == 0: print " Processing evt %i" % ievt
  
    print 'Opening file %s' % fname
    f = ROOT.TFile.Open(fname)
    print f.ls()
  
    tree = f.Get("ana/anatree")
    entries = tree.GetEntriesFast()
  
    for event in tree:

      if opt.maxEvts > 0 and ievt > opt.maxEvts: break
      if ievt%100 == 0: print " Processing evt %i" % ievt
                                   
      ievt += 1
  
      gen_momid = event.GenParticles_mom0pid
      gen_pt = event.GenParticles_genpt
      gen_eta = event.GenParticles_genpt
      gen_id = event.GenParticles_genpid
      for i in range(len(gen_pt)):
        if gen_id[i] == 25: 
          h_genH_pt.Fill(gen_pt[i])
          h_genH_eta.Fill(gen_eta[i])

      pts             = event.AK8JetsPuppi_pt
  
      nak8 = len(pts)
  
      h_cutflow.Fill(1)
  
      ### Selecting at least two AK8 jets:
      if nak8 >= opt.nak8Min:
        h_cutflow.Fill(2)
      else: continue
  
      etas   = event.AK8JetsPuppi_eta
  
      ptsel  = pts[0] > opt.ptak8_0_Min and pts[1] > opt.ptak8_1_Min
      etasel = abs(etas[0]) < opt.etaak8_0_Max and abs(etas[1]) < opt.etaak8_1_Max
  
      if ptsel and etasel: 
        h_cutflow.Fill(3)
      else: continue
  
      detasel = abs(etas[0] - etas[1]) < opt.detaak8Max
      if detasel:
        h_cutflow.Fill(4)
      else: continue
  
      tau1s           = event.AK8JetsPuppi_tau1Puppi
      tau2s           = event.AK8JetsPuppi_tau2Puppi
  
      tau21sel = tau2s[0]/tau1s[0] < opt.t21_0_Max and tau2s[1]/tau1s[1] < opt.t21_1_Max
      if tau21sel:
        h_cutflow.Fill(5)
      else: continue 
  
      sd_masses       = event.AK8JetsPuppi_softDropMassPuppi 
  
      npv =          event.npv
      h2_msd0_npv.Fill(npv, sd_masses[0])
      h2_msd1_npv.Fill(npv, sd_masses[1])
  
      msdsel     = opt.msd_0_Min < sd_masses[0] < opt.msd_0_Max and opt.msd_1_Min < sd_masses[1] < opt.msd_1_Max
      if msdsel:
        h_cutflow.Fill(6)
      else: continue 
  
      #### Store Higgs cand p4 for future use

      phis            = event.AK8JetsPuppi_phi
      masses          = event.AK8JetsPuppi_mass
  
      p4_higgses= []
      p4_ak80 = ROOT.TLorentzVector()
      p4_ak81 = ROOT.TLorentzVector()
      p4_ak80.SetPtEtaPhiM(pts[0], etas[0], phis[0], masses[0])
      p4_ak81.SetPtEtaPhiM(pts[1], etas[1], phis[1], masses[1])
      p4_higgses.append(p4_ak80)
      p4_higgses.append(p4_ak81)

      #### Make subjet b-tag eff. maps (needed for QCD bkg estimation)
  
      sj0_pts         = event.AK8JetsPuppi_sj0pt
      sj1_pts         = event.AK8JetsPuppi_sj1pt
      sj0_etas        = event.AK8JetsPuppi_sj0eta
      sj1_etas        = event.AK8JetsPuppi_sj1eta
      sj0_fls         = event.AK8JetsPuppi_sj0partonflavour
      sj1_fls         = event.AK8JetsPuppi_sj1hadronflavour
      deepcsv_sj0s    = event.AK8JetsPuppi_sj0deepcsv
      deepcsv_sj1s    = event.AK8JetsPuppi_sj1deepcsv
  
      for i in [0,1]:
        if abs(sj0_fls[i]) == 5: h2_bFl_sjpt_sjeta.Fill(sj0_pts[i], sj0_etas[i])
        elif abs(sj0_fls[i]) == 4: h2_cFl_sjpt_sjeta.Fill(sj0_pts[i], sj0_etas[i])
        else: h2_lFl_sjpt_sjeta.Fill(sj0_pts[i], sj0_etas[i])
  
        if abs(sj1_fls[i]) == 5: h2_bFl_sjpt_sjeta.Fill(sj1_pts[i], sj1_etas[i])
        elif abs(sj1_fls[i]) == 4: h2_cFl_sjpt_sjeta.Fill(sj1_pts[i], sj1_etas[i])
        else: h2_lFl_sjpt_sjeta.Fill(sj1_pts[i], sj1_etas[i])
  
        if deepcsv_sj0s[i] > opt.deepcsvMin: 
          if abs(sj0_fls[i]) == 5: h2_bFl_sjpt_sjeta_btagged.Fill(sj0_pts[i], sj0_etas[i])
          elif abs(sj0_fls[i]) == 4: h2_cFl_sjpt_sjeta_btagged.Fill(sj0_pts[i], sj0_etas[i])
          else: h2_lFl_sjpt_sjeta_btagged.Fill(sj0_pts[i], sj0_etas[i])
  
        if deepcsv_sj1s[i] > opt.deepcsvMin: 
          if abs(sj1_fls[i]) == 5: h2_bFl_sjpt_sjeta_btagged.Fill(sj1_pts[i], sj1_etas[i])
          elif abs(sj1_fls[i]) == 4: h2_cFl_sjpt_sjeta_btagged.Fill(sj1_pts[i], sj1_etas[i])
          else: h2_lFl_sjpt_sjeta_btagged.Fill(sj1_pts[i], sj1_etas[i])
  
      ### VBF jet sel:
      pts_ak4         = event.AK4JetsCHS_pt
      etas_ak4        = event.AK4JetsCHS_eta
      phis_ak4        = event.AK4JetsCHS_phi
      energies_ak4    = event.AK4JetsCHS_energy
  
      nak4 = len(pts_ak4)
      h_nak8.Fill(nak8)
      h_nak4.Fill(nak4)
  
      ### Select AK4 jets for VBF pair identification
      p4_ak4sel = []
      for i in range(0,nak4):
        if pts_ak4[i] > opt.ptak4Min and abs(etas_ak4[i]) < opt.etaak4Max: 
          p4 = ROOT.TLorentzVector()
          p4.SetPtEtaPhiE(pts_ak4[i], etas_ak4[i], phis_ak4[i], energies_ak4[i])
          hasOverlaoWithH = False
          for p4_higgs in p4_higgses:
            if p4.DeltaR(p4_higgs) < 1.2: 
              hasOverlaoWithH = True
              continue #### Removing AK4 jets overlapping with the Higgs
          if hasOverlaoWithH: continue
          p4_ak4sel.append(p4)
          h2_ak4pt_ak4eta.Fill(pts_ak4[i], etas_ak4[i])

      ### Find VBF jet pairs:
      nvbfpairs = 0
      for i in range(0, len(p4_ak4sel)):
        p40 = p4_ak4sel[i]
        for j in range(i+1, len(p4_ak4sel)):
          p41 = p4_ak4sel[j]
          detavbf = abs(p40.Eta() - p41.Eta())
          mjjvbf = (p40+p41).Mag()
          h_mjjvbf.Fill(mjjvbf)
          h_deltaEta.Fill(detavbf)
          if p40.Eta()*p41.Eta() < 0. and detavbf > opt.detavbfMin and mjjvbf > opt.mjjvbfMin:
            nvbfpairs += 1
            h_vbf0pt.Fill(p40.Pt())
            h_vbf1pt.Fill(p41.Pt())
            h_vbf0eta.Fill(p40.Eta())
            h_vbf1eta.Fill(p41.Eta())

      vbfsel = nvbfpairs > 0
      h_nvbfpairs.Fill(nvbfpairs)

      if vbfsel:
        h_cutflow.Fill(7)
      else: continue

      sjbtag_1 = deepcsv_sj0s[0] > opt.deepcsvMin or deepcsv_sj1s[0] > opt.deepcsvMin  or deepcsv_sj0s[1] > opt.deepcsvMin or deepcsv_sj1s[1] > opt.deepcsvMin
      sjbtag_2 = (deepcsv_sj0s[0] > opt.deepcsvMin or deepcsv_sj1s[0] > opt.deepcsvMin) and (deepcsv_sj0s[1] > opt.deepcsvMin or deepcsv_sj1s[1] > opt.deepcsvMin) 
      sjbtag_3 = ( (deepcsv_sj0s[0] > opt.deepcsvMin and deepcsv_sj1s[0] > opt.deepcsvMin) and (deepcsv_sj0s[1] > opt.deepcsvMin or deepcsv_sj1s[1] > opt.deepcsvMin) ) or\
          ( (deepcsv_sj0s[0] > opt.deepcsvMin or deepcsv_sj1s[0] > opt.deepcsvMin) and (deepcsv_sj0s[1] > opt.deepcsvMin and deepcsv_sj1s[1] > opt.deepcsvMin) )
      sjbtag_4 = deepcsv_sj0s[0] > opt.deepcsvMin and deepcsv_sj1s[0] > opt.deepcsvMin  and deepcsv_sj0s[1] > opt.deepcsvMin and deepcsv_sj1s[1] > opt.deepcsvMin 
  
      wt_3b = 1
      wt_4b = 1

      #### Get event weights for 3b and 4b selections for QCD samples
      if 'QCD' in fname:
        if opt.deepcsvMin == 0.1522:
          btagwp = 'WPL'
        elif opt.deepcsvMin == 0.4941:
          btagwp = 'WPM'

        nPU = opt.files.rstrip('.txt').split('_')[-1].lstrip('PU')

        if abs(sj0_fls[0]) == 5: effmap = 'beff_{0}_{1}.root'.format(nPU, btagwp)
        elif abs(sj0_fls[0]) == 4: effmap = 'ceff_{0}_{1}.root'.format(nPU, btagwp)
        else: effmap = 'lighteff_{0}_{1}.root'.format(nPU, btagwp)
        btageff_sj00 = getSJBTagEff(sj0_pts[0], sj0_etas[0], "effs/{}".format(effmap))

        if abs(sj0_fls[1]) == 5: effmap = 'beff_{0}_{1}.root'.format(nPU, btagwp)
        elif abs(sj0_fls[1]) == 4: effmap = 'ceff_{0}_{1}.root'.format(nPU, btagwp)
        else: effmap = 'lighteff_{0}_{1}.root'.format(nPU, btagwp)
        btageff_sj01 = getSJBTagEff(sj0_pts[1], sj0_etas[1], "effs/{}".format(effmap))

        if abs(sj1_fls[0]) == 5: effmap = 'beff_{0}_{1}.root'.format(nPU, btagwp)
        elif abs(sj1_fls[0]) == 4: effmap = 'ceff_{0}_{1}.root'.format(nPU, btagwp)
        else: effmap = 'lighteff_{0}_{1}.root'.format(nPU, btagwp)
        btageff_sj10 = getSJBTagEff(sj1_pts[0], sj1_etas[0], "effs/{}".format(effmap))

        if abs(sj1_fls[1]) == 5: effmap = 'beff_{0}_{1}.root'.format(nPU, btagwp)
        elif abs(sj1_fls[1]) == 4: effmap = 'ceff_{0}_{1}.root'.format(nPU, btagwp)
        else: effmap = 'lighteff_{0}_{1}.root'.format(nPU, btagwp)
        btageff_sj11 = getSJBTagEff(sj1_pts[1], sj1_etas[1], "effs/{}".format(effmap))

        #print 'btageff {4} = {0} {5} = {1} {6} = {2} {7} = {3}'.format(btageff_sj00, btageff_sj01, btageff_sj10, btageff_sj11,\
        #    sj0_fls[0], sj0_fls[1], sj1_fls[0], sj1_fls[1])

        wt_3b = ( btageff_sj00 * btageff_sj01 * btageff_sj10 * (1 - btageff_sj11) ) +\
            ( btageff_sj00 * btageff_sj01 * (1 - btageff_sj10) * btageff_sj11 ) + \
            ( btageff_sj00 * (1- btageff_sj01) * btageff_sj10 * btageff_sj11 ) + \
            ( (1 - btageff_sj00) * btageff_sj01 * btageff_sj10 * btageff_sj11 )
        wt_4b = btageff_sj00 * btageff_sj01 * btageff_sj10 * btageff_sj11

        #print 'wt_3b = {0} wt_4b = {1}'.format(wt_3b, wt_4b)
  
      if sjbtag_2:
        h_cutflow.Fill(8)
        if sjbtag_3:
          h_cutflow.Fill(9)
          if sjbtag_4:
            h_cutflow.Fill(10)
  
      mjj = (p4_ak80 + p4_ak81).Mag()
      if sjbtag_3: h_mjj_3b.Fill(mjj, wt_3b)
      if sjbtag_4: h_mjj_4b.Fill(mjj, wt_4b)
  
  fout.cd()
  
  h_cutflow_eff = h_cutflow.Clone("h_cutflow_eff")
  h_cutflow_eff.SetTitle(";;Efficiency;")
  
  h_cutflow_eff.Scale(1./h_cutflow.GetBinContent(1))
  
  for i in range(1,h_cutflow_eff.GetNbinsX()+1):
    print h_cutflow_eff.GetXaxis().GetBinLabel(i), h_cutflow_eff.GetBinContent(i) 
  
  fout.Write()
  fout.Close()

if __name__ == "__main__":
  main()
