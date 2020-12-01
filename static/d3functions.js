/**
 * print all dots from json data 
 * with specifications
 * 
 */
const printDot =
(svg, xAxis, yAxis, data, radius, color='black',translate="", stroke='none') =>{
    svg.append('g')
        .attr('transform', translate)
        .selectAll('dot')
        .data(data)
        .enter()
        .append('circle')
            .attr('cx', d=>{
                return xAxis(d.x)
            })
            .attr('cy', d=>{
                if(d.y == '-Infinity' || d.y == 'Infinity') {
                    return 50
                }
                return yAxis(d.y)
            })
            .attr('r', radius)
            .style('fill', color)
            .style('stroke', stroke)
            .on(
                "mouseover", 
                function(d) {
                    d3.select(this).attr('r', d3.select(this).attr('r')*2)
                    }
                )                  
            .on(
                "mouseout", 
                function(d) {
                    d3.select(this).attr('r', d3.select(this).attr('r')/2)
                    }
                )
}

/**
 * print all dots from json data 
 * with specifications
 * 
 */
const printSymbol =
(svg, data, color='black', symbol=d3.symbolStar, rotate=0, translate="") =>{
    svg.append('g')
        .attr('transform', translate)
        .selectAll('dot')
        .data(data)
        .enter()
        .append('path')
            .attr("transform", d => `translate(${d.x},${d.y})rotate(${rotate})`)
            .attr('d', d3.symbol().type(symbol).size(20))
            .style('fill', color)
            .on(
                "mouseover", 
                function(d) {
                    d3.select(this).attr('d', d3.symbol().type(symbol).size(60))
                    }
                )                  
            .on(
                "mouseout", 
                function(d) {
                    d3.select(this).attr('d', d3.symbol().type(symbol).size(20))
                    }
                )
}

/**
 * prints a horizontal line
 */
const printDiagLine = 
(svg, xAxis, yAxis, x, y) =>
    svg
    .append('line')
        .attr('transform', "translate(25,15)")
        .attr('stroke', 'black')
        .style("stroke-dasharray", ("3, 3"))
        .attr('x1', xAxis(x[0]))
        .attr('x2',xAxis(x[1]))
        .attr('y1',yAxis(y[0]))
        .attr('y2',yAxis(y[1]))
    
/**
 * print path on the chart svg for the emotion[i]
 */
const printPath =
(svg, data, i, xScale, yScale, showAxes=true) => {
    let wid = document.getElementById(`chart1`).getAttribute('width'),
        het = document.getElementById(`chart1`).getAttribute('height')

    let t
    if(showAxes) t = path_translation
    else t = translation

    if(!visible){
        svg.append('g')
            .attr('transform', t)
            .selectAll('dot')
            .data(data[i])
            .enter()
            .append('circle')
                .attr('cx', d=>{
                    return xScale(d.x)
                })
                .attr('cy', d=>{
                    if(d.y == '-Infinity' || d.y == 'Infinity') {
                        return 50
                    }
                    return yScale(d.y)
                })
                .attr('r', 6)
                .style('fill', strokeColors[i])
                .style('stroke', strokeColors[i])
                .on(
                    "mouseover", 
                    function(d) {
                        d3.select(this).attr('r', d3.select(this).attr('r')*2)
                        }
                    )                  
                .on(
                    "mouseout", 
                    function(d) {
                        d3.select(this).attr('r', d3.select(this).attr('r')/2)
                        }
                    )  
                    .on(
                        'click',
                        function(d) {
                            if(dim == 1)
                                $(`#${sliders[i]}`).val(xScale.invert(d3.mouse(this)[0]))
                            else
                            {
                                let coords = {
                                    x: xScale.invert(d3.mouse(this)[0]),
                                    y: yScale.invert(d3.mouse(this)[1])
                                }
                
                                let closest = Math.pow(10, 1000)
                                let index = -1
                
                                for(let j = 0; j < data[i].length; j++)
                                {
                                    if(data[i][j] != null){
                                        let dist = euclideanDistance2D(data[i][j], coords)
                                        if(dist < closest)
                                        {
                                            closest = dist
                                            index = j
                                        }
                                    }
                                    
                                }
                                $(`#${sliders[i]}`).val(index)
                            }
                            //console.log(`d3.mouse(this)[0]: ${d3.mouse(this)[0]}`)
                            //console.log(`currentChartXAxis.invert(d3.mouse(this)[0]) ${xScale.invert(d3.mouse(this)[0])}`)
            
                            /**/
            
                            
                            reload()
                        })
    } else {
        svg.append('path')
        .attr('transform', t)
        .datum(data[i])
        .attr('class', 'input_line')
        .attr('d',
            d3.line()
                .x
                (
                    d=>xScale(d.x)
                )
                .y
                (
                    d=>yScale(d.y)
                )
        )
        .style('display', currentDisplay)
        .style('stroke', strokeColors[i])
        .style('stroke-width', 2)
        .attr('pointer-events', 'visibleStroke')
        .on(
            "mouseover", 
            function(d) {
                d3.select(this).style('stroke-width', 5)
                }
            )                  
        .on(
            "mouseout", 
            function(d) {
                d3.select(this).style('stroke-width', 2)
                }
            )
        .on(
            'click',
            function(d) {
                if(dim == 1)
                    $(`#${sliders[i]}`).val(xScale.invert(d3.mouse(this)[0]))
                else
                {
                    let coords = {
                        x: xScale.invert(d3.mouse(this)[0]),
                        y: yScale.invert(d3.mouse(this)[1])
                    }
    
                    let closest = Math.pow(10, 1000)
                    let index = -1
    
                    for(let j = 0; j < data[i].length; j++)
                    {
                        if(data[i][j] != null){
                            let dist = euclideanDistance2D(data[i][j], coords)
                            if(dist < closest)
                            {
                                closest = dist
                                index = j
                            }
                        }
                        
                    }
                    $(`#${sliders[i]}`).val(index)
                }
                //console.log(`d3.mouse(this)[0]: ${d3.mouse(this)[0]}`)
                //console.log(`currentChartXAxis.invert(d3.mouse(this)[0]) ${xScale.invert(d3.mouse(this)[0])}`)

                /**/

                
                reload()
            }
            )
    }

    if(showAxes)
    {
        svg.append('g').style("font", "1rem times").attr('transform', 'translate(36,480)').call(d3.axisBottom().scale(xScale));
        svg.append('g').style("font", "1rem times").attr('transform', 'translate(36,5)').call(d3.axisLeft().scale(yScale));
    }

    let upper = -8, lower = het-12

    for(let j = 1; j < data[i].length; j++)
    {
        if(crosses_bounds(data[i], yScale, j, upper))
            {
                let intersect = 
                simple_intersection
                    (
                        upper,
                        data[i],
                        xScale,
                        yScale,
                        j
                    )
                
                printSymbol
                    (
                        svg,
                        [intersect],
                        dotColors[i],
                        d3.symbolTriangle,
                        0,
                        t
                    )
            }
            
        if(crosses_bounds(data[i], yScale, j, lower))
            {
                let intersect = 
                simple_intersection
                    (
                        lower,
                        data[i],
                        xScale,
                        yScale,
                        j
                    )
                
                printSymbol
                    (
                        svg,
                        [intersect],
                        dotColors[i],
                        d3.symbolTriangle,
                        180,
                        t
                    )
            }
    }

}