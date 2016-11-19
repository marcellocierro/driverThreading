import sncosmo
from analyzeSN import SNANASims
from analyzeSN import ResChar
import numpy as np
import datetime
import os
import sys

def inferParams(snanaSims, model, infer_method, i, minsnr=3.):
    """
    infer the parameters for the ith supernova in the simulation
    """
    try:
	    snid = snanaSims.headData.index.values[i]
	    z = snanaSims.headData.ix[snid, 'REDSHIFT_FINAL']
	    lcinstance = snanaSims.get_SNANA_photometry(snid=snid)
	    model.set(z=z)
	    print(z)
	    resfit = infer_method(lcinstance.snCosmoLC(), model, vparam_names=['t0', 'x0', 'x1', 'c'],
	            modelcov=True, minsnr=minsnr)
	    reschar = ResChar.fromSNCosmoRes(resfit)
	    return snid, reschar
    except:
	   return None

#!this function finds the location of the Minion file on anyone's laptop
def findLocation():
	for root, dirs, files in os.walk('.'):
             if root == './MINION_1016_10YR_DDF_v2':
                  root = str(root)
                  root = os.path.realpath(root)
                  return (root)

def store(snid, result):
    with open('pResults.dat', 'w') as f:
        write_str = snid
        write_str += ','.join(map(str, result.parameters))
        write_str += ','.join(map(str, np.asarray(result.covariance).flatten().tolist()))
        f.write(write_str)

if __name__ == '__main__':
    snana_eg = SNANASims.fromSNANAfileroot(snanafileroot='LSST_Ia',
                                           location=findLocation(),
                                           coerce_inds2int=False)
    dust = sncosmo.CCM89Dust()
    model = sncosmo.Model(source='salt2-extended',
		          effects=[dust, dust],
                          effect_names=['host', 'mw'],
		          effect_frames=['rest', 'obs'])
    if len(sys.argv) == 1:
		rangeFrom = 0
		rangeTo = 11

    else:
	    rangeFrom = int(sys.argv[1])
	    rangeTo = int(sys.argv[2])

    dsk={}

    for i in range(rangeFrom, rangeTo):
	    dsk.update({'%d' %i: (inferParams, snana_eg, model, sncosmo.fit_lc, i, 3.)})
	
    from dask.threaded import get

    deltaT = datetime.datetime.utcnow()
    sns = get(dsk, ['%d' %i for i in range(rangeFrom, rangeTo)])
    deltaT = datetime.datetime.utcnow() - deltaT
    print('Process time = {}'.format(deltaT))

    for i in range(rangeFrom - rangeFrom, rangeTo - rangeFrom):
	    if sns[i] != None:
		    store(sns[i][0], sns[i][1])
