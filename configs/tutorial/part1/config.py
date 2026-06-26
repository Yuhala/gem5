from m5.objects import (
    ArmO3CPU,
    TournamentBP,
)

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


class MyOutOfOrderCore(BaseCPUCore):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        # 1. Create the base CPU object first
        core_obj = ArmO3CPU()

        # 2. Configure ALL of its parameters while it's a standalone object
        core_obj.fetchWidth = width
        core_obj.decodeWidth = width
        core_obj.renameWidth = width
        core_obj.issueWidth = width
        core_obj.wbWidth = width
        core_obj.commitWidth = width

        core_obj.numROBEntries = rob_size

        core_obj.numPhysIntRegs = num_int_regs
        core_obj.numPhysFloatRegs = num_fp_regs

        # core_obj.branchPred = TournamentBP()

        core_obj.LQEntries = 128
        core_obj.SQEntries = 128

        # 3. Finally, hand it off to the parent Standard Library component class
        super().__init__(core_obj, ISA.ARM)


class MyOutOfOrderProcessor(BaseCPUProcessor):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        cores = [MyOutOfOrderCore(width, rob_size, num_int_regs, num_fp_regs)]
        super().__init__(cores)


my_ooo_processor = MyOutOfOrderProcessor(
    width=8, rob_size=192, num_int_regs=256, num_fp_regs=256
)


main_memory = SingleChannelDDR4_2400(size="2GB")

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)
board = SimpleBoard(
    processor=my_ooo_processor,
    memory=main_memory,
    cache_hierarchy=cache_hierarchy,
    clk_freq="3GHz",
)

board.set_workload(obtain_resource("arm-gapbs-bfs-run"))

simulator = Simulator(board)
simulator.run()
