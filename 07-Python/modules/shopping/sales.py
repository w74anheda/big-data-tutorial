from ..package import nice_print
from modules.package import nice_print

def isum(*nums):
    _sum = 0
    for num in nums:
        _sum+=num
    return _sum