class custom_zip:
    def __init__(self,*iterables):
        self.iterator=[iter(i) for i in iterables]
        
    def __iter__(self):
        return self
    
    def __next__(self):
        items=[]
        
        for it in self.iterator:
            try:
                items.append(next(it))
            except StopIteration:
                raise StopIteration
        return tuple(items)
    
    
for a, b, c in custom_zip([1,2,3], ['x','y','z'], (10,20,30)):
    print(a, b, c)
