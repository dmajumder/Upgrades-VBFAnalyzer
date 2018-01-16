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

files  = sys.argv[1]

fout = ROOT.TFile(files.rstrip().replace('txt', 'root'), 'RECREATE')
fout.cd()

h2_ak8pt_ak8eta              = ROOT.TH2D("h2_ak8pt_ak8eta"              ,";p_{T} (AK8) [GeV]; #eta (AK8);;", 150, 0., 3000, 50, -5, 5)
h2_ak8pt_ak8eta_htagged      = ROOT.TH2D("h2_ak8pt_ak8eta_htagged"      ,";p_{T} (AK8) [GeV]; #eta (AK8);;", 150, 0., 3000, 50, -5, 5)

h2_ak4pt_ak4eta              = ROOT.TH2D("h2_ak4pt_ak4eta"              ,";p_{T} (AK4) [GeV]; #eta (AK4);;", 150, 0., 3000, 50, -5, 5)
h2_ak4pt_ak4genjetpt         = ROOT.TH2D("h2_ak4pt_ak4genjetpt"         ,";p_{T} (AK4 jets) [GeV]; p_{T} (AK4 genjets) [GeV];Events;" ,300,0.,3000,300,0.,3000)

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

h_mjj_vbfsel                 = ROOT.TH1D("h_mjj_vbfsel"                 ,";M(jj) [GeV]; Events;"         ,400  ,500.   ,4500 )
h_mjj_vbfsel_scaledHTagEff   = ROOT.TH1D("h_mjj_vbfsel_scaledHTagEff"   ,";M(jj) [GeV]; Events;"         ,400  ,500.   ,4500 )
h_mjj_novbf_nosjbtag         = ROOT.TH1D("h_mjj_novbf_nosjbtag"         ,";M(jj) [GeV]; Events;"         ,400  ,500.   ,4500 )
h_mjj_novbf_2sjbtag          = ROOT.TH1D("h_mjj_novbf_2sjbtag"          ,";M(jj) [GeV]; Events;"         ,400  ,500.   ,4500 )
h_mjj                        = ROOT.TH1D("h_mjj"                        ,";M(jj) [GeV]; Events;"         ,400  ,500.   ,4500 )

h_cutflow                    = ROOT.TH1D("h_cutflow"                    ,";;Efficiency;"                 ,10   ,0.5    ,10.5 )

h_cutflow.GetXaxis().SetBinLabel(1 ,"All evts") ; 
h_cutflow.GetXaxis().SetBinLabel(2 ,"AK8 jets") ; 
h_cutflow.GetXaxis().SetBinLabel(3 ,"p_{T}+#eta") ; 
h_cutflow.GetXaxis().SetBinLabel(4 ,"#Delta#Eta(JJ)") ; 
h_cutflow.GetXaxis().SetBinLabel(5 ,"#tau_{21}") ; 
h_cutflow.GetXaxis().SetBinLabel(6 ,"M(J)") ; 
h_cutflow.GetXaxis().SetBinLabel(7 ,"> 1 Subjet b") ; 
h_cutflow.GetXaxis().SetBinLabel(8 ,"> 2 Subjet b") ; 
h_cutflow.GetXaxis().SetBinLabel(9 ,"> 3 Subjet b") ; 
h_cutflow.GetXaxis().SetBinLabel(10,"VBF") ; 

fnames = [line.strip() for line in open(files, 'r')]

try: maxEvts = int(sys.argv[2])
except:  maxEvts = -1

