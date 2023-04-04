# Read Fermi value from nscf.out in pbe/pbe-soc calculation.
# Read Fermi value from  hse-soc.out in HSE06 calculation.

import matplotlib.pyplot as plt
import sys
from decimal import Decimal


if len(sys.argv) != 3:
    print("Correct usage code.py band.dat.gnu Fermi-energy")
    exit(0)
else:
    BandFile = sys.argv[1]
    fermi = sys.argv[2]


#Reading band.dat.gnu file
f = open (BandFile,"r").readlines()
#print(len(f))
                                                                                                           
#Count number of bands
Nband = 0
for line in f:
	if len(line.strip()) == 0 :
		Nband = Nband + 1
print("\nNubmer of all bands= "+str(Nband))

#Find Nubmer of k points per band
Nkp = (len(f)/Nband)-1

#print(Nkp)  


#Creat CBM and VBM lists
cbm = []
vbm = []
cbm_k = []
vbm_k = []

for line in f:
    if len(line.strip()) != 0:
        if Decimal(line.split()[1]) > Decimal(fermi):
            cbm.append(Decimal(line.split()[1]))
            cbm_k.append(Decimal(line.split()[0]))
        elif Decimal(line.split()[1]) < Decimal(fermi):
            vbm.append(Decimal(line.split()[1]))
            vbm_k.append(Decimal(line.split()[0]))


#Find edge of cbm 
index_min_cbm = cbm.index(min(cbm))
coord_of_min_cbm = cbm_k[index_min_cbm]

#Find number of bands in cbm
cbmCount=len(cbm)/Nkp
print("\nNumber of bands in CBM= "+str(cbmCount))

print("\nCBM edge coordinate= ("+str(coord_of_min_cbm)+" ,"+str(min(cbm))+")")


#Find edge of vbm 
index_max_vbm = vbm.index(max(vbm))
coord_of_max_vbm = vbm_k[index_max_vbm]

#Find number of bands in vbm
vbmCount=len(vbm)/Nkp
print("\nNumber of bands in VBM= "+str(vbmCount))

print("\nVBM edge coordinate= ("+str(coord_of_max_vbm)+" ,"+str(max(vbm))+")")


#Find gap type. Direct or indirect

kk = Decimal(coord_of_min_cbm) - Decimal(coord_of_max_vbm)

Gap = Decimal(min(cbm)) - Decimal(max(vbm))

if kk == 0:
    print("\nDirect Gap = "+ str(min(cbm)) +" - "+ str(max(vbm))+" = "+str(Gap)+" eV")
else:
    print("\nIndirect Gap = "+ str(min(cbm)) +" - "+ str(max(vbm))+" = "+ str(Gap)+" eV")
#---------------------------------------------------------------------------------------------------------
#Plot bands

#High symmetry points. Read from bondx.out  
labelcoord = [0,	0.5	,	1.0006,	1.2448,	1.9916	,2.5464	,	3.1028,	3.8103,	4.3103,	4.8109,	5.0551 ,5.8019,	6.3567	,6.9131	,7.6205]
#High symmetry points name. Read from materials cloud: https://www.materialscloud.org/work/tools/seekpath
labelname = [r'$\Gamma$',r'$X|Y$',r'$\Gamma$',r'$Z|R2$',r'$\Gamma$',r'$T2|U2$',r'$\Gamma$',r'$V2|\Gamma$',r'$X|Y$',r'$\Gamma$',r'$Z|R2$',r'$\Gamma$',r'$T2|U2$',r'$\Gamma$',r'$V2$']

#Y Gamma Z
labelname = [r'$\Gamma$',r'$Y$',r'$\Gamma$',r'$Z$',r'$\Gamma$',r'$T2|U2$',r'$\Gamma$',r'$V2|\Gamma$',r'$X|Y$',r'$\Gamma$',r'$Z|R2$',r'$\Gamma$',r'$T2|U2$',r'$\Gamma$',r'$V2$']


kp = []
for i in range(Nkp):
    kp.append(f[i].split()[0])


all_band = []
for i in range(Nband):
    band = []
    for j in range(Nkp):
        band.append(Decimal(f[j+i*(Nkp+1)].split()[1])-Decimal(fermi))
    all_band.append((band))

plt.figure(figsize=(2,4)) 

for i in range(vbmCount): 
    plt.plot(kp,all_band[i], '#1f77b4',lw=2.2,zorder=1)

for i in range(vbmCount,Nband):
    plt.plot(kp,all_band[i],color = "orange",lw=2.2,zorder=1)


#scatter plot of edge points
plt.scatter(coord_of_max_vbm,max(vbm)-Decimal(fermi),color="#32CD32",s=150,zorder=2)
plt.scatter(coord_of_min_cbm,min(cbm)-Decimal(fermi),	color='#FF4500',s=150, alpha=1,zorder=2)

plt.ylabel("Energy(eV)")
plt.yticks(size=14)
plt.xticks(labelcoord,labelname,size=14)
#plt.xlim(0.5,1.244)
#plt.ylim(-6,9)
#plt.subplots_adjust(left=0.22,right=0.97,bottom=0.06,top=0.94)
plt.title("Quantum Espresso Band Structure",size=16)
plt.savefig("Band-Structure")
plt.grid()
plt.show()


