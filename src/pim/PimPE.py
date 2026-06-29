#
# Peterson Yuhala
#


from m5.params import *
from m5.proxy import *
from m5.SimObject import SimObject


class PimPE(SimObject):
    type = "PimPE"
    cxx_header = "pim/pim_pe.hh"
    cxx_class = "gem5::pim::PimPE"
    inst_port = ResponsePort("CPU side port, receives requests")
    data_port = ResponsePort("CPU side port, receives requests")
    mem_side = RequestPort("Memory side port, sends requests")
    #time_to_wait = Param.Latency("Time before firing the event")
    #number_of_fires = Param.Int(1, "Number of times to fire the event before "
    #                               "goodbye")
