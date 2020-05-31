import argparse
import re

def boolParse(instr):
    ''' validates command line boolean args '''
    if isinstance(instr, bool):
       return instr
    validTrue = ['yes', 'true', 't', 'y', '1']
    validFalse = ['no', 'false', 'f', 'n', '0']
    if instr.lower() in validTrue:
        return True
    elif instr.lower() in validFalse:
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.{}'.format(validTrue+validFalse))

def smootherParse(selection):
    ''' validates smoother command line options '''
    if selection != selection:
        return selection
    smoothers = ['avg', 'min', 'max']
    selection = selection.lower()
    if selection in smoothers:
        return selection
    elif selection in ['none', 'null', 'nada', 'zip', 'zilch']:
        return None
    else:
        raise argparse.ArgumentTypeError('Expected one of smoother options {}'.format(smoothers))

def kernelParse(selection):
    ''' validates smoother command line options '''
    selection=str(selection)
    dims = selection.split(',')

    if len(dims)!=2:
        raise argparse.ArgumentTypeError('Expected kernel and stride to have 2 values each {}'.format(selection))

    return [int(dim) for dim in dims]
