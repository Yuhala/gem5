#ifndef PIM_PIM_PE_HH_
#define PIM_PIM_PE_HH_

#include "params/PimPE.hh"
#include "sim/sim_object.hh"

namespace gem5
{

namespace pim
{
class PimPE : public SimObject
{
  public:
    PimPE(const PimPEParams &p);
};

} // namespace pim

} // namespace gem5

#endif // PIM_PIM_PE_HH_
