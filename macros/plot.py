#!/usr/bin/env python

import os, sys, imp, copy, ROOT
import numpy as np

'''
The script looks for the following input files in the current dir:
  VBF_M1500_W01_PU0.root
  VBF_M3000_W01_PU0.root
  QCD_Mdijet-1000toInf_PU0.rooto

You may also have the same set of files with PU=200:
  VBF_M1500_W01_PU200.root
  VBF_M3000_W01_PU200.root
  QCD_Mdijet-1000toInf_PU200.root
'''

helper   = imp.load_source('fix'     , 'help.py')
tdrstyle = imp.load_source('tdrstyle', 'tdrstyle.py')
CMS_lumi = imp.load_source('CMS_lumi', 'CMS_lumi.py') 

ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetOptTitle(0) 
ROOT.gStyle.SetOptStat(0000) 
ROOT.gStyle.SetOptFit(0111) 
ROOT.gStyle.SetErrorX(0.0001);

xsecs={
    'QCD'   : 99.1990,
    'TTJets': 864.5,
    'BG1500': 0.001,
    'BG2000': 0.001,
    'BG3000': 0.001,
    }

nEvts={
    0: {
      'QCD':    4098542, 
      'TTJets': 4979816,
      'BG1500': 80200,
      'BG2000': 100000,
      'BG3000': 91351,
      },
    200: {
      'QCD':    3802314,
      'TTJets': 2874776,
      'BG1500': 27720,
      'BG2000': 81850,
      'BG3000': 87507,
      }
    }

lumi=3000000.

def signalEff():

  hframe = ROOT.TH1D("hframe",";;Efficiency;" ,10 ,0.5 ,10.5 )
  hframe.GetXaxis().SetBinLabel(1 ,"All evts") ; 
  hframe.GetXaxis().SetBinLabel(2 ,"AK8 jets") ; 
  hframe.GetXaxis().SetBinLabel(3 ,"p_{T}+#eta") ; 
  hframe.GetXaxis().SetBinLabel(4 ,"#Delta#Eta(JJ)") ; 
  hframe.GetXaxis().SetBinLabel(5 ,"#tau_{21}") ; 
  hframe.GetXaxis().SetBinLabel(6 ,"M(J)") ; 
  hframe.GetXaxis().SetBinLabel(7 ,"> 1 Subjet b") ; 
  hframe.GetXaxis().SetBinLabel(8 ,"> 2 Subjet b") ; 
  hframe.GetXaxis().SetBinLabel(9 ,"> 3 Subjet b") ; 
  hframe.GetXaxis().SetBinLabel(10,"VBF") ;  
  hframe.SetMaximum(25.001)
  hframe.SetMinimum(0.0001)

  c = ROOT.TCanvas('c_sigEff', '', 800, 600)
  c.cd()
  c.SetLogy(1)

  hframe.Draw()
  c.SetSelected(hframe)
  c.Update()

  leg = ROOT.TLegend(0.50,0.60,0.88,0.75,'','brNDC')
  leg.SetBorderSize(0)
  leg.SetFillColor(0)
  leg.SetTextSize(0.030)
  leg.SetMargin(0.2)  
  leg.SetNColumns(2)
  leg.SetColumnSeparation(0.05)
  leg.SetEntrySeparation(0.05)

  masses = [1500, 3000]
  pus = [0, 200]
  for m in masses:
    for pu in pus:
      f = ROOT.TFile.Open('VBF_M%i_W01_PU%i.root' % (m, pu), 'read')
      h = f.Get('h_cutflow')
      h_cutflow = copy.deepcopy(h.Clone('h_cutflow_M%i_PU%i' % (m, pu)))
      h_cutflow.SetLineColor(600+(m/100))
      h_cutflow.SetLineWidth(2)
      h_cutflow.SetLineStyle(1 + pus.index(pu))
      h_cutflow.Draw('histsame')
      c.SetSelected(h_cutflow)
      leg.AddEntry(h_cutflow, "BG%i PU=%i" % (m, pu), 'lp')
      c.Update()

  leg.Draw()

  c.RedrawAxis()
  c.Update()

  CMS_lumi.lumi_14TeV = ""
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Simulation Preliminary"
        
  iPos = 33
  if( iPos==0 ): CMS_lumi.relPosX = 0.13
       
  CMS_lumi.CMS_lumi(c, 5, iPos)
  c.Update() 
 
  c.SaveAs('%s.pdf' % c.GetName())
  c.SaveAs('%s.png' % c.GetName())

