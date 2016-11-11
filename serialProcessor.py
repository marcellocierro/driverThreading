import sncosmo
from analyzeSN import SNANASims
from analyzeSN import ResChar
import numpy as np
import datetime
import os

def inferParams(snanaSims, model, infer_method, i, minsnr=3.):
    """
    infer the parameters for the ith supernova in the simulation
    """
    snid = snanaSims.headData.index.values[i]
    z = snanaSims.headData.ix[snid, 'REDSHIFT_FINAL']
    lcinstance = snanaSims.get_SNANA_photometry(snid=snid)
    model.set(z=z)
    print(z)
    resfit = infer_method(lcinstance.snCosmoLC(), model, vparam_names=['t0', 'x0', 'x1', 'c'],
                          modelcov=True, minsnr=minsnr)
    reschar = ResChar.fromSNCosmoRes(resfit)
    return snid, reschar

#!this function finds the location of the Minion file on anyone's laptop
def findLocation():
	for root, dirs, files in os.walk('.'):
             if root == './MINION_1016_10YR_DDF_v2':#! this will contain the file that needs to be used(Origional file was in: /Users/rbiswas/data/LSST/SNANA_data/MINION_1016_10YR_DDF_v2/)
                  root = str(root)
                  root = os.path.realpath(root)
                  return (root)

snana_eg = SNANASims.fromSNANAfileroot(snanafileroot='LSST_Ia',
                                       location=findLocation(),
                                       coerce_inds2int=False)
if __name__ == '__main__':
    snana_eg = SNANASims.fromSNANAfileroot(snanafileroot='LSST_Ia',
                                           location=findLocation(),
                                           coerce_inds2int=False)
    dust = sncosmo.CCM89Dust()
    model = sncosmo.Model(source='salt2-extended',
		          effects=[dust, dust],
                          effect_names=['host', 'mw'],
		          effect_frames=['rest', 'obs'])
    deltaT = datetime.datetime.utcnow()
    for i in range(3):
	try:
	    snid, r = inferParams(snana_eg, model, sncosmo.fit_lc, i, minsnr=3.)
	    with open('results.dat', 'w') as fh: # Should Not be a text file when improved!
                write_str = snid
                write_str += ','.join(map(str, r.parameters)) 
                # We should only keep the the independent components
                # unlike what I am doing here
	        write_str += ','.join(map(str, np.asarray(r.covariance).flatten().tolist()))
                fh.write(write_str)
	except:
	    print('SN {} failed'.format(i))
    deltaT = datetime.datetime.utcnow() - deltaT
    print('Process time = {}'.format(deltaT))
