

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