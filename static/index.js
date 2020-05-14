/********* variables *********/

var 
    svg,
    currentData, currentFaceData,

    cWidth, cWidth,
    fWidth, fHeight,
    currentChartXExtent, currentChartYExtent,
    
    currentChartXAxis,currentChartYAxis, 
    currentFaceXAxis, currentFaceYAxis,

    rangeUpperBound, 
    rangeLowerBound,

    boxWidth = 100

const 
    //all valid emotions
    emotions = 
    [
        'Angry', 
        'Disgust',
        'Fear', 
        'Happy', 
        'Sad', 
        'Surprise'
    ],
    //all valid face subsections
    subsections = 
    [
        'leftEye', 
        'rightEye', 
        'leftEyebrow', 
        'rightEyebrow', 
        'nose', 
        'mouth', 
        'jawline'
    ],
    //all valid face svg ids
    faces = 
    [
        'face1', 
        'face2', 
        'face3', 
        'face4', 
        'face5', 
        'face6'
    ],
    //all valid slider ids
    sliders = 
    [
        'frameSlider1', 
        'frameSlider2', 
        'frameSlider3', 
        'frameSlider4', 
        'frameSlider5', 
        'frameSlider6'
    ],
    //all dot colors used in linegraph
    dotColors = 
    [
        'blue', 
        'green', 
        'red', 
        'black', 
        'grey', 
        'purple'
    ],
    //all line stroke colors used in linegraph
    strokeColors = dotColors.reverse(),
    //margins for SVGs
    margin = 
    {
        left: 10, 
        right: 15, 
        top: 10, 
        bottom: 15
    },
    translation = 'translate(' + margin.left + ',' + margin.top + ')'

/** housekeeping functions **/

//makes the program sleep for ms milliseconds
const sleep = 
ms => 
    new Promise
        (
            resolve => 
                setTimeout(resolve, ms)
        )

/**
 * finds the extents of the input svg for the axis
 * if the axis is x, the extent is 0 to the max length of the datasets
 * if the axis is not x, it is y, 
 * and the extent is the minimum to maximum values of all the datasets
 */
const findExtents = 
x => 
    x ? 
        R.compose(
            d3.extent,
            R.flip(R.append)([0]),
            R.reduce(R.max, -Infinity),
            R.map(R.length)
        )
      : 
        R.compose(
            d3.extent,
            R.map(d=>d.y),
            R.reduce(R.concat,[]),
            R.filter(d=>d!=null)
        )

/**
 * returns the axis for the domain and range
 */
const findAxis = 
(dom, ran) =>
    d3.scaleLinear()
            .domain(dom)
            .range(ran)

/**
 * returns the x and y values for the dot
 * corresponding to the particular slider[i]
 */
const calcDotCoordinates =
i => 
    {
        let xVal = $(`#${sliders[i]}`).val()
        
        return {
            x: xVal,
            y: currentData[i][xVal].y
        }
    }

/**
 * makes a GET request and handles the response 
 * takes in the route to GET from
 * the function func to handle the response
 */
const getRequest = 
extra =>
    route => 
        func => 
            d3.json(
                `${route}?${$('#settings').serialize()}&emotion=${extra}`,
                func
            )

/**
 * handles current checked options
 * for face subsections and emotions
 */
const checks = 
() =>
    R.forEach(
        R.ifElse(
            isChecked,          //if
            toggleHidden(true), //then
            toggleHidden(false) //else
        )
    )     

/**
 * perform setup calculations for d3 svg
 */
