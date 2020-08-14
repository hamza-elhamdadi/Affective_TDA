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
 * prints a vertical line
 */
const printVertLine = 
(svg, xAxis, yAxis, y, i) =>
    svg
    .append('line')
        .attr('transform', translation)
        .attr('stroke', 'black')
        .attr('x1',xAxis(i))
        .attr('x2',xAxis(i))
        .attr('y1',yAxis(y[0]))
        .attr('y2',yAxis(y[1]))

/**
 * prints a rectangle
 */
const printRect = 
(svg, xAxis, yAxis, xStart, xVal1, xVal2, yVal1, yVal2, color, stroke='black') =>
{
    let x = xAxis(xStart),
        y = yAxis(yVal1),
        w = xAxis(xVal2)-xAxis(xVal1),
        h = yAxis(yVal2)-yAxis(yVal1)

    if(w == 'Infinity') w = 50

    svg.append('rect')
        .attr('transform', translation)
        .attr('x', x)
        .attr('y', y)
        .attr('width', w)
        .attr('height', h)
        .attr('stroke', 'black')
        .attr('fill', `${color}`)
        .attr('stroke', stroke);
}
    


/**
 * prints a horizontal line
 */
const printHorizLine = 
(svg, xAxis, yAxis, x, i) =>
    svg
    .append('line')
        .attr('transform', translation)
        .attr('stroke', 'black')
        .attr('x1',xAxis(x[0]))
        .attr('x2',xAxis(x[1]))
        .attr('y1',yAxis(i))
        .attr('y2',yAxis(i))

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
(svg, i, xScale, yScale) => {

    let wid = document.getElementById("chart").getAttribute('width'),
        het = document.getElementById("chart").getAttribute('height')

    svg.append('path')
        .attr('transform', translation)
        .datum(currentData[i])
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
                //console.log(`d3.mouse(this)[0]: ${d3.mouse(this)[0]}`)
                //console.log(`currentChartXAxis.invert(d3.mouse(this)[0]) ${xScale.invert(d3.mouse(this)[0])}`)

                /*let coords = {
                    x: xScale.invert(d3.select(this)[0]),
                    y: xScale.invert(d3.select(this)[1])
                }

                console.log(currentData[i])

                let closest = Math.pow(10, 1000)
                let index = -1

                for(let j = 0; j < currentData[i].length; j++)
                {
                    let dist = euclideanDistance2D(currentData[i][j], coords)
                    if(dist < closest)
                    {
                        closest = dist
                        index = j
                    }
                }*/

                $(`#${sliders[i]}`).val(xScale.invert(d3.mouse(this)[0]))
                reload()
            }
            )

    let upper = -8, lower = het-12

    for(let j = 1; j < currentData[i].length; j++)
    {
        if(crosses_bounds(currentData[i], currentChartYAxis, j, upper))
            {
                let intersect = 
                simple_intersection
                    (
                        upper,
                        currentData[i],
                        currentChartXAxis,
                        currentChartYAxis,
                        j
                    )
                
                printSymbol
                    (
                        svg,
                        [intersect],
                        dotColors[i],
                        d3.symbolTriangle,
                        0,
                        translation
                    )
            }
            
        if(crosses_bounds(currentData[i], currentChartYAxis, j, lower))
            {
                let intersect = 
                simple_intersection
                    (
                        lower,
                        currentData[i],
                        currentChartXAxis,
                        currentChartYAxis,
                        j
                    )
                
                printSymbol
                    (
                        svg,
                        [intersect],
                        dotColors[i],
                        d3.symbolTriangle,
                        180,
                        translation
                    )
            }
    }

}