def plotStacked(hists, pu, xtitle, ytitle, xlow, xhigh, rebin, logy):

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
  #fqcd = ROOT.TFile.Open('QCD_Mdijet-1000toInf_PU%i.root' % pu)
  #fqcd = ROOT.TFile.Open('/afs/cern.ch/user/l/lata/public/plots/QCD_%iPU.root' % pu)
  fqcd = ROOT.TFile.Open('/afs/cern.ch/work/l/lata/public/FS_root/root_btag_wpm/root_files6/QCD_%iPU.root' % pu)
  for hist in histnames:
    if hqcd.GetName() == '': hqcd = fqcd.Get('h_mjj_vbfsel_scaledHTagEff')
    else: hqcd.Add(fqcd.Get('h_mjj_vbfsel_scaledHTagEff'))
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

  fout = ROOT.TFile('mjj_PU%i.root' % pu, 'recreate')

  msigs = [1500, 2000, 3000]
  hsig = ROOT.TH1D()
  for m in msigs:
    #fsig = ROOT.TFile.Open('/afs/cern.ch/user/l/lata/public/plots/root_files/VBF_M%i_W01_PU%i.root' % (m, pu))
    fsig = ROOT.TFile.Open('/afs/cern.ch/work/l/lata/public/FS_root/root_btag_wpm/root_files6/VBF_M%i_W01_PU%i.root' % (m, pu))
    hs = ROOT.TH1D()
    for h in histnames:
      if hs.GetName() == '': hs = fsig.Get(h)
      else: hs.Add(fsig.Get(h))
    hsig = copy.deepcopy(hs.Clone(hists.replace(',', '_')+'BG%i' % m))
    hsig.Rebin(rebin)
    helper.fix(hsig)
    hsig.Scale(xsecs['BG%s' % str(m)]*lumi/nEvts[pu]['BG%s' % str(m)])
    ymax = max(ymax, hsig.GetMaximum())
    hsig.SetName("h_mjj_BG%i" % m)
    hsig.SetLineStyle(1+msigs.index(m))
    hsig.SetLineColor(600+(m/100))
    hsig.SetLineWidth(3)
    hsig.Draw('histsame')
    c0.SetSelected(hsig)
    leg.AddEntry(hsig, 'BG%i' % m, 'lf')
    c0.Update()
    print "Nsig %s = %f" % (hsig.GetName(),hsig.Integral())
    fout.cd()
    hsig.Write()

  hqcd.SetName('h_mjj_QCD')
  hqcd.SetMaximum(ymax* 1.3*(100*logy+1))

  fout.cd()
  hqcd.Write()

  h_mjj_data_obs = hqcd.Clone('h_mjj_data_obs')
  h_mjj_data_obs.Write()

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

  print "Nqcd = %f" % hqcd.Integral()

  fout.Close()

#signalEff()

#plotStacked('h_mjj'                       ,   200, 'm_{JJ} [GeV]', 'Events', 1000., 4000., 5, 1)
#plotStacked('h_mjj'                       ,     0, 'm_{JJ} [GeV]', 'Events', 1000., 4000., 5, 1)

