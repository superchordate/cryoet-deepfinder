import numpy as np

import warnings
warnings.simplefilter('ignore') # to mute some warnings produced when opening the tomos with mrcfile

from lxml import etree
from copy import deepcopy
#from sklearn.metrics import pairwise_distances
from contextlib import redirect_stdout # for writing txt file

def add_obj(objlIN, label, coord, tomo_idx=None, orient=(None,None,None), cluster_size=None):
    obj = {
        'tomo_idx': tomo_idx,
        'label': label,
        'x'    :coord[2] ,
        'y'    :coord[1] ,
        'z'    :coord[0] ,
        'psi'  :orient[0],
        'phi'  :orient[1],
        'the'  :orient[2],
        'cluster_size':cluster_size
    }
    # return objlIN.append(obj)
    objlIN.append(obj)
    return objlIN

def disp(objlIN):
    for p in range(len(objlIN)):
        tidx  = objlIN[p]['tomo_idx']
        lbl   = objlIN[p]['label']
        x     = objlIN[p]['x']
        y     = objlIN[p]['y']
        z     = objlIN[p]['z']
        psi   = objlIN[p]['psi']
        phi   = objlIN[p]['phi']
        the   = objlIN[p]['the']
        csize = objlIN[p]['cluster_size']

        strout = 'obj ' + str(p) + ': ('
        if tidx!=None:
            strout = strout + 'tomo_idx:' + str(tidx) + ', '
        strout = strout + 'lbl:' + str(lbl) + ', x:' + str(x) + ', y:' + str(y) + ', z:' + str(z) + ', '
        if psi!=None or phi!=None or the!=None:
            strout = strout + 'psi:' + str(psi) + ', phi:' + str(phi) + ', the:' + str(the) + ', '
        if csize!=None:
            strout = strout + 'cluster_size:' + str(csize)
        strout = strout + ')'

        print(strout)

def read_xml(filename):
    tree = etree.parse(filename)
    objl_xml = tree.getroot()

    objlOUT = []
    for p in range(len(objl_xml)):
        tidx  = objl_xml[p].get('tomo_idx')
        lbl   = objl_xml[p].get('class_label')
        x     = objl_xml[p].get('x')
        y     = objl_xml[p].get('y')
        z     = objl_xml[p].get('z')
        psi   = objl_xml[p].get('psi')
        phi   = objl_xml[p].get('phi')
        the   = objl_xml[p].get('the')
        csize = objl_xml[p].get('cluster_size')

        # if facultative attributes exist, then cast to correct type:
        if tidx!=None:
            tidx = int(tidx)
        if csize!=None:
            csize = int(csize)
        if psi!=None or phi!=None or the!=None:
            psi = float(psi)
            phi = float(phi)
            the = float(the)

        add_obj(objlOUT, tomo_idx=tidx, label=lbl, coord=(float(x), float(y), float(z)), orient=(psi,phi,the), cluster_size=csize)
    return objlOUT

def write_xml(objlIN, filename):
    objl_xml = etree.Element('objlist')
    for idx in range(len(objlIN)):
        tidx  = objlIN[idx]['tomo_idx']
        lbl   = objlIN[idx]['label']
        x     = objlIN[idx]['x']
        y     = objlIN[idx]['y']
        z     = objlIN[idx]['z']
        psi   = objlIN[idx]['psi']
        phi   = objlIN[idx]['phi']
        the   = objlIN[idx]['the']
        csize = objlIN[idx]['cluster_size']

        obj = etree.SubElement(objl_xml, 'object')
        if tidx!=None:
            obj.set('tomo_idx', str(tidx))
        obj.set('class_label' , str(lbl))
        obj.set('x'           , '%.3f' % x)
        obj.set('y'           , '%.3f' % y)
        obj.set('z'           , '%.3f' % z)
        if psi!=None:
            obj.set('psi', '%.3f' % psi)
        if phi!=None:
            obj.set('phi', '%.3f' % phi)
        if the!=None:
            obj.set('the', '%.3f' % the)
        if csize!=None:
            obj.set('cluster_size', str(csize))

    tree = etree.ElementTree(objl_xml)
    tree.write(filename, pretty_print=True)

# TODO: handle psi phi theta & tomoIDX
def read_txt(filename):
    objlOUT = []
    with open(str(filename), 'rU') as f:
        for line in f:
            lbl, z, y, x, *_ = line.rstrip('\n').split()
            add_obj(objlOUT, label=lbl, coord=(float(x), float(y), float(z)))
    return objlOUT