ievt = 0
for fname in fnames:
  if maxEvts > 0 and ievt > maxEvts: break
  if ievt%100 == 0: print " Processing evt %i" % ievt

  print 'Opening file %s' % fname
  f = ROOT.TFile.Open(fname)
  print f.ls()

  tree = f.Get("ana/anatree")
  entries = tree.GetEntriesFast()

  for event in tree:

    if maxEvts > 0 and ievt > maxEvts: break
    if ievt%100 == 0: print " Processing evt %i" % ievt

    pts             = event.AK8JetsPuppi_pt
    etas            = event.AK8JetsPuppi_eta
    phis            = event.AK8JetsPuppi_phi
    masses          = event.AK8JetsPuppi_mass
    tau1s           = event.AK8JetsPuppi_tau1Puppi
    tau2s           = event.AK8JetsPuppi_tau2Puppi
    sd_masses       = event.AK8JetsPuppi_softDropMassPuppi 

    pts_ak4         = event.AK4JetsCHS_pt
    pts_ak4gen      = event.AK4JetsCHS_genjetpt
    etas_ak4        = event.AK4JetsCHS_eta
    phis_ak4        = event.AK4JetsCHS_phi
    energies_ak4    = event.AK4JetsCHS_energy

    sj0_pts         = event.AK8JetsPuppi_sj0pt
    sj1_pts         = event.AK8JetsPuppi_sj1pt
    csvv2_sj0s      = event.AK8JetsPuppi_sj0csvv2
    csvv2_sj1s      = event.AK8JetsPuppi_sj1csvv2
    deepcsv_sj0s    = event.AK8JetsPuppi_sj0deepcsv
    deepcsv_sj1s    = event.AK8JetsPuppi_sj1deepcsv

    nak8 = len(pts)
    nak4 = len(pts_ak4)

    for i in range(0, len(pts_ak4gen)):
      h2_ak4pt_ak4genjetpt.Fill(pts_ak4[i], pts_ak4gen[i])

    h_cutflow.Fill(1)

    ### Selecting at least two AK8 jets with two subjets, and at least two AK4 jets per event:
    if nak8 < 2 or nak4 < 2 or len(sj0_pts) < 2 or len(sj1_pts) < 2: continue

    h_nak8.Fill(nak8)
    h_nak4.Fill(nak4)

    deepcsvl = 0.2219 
    deepcsvm = 0.6324 

    ### Higgs jet sel:

    ptsel      = pts[0] > 300 and pts[1] > 300
    etasel     = abs(etas[0]) < 3 and abs(etas[1]) < 3 
    detasel    = abs(etas[0] - etas[1]) < 1.0
    tau21sel   = tau2s[0]/tau1s[0] < 0.6 and tau2s[1]/tau1s[1] < 0.6
    msdsel     = 80 < sd_masses[0] < 160 and 60 < sd_masses[1] < 140

    sjbtag_1 = deepcsv_sj0s[0] > deepcsvl or deepcsv_sj1s[0] > deepcsvl  or deepcsv_sj0s[1] > deepcsvl or deepcsv_sj1s[1] > deepcsvl
    sjbtag_2 = (deepcsv_sj0s[0] > deepcsvl or deepcsv_sj1s[0] > deepcsvl) and (deepcsv_sj0s[1] > deepcsvl or deepcsv_sj1s[1] > deepcsvl) 
    sjbtag_3 = ( (deepcsv_sj0s[0] > deepcsvl and deepcsv_sj1s[0] > deepcsvl) and (deepcsv_sj0s[1] > deepcsvl or deepcsv_sj1s[1] > deepcsvl) ) or\
        ( (deepcsv_sj0s[0] > deepcsvl or deepcsv_sj1s[0] > deepcsvl) and (deepcsv_sj0s[1] > deepcsvl and deepcsv_sj1s[1] > deepcsvl) )
    sjbtag_4 = deepcsv_sj0s[0] > deepcsvl and deepcsv_sj1s[0] > deepcsvl  and deepcsv_sj0s[1] > deepcsvl and deepcsv_sj1s[1] > deepcsvl 

    hjetssel   = ptsel and etasel and msdsel and tau21sel 

    ### Select AK4 jets for VBF pair identification
    p4_ak4sel = []
    for i in range(0,nak4):
      if pts_ak4[i] > 50. and abs(etas_ak4[i]) < 5.: 
        p4 = ROOT.TLorentzVector()
        p4.SetPtEtaPhiE(pts_ak4[i], etas_ak4[i], phis_ak4[i], energies_ak4[i])
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
        if detavbf > 4. and mjjvbf > 300.:
          nvbfpairs += 1
        ### Fill VBF related quantities
        if hjetssel:
          h_mjjvbf.Fill(mjjvbf)
          h_deltaEta.Fill(detavbf)
          if detavbf > 4. and mjjvbf > 300.:
          h_vbf0pt.Fill(p40.Pt())
          h_vbf1pt.Fill(p41.Pt())
          h_vbf0eta.Fill(p40.Eta())
          h_vbf1eta.Fill(p41.Eta())
    ### VBF jet sel:
    vbfsel = nvbfpairs > 0

    h_cutflow.Fill(2)
    if ptsel and etasel: 
      h_cutflow.Fill(3)
      if detasel:
        h_cutflow.Fill(4)
        if tau21sel:
          h_cutflow.Fill(5)
          if msdsel:
            h_cutflow.Fill(6)
            if sjbtag_2:
              h_cutflow.Fill(7)
              if sjbtag_3:
                h_cutflow.Fill(8)
                if sjbtag_4:
                  h_cutflow.Fill(9)
              if vbfsel:
                h_cutflow.Fill(10)

    h_nvbfpairs.Fill(nvbfpairs)

    h2_ak8pt_ak8eta.Fill(pts[0], etas[0])
    h2_ak8pt_ak8eta.Fill(pts[1], etas[1])
   
    ### Jet 1 passing Higgs tagging:
    if 80 < sd_masses[0] < 160 and tau2s[0]/tau1s[0] < 0.6 and deepcsv_sj0s[0] > deepcsvl and deepcsv_sj1s[0] > deepcsvl:
      h2_ak8pt_ak8eta_htagged.Fill(pts[0], etas[0])
    ### Jet 2 passing Higgs tagging:
    if 80 < sd_masses[1] < 160 and tau2s[1]/tau1s[1] < 0.6 and deepcsv_sj0s[1] > deepcsvl and deepcsv_sj1s[1] > deepcsvl:
      h2_ak8pt_ak8eta_htagged.Fill(pts[1], etas[1])

    ### Fill Higgs jet quantities after VBF selection:
    p4_ak80 = ROOT.TLorentzVector()
    p4_ak81 = ROOT.TLorentzVector()
    p4_ak80.SetPtEtaPhiM(pts[0], etas[0], phis[0], masses[0])
    p4_ak81.SetPtEtaPhiM(pts[1], etas[1], phis[1], masses[1])
    mjj = (p4_ak80 + p4_ak81).Mag()

    if ptsel and etasel and msdsel and tau21sel:
      h_mjj_novbf_nosjbtag.Fill(mjj)

    if vbfsel:
      h_mjj_vbfsel.Fill(mjj)
      hjet1eff = getHTagEff(pts[0], etas[0])
      hjet2eff = getHTagEff(pts[1], etas[1])
      h_mjj_vbfsel_scaledHTagEff.Fill(mjj, hjet1eff*hjet2eff)

      if etasel and msdsel and tau21sel and sjbtagsel:
        h_ak80pt.Fill(pts[0])
        h_ak81pt.Fill(pts[1])

      if ptsel and msdsel and tau21sel and sjbtagsel:
        h_ak80eta.Fill(etas[0])
        h_ak81eta.Fill(etas[1])

      if ptsel and etasel and tau21sel and sjbtagsel:
        h_sdmass_ak80.Fill(sd_masses[0])
        h_sdmass_ak81.Fill(sd_masses[1])

      if ptsel and etasel and msdsel and sjbtagsel:
        h_ak80_tau2_tau1.Fill(tau2s[0]/tau1s[0])
        h_ak81_tau2_tau1.Fill(tau2s[1]/tau1s[1])

      if ptsel and etasel and msdsel and tau21sel:
        h_mjj_novbf_nosjbtag.Fill(mjj)
        h_sj0_pts.Fill(sj0_pts[0]) 
        h_sj0_pts.Fill(sj0_pts[1]) 
        h_sj1_pts.Fill(sj1_pts[0]) 
        h_sj1_pts.Fill(sj1_pts[1]) 
        h_sj0_csvv2.Fill(csvv2_sj0s[0]) 
        h_sj0_csvv2.Fill(csvv2_sj0s[1]) 
        h_sj1_csvv2.Fill(csvv2_sj1s[0]) 
        h_sj1_csvv2.Fill(csvv2_sj1s[1]) 
        h_sj0_deepcsv.Fill(deepcsv_sj0s[0]) 
        h_sj0_deepcsv.Fill(deepcsv_sj0s[1]) 
        h_sj1_deepcsv.Fill(deepcsv_sj1s[0]) 
        h_sj1_deepcsv.Fill(deepcsv_sj1s[1]) 

      if ptsel and etasel and msdsel and tau21sel and sjbtag_2:
        h_mjj_novbf_2sjbtag.Fill(mjj)

    ### Full event selection
    if hjetssel and vbfsel:
      h_mjj.Fill(mjj)
                                 
    ievt += 1

h_cutflow.Scale(1./h_cutflow.GetBinContent(1))

fout.Write()
fout.Close()
