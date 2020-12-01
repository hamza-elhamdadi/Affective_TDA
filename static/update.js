const path_helper =
(svg,data,xAxis,yAxis) =>
{
    R.forEach
    (
        index=>{
            if(!isNull(data[index]))
            {
                printPath
                (
                    svg,
                    data,
                    index,
                    xAxis,
                    yAxis
                )

                let coords = calcDotCoordinates(index, data)
                //console.log(currentChartXAxis(coords.x))
    
                printDot
                    (
                        svg,
                        xAxis,
                        yAxis,
                        [coords],
                        6,
                        dotColors[index],
                        path_translation
                    )
            }
        },
        R.range(0,6)
    )
}

/**
 * updates the linechart svg for the current
 * specifications and data
 */
const update_linechart = 
() =>
{
    emptyChart(`#chart1`)
    
    svg.append("rect")
        .attr("width", '100%')
        .attr("height", '100%')
        .attr("fill", "white")
        .on('click', function(){
            visible = !visible
            reload()
        })

    path_helper(svg, currentData, currentChartXAxis, currentChartYAxis)

    //svg.append('g').attr("transform", `translate(25, 305)`).call(d3.axisBottom().scale(currentChartXAxis).ticks(2))
    //svg.append('g').attr("transform", `translate(25, 15)`).call(d3.axisLeft().scale(currentChartYAxis).ticks(2))
}

const update_faceData = 
(jsonData, chartName, color) => 
    {
        $(chartName).empty()

        let chartSvg = d3Setup(chartName, jsonData, null, true)

        chartSvg.append("rect")
                .attr("width", '100%')
                .attr("height", '100%')
                .attr("fill", "white");

        let greyData = [], colorData = []

        let subs = subsectionvalues.split('&').map(d=>{return d.split('=')[0]})
        
        for(s of subsections)
        {
            let sect = jsonData.slice(subsectionranges[s][0],subsectionranges[s][1])
            if(subs.includes(s))
            {
                colorData = colorData.concat(sect)
            }
            else{
                greyData = greyData.concat(sect)
            }
        }

        if(!(greyData.length == 0))
        {
            printDot
            (
                chartSvg,
                currentFaceXAxis,
                currentFaceYAxis,
                greyData,
                2,
                'lightgrey',
                translation
            )
        }

        printDot
            (
                chartSvg,
                currentFaceXAxis,
                currentFaceYAxis,
                colorData,
                2,
                color,
                translation
            )
    }

const update_persistenceDiagram = 
(jsonData, chartName, color) =>
    {
        $(chartName).empty()

        let chartSvg = d3Setup(chartName, '', jsonData, 20, -16),
            height = document.getElementById(chartName.substring(1)).getAttribute('height')

        chartSvg.append("rect")
                .attr("width", '100%')
                .attr("height", '100%')
                .attr("fill", "white");

        printSymbol
            (
                chartSvg,
                jsonData[0].map(d=>{return {x:currentPDiagXAxis(d.x),y:currentPDiagYAxis(d.y)}}),
                color,
                d3.symbolDiamond,
                0,
                `translate(28,8)`
            )

        printDot
            (
                chartSvg,
                currentPDiagXAxis,
                currentPDiagYAxis,
                jsonData[1],
                2,
                'white',
                `translate(28,11)`,
                color
            )

        printDiagLine
            (
                chartSvg, 
                currentPDiagXAxis, 
                currentPDiagYAxis, 
                [
                    0,
                    document.getElementById(chartName.substring(1)).getAttribute('width')
                ], 
                [
                    0,
                    height
                ]
            )

        chartSvg.append('g').attr("transform", `translate(25, 130)`).call(d3.axisBottom().scale(currentPDiagXAxis).ticks(5))
        chartSvg.append('g').attr("transform", `translate(25, 15)`).call(d3.axisLeft().scale(currentPDiagYAxis).ticks(5))
    }

const update_shepard =
(chartName, jsonData) =>
    {
        $(chartName).empty()
        
        let chartSvg = d3Setup(chartName, jsonData),
            height = document.getElementById('shepard').getAttribute('height')

        chartSvg.append("rect")
            .attr("width", '100%')
            .attr("height", '100%')
            .attr("fill", "white");
        
        printDot
            (
                chartSvg,
                currentShepardXAxis,
                currentShepardYAxis,
                jsonData,
                2,
                'white',
                `translate(28,11)`,
                'blue'
            )
    
        chartSvg.append('g').attr("transform", `translate(25, 380)`).call(d3.axisBottom().scale(currentShepardXAxis).ticks(5))
        chartSvg.append('g').attr("transform", `translate(25, 15)`).call(d3.axisLeft().scale(currentShepardYAxis).ticks(5))
    }

const update_chart = 
(chartName) => 
    {
        emptyChart(chartName)

        svg = d3Setup(chartName)

        update_linechart()
        //confidence_interval()
    }