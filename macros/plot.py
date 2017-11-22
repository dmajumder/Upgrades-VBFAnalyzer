#!/usr/bin/env python

import os, sys, imp, copy, ROOT

'''
The script looks for the following input files in the current dir:
  VBF_M1500_W01_PU0.root
  VBF_M3000_W01_PU0.root
  QCD_Mdijet-1000toInf_PU0.rooto

You may also have the same set of files with PU=200:
  VBF_M1500_W01_PU200.root
  VBF_M3000_W01_PU200.root
  QCD_Mdijet-1000toInf_PU200.rooto
'''

helper   = imp.load_source('fix'     , 'help.py')
tdrstyle = imp.load_source('tdrstyle', 'tdrstyle.py')
CMS_lumi = imp.load_source('CMS_lumi', 'CMS_lumi.py') 

xsecs={
    'QCD'   : 99.1990,
    'TTJets': 864.5,
    'BG1500': 1.,
    'BG3000': 1.,
    }

nEvts={
    0: {
      'QCD':     4098542, 
      'TTJets':  4979816,
      'BG1500':  80200,
      'BG3000':  91351,
      },
    200: {
      'QCD':    3802314,
      'TTJets': 2874776,
      'BG1500': 27720,
      'BG3000': 87507,
      }
    }

lumi=3000.

def plotStacked(hists, pu, xtitle, ytitle, xlow, xhigh, rebin, logy):

  ROOT.gROOT.SetBatch()
  ROOT.gROOT.SetStyle('Plain')
  ROOT.gStyle.SetOptTitle(0) 
  ROOT.gStyle.SetOptStat(0000) 
  ROOT.gStyle.SetOptFit(0111) 
  ROOT.gStyle.SetErrorX(0.0001);

  histnames = hists.split(',')

  c0 = ROOT.TCanvas('c_compare_%s_%i_Logy%i' % (hists.replace(',','_'), pu, logy),'',800,600)
  c0.cd()
  c0.SetLogy(logy)

  leg = ROOT.TLegend(0.50,0.60,0.88,0.75,'','brNDC')
  leg.SetHeader('PU = %i' % pu)
  leg.SetBorderSize(0)
  leg.SetFillColor(0)
  leg.SetTextSize(0.030)
  leg.SetMargin(0.2)  
  leg.SetNColumns(2)
  leg.SetColumnSeparation(0.05)
  leg.SetEntrySeparation(0.05)

  hqcd = ROOT.TH1D()
  fqcd = ROOT.TFile.Open('/afs/cern.ch/user/l/lata/public/plots/QCD_Mdijet-1000toInf_PU%i.root' % pu)
  for hist in histnames:
    if hqcd.GetName() == '': hqcd = fqcd.Get(hist)
    else: hqcd.Add(fqcd.Get(hist))
  hqcd.Rebin(rebin)
  helper.fix(hqcd)
  hqcd.Scale(xsecs['QCD']*lumi/nEvts[pu]['QCD'])

  hqcd.SetLineColor(14)
  hqcd.SetFillColor(14)
  hqcd.Draw('hist')

  ymax = hqcd.GetMaximum()
  hqcd.GetXaxis().SetRangeUser(xlow,xhigh)
  hqcd.GetXaxis().SetTitle(xtitle)
  hqcd.GetYaxis().SetTitle(ytitle)

  leg.AddEntry(hqcd, 'QCD', 'lf')

  print 'histnames = ', histnames

  msigs = [1500, 3000]
  hsig = ROOT.TH1D()
  for m in msigs:
    fsig = ROOT.TFile.Open('/afs/cern.ch/user/l/lata/public/plots/VBF_M%i_W01_PU%i.root' % (m, pu))
    hs = ROOT.TH1D()
    for h in histnames:
      if hs.GetName() == '': hs = fsig.Get(h)
      else: hs.Add(fsig.Get(h))
    hsig = copy.deepcopy(hs.Clone(hists.replace(',', '_')+'BG%i' % m))
    hsig.Rebin(rebin)
    helper.fix(hsig)
    hsig.Scale(xsecs['BG%s' % str(m)]*lumi/nEvts[pu]['BG%s' % str(m)])
    ymax = max(ymax, hsig.GetMaximum())
    hsig.SetName(hsig.GetName()+"BG%i" % m)
    hsig.SetLineStyle(1+msigs.index(m))
    hsig.SetLineColor(600+(m/100))
    hsig.SetLineWidth(3)
    hsig.Draw('histsame')
    c0.SetSelected(hsig)
    leg.AddEntry(hsig, 'BG%i' % m, 'lf')
    c0.Update()

  hqcd.SetMaximum(ymax* 1.3*(100*logy+1))

  leg.Draw()

  c0.RedrawAxis()
  c0.Update()

  CMS_lumi.lumi_14TeV = ""
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Simulation Preliminary"
        
  iPos = 33
  if( iPos==0 ): CMS_lumi.relPosX = 0.13
       
  CMS_lumi.CMS_lumi(c0, 5, iPos)
  c0.Update() 
 
  c0.SaveAs(c0.GetName()+'.pdf')
  c0.SaveAs(c0.GetName()+'.png')

