import math, numpy as np

def intersection(list1, list2):
    count = []
    for l in list1:
        if l in list2:
            count.append(l)
    return count

# euclidean point point distance
def euclideanDistance(p0, p1, dimension):
    return math.sqrt(sum([(p1[i]-p0[i])**2 for i in range(dimension)])) 

# distance between point p and segment Q = a + t*(b-a)
def pointSegmentDistance(p, a, b):
    n = np.subtract(np.asarray(b),np.asarray(a))
    nmag = np.linalg.norm(n)
    normalized_n = np.divide(n,nmag)

    pmina = np.subtract(np.asarray(p),np.asarray(a))
    t = np.dot(pmina, normalized_n)

    if(t < 0):
        t = 0
    elif(t > nmag):
        t = nmag

    normal = np.add(np.subtract(np.asarray(a),np.asarray(p)), np.multiply(t, normalized_n))

    dist = np.linalg.norm(normal)

    return dist

# distance between segment P = p + s*(q-p) and segment Q = m + t*(n-m)
def segmentSegmentDistance(p,q,m,n):
    isn = intersection([p,q],[m,n])

    if len(isn) == 1:
        return math.pow(10,-8)

    p = np.asarray(p)
    q = np.asarray(q)
    m = np.asarray(m)
    n = np.asarray(n)

    u = np.subtract(q,p)
    v = np.subtract(n,m)
    w = np.subtract(p,m)

    a = np.dot(u,u) # mag(u)**2
    b = np.dot(u,v) # proj_v(u)
    c = np.dot(v,v) # mag(v)**2
    d = np.dot(u,w) # proj_w(u)
    e = np.dot(v,w) # proj_w(v)
    
    denominator = a*c - b**2
    
    if denominator < math.pow(10,-8):
        s = 0
        t = d/b
    else:
        s = (b*e -  c*d)/denominator
        t = (a*e - b*d)/denominator

    if s < 0:
        s = 0
    if s > 1:
        s = 1
    if t < 0:
        t = 0
    if t > 1:
        t = 1

    ps = np.add(p, np.multiply(s,u))
    qt = np.add(m, np.multiply(t,v))

    return euclideanDistance(ps, qt, 3)

if __name__ == '__main__':
    print(segmentSegmentDistance([1,0,0],[2,4,5],[1,0,0],[3,5,6]))