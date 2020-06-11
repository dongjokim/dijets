
import numpy as np
import ROOT

import scipy
from scipy import interpolate

import sys
sys.path.append("JPyPlotRatio");
#sys.path.append("/home/jasper/Asiakirjat/projects/JPyPlotRatio");


import JPyPlotRatio


f = ROOT.TFile("Normalized_AnalysisResults-combined-v2.root","read");
#fpp   = ROOT.TFile("results/Output_JCIaaJt_legotrain_CF_pp-1773_20180423-1806-LHC17p_pass1_CENT_woSDD.root","read");
dataTypePlotParams = [
	{'plotType':'data','color':'k','fmt':'s','markersize':5.0},
	{'plotType':'data','color':'r','fmt':'o','markersize':5.0},
	{'plotType':'data','color':'b','fmt':'P','markersize':5.0},
	{'plotType':'data','color':'m','fmt':'X','markersize':5.0},
	{'plotType':'data','color':'k','fmt':'o','fillstyle':'none','markersize':5.0} #PP
];


# define panel/xaxis limits/titles
nrow = 1;
ncol = 2;
xlimits = [(0.0,8.1),(0.08,0.3)];
ylimits = [(1E-6,0.9E+0)];
#rlimits = [(-0.1,0.1)];
rlimits = [(-0.1,1.0)];
#JCDijetBaseTask-Esche/jcdijet/h_rho/h_rhoCentBin00
#					/jcdijetDetMC/
rhoType = ["rho","rhom"];
signalType =["jcdijet","jcdijetDetMC"];
NR = len(rhoType);
ND = len(signalType);
xtitle = ["$\\rho$ (GeV/$c$)","$\\rhom$ (GeV/$c$)"];
ytitle = ["$\\frac{1}{N_{evt}}\\frac{dN}{d\\rho}$"];
plabel = {i: "{:s}".format(rhoType[i]) for i in range(0,NR)};
# Following two must be added
toptitle = "pp $\\sqrt{s}$ = 5.02 TeV"; # need to add on the top


plot = JPyPlotRatio.JPyPlotRatio(panels=(nrow,ncol),
	rowBounds=ylimits,  # for nrow
	colBounds=xlimits,  # for ncol
	panelLabel=plabel,  # nrowxncol
	#ratioType="diff",
	ratioBounds=rlimits,# for nrow
	panelLabelLoc=(0.12,0.92),panelLabelSize=10,panelLabelAlign="left",
	legendPanel=1,
	legendLoc=(0.78,0.68),legendSize=9,xlabel=xtitle[0],ylabel=ytitle[0]);



plot.EnableLatex(True);

plotMatrix = np.empty((NR,ND),dtype=int);

for iT in range(0,NR):
	plot.GetAxes(iT).set_yscale("log");
	for j in range(0,ND):
		#print("hjTsignalsC{:02}X01/hjTsignalsC{:02}X01T{:02}".format(j,j,iT));
		#JCDijetBaseTask-Esche/jcdijet/h_rho/h_rhoCentBin00
		gr = f.Get("JCDijetBaseTask-Esche/{:s}/h_{:s}/h_{:s}CentBin00".format(signalType[j],rhoType[iT],rhoType[iT]));
		#gr.Print();
		plotMatrix[iT,j] = plot.AddTH1(iT,gr,**dataTypePlotParams[j],label=signalType[j]);	
		
		if(j>0):
			plot.Ratio(plotMatrix[iT,j],plotMatrix[iT,0],style="default"); #Calculate and plot ratio between data and theory

f.Close();

plot.GetPlot().text(0.3,0.82,toptitle,fontsize=9);
#plot.GetPlot().text(0.25,0.80,dataDetail,fontsize=9);
#plot.GetPlot().text(0.23,0.77,strXlong[xlong],fontsize=9);
#plot.GetAxes(3).text(0.1,0.1,dataDetail,fontsize=9);

plot.Plot();

#plot.GetRatioAxes(3).remove();

plot.Save("figs/Fig_rhodist.pdf");
plot.Show();

