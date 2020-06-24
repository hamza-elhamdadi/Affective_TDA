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
                        dotColors[i]
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
() => 
    {
        R.forEach
        (
            i=>{
                emptyChart(boxplots[i])

                let chartSvg = d3Setup(boxplots[i], currentData[i])

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
                            currentChartXAxis,
                            currentChartYAxis,
                            [data.min, data.max],
                            0.5
                        )

                    printRect
                        (
                            chartSvg,
                            currentChartXAxis,
                            currentChartYAxis,
                            0.33,
                            0.33,
                            0.66,
                            upperQuartile,
                            lowerQuartile,
                            dotColors[i]
                        )
                    
                    printHorizLine
                        (
                            chartSvg,
                            currentChartXAxis,
                            currentChartYAxis,
                            [0.33,0.66],
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
                color
            )
    }

const update_persistenceDiagram = 
(jsonData, chartName, color) =>
    {
        $(chartName).empty()

        let chartSvg = d3Setup(chartName, jsonData, 20, -16),
            height = document.getElementById(chartName.substring(1)).getAttribute('height')
        
        printDot
            (
                chartSvg,
                currentPDiagXAxis,
                currentPDiagYAxis,
                jsonData[0],
                2.5,
                color,
                "translate(22,0)"
            )

        printDot
            (
                chartSvg,
                currentPDiagXAxis,
                currentPDiagYAxis,
                jsonData[1],
                1.5,
                'none',
                "translate(10,0)",
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

        chartSvg.append('g').attr("transform", `translate(22, 130)`).call(d3.axisBottom().scale(currentPDiagXAxis))
        chartSvg.append('g').attr("transform", `translate(20, 0)`).call(d3.axisLeft().scale(currentPDiagYAxis))
    }

const update_persistenceBarcode =
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
    }


const update_chart = 
(chartName) => 
    {
        emptyChart(chartName)

        svg = d3Setup(chartName)

        update_linechart()
        confidence_interval()
    }