const d3Setup = 
(chartName, data=null) =>
    {
        let xExtent, yExtent

        let chartSvg = d3.select(chartName)

        let svgWidth = +chartSvg.attr('width'),
            svgHeight = +chartSvg.attr('height')

        let chartWidth = svgWidth - (margin.left + margin.right),
            chartHeight = svgHeight - (margin.top + margin.bottom)

        if(R.equals(chartName,'#chart') 
            && R.equals(getChartType(),'linechart'))
        {
            xExtent = 
                findExtents
                    (true)
                    (currentData)
            yExtent = 
                findExtents
                    (false)
                    (currentData)

            cWidth = chartWidth
            cHeight = chartHeight
        }
        else if(R.equals(chartName,'#chart') 
                && R.equals(getChartType(),'boxplot'))
        {
            xExtent = [0,5]
            yExtent = 
                findExtents
                    (false)
                    (currentData)
                
            cWidth = chartWidth
            cHeight = chartHeight
        }
        else
        {
            xExtent = d3.extent(data.map(e => e.x))
            yExtent = d3.extent(data.map(e => e.y))

            fWidth = chartWidth
            fHeight = chartHeight
        }

        setMinimumYVal(yExtent[0])
        setMaximumYVal(yExtent[1])
        
        let xAxis = 
                findAxis
                    (
                        xExtent,
                        [0,chartWidth]
                    ),
            yAxis =
                findAxis
                    (
                        yExtent,
                        [chartHeight,0]
                    )

        if(R.equals(chartName,'#chart'))
        {
            currentChartXExtent = xExtent
            currentChartYExtent = yExtent
            currentChartXAxis = xAxis
            currentChartYAxis = yAxis
        }
        else
        {
            currentFaceXAxis = xAxis
            currentFaceYAxis = yAxis
        }

        return chartSvg
    }

/**
 * print all dots from json data 
 * with specifications
 * 
 */
const printDot =
(svg, xAxis, yAxis, data, radius) =>{
    svg.append('g')
        .attr('transform', translation)
        .selectAll('dot')
        .data(data)
        .enter()
        .append('circle')
            .attr('cx', d=>xAxis(d.x))
            .attr('cy', d=>yAxis(d.y))
            .attr('r', radius)
}
    
/**
 * print path on the chart svg for the emotion[i]
 */
const printPath =
(svg, i) =>
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

/**
 * TODO
 */
const printVertLine = 
(svg, data, i) =>
    svg
    .append('g')
        .selectAll('vertlines')
        .data(data)
        .enter()
        .append('line')
            .attr('x1',i)
            .attr('x2',i)
            .attr('y1',d=>d.min)
            .attr('y2',d=>d.max)
            .attr('stroke', 'black')
            .style('width', 40)


/**
 * TODO
 */
const printRect = null

/**
 * TODO
 */
const printHorizLine = null

/** getters and setters **/

//gets the minimum value for the y axis
const getMinimumYVal = 
() =>
    $('#yMin')
        .val()

//gets the maximum value for the y axis
const getMaximumYVal = 
() =>
    $('#yMax')
        .val()

//sets the minimum value for the y axis
const setMinimumYVal =
value =>
    $('#yMin')
        .val(value)

//sets the maximum value for the y axis
const setMaximumYVal =
value =>
    $('#yMax')
        .val(value)

//gets the value of the chart type (can be linechart or boxplot)
const getChartType = 
() => 
    $(`#graphType`)
        .val()

//checks if value is null
const isNull =
    R.equals(null)

//gets whether the button has been checked
const isChecked = 
button => 
    R.equals
    (
        $(`#${button}`)
            .prop('checked'),
        true
    )

//toggles hidden button
const toggleHidden = 
button => 
    disable => 
        $(`#${button}Hidden`)
            .prop
            (
                'disabled', 
                disable
            )

/**
 * empties the svg for the chart 
 * with chartname stored in "chart"
 */
const emptyChart = 
chart =>
    $(chart).empty()

/****** web functions ******/            

const calc_box_data = 
data => 
{ 
    let m = 
        R.compose
            (
                R.mean,
            )
            (data)
    
    let sd = 
        R.compose
            (
                Math.sqrt,
                R.mean,
                R.map(d=>R.multiply(d-m,d-m))
            )
            (data)

    let mn = R.reduce(R.min, Infinity, data)
        mx = R.reduce(R.max, -Infinity, data)

    return {
        mean: m,
        std_dev: sd,
        min: mn,
        max: mx
    }
}
    



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
                        5
                    )
            }
        },
        R.range(0,currentData.length)
    )
}
    
                
/**
 * TODO: finish printing the box plots (replace the dots that are currently on the page)
 */
