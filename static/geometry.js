
const lerp = 
    (x1, x2, alpha) => {

        if(alpha > 1 || alpha < 0)
            {
                console.error('alpha value in lerp not between 0 and 1')
                return NaN
            }

        let a = x1*(1-alpha),
            b = x2*alpha

        return a + b

    }

const simple_intersection = 
    (f, data, xAxis, i) => {
        let numer = f - xAxis(data[i-1].x),
            denom = xAxis(data[i].x)-xAxis(data[i-1].x)

        let alpha = numer/denom

        return [lerp(xAxis(data[i-1].x), xAxis(data[i].x), alpha), f]
    }

const crosses_bounds =
    (data, xAxis, i, f) => {
        let check1 = xAxis(data[i-1].x) > f && xAxis(data[i].x) < f,
            check2 = xAxis(data[i-1].x) < f && xAxis(data[i].x) > f

        return check1 || check2
    }

const line_intersection = 
    (p1,p2,p3,p4) => {
        let ret = {}

        let denom = (p1.x-p2.x)*(p3.y - p4.y) - (p1.y-p2.y)*(p3.x-p4.x),
            first = p1.x*p2.y - p1.y*p2.x,
            second = p3.x*p4.y - p3.y*p4.x

        ret.x = (first*(p3.x - p4.x) - (p1.x-p2.x)*second) / denom
        ret.y = (first*(p3.y - p4.y) - (p1.y-p3.y)*second) / denom

        return ret
    }