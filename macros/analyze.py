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

files  = sys.argv[1]

fout = ROOT.TFile(files.rstrip().replace('txt', 'root'), 'RECREATE')
fout.cd()

h2_ak8pt_ak8eta  = ROOT.TH2D("h2_ak8pt_ak8eta"   , ";p_{T} (AK8) [GeV]; #eta (AK8);;", 150, 0., 3000, 50, -5, 5)

h_mjj            = ROOT.TH1D("h_mjj"             , ";M(jj) [GeV]; Events;"        ,60   ,1000. ,4000 )
h_ak80pt         = ROOT.TH1D("h_ak80pt"          , ";p_{T} [GeV]; Events;;"       ,60   ,1000. ,4000 )
h_ak81pt         = ROOT.TH1D("h_ak81pt"          , ";p_{T} [GeV]; Events;;"       ,150  ,0.    ,3000 )
h_ak80eta        = ROOT.TH1D("h_ak80eta"         ,";#eta;;"                       ,50   ,-5    ,5    )
h_ak81eta        = ROOT.TH1D("h_ak81eta"         ,";#eta;;"                       ,50   ,-5    ,5    )
h_ak80_tau2_tau1 = ROOT.TH1D("h_ak80_t2byt1"     ,";#tau_{2}/#tau_{1};;"          ,100  ,0     , 1   )
h_sdmass_ak80    = ROOT.TH1D("h_sdmass_ak80"     ,";softdropped_mass[GeV];;"      ,100  ,0     ,200  )
h_ak81_tau2_tau1 = ROOT.TH1D("h_ak81_t2byt1"     ,";#tau_{2}/#tau_{1} ;;"         ,100  ,0     , 1   )
h_sdmass_ak81    = ROOT.TH1D("h_sdmass_ak81"     ,";softdropped_mass[GeV];;"      ,100  ,0     ,200  )
h_deltaEta       = ROOT.TH1D("h_deltaEta"        ,";#delta#eta of VBF add. jets;;",20   ,0     ,10   )
h_sj0_pts        = ROOT.TH1D("h_subjet0_pt"      ,";p_{T} of subjet_1;;"          ,100  ,0     ,3000 )
h_sj1_pts        = ROOT.TH1D("h_subjet1_pt"      ,";p_{T} of subjet_2;;"          ,100  ,0     ,3000 )
h_sj0_csvv2      = ROOT.TH1D("h_subjet0_csvv2"   ,";CSVv2 of subjet_1;;"          ,50   ,0.    ,1.   )
h_sj1_csvv2      = ROOT.TH1D("h_subjet1_csvv2"   ,";CSVv2 of subjet_2;;"          ,50   ,0.    ,1.   )
h_sj0_deepcsv    = ROOT.TH1D("h_subjet0_deepcsv" ,";DeepCSV of subjet_1;;"        ,50   ,0.    ,1.   )
h_sj1_deepcsv    = ROOT.TH1D("h_subjet1_deepcsv" ,";DeepCSV of subjet_2;;"        ,50   ,0.    ,1.   )

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
    etas_ak4        = event.AK4JetsCHS_eta

    sj0_pts         = event.AK8JetsPuppi_sj0pt
    sj1_pts         = event.AK8JetsPuppi_sj1pt
    csvv2_sj0s      = event.AK8JetsPuppi_sj0csvv2
    csvv2_sj1s      = event.AK8JetsPuppi_sj1csvv2
    deepcsv_sj0s    = event.AK8JetsPuppi_sj0deepcsv
    deepcsv_sj1s    = event.AK8JetsPuppi_sj1deepcsv

    nak8 = len(pts)

    if nak8 < 2: continue
    if (len(sj0_pts)) < 2 or (len(sj1_pts)) < 2: continue

    h2_ak8pt_ak8eta.Fill(pts[0], etas[0])
    h2_ak8pt_ak8eta.Fill(pts[1], etas[1])

    h_ak80pt.Fill(pts[0])
    h_ak81pt.Fill(pts[1])

### pt selection cuts #####
    if pts[0] > 300 and pts[1] > 300 :
      h_ak80eta.Fill(etas[0])
      h_ak81eta.Fill(etas[0])

### eta selection cut ######
      if abs(etas[0]) < 3 and abs(etas[1]) < 3 :
        h_sdmass_ak80.Fill(sd_masses[0])
        h_sdmass_ak81.Fill(sd_masses[1])

#### SD_Mass cut #######
        if 160 > sd_masses[0] > 80 and 140 > sd_masses[1] > 60 :
          h_ak81_tau2_tau1.Fill(tau2s[0]/tau1s[0])
          h_ak80_tau2_tau1.Fill(tau2s[1]/tau1s[1])

          h_sj0_csvv2.Fill(csvv2_sj0s[0]) 
          h_sj1_csvv2.Fill(csvv2_sj1s[1]) 
          h_sj0_deepcsv.Fill(deepcsv_sj0s[0]) 
          h_sj1_deepcsv.Fill(deepcsv_sj1s[1]) 

##### cuts for VBF Jets ########
          if (len(etas_ak4))>=2 :
            if abs(etas_ak4[0]) < 5 and abs(etas_ak4[1]) < 5 :
               if etas_ak4[0]*etas_ak4[1] < 0 :
                 h_deltaEta.Fill(abs(etas_ak4[0]-etas_ak4[1]))

####### cuts for subjets ###########

### b-tagging of subjets DeepCSVM ##### https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
                 if deepcsv_sj0s[0] > 0.6324 and deepcsv_sj1s[1] > 0.6324:
                   h_sj0_pts.Fill(sj0_pts[0])
                   h_sj1_pts.Fill(sj1_pts[0])

                   p4_ak80 = ROOT.TLorentzVector()
                   p4_ak81 = ROOT.TLorentzVector()
                   p4_ak80.SetPtEtaPhiM(pts[0], etas[0], phis[0], masses[0])
                   p4_ak81.SetPtEtaPhiM(pts[1], etas[1], phis[1], masses[1])
                   mjj = (p4_ak80 + p4_ak81).Mag()

                   h_mjj.Fill(mjj)
                                 
#  genjetpts = event.AK8JetsPuppi_genjetpt

    ievt += 1

fout.Write()
fout.Close()
