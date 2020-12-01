/********* variables *********/

var svg,
    currentData, 
    
    currentFaceData = 
        {
            'Angry': null,
            'Disgust': null,
            'Fear': null,
            'Happy': null,
            'Sad': null,
            'Surprise': null
        },

    cWidth, cWidth,
    fWidth, fHeight,
    currentChartXExtent, currentChartYExtent,
    currentPlotXExtent, currentPlotYExtent,
    
    currentChartXAxis, currentChartYAxis, 
    currentFaceXAxis, currentFaceYAxis,
    currentPlotXAxis, currentPlotYAxis,
    currentPDiagXAxis, currentPDiagYAxis,
    currentShepardXAxis, currentShepardYAxis,

    rangeUpperBound, 
    rangeLowerBound,

    subsectionranges = {
        'leftEye': [0,8],
        'rightEye': [8,16],
        'leftEyebrow': [16,26],
        'rightEyebrow': [26,36],
        'nose': [36,48],
        'mouth': [48,68],
        'jawline': [68,83]
    }

    subsectionvalues = 'leftEye=leftEye&rightEye=rightEye&leftEyebrow=leftEyebrow&rightEyebrow=rightEyebrow&nose=nose&mouth=mouth&jawline=jawline',
    classes = 'personData', //options: differenceMetric, personData, nonMetric, embeddingType, reld
    subcalls = [
        'leftEye=leftEye&rightEye=rightEye&leftEyebrow=leftEyebrow&rightEyebrow=rightEyebrow&nose=nose&mouth=mouth&jawline=jawline',
        'leftEye=leftEye&rightEye=rightEye&nose=nose',
        'nose=nose&mouth=mouth',
        'leftEyebrow=leftEyebrow&rightEyebrow=rightEyebrow&nose=nose'
    ],

    selected = [true, true, true, true, true, true], //Angry, Disgust, Fear, Happy, Sad, Surprise

    currentDisplay = 'inline',
    visible = true,
    dim = 2,

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
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b"
    ],
    boxplots = 
    [
        '#plot1',
        '#plot2',
        '#plot3',
        '#plot4',
        '#plot5',
        '#plot6',
        '#plot7',
        '#plot8',
        '#plot9',
        '#plot10',
        '#plot11',
        '#plot12',
        '#plot13',
        '#plot14',
        '#plot15',
        '#plot16',
        '#plot17',
        '#plot18'
    ]
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
    path_translation = 'translate(40,0)'