plotStacked('h_mjj'                       ,   0, 'm_{JJ} [GeV]', 'Events', 1000., 4000., 5, 1)
plotStacked('h_nak8'                      ,   0, 'AK8 jet multiplicity', 'Events', 0., 20, 1, 1)
plotStacked('h_nak4'                      ,   0, 'AK4 jet multiplicity', 'Events', 0., 20, 1, 1)
plotStacked('h_ak80pt,h_ak81pt'           ,   0, 'p_{T} (leading two A8 jets) [GeV]', 'Events', 0., 3000., 5, 1)
plotStacked('h_ak80eta,h_ak81eta'         ,   0, '#eta (leading two A8 jets)', 'Events', -3., 3., 5, 1)
plotStacked('h_ak80_t2byt1,h_ak81_t2byt1' ,   0, '#tau_{21} (leading two A8 jets)', 'Events', 0., 1., 5, 1)
plotStacked('h_sj0_deepcsv,h_sj1_deepcsv' ,   0, 'DeepCSV (leading two A8 jets)', 'Events', 0., 1., 5, 1)
plotStacked('h_vbf0pt,h_vbf0pt'           ,   0, 'p_{T} (VBF jets) [GeV]', 'Events', 0., 1000., 5, 1)
plotStacked('h_mjjvbf'                    ,   0, 'm(jj) (VBF jets) [GeV]', 'Events', 0., 2000., 5, 1)
plotStacked('h_deltaEta'                  ,   0, '#Delta#eta(jj) (VBF jets) [GeV]', 'Events', 0., 5., 1, 1)

plotStacked('h_mjj'                       , 200, 'm_{JJ} [GeV]', 'Events', 1000., 4000., 5, 1)
plotStacked('h_nak8'                      , 200, 'AK8 jet multiplicity', 'Events', 0., 20, 1, 1)
plotStacked('h_nak4'                      , 200, 'AK4 jet multiplicity', 'Events', 0., 200, 1, 1)
plotStacked('h_ak80pt,h_ak81pt'           , 200, 'p_{T} (leading two A8 jets) [GeV]', 'Events', 0., 3000., 5, 1)
plotStacked('h_ak80eta,h_ak81eta'         , 200, '#eta (leading two A8 jets)', 'Events', -3., 3., 5, 1)
plotStacked('h_ak80_t2byt1,h_ak81_t2byt1' , 200, '#tau_{21} (leading two A8 jets)', 'Events', 0., 1., 5, 1)
plotStacked('h_sj0_deepcsv,h_sj1_deepcsv' , 200, 'DeepCSV (leading two A8 jets)', 'Events', 0., 1., 5, 1)
plotStacked('h_vbf0pt,h_vbf0pt'           , 200, 'p_{T} (VBF jets) [GeV]', 'Events', 0., 1000., 5, 1)
plotStacked('h_mjjvbf'                    , 200, 'm(jj) (VBF jets) [GeV]', 'Events', 0., 2000., 5, 1)
plotStacked('h_deltaEta'                  , 200, '#Delta#eta(jj) (VBF jets) [GeV]', 'Events', 0., 5., 1, 1)
