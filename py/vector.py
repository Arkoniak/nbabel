"""
We would need a fixed size homogeneous mutable container.

In Julia, you can do::

    positions = Vector{Point4D}(undef, N)

In Python, it would be nice to be able to do::

    positions = Vector[Point4D].empty(N)

"""


class MetaVector(type):
    def __getitem__(cls, dtype):
        return type(
            f"Vector{dtype.__name__.capitalize()}",
            (cls,),
            {"dtype": dtype},
        )


class Vector(metaclass=MetaVector):
    @classmethod
    def from_list(cls, data):
        return cls(len(data), data=data)

    @classmethod
    def empty(cls, size):
        return cls(size)

    @classmethod
    def zeros(cls, size):
        vector = cls.empty(size)
        i = 0
        while i < size:
            vector[i] = cls.dtype._zero()
            i += 1
        return vector

    def zeros_like(self):
        vector = self.empty(len(self))
        i = 0
        while i < len(self):
            vector[i] = self.dtype._zero()
            i += 1
        return vector

    def __init__(self, size, data=None):
        if data is None:
            self._data = [None] * size
        else:
            self._data = list(data).copy()

        self.__iter__ = self._data.__iter__

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __len__(self):
        return self._data.__len__()

    def __repr__(self):
        return self._data.__repr__()


if __name__ == "__main__":

    class Point2d:
        @classmethod
        def _zero(cls):
            return cls(0.0, 0.0)

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"[{self.x}, {self.y}]"

    VectorP = Vector[Point2d]

    a = VectorP.empty(4)
    b = a.zeros_like()
