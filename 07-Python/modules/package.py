def nice_print(text):
    print('-'*(len(str(text))+4))
    print(f'| {text} |')
    print('-'*(len(str(text))+4))

def isum(*nums):
    _sum = 0
    for num in nums:
        _sum+=num
    return _sum
