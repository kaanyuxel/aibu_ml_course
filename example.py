#!/usr/bin/env python
import ROOT


ROOT.gSystem.Load("libDelphes")

try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass


inputFile = '/Users/koyulmaz/program_files/MG5_aMC_v3_5_3/bin/pp2z2bb/Events/run_01/tag_1_delphes_events.root'
type = 'background'
# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain.Add(inputFile)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Get pointers to branches used in this analysis
branchJet = treeReader.UseBranch("Jet")

# Create root file
myfile = ROOT.TFile(type + '.root', 'RECREATE')
# Define a ntuple with some variables inside of root file
ntuple = ROOT.TNtuple(type, type, "jet1_pt:jet2_pt:jet1_eta:jet2_eta:jet1_phi:jet2_phi:jet1_mass:jet2_mass:m_bb")

# Loop over all events
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)

  # If event contains at least 2 jets
  if branchJet.GetEntries() > 1:
    # Take first jet
    jet1 = branchJet.At(0) # Get First Jet
    jet2 = branchJet.At(1) # Get Second Jet
    v1 = ROOT.Math.PtEtaPhiMVector(jet1.PT, jet1.Eta, jet1.Phi, jet1.Mass) #Lorentz Vector of First Jet
    v2 = ROOT.Math.PtEtaPhiMVector(jet2.PT, jet2.Eta, jet2.Phi, jet2.Mass) #Lorentz Vector of Second Jet
    m_bb = (v1 + v2).M() # Reconstructed Mass
    if jet1.BTag == 1 and jet2.BTag == 1: # Write data if both are btagged jet
      ntuple.Fill(
        jet1.PT,
        jet2.PT,
        jet1.Eta,
        jet2.Eta,
        jet1.Phi,
        jet2.Phi, 
        jet1.Mass,
        jet2.Mass,     
        m_bb
      )

ntuple.Write() # Write the to file 
myfile.Write("",ROOT.TObject.kWriteDelete) # Close the file saving ntuple