const update_boxplot = 
() => 
    {
        console.clear()
        console.log('Data for Box_Plots')

        R.forEach
        (
            i=>{
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
                    
                    console.log(data)
                    
                    let upperQuartile = data.mean + 2*data.std_dev,
                        lowerQuartile = data.mean - 2*data.std_dev
                    
                    printDot
                        (
                            svg,
                            currentChartXAxis,
                            currentChartYAxis,
                            [{x:i,y:data.mean}],
                            3
                        )

                    printDot
                        (
                            svg,
                            currentChartXAxis,
                            currentChartYAxis,
                            [{x:i,y:data.min}],
                            3
                        )
                    
                    printDot
                        (
                            svg,
                            currentChartXAxis,
                            currentChartYAxis,
                            [{x:i,y:data.max}],
                            3
                        )

                    printDot
                        (
                            svg,
                            currentChartXAxis,
                            currentChartYAxis,
                            [{x:i,y:upperQuartile}],
                            3
                        )

                    printDot
                        (
                            svg,
                            currentChartXAxis,
                            currentChartYAxis,
                            [{x:i,y:lowerQuartile}],
                            3
                        )
                    
                }
            },
            R.range(0,currentData.length)
        )

    }

const update_faceData = 
(jsonData, emotion, chartName) => 
    {
        $(chartName).empty()

        let chartSvg = d3Setup(chartName, jsonData)

        printDot
            (
                chartSvg,
                currentFaceXAxis,
                currentFaceYAxis,
                jsonData,
                2
            )
    }


const update_chart = 
chartName => 
    {
        emptyChart(chartName)

        console.log('dude, it got here')

        svg = d3Setup(chartName)

        console.log('but also it got here')

        if(R.equals(getChartType(), 'linechart')) update_linechart()
        else update_boxplot()
    }

//update linechart axes
const changeChartAxes =
() =>
    {
        console.log('here')

        let yExtent = [getMinimumYVal(),getMaximumYVal()]

        console.log('then here')

        currentChartYAxis = 
            findAxis
                (
                    yExtent,
                    [cHeight,0]
                )

        console.log('and here')

        update_linechart()
    }

/**
 * performs the slide functionality of the webapp
 * 1. Gets the data by requesting from /face for the respective slider (i)
 * 2. Handles the response
 *      a. checks if the face data was returned for the respective slider
 *      b. if it was not, it empties the corresponding SVG
 *      c. else it calls update_faceData
 */
const slide = 
i => 
    getRequest
        (i)
        ('face')
        (
            jsonData => {
                currentFaceData = jsonData

                if(isNull(jsonData[i]))
                    $(`#${faces[i]}`).empty()
                else
                    update_faceData         
                    ( 
                        jsonData[i], 
                        emotions[i],
                        `#${faces[i]}`
                    )
                
                update_chart('#chart')
            }
        )

/**
 * Reloads the graph and each of the faces
 */
const reload = 
() => 
{
    console.log('this is the first check')

    checks(emotions)
    checks(subsections)

    getRequest
        (null)
        ('embedding')
        (
            jsonData => {
                currentData = jsonData
                update_chart('#chart')

                R.forEach
                (
                    slide,
                    R.range(0,6)
                )
            }
        )
    
}

/**
 * Plays through the frames of the particular emotion
 */
const play = 
async i => 
{
    let slider = $(`#${sliders[i]}`),
        rangeList = R.append
                    (
                        0,
                        R.range
                        (
                            0,
                            parseInt(slider.attr('max'))+1
                        )
                    )
            
    for (index of rangeList)
    {
        slider.val(index)
        slide(i)
        await sleep(100)
    }

    return false
}

window.onload = function(){
    console.log('did it even get here?')
    reload()
}