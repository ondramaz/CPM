# CPM

DATA preparation:
1. Download behavioral and connectome data:

https://db.humanconnectome.org/data/projects/HCP_1200

Quick downloads:
behavioral data ->  *.csv file

HCP1200 Parcellation+Timeseries+Netmats (PTN)
1003 or 812 subjects

2. Unpack
HCP1200_Parcellation_Timeseries_Netmats.zip
->

groupICA_3T_HCP1200_MSMAll.tar.gz
netmats_3T_HCP1200_MSMAll_ICAd100_ts2.tar.gz
netmats_3T_HCP1200_MSMAll_ICAd15_ts2.tar.gz
netmats_3T_HCP1200_MSMAll_ICAd200_ts2.tar.gz
netmats_3T_HCP1200_MSMAll_ICAd25_ts2.tar.gz
netmats_3T_HCP1200_MSMAll_ICAd300_ts2.tar.gz
netmats_3T_HCP1200_MSMAll_ICAd50_ts2.tar.gz
NodeTimeseries_3T_HCP1200_MSMAll_ICAd100_ts2.tar.gz
NodeTimeseries_3T_HCP1200_MSMAll_ICAd15_ts2.tar.gz
NodeTimeseries_3T_HCP1200_MSMAll_ICAd200_ts2.tar.gz
NodeTimeseries_3T_HCP1200_MSMAll_ICAd25_ts2.tar.gz
NodeTimeseries_3T_HCP1200_MSMAll_ICAd300_ts2.tar.gz
NodeTimeseries_3T_HCP1200_MSMAll_ICAd50_ts2.tar.gz
scripts.tar.gz
subjectIDs_recon1.txt
subjectIDs_recon2.txt
subjectIDs.txt


netmats*.tar.gz - contains connectome matrix data for 1003 subjects and 15..300 nodes
subjectIDs.txt - order of subjects in connectome matrices


Documentation :
https://www.humanconnectome.org/storage/app/media/documentation/s1200/HCP1200-DenseConnectome+PTN+Appendix-July2017.pdf

Network matrices (individual subjects and group-averaged)
Network-matrices (also referred to as "netmats" or "parcellated connectomes") were derived from the node-timeseries. For each subject, the N (15-
300) node-timeseries were fed into network modelling, creating an NxN matrix of connectivity estimates. Network modelling was carried out using the
FSLNets toolbox (fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLNets). Netmats were estimated for the 1003 subjects (complete timeseries) described above. We
applied network modelling in two ways:
1. netmats1: Using "full" normalized temporal correlation between every node timeseries and every other. This is a common approach and is
very simple, but it has various practical and interpretational disadvantages [Smith 2012].
2. netmats2: Using partial temporal correlation between nodes' timeseries. This aims to estimate direct connection strengths better than
achieved by full correlation. To slightly improve the estimates of partial correlation coefficients, a small amount of L2 regularization is
applied (setting rho=0.01 in the Ridge Regression netmats option in FSLNets) [Smith OHBM 2014, FSLNets].
Netmat values were Gaussianised from Pearson correlation scores (r-values) into Z-stats, and are released for individual subjects, as well as groupaveraged over all subjects. The average netmats are provided as “pconn” files, readable by HCP Connectome Workbench software (and directly
viewable in the wb_view workbench display tool). The individual subjects’ netmats are saved as raw text files, with one row per subject; each row
contains the NxN matrix of connectivity estimates, unwrapped to a long single row of N2 values. The row ordering matches the list of subject IDs
saved in the file subjectIDs.txt


3. unpack netmats_3T_HCP1200_MSMAll_ICAd50_ts2.tar.gz  (50 nodes - for example)

Use netmats1.txt or netmats2.txt as connectome matrix

4. run main.py

The script runs functions:

Cross validation:   cv('netmats1.txt', 'subjectIDs.txt', 'unrestricted_ondramaz_6_21_2020_8_5_28.csv', 'Strength_Unadj')

Train model:        train('netmats1.txt', 'subjectIDs.txt', 'unrestricted_ondramaz_6_21_2020_8_5_28.csv', 'Strength_Unadj','savemodel.mod')

Predict data:       predict('netmats1.txt','savemodel.mod')
