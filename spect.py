#!/usr/bin/python

import wave
import sys
from pylab import *

import numpy as np
import scipy.interpolate
import scipy.ndimage


def getPerfectPattern(filename, t=10, m=40, threshold=.3):

  fp = wave.open(filename, "rb")
  data = fp.readframes(-1)
  data = fromstring(data, 'int16')

  fr = fp.getframerate();
  print "framerate:", fr
  print "length of data", len(data)
  spock = specgram(data, Fs=fr, scale_by_freq=True, sides='default', cmap=cm.gist_heat)
  print "size of spectral data:", spock[0].shape
  res = smoothen(spock[0],(m,t))
  #imshow(res, vmin=0.0, vmax=100.0, cmap=cm.gray)

  result = np.empty([t,m])
  for i in range(m):
    for j in range(t):
      if res[i,j] > threshold: 
        result[j,i] = int(1)
      else: 
        result[j,i] = int(0)
  #matshow(result)
  #show()
  fp.close()
  return result

def smoothen(a, newDims):
  if not a.dtype in [np.float64, np.float32]:
    a = np.cast[float](a)

  ofs = 0.5
  old = np.array( a.shape )
  ndims = len( a.shape )

  newDims = np.asarray( newDims, dtype=float )
  dimlist = []

  # calculate new dims
  for i in range( ndims ):
    base = np.arange( newDims[i] )
    dimlist.append( (old[i]) / (newDims[i]) \
          * (base + ofs) - ofs )
  
  olddims = [np.arange(i, dtype = np.float) for i in list( a.shape )]
  mint = scipy.interpolate.interp1d( olddims[-1], a, kind='nearest' )
  newa = mint( dimlist[-1] )

  trorder = [ndims - 1] + range( ndims - 1 )
  for i in range( ndims - 2, -1, -1 ):
    newa = newa.transpose( trorder )

    mint = scipy.interpolate.interp1d( olddims[i], newa, kind='nearest' )
    newa = mint( dimlist[i] )

  if ndims > 1:
    # need one more transpose to return to original dimensions
      newa = newa.transpose( trorder )
  return newa
