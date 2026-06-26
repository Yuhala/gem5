#
# Peterson Yuhala
#


from m5.params import *
from m5.SimObject import SimObject


class PimPE(SimObject):
    type = "PimPE"
    cxx_header = "pim/pim_pe.hh"
    cxx_class = "gem5::pim::PimPE"