#plotStacked('h_mjj'                       ,   0, 'm_{JJ} [GeV]', 'Events', 1000., 4000., 5, 1)
#plotStacked('h_nak8'                      ,   0, 'AK8 jet multiplicity', 'Events', 0., 20, 1, 1)
#plotStacked('h_nak4'                      ,   0, 'AK4 jet multiplicity', 'Events', 0., 20, 1, 1)
#plotStacked('h_ak80pt,h_ak81pt'           ,   0, 'p_{T} (leading two A8 jets) [GeV]', 'Events', 0., 3000., 5, 1)
#plotStacked('h_ak80eta,h_ak81eta'         ,   0, '#eta (leading two A8 jets)', 'Events', -3., 3., 5, 1)
#plotStacked('h_ak80_t2byt1,h_ak81_t2byt1' ,   0, '#tau_{21} (leading two A8 jets)', 'Events', 0., 1., 5, 1)
#plotStacked('h_sj0_deepcsv,h_sj1_deepcsv' ,   0, 'DeepCSV (leading two A8 jets)', 'Events', 0., 1., 5, 1)
#plotStacked('h_vbf0pt,h_vbf0pt'           ,   0, 'p_{T} (VBF jets) [GeV]', 'Events', 0., 1000., 5, 1)
#plotStacked('h_mjjvbf'                    ,   0, 'm(jj) (VBF jets) [GeV]', 'Events', 0., 2000., 5, 1)
#plotStacked('h_deltaEta'                  ,   0, '#Delta#eta(jj) (VBF jets) [GeV]', 'Events', 0., 5., 1, 1)
#
#plotStacked('h_mjj'                       , 200, 'm_{JJ} [GeV]', 'Events', 1000., 4000., 5, 1)
#plotStacked('h_nak8'                      , 200, 'AK8 jet multiplicity', 'Events', 0., 20, 1, 1)
#plotStacked('h_nak4'                      , 200, 'AK4 jet multiplicity', 'Events', 0., 200, 1, 1)
#plotStacked('h_ak80pt,h_ak81pt'           , 200, 'p_{T} (leading two A8 jets) [GeV]', 'Events', 0., 3000., 5, 1)
#plotStacked('h_ak80eta,h_ak81eta'         , 200, '#eta (leading two A8 jets)', 'Events', -3., 3., 5, 1)
#plotStacked('h_ak80_t2byt1,h_ak81_t2byt1' , 200, '#tau_{21} (leading two A8 jets)', 'Events', 0., 1., 5, 1)
#plotStacked('h_sj0_deepcsv,h_sj1_deepcsv' , 200, 'DeepCSV (leading two A8 jets)', 'Events', 0., 1., 5, 1)
#plotStacked('h_vbf0pt,h_vbf0pt'           , 200, 'p_{T} (VBF jets) [GeV]', 'Events', 0., 1000., 5, 1)
#plotStacked('h_mjjvbf'                    , 200, 'm(jj) (VBF jets) [GeV]', 'Events', 0., 2000., 5, 1)
#plotStacked('h_deltaEta'                  , 200, '#Delta#eta(jj) (VBF jets) [GeV]', 'Events', 0., 5., 1, 1)

def htagEff(fname):

  f = ROOT.TFile.Open(fname)
  hd = f.Get('h2_ak8pt_ak8eta')
  hn = f.Get('h2_ak8pt_ak8eta_htagged')

  ptbins = [300., 500., 1000., 3000.]
  etabins = [0., 0.8, 2.4]
  hden = ROOT.TH2D('hden', '', len(ptbins)-1, np.asarray(ptbins, 'd'), len(etabins)-1, np.asarray(etabins, 'd'))
  hnum = ROOT.TH2D('hnum', '', len(ptbins)-1, np.asarray(ptbins, 'd'), len(etabins)-1, np.asarray(etabins, 'd'))

  nbinsx = hd.GetNbinsX()
  nbinsy = hd.GetNbinsY()

  for i in range(0, nbinsx+1):
    for j in range(0, nbinsy+1):
      pt = hd.GetXaxis().GetBinCenter(i)
      eta = abs(hd.GetYaxis().GetBinCenter(j))
      d = hd.GetBinContent(i, j)
      n = hn.GetBinContent(i, j)
      hden.Fill(pt, eta, d)
      hnum.Fill(pt, eta, n)

  heff = hnum.Clone('heff')
  heff.Divide(hden)

  for i in range(1, heff.GetNbinsX()+1):
    for j in range(1, heff.GetNbinsY()+1):
      print "pt %f eta %f eff %f" % (heff.GetXaxis().GetBinCenter(i), heff.GetYaxis().GetBinCenter(j), heff.GetBinContent(i, j))

  ceff = ROOT.TCanvas('ceff_htag', '', 800, 600)
  ceff.cd()
  heff.Draw('colz')
  ceff.SaveAs(ceff.GetName()+'.pdf')

  fout = ROOT.TFile('heff.root', 'recreate')
  fout.cd()
  hnum.Write()
  hden.Write()
  heff.Write()
  fout.Close()

  return heff

