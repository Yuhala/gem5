
#include "pim/pim_pe.hh"

#include <iostream>

namespace gem5
{
namespace pim
{
PimPE::PimPE(const PimPEParams &params) : SimObject(params)
{
    std::cout << "Hello from a PIM PE!" << std::endl;
}

} // namespace pim

} // namespace gem5
