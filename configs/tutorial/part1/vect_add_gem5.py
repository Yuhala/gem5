from m5.objects import X86O3CPU

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

BINARY = "/home/peterson/projects/pim-tee/gem5/my-programs/vec_add_x86"


class MyX86O3Core(BaseCPUCore):
    def __init__(self):
        core = X86O3CPU()
        super().__init__(core, ISA.X86)


class MyX86Processor(BaseCPUProcessor):
    def __init__(self):
        super().__init__([MyX86O3Core()])


processorx = MyX86Processor()

processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.X86, num_cores=1)

ddr_memory = SingleChannelDDR4_2400(size="2GB")
hbm_memory = HBM_2000_4H_1x64()

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32kB",
    l1i_size="32kB",
    l2_size="256kB",
)

boardx = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=ddr_memory,
    cache_hierarchy=cache_hierarchy,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=hbm_memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(BinaryResource(local_path=BINARY))

simulator = Simulator(board=board)
simulator.run()
