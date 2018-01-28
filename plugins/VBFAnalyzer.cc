// -*- C++ -*-
//
// Package:    FS_ROOT/VBFAnalyzer
// Class:      VBFAnalyzer
// 
/**\class VBFAnalyzer VBFAnalyzer.cc FS_ROOT/VBFAnalyzer/plugins/VBFAnalyzer.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  Lata Panwar
//         Created:  Tue, 24 Oct 2017 18:28:14 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//
// class declaration
//
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/MuonReco/interface/MuonCocktails.h"
#include "Upgrades/VBFAnalyzer/interface/VBFTree.h"

#include "TTree.h"
#include "TFile.h"
#include "TLorentzVector.h"

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

using namespace std;

class VBFAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
  public:
    explicit VBFAnalyzer(const edm::ParameterSet&);
    ~VBFAnalyzer();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    virtual void endJob() override;

    // ----------member data ---------------------------

    edm::EDGetTokenT<edm::View<pat::Jet> >      ak4jetsToken_;
    edm::EDGetTokenT<edm::View<pat::Jet> >      ak8jetsToken_;
    edm::EDGetTokenT<edm::View<pat::Jet> >      subak8jetsToken_;
    edm::EDGetTokenT<reco::VertexCollection >   vtxToken_;
    edm::EDGetTokenT<reco::GenParticleCollection> genparToken_;

    double ak4ptmin_, ak4etamax_, ak8ptmin_, ak8etamax_;

    edm::Service<TFileService> fs_;
    TTree* tree_;

    VBFEventInfoBranches evt_;
    VBFGenParticleInfoBranches gen_;
    VBFJetInfoBranches ak4jets_;
    VBFJetInfoBranches ak8jets_;
};

//
// constants, enums and typedefs
//
// Define some simple structures
//
// static data member definitions
//

//
// constructors and destructor
//
VBFAnalyzer::VBFAnalyzer(const edm::ParameterSet& iConfig):
  ak4jetsToken_   (consumes<edm::View<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jets"))),
  ak8jetsToken_   (consumes<edm::View<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jets_ak8"))),
  subak8jetsToken_(consumes<edm::View<pat::Jet> >(iConfig.getParameter<edm::InputTag>("subjets_ak8"))),
  vtxToken_       (consumes<reco::VertexCollection >(iConfig.getParameter<edm::InputTag>("vertices"))), 
  genparToken_    (consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genparToken"))),
  ak4ptmin_       (iConfig.getParameter<double>("ak4ptmin")),
  ak4etamax_      (iConfig.getParameter<double>("ak4etamax")),
  ak8ptmin_       (iConfig.getParameter<double>("ak8ptmin")),
  ak8etamax_      (iConfig.getParameter<double>("ak8etamax")) 
{
  //now do what ever initialization is needed
  usesResource("TFileService");
}


VBFAnalyzer::~VBFAnalyzer()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
VBFAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   
  gen_.clearTreeVectors();
  ak4jets_.clearTreeVectors();
  ak8jets_.clearTreeVectors();

  edm::Handle<std::vector<reco::GenParticle>> h_genpar;
  iEvent.getByToken(genparToken_, h_genpar);
  for (reco::GenParticle igen : *(h_genpar.product())) {
    if ( igen.isHardProcess() || igen.fromHardProcessFinalState() || igen.fromHardProcessDecayed() 
        || igen.fromHardProcessBeforeFSR() || igen.statusFlags().isLastCopy() ) {

      gen_.genpid    .push_back(igen.pdgId()); 
      gen_.genpt     .push_back(igen.pt()); 
      gen_.geneta    .push_back(igen.eta()); 
      gen_.genphi    .push_back(igen.phi()); 
      gen_.genmass   .push_back(igen.mass()); 
      gen_.gencharge .push_back(igen.charge()); 
      gen_.genstatus .push_back(igen.status()); 
      if (igen.numberOfMothers() > 0 && igen.mother(0) != nullptr) {
        gen_.mom0pt    .push_back(igen.mother(0)->pt()); 
        gen_.mom0eta   .push_back(igen.mother(0)->eta()); 
        gen_.mom0phi   .push_back(igen.mother(0)->phi()); 
        gen_.mom0pid   .push_back(igen.mother(0)->pdgId());
        gen_.mom0status.push_back(igen.mother(0)->status());
      }
      if (igen.numberOfMothers() > 1 && igen.mother(1) != nullptr) {
        gen_.mom1pt    .push_back(igen.mother(1)->pt()); 
        gen_.mom1eta   .push_back(igen.mother(1)->eta()); 
        gen_.mom1phi   .push_back(igen.mother(1)->phi()); 
        gen_.mom1pid   .push_back(igen.mother(1)->pdgId());
        gen_.mom1status.push_back(igen.mother(1)->status());
      }
      if (igen.numberOfDaughters() > 0 && igen.daughter(0) != nullptr) {
        gen_.dau0pt    .push_back(igen.daughter(0)->pt()); 
        gen_.dau0eta   .push_back(igen.daughter(0)->eta()); 
        gen_.dau0phi   .push_back(igen.daughter(0)->phi()); 
        gen_.dau0pid   .push_back(igen.daughter(0)->pdgId());
        gen_.dau0status.push_back(igen.daughter(0)->status());
      }
      if (igen.numberOfDaughters() > 1 && igen.daughter(1) != nullptr) {
        gen_.dau1pt    .push_back(igen.daughter(1)->pt()); 
        gen_.dau1eta   .push_back(igen.daughter(1)->eta()); 
        gen_.dau1phi   .push_back(igen.daughter(1)->phi()); 
        gen_.dau1pid    .push_back(igen.daughter(1)->pdgId());
        gen_.dau1status .push_back(igen.daughter(1)->status());
      }

    }
  }

  edm::Handle<reco::VertexCollection> h_vertices;
  iEvent.getByToken(vtxToken_, h_vertices);
  if (h_vertices->empty()) return; 
  evt_.npv = h_vertices->size(); 

  edm::Handle<edm::View<pat::Jet> > h_ak4jets;
  iEvent.getByToken(ak4jetsToken_, h_ak4jets);
  for (const pat::Jet & j : *h_ak4jets) {
    if (j.pt() < ak4ptmin_ || abs(j.eta()) > ak4etamax_) continue; 
    const reco::GenJet* genjet = j.genJet() ; 
    if (genjet != nullptr) ak4jets_.genjetpt.push_back(j.genJet()->pt())  ;
    else ak4jets_.genjetpt.push_back(-9999)  ;
    ak4jets_.pt           .push_back(j.pt())  ;
    ak4jets_.eta          .push_back(j.eta()) ;
    ak4jets_.phi          .push_back(j.phi()) ;
    ak4jets_.energy       .push_back(j.energy());
    ak4jets_.mass         .push_back(j.mass());
    ak4jets_.partonFlavour.push_back(j.partonFlavour()); 
    ak4jets_.hadronFlavour.push_back(j.hadronFlavour()); 
    ak4jets_.csvv2        .push_back(j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
    ak4jets_.deepcsv      .push_back(j.bDiscriminator("pfDeepCSVJetTags:probb") 
        + j.bDiscriminator("pfDeepCSVJetTags:probbb"));
    ak4jets_.pujetid      .push_back(j.userFloat("pileupJetId:fullDiscriminant")); 
  }

  edm::Handle<edm::View<pat::Jet> > h_ak8jets;
  iEvent.getByToken(ak8jetsToken_, h_ak8jets);
  for (const pat::Jet & j : *h_ak8jets) {
    if (j.pt() < ak8ptmin_ || abs(j.eta()) > ak8etamax_) continue; 
    const reco::GenJet* genjet = j.genJet() ; 
    if (genjet != nullptr) ak8jets_.genjetpt.push_back(j.genJet()->pt())  ;
    else ak8jets_.genjetpt.push_back(-9999)  ;
    ak8jets_.pt               .push_back(j.pt())  ;
    ak8jets_.eta              .push_back(j.eta()) ;
    ak8jets_.phi              .push_back(j.phi()) ;
    ak8jets_.energy           .push_back(j.energy());
    ak8jets_.mass             .push_back(j.mass());
    ak8jets_.ptCHS            .push_back(j.userFloat("ak8PFJetsCHSValueMap:pt"))  ;
    ak8jets_.etaCHS           .push_back(j.userFloat("ak8PFJetsCHSValueMap:eta"))  ;
    ak8jets_.phiCHS           .push_back(j.userFloat("ak8PFJetsCHSValueMap:phi"))  ;
    ak8jets_.massCHS          .push_back(j.userFloat("ak8PFJetsCHSValueMap:mass"))  ;
    ak8jets_.softDropMassCHS  .push_back(j.userFloat("ak8PFJetsCHSValueMap:ak8PFJetsCHSSoftDropMass")) ;  
    ak8jets_.prunedMassCHS    .push_back(j.userFloat("ak8PFJetsCHSValueMap:ak8PFJetsCHSPrunedMass")) ;  
    ak8jets_.tau1CHS          .push_back(j.userFloat("ak8PFJetsCHSValueMap:NjettinessAK8CHSTau1"));
    ak8jets_.tau2CHS          .push_back(j.userFloat("ak8PFJetsCHSValueMap:NjettinessAK8CHSTau2")); 
    ak8jets_.tau3CHS          .push_back(j.userFloat("ak8PFJetsCHSValueMap:NjettinessAK8CHSTau3"));
    ak8jets_.softDropMassPuppi.push_back(j.userFloat("ak8PFJetsPuppiSoftDropMass")) ;  
    ak8jets_.tau1Puppi        .push_back(j.userFloat("NjettinessAK8Puppi:tau1"));
    ak8jets_.tau2Puppi        .push_back(j.userFloat("NjettinessAK8Puppi:tau2")); 
    ak8jets_.tau3Puppi        .push_back(j.userFloat("NjettinessAK8Puppi:tau3"));
    ak8jets_.csvv2            .push_back(j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
    ak8jets_.deepcsv          .push_back(j.bDiscriminator("pfDeepCSVJetTags:probb") 
        + j.bDiscriminator("pfDeepCSVJetTags:probbb"));
    ak8jets_.partonFlavour    .push_back(j.partonFlavour()); 
    ak8jets_.hadronFlavour    .push_back(j.hadronFlavour()); 

    std::vector<edm::Ptr<pat::Jet> > const& sdsubjets = j.subjets("SoftDropPuppi") ;
    if (sdsubjets.size() < 2) continue ;
    ak8jets_.sj0pt           .push_back(sdsubjets.at(0)->pt()) ; 
    ak8jets_.sj1pt           .push_back(sdsubjets.at(1)->pt()) ; 
    ak8jets_.sj0eta          .push_back(sdsubjets.at(0)->eta()) ; 
    ak8jets_.sj1eta          .push_back(sdsubjets.at(1)->eta()) ; 
    ak8jets_.sj0phi          .push_back(sdsubjets.at(0)->phi()) ; 
    ak8jets_.sj1phi          .push_back(sdsubjets.at(1)->phi()) ; 
    ak8jets_.sj0partonFlavour.push_back(sdsubjets.at(0)->partonFlavour()); 
    ak8jets_.sj0hadronFlavour.push_back(sdsubjets.at(0)->hadronFlavour()); 
    ak8jets_.sj1partonFlavour.push_back(sdsubjets.at(1)->partonFlavour()); 
    ak8jets_.sj1hadronFlavour.push_back(sdsubjets.at(1)->hadronFlavour()); 
    ak8jets_.sj0csvv2        .push_back(sdsubjets.at(0)->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
    ak8jets_.sj1csvv2        .push_back(sdsubjets.at(1)->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
    ak8jets_.sj0deepcsv      .push_back(sdsubjets.at(0)->bDiscriminator("pfDeepCSVJetTags:probb") 
        + sdsubjets.at(0)->bDiscriminator("pfDeepCSVJetTags:probbb"));
    ak8jets_.sj1deepcsv      .push_back(sdsubjets.at(1)->bDiscriminator("pfDeepCSVJetTags:probb") 
        + sdsubjets.at(1)->bDiscriminator("pfDeepCSVJetTags:probbb"));
  }

  tree_->Fill();

}
// ------------ method called once each job just before starting event loop  ------------
  void 
VBFAnalyzer::beginJob()
{

  tree_ = fs_->make<TTree>("anatree", "anatree") ; 
  evt_.RegisterTree(tree_, "SelectedEvt") ;
  gen_.RegisterTree(tree_, "GenParticles") ; 
  ak4jets_.RegisterTree(tree_, "AK4JetsCHS") ; 
  ak8jets_.RegisterTree(tree_, "AK8JetsPuppi") ; 

}

// ------------ method called once each job just after ending the event loop  ------------
  void 
VBFAnalyzer::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
VBFAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(VBFAnalyzer);
