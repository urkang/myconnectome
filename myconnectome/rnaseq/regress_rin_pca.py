"""
regress out both RIN and top 3 PCs 
"""

import numpy
import sklearn.decomposition
import os

basedir=os.environ['MYCONNECTOME_DIR']
rnaseqdir=os.path.join(basedir,'rna-seq')

def regress_rin_pca():
    rin=numpy.loadtxt(os.path.join(rnaseqdir,'rin.txt'))
    
    f=open(os.path.join(rnaseqdir,'varstab_data_prefiltered.txt'))
    subs=f.readline()
    gene_names=[]
    data=[]
    for l in f.readlines():
        l_s=l.strip().split()
        gene_names.append(l_s[0])
        data.append(l_s[1:])
    f.close()
    
    varstab=numpy.zeros((len(gene_names),48))
    
    varstab_rinregressed=numpy.zeros(varstab.shape)
    
    for i in range(len(gene_names)):
        varstab[i,:]=[float(x) for x in data[i]]
    pca=sklearn.decomposition.PCA(n_components=3)
    pca.fit(varstab.T)
    
    rin=numpy.array(rin,ndmin=2).T
    X=numpy.hstack((rin - numpy.mean(rin),pca.transform(varstab.T),numpy.ones((48,1))))
    
    for i in range(len(gene_names)):
        y=varstab[i,:].reshape((48,1))
        #print numpy.corrcoef(y.T,rin.T)[0,1]
        result=numpy.linalg.lstsq(X,y)
        resid=y - X.dot(result[0])
        varstab_rinregressed[i,:]=resid[:,0]
        
    f=open(os.path.join(rnaseqdir,'varstab_data_prefiltered_rin_3PC_regressed.txt'),'w')
    f.write(subs)
    for i in range(len(gene_names)):
        f.write(gene_names[i])
        for j in range(48):
            f.write(' %f'%varstab_rinregressed[i,j])
        f.write('\n')
    f.close()

if __name__ == "__main__":
    regress_rin_pca()