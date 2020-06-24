/**
 * print all dots from json data 
 * with specifications
 * 
 */
const printDot =
(svg, xAxis, yAxis, data, radius, color='black',translate="", stroke='none') =>{
    svg.append('g')
        .attr('transform', translation+translate)
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
}

/**
 * print all dots from json data 
 * with specifications
 * 
 */
const printSymbol =
(svg, xAxis, yAxis, data, color='black', symbol=d3.symbolStar, rotate=0, translate="") =>{
    svg.append('g')
        .attr('transform', translation+translate)
        .selectAll('dot')
        .data(data)
        .enter()
        .append('path')
            .attr("transform", d => `translate(${xAxis(d.x)},${yAxis(d.y)})rotate(${rotate})`)
            .attr('d', d3.symbol().type(symbol).size(20))
            .style('fill', color)
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
        .attr('transform', translation+"translate(20,-3)")
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
(svg, i) => {

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
                    d=>currentChartXAxis(d.x)
                )
                .y
                (
                    d=>currentChartYAxis(d.y)
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
                //console.log(d3.mouse(this)[1])
                console.log(currentChartXAxis(d3.mouse(this)[1]))
                console.log(document.getElementById("chart").getAttribute('height'))
                //console.log(currentChartXAxis.invert(d3.mouse(this)[1]))

                $(`#${sliders[i]}`).val(currentChartXAxis.invert(d3.mouse(this)[0]))
                reload()
            }
            )

    let lastOut1 = false, lastOut2 = false

    for(let j = 1; j < currentData[i].length; j++)
    {
        if((currentChartYAxis(currentData[i][j].y) < -15) != lastOut1)
            {
                let intersect = line_intersection
                (
                    {x:0,y:0},
                    {x:wid,y:0},
                    currentData[i][j-1],
                    currentData[i][j]
                )
                
                printSymbol
                    (
                        svg,
                        currentChartXAxis,
                        currentChartYAxis,
                        [
                            {
                                x:intersect.x,
                                y:currentChartYAxis.invert(0)
                            }
                        ],
                        dotColors[i],
                        d3.symbolTriangle
                    )

                lastOut1 = !lastOut1
            }
            
        if((currentChartYAxis(currentData[i][j].y) > het) != lastOut2)
            {
                let intersect = line_intersection
                (
                    {x:0,y:het-5},
                    {x:wid,y:het-5},
                    currentData[i][j],
                    currentData[i][j-1]
                )
                
                printSymbol
                    (
                        svg,
                        currentChartXAxis,
                        currentChartYAxis,
                        [
                            {
                                x:intersect.x, 
                                y:currentChartYAxis.invert(het-4)
                            }
                        ],
                        dotColors[i],
                        d3.symbolTriangle,
                        180
                    )

                lastOut2 = !lastOut2
            }
    }

}