/**
 * updates the linechart svg for the current
 * specifications and data
 */
const update_linechart = 
() =>
{
    emptyChart('#chart')

    R.forEach
    (
        i=>{
            if(!isNull(currentData[i]))
            {
                printPath
                (
                    svg,
                    i
                )

    
                printDot
                    (
                        svg,
                        currentChartXAxis,
                        currentChartYAxis,
                        [calcDotCoordinates(i)],
                        5,
                        dotColors[i],
                        translation
                    )
            }
        },
        R.range(0,currentData.length)
    )
}
                
/**
 * Shows the boxplots for the selected emotions. 
 */
const update_boxplot = 
(setup=true) => 
    {
        R.forEach
        (
            i=>{
                emptyChart(boxplots[i])

                let chartSvg = d3Setup(boxplots[i], currentData[i], setup)

                if(!isNull(currentData[i]))
                {
                    let data = 
                        calc_box_data
                            (
                                R.map
                                    (
                                        d=>d.y,
                                        currentData[i]
                                    )
                            )
                    
                    let upperQuartile = data.mean + 2*data.std_dev,
                        lowerQuartile = data.mean - 2*data.std_dev
                    
                    if(upperQuartile > data.max) upperQuartile = data.max
                    if(lowerQuartile < data.min) lowerQuartile = data.min

                    printVertLine
                        (
                            chartSvg,
                            currentPlotXAxis,
                            currentPlotYAxis,
                            [data.min, data.max],
                            0.5
                        )

                    printRect
                        (
                            chartSvg,
                            currentPlotXAxis,
                            currentPlotYAxis,
                            -0.5,
                            -0.5,
                            1.5,
                            upperQuartile,
                            lowerQuartile,
                            dotColors[i]
                        )
                    
                    printHorizLine
                        (
                            chartSvg,
                            currentPlotXAxis,
                            currentPlotYAxis,
                            [-0.5,1.5],
                            data.mean
                            
                        )
                    
                }
            },
            R.range(0,currentData.length)
        )

    }

const update_faceData = 
(jsonData, chartName, color) => 
    {
        $(chartName).empty()

        let chartSvg = d3Setup(chartName, jsonData)

        printDot
            (
                chartSvg,
                currentFaceXAxis,
                currentFaceYAxis,
                jsonData,
                2,
                color,
                translation
            )
    }

const update_persistenceDiagram = 
(jsonData, chartName, color) =>
    {
        $(chartName).empty()

        let chartSvg = d3Setup(chartName, jsonData, 20, -16),
            height = document.getElementById(chartName.substring(1)).getAttribute('height')

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
                `translate(23,13)`,
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

/*const update_persistenceBarcode =
(jsonData, chartName, color) =>
    {
        $(chartName).empty()
        let chartSvg = d3Setup(chartName, jsonData)
        R.forEach
            (
                i =>
                    {
                        let yVal2
                        if(jsonData[0][i].y == 'Infinity')
                            {
                                yVal2 = 50
                            }
                        else yVal2 = jsonData[0][i].y
                        printRect
                            (
                                chartSvg,
                                currentChartXAxis,
                                currentChartYAxis,
                                jsonData[0][i].x,
                                jsonData[0][i].x,
                                jsonData[0][i].y,
                                currentChartYAxis.invert(3*i),
                                currentChartYAxis.invert(3*i + 3),
                                color,
                                'none'
                            )
                    },
                R.range(0,jsonData[0].length)
            )
        
        R.forEach
            (
                i =>
                    {
                        let shift = jsonData[0].length
                        printRect
                            (
                                chartSvg,
                                currentChartXAxis,
                                currentChartYAxis,
                                jsonData[1][i].x,
                                jsonData[1][i].x,
                                jsonData[1][i].y,
                                currentChartYAxis.invert(3*(shift + i)),
                                currentChartYAxis.invert(3*(shift + i) + 3),
                                color,
                                'none'
                            )
                    },
                R.range(0,jsonData[1].length)
            )
    }*/


const update_chart = 
(chartName) => 
    {
        emptyChart(chartName)

        svg = d3Setup(chartName)

        update_linechart()
        confidence_interval()
    }