from mpi4py.futures import MPIPoolExecutor

nx, ny = 640*2, 480*2
x0, x1 = -2.0, 2.0
y0, y1 = -1.5, 1.5


def f(k):
    dx = (x1 - x0) / nx
    dy = (y1 - y0) / ny
    c = complex(0, 0.65)

    x_arr = bytearray(nx)
    y = y1 - k * dy
    for j in range(nx):
        x = x0 + j * dx
        z = complex(x, y)
        n = 255
        while abs(z) < 3 and n > 1:
            z = z**2 + c
            n -= 1
        x_arr[j] = n
    return x_arr


if __name__ == '__main__':
    communicator = MPIPoolExecutor()
    obj = communicator.map(f, range(ny))
    f = open('test.pgm', 'wb')
    f.write(b'P5 %d %d %d\n'.format(nx, ny, 255))
    for line in obj:
        f.write(line)