def write_txt(objlIN, filename):
    with open(filename, 'w') as f:
        with redirect_stdout(f):
            for idx in range(len(objlIN)):
                lbl = objlIN[idx]['label']
                x = objlIN[idx]['x']
                y = objlIN[idx]['y']
                z = objlIN[idx]['z']
                csize = objlIN[idx]['cluster_size']
                if csize==None:
                    print(lbl + ' ' + str(z) + ' ' + str(y) + ' ' + str(x))
                else:
                    print(lbl + ' ' + str(z) + ' ' + str(y) + ' ' + str(x) + ' ' + str(csize))


# label can be int or str (is casted to str)
def get_class(objlIN, label):
    idx_class = []
    for idx in range(len(objlIN)):
        if str(objlIN[idx]['label'])==str(label):
            idx_class.append(idx)

    objlOUT = []
    for idx in range(len(idx_class)):
        objlOUT.append(objlIN[idx_class[idx]])
    return objlOUT

def above_thr(objlIN, thr):
    idx_thr = []
    for idx in range(len(objlIN)):
        csize = objlIN[idx]['cluster_size']
        if csize != None:
            if csize>=thr:
                idx_thr.append(idx)
        else:
            print('/!\ Object ' + str(idx) + ' has no attribute cluster_size')

    objlOUT = []
    for idx in range(len(idx_thr)):
        objlOUT.append( objlIN[idx_thr[idx]] )
    return objlOUT

def above_thr_per_class(objlIN, lbl_list, thr_list):
    objlOUT = []
    for lbl in lbl_list:
        objl_class = get_class(objlIN, lbl)
        objl_class = above_thr(objl_class, thr_list[lbl-1])
        for p in range(len(objl_class)):
            objlOUT.append(objl_class[p])
    return objlOUT

# TODO check why np.round is used
def scale_coord(objlIN, scale):
    objlOUT = deepcopy(objlIN) # necessary else the original objl is scaled too
    for idx in range(len(objlIN)):
        x = int(np.round(float(objlIN[idx]['x'])))
        y = int(np.round(float(objlIN[idx]['y'])))
        z = int(np.round(float(objlIN[idx]['z'])))
        objlOUT[idx]['x'] = scale * x
        objlOUT[idx]['y'] = scale * y
        objlOUT[idx]['z'] = scale * z
    return objlOUT

# Returns a list with different (unique) labels contained in input objl
def get_labels(objlIN):
    class_list = []
    for idx in range(len(objlIN)):
        class_list.append(objlIN[idx]['label'])
    # Set only stores a value once even if it is inserted more then once:
    lbl_set  = set(class_list) # insert the list to the set
    lbl_list = (list(lbl_set)) # convert the set to the list
    return lbl_list

# INPUT:
#   objlIN: object list with objects from various tomograms
# OUTPUT:
#   objlOUT: object list with objects from tomogram 'tomo_idx'
def get_tomo(objlIN, tomo_idx):
    idx_tomo = []
    for idx in range(len(objlIN)):
        if objlIN[idx]['tomo_idx'] == tomo_idx:
            idx_tomo.append(idx)

    objlOUT = []
    for idx in range(len(idx_tomo)):
        objlOUT.append(objlIN[idx_tomo[idx]])
    return objlOUT

# # /!\ for now this function does not know how to handle empty objlists
# def get_Ntp(objl_gt, objl_df, tol_pos_err):
#     # tolerated position error (in voxel)
#     Ngt = len(objl_gt)
#     Ndf = len(objl_df)
#     coords_gt = np.zeros((Ngt,3))
#     coords_df = np.zeros((Ndf,3))
#
#     for idx in range(0,Ngt):
#         coords_gt[idx,0] = objl_gt[idx].get('x')
#         coords_gt[idx,1] = objl_gt[idx].get('y')
#         coords_gt[idx,2] = objl_gt[idx].get('z')
#     for idx in range(0,Ndf):
#         coords_df[idx,0] = objl_df[idx].get('x')
#         coords_df[idx,1] = objl_df[idx].get('y')
#         coords_df[idx,2] = objl_df[idx].get('z')
#
#     # Get pairwise distance matrix:
#     D = pairwise_distances(coords_gt, coords_df, metric='euclidean')
#
#     # Get pairs that are closer than tol_pos_err:
#     D = D<=tol_pos_err
#
#     # A detected object is considered a true positive (TP) if it is closer than tol_pos_err to a ground truth object.
#     match_vector = np.sum(D,axis=1)
#     Ntp = np.sum(match_vector==1)
#     return Ntp