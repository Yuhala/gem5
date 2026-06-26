No, that is an important distinction. PIM compute units in Aquabolt are **not** RISC-V cores. They are much simpler than that.

---

**What Samsung Aquabolt actually puts in the logic layer**

```
NOT this:                          THIS:
┌─────────────────┐               ┌─────────────────┐
│   Full RISC-V   │               │   Fixed-function │
│   core          │               │   MAC unit       │
│   - fetch       │               │                  │
│   - decode      │               │   multiply       │
│   - branch pred │               │   accumulate     │
│   - OOO exec    │               │   add            │
│   - TLB         │               │   (that's it)    │
│   - OS support  │               │                  │
└─────────────────┘               └─────────────────┘
     ~500K gates                       ~2K gates
```

Aquabolt's PIM unit is essentially a **hardwired multiply-accumulate (MAC) datapath** — no instruction fetch, no decode, no branch predictor, no register renaming. It has:

- A small register file (16 x 32-bit registers called PIM registers)
- A single ALU that does either ADD or MAC
- A simple state machine that reads operands from a bank row, computes, writes back
- No ability to run arbitrary code

The reason for this simplicity is area and power budget. The logic layer in an HBM stack has extremely tight constraints — you cannot afford a full CPU core next to every two banks. Samsung's goal was to add the minimum logic needed to avoid moving data across the HBM bus for the most bandwidth-hungry operation in ML inference, which is GEMV.

---

**The programming model is command-driven, not instruction-driven**

Instead of executing a program, the PIM unit responds to special DRAM commands issued by the host CPU:

```
Host CPU issues:   PIM_OP (ADD or MAC) + bank address
PIM unit responds: reads two rows from its local banks
                   performs the operation element-wise
                   writes result back to a result row
                   signals completion
```

The host CPU orchestrates the entire computation by issuing a sequence of these commands — it is closer to programming a DMA engine than running a CPU core.

---

**How this changes the gem5 model**

This means in gem5 you do not instantiate a `MinorCPU` or `RiscvO3CPU` inside the PIM engine. Instead you model it as a simple state machine with a fixed latency:

```cpp
void PIMEngine::executePIMOp(PIMOpcode op, uint32_t *row_A,
                              uint32_t *row_B, uint32_t *row_C,
                              int num_elements) {
    // No fetch, no decode — just directly execute the fixed operation
    switch (op) {
        case PIM_ADD:
            for (int i = 0; i < num_elements; i++)
                row_C[i] = row_A[i] + row_B[i];
            break;

        case PIM_MAC:
            for (int i = 0; i < num_elements; i++)
                accumulator += row_A[i] * row_B[i];
            break;
    }

    // Schedule completion event after fixed PIM latency
    // (Aquabolt adds ~10ns overhead vs normal DRAM access)
    schedule(completionEvent, curTick() + pim_latency);
}
```

The state machine has maybe four states:

```
IDLE → FETCH_OPERANDS → COMPUTE → WRITEBACK → IDLE
```

Each state transition takes a fixed number of cycles that you calibrate to match Samsung's published numbers.

---

**Where RISC-V cores do appear in PIM research**

You are probably thinking of a different class of PIM architectures like **UPMEM** or research proposals like **PIM-enabled instructions (PEI)** from Carnegie Mellon, where each DRAM bank does get a simple in-order core. Those are called **Processing Near Memory (PNM)** rather than **Processing In Memory (PIM)** in the strict sense, and they do use simple RISC-V or custom ISA cores. The distinction is:

```
Processing In Memory (PIM)   — fixed function, inside the array
  Examples: Samsung Aquabolt, SK Hynix AiM

Processing Near Memory (PNM) — programmable core, near the array
  Examples: UPMEM DIMMs, Micron Automata
```

Aquabolt is strictly PIM — fixed function, no programmable core.
