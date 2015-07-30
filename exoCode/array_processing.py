'''
Copyright (c) 2015, Laura Eckman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import numpy as np

def lingray(x, survey='', a=None, b=None):
    """
    Auxiliary function that specifies the linear gray scale.
    a and b are the cutoffs : if not specified, min and max are used
    Prancer Physics Louisville
    """
    if a == None:
        a = np.min(x)
    if b == None:
        b = np.max(x)
    if survey == 'DSS':
        return (x-float(a))/(b-a)*255.0
    return (x-float(a))/(b-a)

def loggray(x, survey='',a=None, b=None):
    """
    Auxiliary function that specifies the logarithmic gray scale.
    a and b are the cutoffs : if not specified, min and max are used
    Prancer Physics Louisville
    """
    if a == None:
        a = np.min(x)
    if b == None:
        b = np.max(x)          
    linval = 10.0 + 990.0 * (x-float(a))/(b-a)
    if survey == 'DSS':
        return (np.log10(linval)-1.0)*0.5*255.0
    return (np.log10(linval)-1.0)*0.5
