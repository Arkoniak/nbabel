from math import sqrt
from time import perf_counter

from vector import Vector


class PointND:
    @classmethod
    def _zero(cls):
        return cls(0.0, 0.0, 0.0)

    def norm(self):
        return sqrt(self.norm2())

    def norm_cube(self):
        norm2 = self.norm2()
        return norm2 * sqrt(norm2)

    def __repr__(self):
        return f"[{self.x:.10f}, {self.y:.10f}, {self.z:.10f}]"

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]

    @x.setter
    def x(self, value):
        self.data[0] = value


class Point4D(PointND):
    def __init__(self, x, y, z, w=0.0):
        self.data = [x, y, z, w]

    @property
    def w(self):
        return self.data[3]

    def norm2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2

    def __add__(self, other):
        return Point4D(
            self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w
        )

    def __sub__(self, other):
        return Point4D(
            self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w
        )

    def __mul__(self, other):
        return Point4D(
            other * self.x, other * self.y, other * self.z, other * self.w
        )

    __rmul__ = __mul__

    def reset_to_0(self):
        self.data = [0.0, 0.0, 0.0, 0.0]


class Point3D(PointND):
    def __init__(self, x, y, z):
        self.data = [x, y, z]

    def norm2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point3D(other * self.x, other * self.y, other * self.z)

    __rmul__ = __mul__

    def reset_to_0(self):
        self.data = [0.0, 0.0, 0.0]


class Points(Vector):
    def reset_to_0(self):
        for point in self:
            point.reset_to_0()


def compute_accelerations(accelerations, masses, positions):
    nb_particules = len(masses)
    for i0 in range(nb_particules - 1):
        for i1 in range(i0 + 1, nb_particules):
            delta = positions[i0] - positions[i1]
            distance_cube = delta.norm_cube()
            accelerations[i0] -= masses[i1] / distance_cube * delta
            accelerations[i1] += masses[i0] / distance_cube * delta


def main(Point):

    number_particles = 1000

    Points_ = Points[Point]

    masses = number_particles * [1.0]
    positions = Points_.zeros(number_particles)

    x = 0.0
    for position in positions:
        position.x = x
        x += 1.0

    accelerations = positions.zeros_like()

    compute_accelerations(accelerations, masses, positions)
    t_start = perf_counter()
    compute_accelerations(accelerations, masses, positions)
    clock_time = perf_counter() - t_start

    nb_steps = int(2 / clock_time)

    times = []

    for step in range(nb_steps):
        t_start = perf_counter()
        compute_accelerations(accelerations, masses, positions)
        times.append(perf_counter() - t_start)

    print(f"{Point.__name__}: {min(times) * 1000:.3f} ms")


if __name__ == "__main__":

    main(Point3D)
    main(Point4D)
