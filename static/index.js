// left eye:            1-8
// right eye:           9-16
// left eyebrow:        17-26
// right eyebrow:       27-36
// nose:                37-48
// mouth:               49-68
// jawline:             69-83

// 127 combinations of the above

var currentData = [null], 
    currentChartXExtent = [], 
    currentChartYExtent = [], 
    currentFaceXAxis = d=>d, 
    currentFaceYAxis = d=>d;

const emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']
const subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline']
const faces = ['face1', 'face2', 'face3', 'face4', 'face5', 'face6']

let stringize = value => {
    return value.toFixed(4)
}

let findExtents = () => {
    let data = [], max = 0
    for(let i = 0; i < currentData.length; i++){
        if(currentData[i] != null){
            data = data.concat(currentData[i])

            if(currentData[i].length-1 > max){
                max = currentData[i].length-1
            }
        }
    }

    currentChartXExtent = [0,max]
    currentChartYExtent = d3.extent(data.map(e=>e.y))
    
}

let update_linechart = (chartName) => {
    $(chartName).empty()
    findExtents()

    let dotColors = ['blue', 'green', 'red', 'black', 'grey', 'purple']
    let strokeColors = dotColors.reverse()

    let x = $('#frameSlider').val()

    let chartSvg = d3.select(chartName)
    let svgWidth = +chartSvg.attr('width')
    let svgHeight = +chartSvg.attr('height')

    let svgMargin = {left: 10, right: 15, top: 10, bottom: 15},
        chartWidth = svgWidth - (svgMargin.left + svgMargin.right),
        chartHeight = svgHeight - (svgMargin.top + svgMargin.bottom)

    xAxis = d3.scaleLinear().domain(currentChartXExtent).range([0,chartWidth]) 
    yAxis = d3.scaleLinear().domain(currentChartYExtent).range([chartHeight,0])

    for(let i = 0; i < currentData.length; i++){
        if(currentData[i] != null){
            let y = currentData[i][x].y

            chartSvg.append('path')
                    .attr('transform', 'translate(' + svgMargin.left + ',' + svgMargin.top + ')')
                    .datum(currentData[i])
                    .attr('class', 'input_line')
                    .attr('d', d3.line().x(d=>
                        xAxis(d.x)
                    ).y(d=>
                        yAxis(d.y)
                    ))
                    .style('stroke', strokeColors[i])

            chartSvg.append('g')
                    .attr('transform', 'translate(' + svgMargin.left + ',' + svgMargin.top + ')')
                    .append('circle')
                        .attr('cx', xAxis(x))
                        .attr('cy', yAxis(y))
                        .attr('r', 5)
                        .style('stroke', dotColors[i])
        }
    }
            
}

let update_faceData = (chartName, jsonData, emotion) => {
    $(chartName).empty()

    let chartSvg = d3.select(chartName)
    let svgWidth = +chartSvg.attr('width')
    let svgHeight = +chartSvg.attr('height')

    let svgMargin = {left: 10, right: 15, top: 10, bottom: 15},
        chartWidth = svgWidth - (svgMargin.left + svgMargin.right),
        chartHeight = svgHeight - (svgMargin.top + svgMargin.bottom)
    
    let xExtent = d3.extent(jsonData.map(e => e.x))
    let yExtent = d3.extent(jsonData.map(e => e.y))

    currentFaceXAxis = d3.scaleLinear().domain(xExtent).range([0,chartWidth])
    currentFaceYAxis = d3.scaleLinear().domain(yExtent).range([chartHeight,0])

    chartSvg.append('g')
            .attr('transform', 'translate(' + svgMargin.left + ',' + svgMargin.top + ')')
            .selectAll('dot')
            .data(jsonData)
            .enter()
            .append('circle')
                .attr('cx', d=>currentFaceXAxis(d.x))
                .attr('cy', d=>currentFaceYAxis(d.y))
                .attr('r', 2)
}

let checks = () => {
    for(let i = 0; i < emotions.length; i++){
        if($(`#${emotions[i]}`).prop('checked') == true){
            $(`#${emotions[i]}Hidden`).prop('disabled', true)
        }
        else{
            $(`#${emotions[i]}Hidden`).prop('disabled', false)
        }
    }

    for(let i = 0; i < subsections.length; i++){
        if($(`#${subsections[i]}`).prop('checked') == true){
            $(`#${subsections[i]}Hidden`).prop('disabled', true)
        }
        else{
            $(`#${subsections[i]}Hidden`).prop('disabled', false)
        }
    }
}

let reload = () => {
    let num = $('#compare').val() 
    checks()

    d3.json('embedding?' + $('#settings').serialize(), jsonData => {
        currentData = jsonData
        update_linechart('#chart')
    })
    slide()
}

let slide = () => {
    d3.json('face?' + $('#settings').serialize(), jsonData => {
        for(let i = 0; i < emotions.length; i++){
            if(jsonData[i] != null) update_faceData(`#${faces[i]}`, jsonData[i], emotions[i])
            else $(`#${faces[i]}`).empty()
        }
    })
    update_linechart('#chart')
}