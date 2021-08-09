import math


pi, e, i = math.pi, math.e, 1j


def cubic_bezier(t, initial, ct1, ct2, final):
    return (1-t)**3 * initial + 3*t*(1-t)**2*ct1 + 3*t**2*(1-t)*ct2 + t**3*final


def line(t, initial, final):
    return (1-t)*initial + t*final


curves_functions = {'C': cubic_bezier, 'L': line}


def f(t, curves):
    curves_num = len(curves)
    curve_idx = math.ceil(t * curves_num) - 1
    return curves_functions[curves[curve_idx][0]](t * curves_num - curve_idx, *curves[curve_idx][1:])


def integrate_trapezium(f, a, b, n=50):
    """A simple implementation of trapezium rule for numerical integration.
    I preferred this to other methods from the standard libraries as I had issues with
    integrating complex functions"""
    h = (b - a) / n
    sigma = 0
    sigma += (f(a) + f(b))
    for k in range(1, n):
        sigma += (2 * f(a + h * k))
    sigma = sigma * h / 2
    return sigma


def compute_fourier_coeff(f, m, curves):
    coeff = []
    for n in range(-m, m + 1):
        cur = integrate_trapezium(lambda t: f(t, curves) * e ** (-n*2*pi*i*t), 0, 1, 4000)
        coeff.append([n, (cur.real, cur.imag)])
    return coeff


def extract_path(filename):
    """"The function extracts the path attribute of an SVG file"""
    f = open(filename, 'r')
    s = ''
    for line in f.readlines():
        s += line.strip()
    f.close()
    s = s[s.find('<path'):]
    s = s[s.find('d=') + 3:]
    s = s[:s.find('"')]
    return s


def process_svg(filename):
    """The function processes SVG file and transforms it from a compressed representation to
    a more human readable format by adding and spaces splitting each curve in a separate block"""
    s = extract_path(filename)
    s = list(s)
    for i in range(len(s)):
        if s[i] == ' ' and ('a' <= s[i+1] <= 'z' or 'A' <= s[i+1] <= 'Z'):
            s[i] = ''
        elif s[i] == ' ' and s[i-1][-1] != ',' and s[i+1][0] != ',':
            s[i] = ','
        elif s[i] == ' ' and (s[i-1][-1] == ',' or s[i+1][0] == ','):
            s[i] = ''
        elif s[i] == '-' and s[i-1][-1] != ',':
            s[i] = ',' + s[i]
        elif ('a' <= s[i] <= 'z' or 'A' <= s[i] <= 'Z') and i + 1 < len(s) and s[i+1] != ',':
            s[i] = s[i] + ','
    res = ''
    for i in s:
        res += i
    s = res
    start = 0
    curves = []
    for i in range(1, len(s)):
        if 'a' <= s[i] <= 'z' or 'A' <= s[i] <= 'Z':
            curves.append(s[start:i])
            start = i
    for i in range(len(curves)):
        curves[i] = curves[i].split(',')
    # len_curves = len(curves)
    # key_points_num = {'M':2, 'm':2, 'l':2, 'L':2, 'C':6, 'c':6}
    # for j in range(len_curves):
    #     points_num = key_points_num[curves[0][0]]
    #     for k in range((len(curves[0]) - 1) // points_num):
    #         t = [curves[0][0]] + curves[0][k * points_num + 1: k * points_num + points_num + 1]
    #         curves.append(t)
    #     curves = curves[1:]
    return curves


def transform_path(curves):
    """"Converts the curves from strings to their numerical representation:
    string --> float --> rel to abs --> shifts to the origin --> y direction is flipped -->
    S curves to C curves --> complex"""
    # converts string to float
    for i in range(len(curves)):
        for j in range(1, len(curves[i])):
            curves[i][j] = float(curves[i][j])
    # adds the start point to each array, converts relative coordinates to absolute
    for i in range(1, len(curves)):
        if curves[i][0] not in ('z', 'M'):
            start_pts = [curves[i-1][-2], curves[i-1][-1]]
            curves[i] = [curves[i][0]] + start_pts + curves[i][1:]
        for j in range(3, len(curves[i])):
            if 'a' <= curves[i][0] <= 'z':
                curves[i][j] += curves[i][1] if j % 2 == 1 else curves[i][2]
        curves[i][0] = curves[i][0].upper()
    curves = curves[1:]
    # finds min and max coordinates
    mxx, mxy, mnx, mny = 0, 0, math.inf, math.inf
    for i in range(len(curves)):
        for j in range(1, len(curves[i])):
            if j % 2 == 0:
                if curves[i][j] > mxy:
                    mxy = curves[i][j]
                if curves[i][j] < mny:
                    mny = curves[i][j]
            else:
                if curves[i][j] > mxx:
                    mxx = curves[i][j]
                if curves[i][j] < mnx:
                    mnx = curves[i][j]
    # shifting the points to the origin and flipping y values
    x_shift = -(mxx + mnx) / 2
    y_shift = -(mxy + mny) / 2
    for i in range(len(curves)):
        for j in range(1, len(curves[i])):
            curves[i][j] += x_shift if j % 2 == 1 else y_shift
            if j % 2 == 0:
                curves[i][j] *= -1
    # converting S curves to C curves
    for i in range(1, len(curves)):
        if curves[i][0] == 'S':
            st_ctrl_pt = curves[i - 1][5:7] if curves[i - 1][0] == 'C' else curves[i][1:3]
            curves[i] = curves[i][:3] + st_ctrl_pt + curves[i][3:]
            curves[i][0] = 'C'
    # converting to complex numbers
    for i in range(len(curves)):
        c_arr = [curves[i][0]]
        for j in range(1, len(curves[i]), 2):
            c_arr.append(complex(curves[i][j], curves[i][j+1]))
        curves[i] = c_arr[:]
    return curves


def get_fourier(filename, m):
    """"Returns fourier coefficients depending on m - the number of rotating pairs"""
    _ = process_svg(filename)
    processed = transform_path(_)
    fourier_coeff = compute_fourier_coeff(f, m, processed)
    fourier_coeff.sort(key=lambda coor: math.sqrt(coor[1][0] ** 2 + coor[1][1] ** 2), reverse=True)
    idx0 = 0
    # puts the only vector that doesn't rotate at the beginning
    for k in range(len(fourier_coeff)):
        if fourier_coeff[k][0] == 0:
            idx0 = k
            break
    fourier_coeff = [fourier_coeff[idx0]] + fourier_coeff[:idx0] + fourier_coeff[idx0+1:]
    return fourier_coeff
