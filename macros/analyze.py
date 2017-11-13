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

fout = ROOT.TFile('fout.root', 'RECREATE')
fout.cd()

h_ak80pt    	= 	ROOT.TH1D("h_ak80pt", ";p_{T} [GeV]; Events;;", 150, 0., 3000)
h_ak81pt	= 	ROOT.TH1D("h_ak81pt", ";p_{T} [GeV]; Events;;", 150, 0., 3000)
h_ak80eta 	= 	ROOT.TH1D("h_ak80eta",";#eta;;", 50 , -5 , 5 )
h_ak81eta 	= 	ROOT.TH1D("h_ak81eta",";#eta;;", 50,  -5 , 5 )
h_ak80_tau2_tau1= 	ROOT.TH1D("h_ak80_t2byt1",";#tau_{2}/#tau_{1};;",  100,   0,  1)
h_sdmass_ak80   =       ROOT.TH1D("h_sdmass_ak80",";softdropped_mass[GeV];;", 100, 0, 200)
h_ak81_tau2_tau1= 	ROOT.TH1D("h_ak81_t2byt1",";#tau_{2}/#tau_{1} ;;",  100,   0,  1)
h_sdmass_ak81   =       ROOT.TH1D("h_sdmass_ak81",";softdropped_mass[GeV];;", 100, 0, 200)
h_deltaEta      =       ROOT.TH1D("h_deltaEta",";#delta#eta of VBF add. jets;;", 20, 0, 10)
h_sbjet0_pt     =	ROOT.TH1D("h_subjet0_pt",";p_{T} of subjet_1;;",100,0,3000)
h_sbjet1_pt     =       ROOT.TH1D("h_subjet1_pt",";p_{T} of subjet_2;;",100,0,3000)
#fin = sys.argv[1]
#f = ROOT.TFile(fin, "READ")
data = [line.strip() for line in open("filenames1.txt", 'r')]
maxEvts = -1
for i in data:
  print i
  f = ROOT.TFile.Open(i)
  print f.ls()

  tree = f.Get("ana/anatree")
  entries = tree.GetEntriesFast()

  ievt = 0
  for event in tree:

   if maxEvts > 0 and ievt > maxEvts: break
   print " Processing evt %i" % ievt

   pts         = event.AK8JetsPuppi_pt
   etas        = event.AK8JetsPuppi_eta
   tau1        = event.AK8JetsPuppi_tau1Puppi
   tau2        = event.AK8JetsPuppi_tau2Puppi
   sd_mass     = event.AK8JetsPuppi_softDropMassPuppi 
   etas_ak4    = event.AK4JetsCHS_eta
   btag_sbjet0 = event.AK8JetsPuppi_sj0csvv2
   btag_sbjet1 = event.AK8JetsPuppi_sj1csvv2
   sbjet0_pt   = event.AK8JetsPuppi_sj0pt
   sbjet1_pt   = event.AK8JetsPuppi_sj1pt

   if (len(pts)-2) >= 0:    
     h_ak80pt.Fill(pts[len(pts)-2])
     h_ak81pt.Fill(pts[len(pts)-1])

### pt selection cuts #####
     if pts[len(pts)-2] > 300 and pts[len(pts)-1] > 300 :
       h_ak80eta.Fill(etas[len(etas)-2])
       h_ak81eta.Fill(etas[len(etas)-1])

### eta selection cut ######
       if abs(etas[len(etas)-2]) < 3 and abs(etas[len(etas)-1]) < 3 :
         h_sdmass_ak81.Fill(sd_mass[len(sd_mass)-1])
         h_sdmass_ak80.Fill(sd_mass[len(sd_mass)-2])

#### SD_Mass cut #######
         if 160 > sd_mass[len(sd_mass)-2] > 80 and 140 > sd_mass[len(sd_mass)-1] > 60 :
           h_ak81_tau2_tau1.Fill(tau2[len(tau2)-1]/tau1[len(tau1)-1])
           h_ak80_tau2_tau1.Fill(tau2[len(tau2)-2]/tau1[len(tau1)-2])

##### cuts for VBF Jets ########
           if (len(etas_ak4))>=2 :
             if abs(etas_ak4[len(etas_ak4)-2]) < 5 and abs(etas_ak4[len(etas_ak4)-1]) < 5 :
                if etas_ak4[len(etas_ak4)-2]*etas_ak4[len(etas_ak4)-1] < 0 :
                  h_deltaEta.Fill(abs(etas_ak4[len(etas_ak4)-2]-etas_ak4[len(etas_ak4)-1]))

####### cuts for subjets ###########
           if (len(sbjet0_pt)) >= 2 and (len(sbjet1_pt)) >= 2:

### b-tagginf for subjets#####
##not woking      if btag_sbjet0[len(sbjet0_pt)-2] > 1.0 and btag_sbjet1[len(sbjet1_pt)-2] > 1.0:
             h_sbjet0_pt.Fill(sbjet0_pt[len(sbjet0_pt)-2])
             print sbjet0_pt[len(sbjet0_pt)-2]
             h_sbjet1_pt.Fill(sbjet1_pt[len(sbjet1_pt)-2])
                             
  
#  genjetpts = event.AK8JetsPuppi_genjetpt

   ievt += 1

fout.Write()
fout.Close()