def msd(fin):
  f = ROOT.TFile.Open(fin, "read")

  h2_msd0_npv = f.Get("h2_msd0_npv")
  h2_msd1_npv = f.Get("h2_msd1_npv")

  h2_msd0_npv_pfx = h2_msd0_npv.ProfileX()
  h2_msd1_npv_pfx = h2_msd1_npv.ProfileX()

  h2_msd0_npv_pfx.SetMarkerStyle(20)
  h2_msd1_npv_pfx.SetMarkerStyle(20)

  h2_msd0_npv.GetZaxis().SetTitle("Events/ bin")
  h2_msd1_npv.GetZaxis().SetTitle("Events/ bin")

  c0 = ROOT.TCanvas("c_msd0_npv", "", 800, 600)
  c0.cd()
  c0.SetRightMargin(0.15)
  h2_msd0_npv.Draw("colz")
  h2_msd0_npv_pfx.Draw("same")
  c0.SaveAs(c0.GetName()+".pdf")

  c1 = ROOT.TCanvas("c_msd1_npv", "", 800, 600)
  c1.cd()
  c1.SetRightMargin(0.15)
  h2_msd1_npv.Draw("colz")
  h2_msd1_npv_pfx.Draw("same")
  c1.SaveAs(c1.GetName()+".pdf")

#msd("VBF_M1500_W01_PU200.root")
#msd("VBF_M3000_W01_PU200.root")

def plotCompare(fins, hname, labels):
  
  hframe = ROOT.TH1D("hframe",";N(VBF pairs); A.U.;" ,201  ,-0.5  ,200.5)

  c = ROOT.TCanvas("c_%s" % hname, "", 800, 600)
  c.cd()
  c.SetLogy()

  hframe.Draw()
  c.SetSelected(hframe)
  c.Modified()
  c.Update()

  leg = ROOT.TLegend(0.50,0.60,0.88,0.75,'','brNDC')
  leg.SetBorderSize(0)
  leg.SetFillColor(0)
  leg.SetTextSize(0.030)
  leg.SetMargin(0.2)  
  leg.SetNColumns(2)
  leg.SetColumnSeparation(0.05)
  leg.SetEntrySeparation(0.05)
  leg.SetHeader("Signal: M=3000 GeV")
  
  hmax = 2
  i = 1
  for fin in fins:
    f = ROOT.TFile.Open(fin, "read")
    label = labels[fins.index(fin)]
    hist = f.Get(hname)
    h = copy.deepcopy(hist)
    h.Scale(1./h.Integral())

    if h.GetMaximum() > hmax: hmax = h.GetMaximum()
    hframe.SetMaximum(1.2* hmax)

    h.SetName("%s_label" % hname)
    h.Draw("histsame")
    h.SetLineWidth(2)
    h.SetLineColor(i)

    c.SetSelected(h)
    leg.AddEntry(h, label, 'l')

    i += 1

  leg.Draw()

  c.RedrawAxis()
  c.Update()

  c.SaveAs('%s.pdf' % c.GetName())
  c.SaveAs('%s.png' % c.GetName())

fins=['VBF_M3000_W01_PU200_vbfpairs.root', 'VBF_M3000_W01_PU0_vbfpairs.root']
labels = ['PU200', 'PU0']

plotCompare(fins, "h_nvbfpairs", labels)

#htagEff('/afs/cern.ch/user/l/lata/public/plots/QCD_0PU.root')
