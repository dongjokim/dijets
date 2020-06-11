
import numpy as np
import ROOT

import scipy
from scipy import interpolate

import sys
sys.path.append("JPyPlotRatio");
#sys.path.append("/home/jasper/Asiakirjat/projects/JPyPlotRatio");


import JPyPlotRatio



dataTypePlotParams = [
	{'plotType':'theory','facecolor':'C0','edgecolor':'C0','alpha':0.5,'linestyle':'solid','linecolor':'C0'},
	{'plotType':'theory','facecolor':'C1','edgecolor':'C1','alpha':0.5,'linestyle':'dotted','linecolor':'C1'},
	{'plotType':'theory','facecolor':'C2','edgecolor':'C2','alpha':0.5,'linestyle':'dashed','linecolor':'C2'},
	{'plotType':'theory','facecolor':'C3','edgecolor':'C3','alpha':0.5,'linestyle':'dashdot','linecolor':'C3'},
	{'plotType':'theory','facecolor':'C4','edgecolor':'C4','alpha':0.5,'linestyle':'dashdot','linecolor':'C4'},
	{'plotType':'theory','facecolor':'C5','edgecolor':'C5','alpha':0.5,'linestyle':'dashdot','linecolor':'C5'},
];

Modelfiles = [
			  "mc/JCIaa_legotrain_MCGen_PbPb-1752_20200609-1158-JEWEL_vacuum_PtHard03.root",
			  "mc/JCIaa_legotrain_MCGen_PbPb-1750_20200609-1158-JEWEL_0_10_PtHard03.root",
			  "mc/JCIaa_legotrain_MCGen_PbPb-1751_20200609-1158-JEWEL_0_10_PtHard03_keepRecoil.root"
			];


fModel = [ROOT.TFile(elm) for elm in Modelfiles];

ModelLabel = [
"~~~JEWEL vacuum",
"~~~JEWEL ",
"~~~JEWEL with Recoils"
];

# define panel/xaxis limits/titles
nrow = 1;
ncol = 3;
xlimits = [(0.0,91),(5.0,200),(5.0,400)];
ylimits = [(2.1E-5,1.2E+1)];
#rlimits = [(-0.01,0.01)];
rlimits = [(0.2,1.3)];
#JCDijetBaseTask-Esche/jcdijet/h_rho/h_rhoCentBin00
#					/jcdijetDetMC/
signalType =["h_pt/h_ptCentBin00","h_jetPt_ALICE/h_jetPt_ALICECentBin00JetBin01","h_dijetInvMDeltaPhiCut/h_dijetInvMDeltaPhiCutCentBin00JetBin01"];


xtitle = ["$p_{T,h}$ (GeV/$c$)","$p_{T,jet}$ (GeV/$c$)","$m_{jj}$"];
ytitle = ["$\\frac{1}{N_{evt}}\\frac{dN}{dp_{T}}$"];
plables = ["$h^{\\pm}$","Jets,anti-${k_{T}}$ $R=0.4$ $|\\eta|<0.4$","dijet"];
# Following two must be added
toptitle = "$\\sqrt{s}$ = 5.02 TeV, 0-10\%"; # need to add on the top


plot = JPyPlotRatio.JPyPlotRatio(panels=(nrow,ncol),
	rowBounds=ylimits,  # for nrow
	colBounds=xlimits,  # for ncol
	panelLabel=plables,  # nrowxncol
	#ratioType="diff",
	ratioBounds=rlimits,# for nrow
	panelLabelLoc=(0.12,0.92),panelLabelSize=10,panelLabelAlign="left",
	legendPanel=1,
	legendLoc=(0.5,0.68),legendSize=9,xlabel={0:xtitle[0],1:xtitle[1],2:xtitle[2]},ylabel=ytitle[0]);


plot.EnableLatex(True);
ND = len(Modelfiles);

plotMatrix = np.empty((ncol,ND),dtype=int);

for iT in range(0,ncol):
	plot.GetAxes(iT).set_yscale("log");
	for j in range(0,ND):
		gr = fModel[j].Get("JFJTask/jcdijet/{:s}".format(signalType[iT]));
		hvtx = fModel[j].Get("JFJTask/jcdijet/h_zvtx");
		gr.Scale(1./hvtx.GetEntries(),"width");
		gr.Print();
		plotMatrix[iT,j] = plot.AddTH1(iT,gr,**dataTypePlotParams[j],label=ModelLabel[j]);	
		
		if(j>0):
			plot.Ratio(plotMatrix[iT,j],plotMatrix[iT,0],style="default"); #Calculate and plot ratio between data and theory


plot.GetPlot().text(0.15,0.82,toptitle,fontsize=9);


plot.Plot();

#plot.GetRatioAxes(3).remove();

plot.Save("figs/Fig_hjetpt.pdf");
plot.Show();

