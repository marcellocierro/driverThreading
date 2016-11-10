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
             if root == './MINION_1016_10YR_DDF_v2':
                  root = str(root)
                  root = os.path.realpath(root)
                  return (root)

def store(result):
    with open('pResults.dat', 'w') as f:
        write_str = result
        write_str += ','.join(map(str, r.parameters))
        write_str += ','.join(map(str, np.asarray(r.covariance).flatten().toList()))
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
    dsk={'snana_eg': snana_eg,
         'model': model,
         'fit': sncosmo.fit_lc,
         'minsnr': 3,
         'iP-0': (inferParams, 'snana_eg', 'model', 'fit', 0, 'minsnr'),
         'iP-1': (inferParams, 'snana_eg', 'model', 'fit', 1, 'minsnr'),
         'iP-2': (inferParams, 'snana_eg', 'model', 'fit', 2, 'minsnr'),
         'store': (store, ['iP-%d' %i for i in [0,1,2]])}
    from dask.threaded import get
    try:
        deltaT = datetime.datetime.utcnow()
        get(dsk, 'store')
        deltaT = datetime.datetime.utcnow()
        print('Process time = {}'.format(deltaT))
    except:
        print('Fail')
        deltaT = datetime.datetime.utcnow()
        print('Process time = {}'.format(deltaT))
