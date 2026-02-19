class MyEnumerate:
    """Your version of enumerate()"""

    def __init__(self, iterable, start=0):
        self.iterable = iter(iterable)  
        self.index = start              # start index

    def __iter__(self):
        return self                     

    def __next__(self):
        value = next(self.iterable)     
        result = (self.index, value)
        self.index += 1                 # increment index
        return result


# Test
for idx, val in MyEnumerate(['a', 'b', 'c']):
    print(idx, val) 