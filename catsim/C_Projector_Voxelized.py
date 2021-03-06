# Copyright 2020, General Electric Company. All rights reserved. See https://github.com/xcist/code/blob/master/LICENSE

import numpy as np
from ctypes import *
from numpy.ctypeslib import ndpointer
from catsim.CommonTools import *

def C_Projector_Voxelized(cfg, viewId, subViewId):
    ###------- C function and interface
    fun = cfg.clib.voxelized_projector
    fun.argtypes = [POINTER(c_int), c_float, ndpointer(c_float), ndpointer(c_float), c_int, \
        POINTER(c_float), c_int, POINTER(c_int), \
        c_int, ndpointer(c_int), ndpointer(c_float), ndpointer(c_float), ndpointer(c_float), \
        c_int, c_int, c_int, c_int, c_float, c_int]
    fun.restype = None
    
    ###------- loop of materials
    det = cfg.detNew
    src = cfg.srcNew
    
    pValueSpectrum = 0
    thisView = np.zeros([det.totalNumCells, cfg.spec.nEbin], dtype=np.single) # buffer for C
    for i in range(cfg.phantom.numberOfMaterials):
        Status = [0]
        Status = (c_int*1)(*Status)
        unused1 = 1
        thisView[:] = 0
        sourcePoints = src.samples
        nSubSources = src.nSamples
        unused2 = [2]
        unused2 = (c_float*1)(*unused2)
        unused3 = 3
        unused4 = [4]
        unused4 = (c_int*1)(*unused4)
        nModulesIn = det.nMod
        modTypeInds = det.modTypes
        Up = det.vvecs
        Right = det.uvecs
        Center = det.modCoords
        unused5 = 5
        unused6 = 6
        MaterialIndex = i+1
        MaterialIndexInMemory = MaterialIndex
        unused7 = 7
        freeTheMemory = 0
        
        if viewId==cfg.sim.stopViewId and subViewId==cfg.sim.subViewCount-1 and i==cfg.phantom.numberOfMaterials-1:
            freeTheMemory = 1
        
        # the C func wants data order: (row -> col) or xyz or Ebin -> pixel_ind or sample_ind
        fun(Status, unused1, thisView, sourcePoints, nSubSources, \
            unused2, unused3, unused4, \
            nModulesIn, modTypeInds, Up, Right, Center, \
            unused5, unused6, MaterialIndex, MaterialIndexInMemory, unused7, freeTheMemory)
        pValueSpectrum += thisView
    
    cfg.thisSubView *= np.exp(-pValueSpectrum)

    return cfg
