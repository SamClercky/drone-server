class ref:
    """Pointer simulation of a pointer in python"""
    def __init__(self, obj):
        self.obj = obj
    
    def get(self):
        """Gets the value"""
        return self.obj

    def set(self, obj):
        """Sets the value"""
        self.obj = obj
        return self.obj