function pathToggle(d) {
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
            
                            
    reload()
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
(i) => 
{
    let twoD = '3d'
    //if(document.getElementById('twoD').checked) twoD = '2d'
    //else twoD = '3d'

    document.getElementById(`value${i+1}`).innerHTML = $(`#frameSlider${i+1}`).val()
    

    getRequest
        (twoD)
        ('face')
        (
            jsonData => {
                currentFaceData = jsonData

                if(isNull(currentFaceData[i]))
                    $(`#face${i+1}`).empty()
                else{
                    update_faceData         
                        ( 
                            currentFaceData[i],
                            `#face${i+1}`,
                            dotColors[i]
                        )
                    
                }

                let eType

                for(d of document.getElementsByName('embeddingType'))
                {
                    if(d.checked == true) eType = d.value
                }

                if(eType != 'reld' && classes != 'reld')
                {
                    getRequest
                        (twoD)
                        ('shepard')
                        (
                            jsonData => {
                                update_chart('#chart1')

                                d3.select('#chart1').append('text').attr('x', 770).attr('y', 470).text(`Rank: ${jsonData[0].toFixed(2)}`)
                            }
                        )
                }
                else{
                    update_chart('#chart1')
                }

                
            }
        )

    
    
    if($(`#embeddingType`).val() == 'reld'){
        getRequest
            (twoD)
            ('embedding')
            (
                jsonData => {
                    currentData = jsonData
                    update_chart('#chart1')
                }
            )
    }
    

    /*getRequest
        (twoD)
        ('persistence')
        (
            (err,jsonData) => {
                if(err) console.log('error fetching data')
                
                if(isNull(jsonData[i]))
                    $(`#pdiag${i+1}`).empty()
                else
                    {
                        //console.log(jsonData)
                        update_persistenceDiagram         
                            ( 
                                jsonData[i],
                                `#pdiag${i+1}`,
                                dotColors[i]
                            )
                        
                        update_persistenceBarcode        
                            ( 
                                jsonData[i],
                                `#bar${i+1}`,
                                dotColors[i]
                            )
                    }
            }
        )*/
}
    
//update linechart axes
const changeChartAxes =
(yExtent) =>
    {
        currentChartYAxis = 
            findAxis
                (
                    yExtent,
                    [cHeight,0]
                )
        
        currentPlotYAxis = 
            findAxis
                (
                    yExtent,
                    [cHeight,0]
                )

        update_linechart()
    }

const small_multiples = 
() =>
{
    for(let i = 0; i < 2; i++)
    {
        for(let j = 0; j < 6; j++)
        {
            for(let k = 0; k < 4; k++)
            {
                let slidevalues = $('#sliders').serialize()
                let settings = $('#settings').find(":input:not(:hidden)").serialize()

                let binary_selected = selected.map(d => {if(d) return 1; else return 0;})

                let emotionvalues = `Angry=${binary_selected[0]}&Disgust=${binary_selected[1]}&Fear=${binary_selected[2]}&Happy=${binary_selected[3]}&Sad=${binary_selected[4]}&Surprise=${binary_selected[5]}`, subs
                let specs, selection = document.getElementsByName('selection')[k+(i*4)].value

                subs = subcalls[k%4]

                if(classes == 'reld') specs = `embeddingType=${selection}`
                else specs = `${classes}=${selection}`

                let request = `embedding?${settings}&${specs}&focalEmotion=${$('#focalEmotion').val()}&${subs}&${emotionvalues}&perplexity=30&${slidevalues}&twoD=3d`

                d3.json(request, jsonData =>{
                    let xExtent, yExtent, chartSvg = d3.select(`#chart${i}_${j}_${k}`)
                    let svgWidth = +chartSvg.attr('width'),
                        svgHeight = +chartSvg.attr('height')
                    let chartWidth = svgWidth - (margin.left + margin.right),
                        chartHeight = svgHeight - (margin.top + margin.bottom)

                    if(dim == 1) xExtent = findTimeExtents(jsonData)
                    else xExtent = findDataExtents(d=>d.x)(jsonData)
                    
                    yExtent = findDataExtents(d=>d.y)(jsonData)

                    let xAxis = findAxis(xExtent, [0,chartWidth]),
                        yAxis = findAxis(yExtent,[chartHeight,0])

                    emptyChart(`#chart${i}_${j}_${k}`)

                    if(!isNull(jsonData[j]))
                    {
                        chartSvg.append("rect")
                            .attr("width", '100%')
                            .attr("height", '100%')
                            .attr("fill", "white")
                            .on('click', function(){
                                selected[j] = !selected[j]
                                reload()
                            })
                        printPath(chartSvg, jsonData, j, xAxis, yAxis, false)
                        //printDot(chartSvg, xAxis, yAxis, [calcDotCoordinates(j, jsonData)], 5, dotColors[j], translation)
                    }
                    else{
                        chartSvg.append("rect")
                            .attr("width", '100%')
                            .attr("height", '100%')
                            .attr("fill", "whitesmoke")
                            .on('click', function(){
                                selected[j] = !selected[j]
                                reload()
                            })
                    }
                })
            }
        }
    
    //toggleSVG()

    }
}

/**
 * Reloads the graph and each of the faces
 */
const reload = 
() => 
{
    let twoD = '3d'

    small_multiples()

    getRequest
        (twoD)
        ('embedding')
        (
            jsonData => {
                currentData = jsonData
                for(let i = 0; i < 6; i++)
                {
                    if(!isNull(currentData[i]))
                    {
                        $(`#frameSlider${i+1}`).attr('max', currentData[i].length-1)
                    }
                        
                }
                update_chart('#chart1')
                R.forEach(slide, R.range(0,6))
            }
        )
    
}

const clear_cache = 
() => 
{
    d3.json(`clear_cache?${$('#settings').serialize()}`, d=>{console.log(d)})
    reload()
}

const save_image = 
() =>
{
    let emotions = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise']
    let filename = prompt('Enter filename: ', 'temp.png')
    
    saveSVGImage(d3.select(`#chart1`), filename)

    for(let i = 0; i < 6; i++)
    {
        if(selected[i])
        {
            let filename = prompt('Enter filename: ', emotions[i] + '.png')

            saveSVGImage(d3.select(`#face${i+1}`), filename)
        }
    }

}

const setClasses = 
(className) => {
    let selections = document.getElementsByName('selection')

    classes = className
    switch(className){
        case 'differenceMetric':
            document.getElementById('title1').innerHTML = 'Bottleneck'
            document.getElementById('title2').innerHTML = 'Wasserstein'
            document.getElementById('class1').style.visibility = 'visible'
            document.getElementById('option1').style.display = 'none'
            document.getElementById('option2').style.display = 'inline'
            document.getElementById('option3').style.display = 'inline'
            document.getElementById('option4').style.display = 'inline'
            document.getElementById('option5').style.visibility = 'hidden'
            for(let i = 0; i < selections.length; i++)
                if(i < 4) selections[i].value = 'bottleneck'
                else selections[i].value = 'wasserstein'
            break
        case 'personData':
            document.getElementById('title1').innerHTML = 'Male'
            document.getElementById('title2').innerHTML = 'Female'
            document.getElementById('class1').style.visibility = 'visible'
            document.getElementById('option1').style.display = 'inline'
            document.getElementById('option2').style.display = 'none'
            document.getElementById('option3').style.display = 'inline'
            document.getElementById('option4').style.display = 'inline'
            document.getElementById('option5').style.visibility = 'hidden'
            for(let i = 0; i < selections.length; i++)
                if(i < 4) selections[i].value = 'M001'
                else selections[i].value = 'F001'
            break
        case 'nonMetric':
            document.getElementById('title1').innerHTML = 'Metric'
            document.getElementById('title2').innerHTML = 'Nonmetric'
            document.getElementById('class1').style.visibility = 'visible'
            document.getElementById('option1').style.display = 'inline'
            document.getElementById('option2').style.display = 'inline'
            document.getElementById('option3').style.display = 'inline'
            document.getElementById('option4').style.display = 'none'
            document.getElementById('option5').style.visibility = 'hidden'
            for(let i = 0; i < selections.length; i++)
                if(i < 4) selections[i].value = 'metric'
                else selections[i].value = 'nonmetric'
            break
        case 'embeddingType':
            document.getElementById('title1').innerHTML = 'MDS'
            document.getElementById('title2').innerHTML = 't-SNE'
            document.getElementById('class1').style.visibility = 'visible'
            document.getElementById('option1').style.display = 'inline'
            document.getElementById('option2').style.display = 'inline'
            document.getElementById('option3').style.display = 'none'
            document.getElementById('option4').style.display = 'inline'
            document.getElementById('option5').style.visibility = 'hidden'
            for(let i = 0; i < selections.length; i++)
                if(i < 4) selections[i].value = 'mds'
                else selections[i].value = 'tsne'
            break
        case 'reld':
            document.getElementById('title1').innerHTML = ''
            document.getElementById('title2').innerHTML = 'Relative Distance'
            document.getElementById('class1').style.visibility = 'hidden'
            document.getElementById('option1').style.display = 'inline'
            document.getElementById('option2').style.display = 'inline'
            document.getElementById('option3').style.display = 'none'
            document.getElementById('option4').style.display = 'inline'
            document.getElementById('option5').style.visibility = 'visible'
            document.getElementsByName('selection')[4].checked = true
            for(let i = 0; i < selections.length; i++)
                selections[i].value = 'reld'
            break
    }
    

    reload()
}

const setSubsections = 
(selectedSubsections, column_number) =>
{
    subsectionvalues = selectedSubsections
    for(let i = 1; i < 9; i++)
    {
        if(i != column_number)
        {
            document.getElementById(`column_${i}`).style.border = ''
        }
        else{
            document.getElementById(`column_${i}`).style.border = 'thick solid black'
        }
    }
    reload()
}

window.onload = function(){
    setClasses('personData')
    setSubsections('leftEye=leftEye&rightEye=rightEye&leftEyebrow=leftEyebrow&rightEyebrow=rightEyebrow&nose=nose&mouth=mouth&jawline=jawline', 1)
    

    reload()
}