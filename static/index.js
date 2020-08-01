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
    
    currentChartXAxis,currentChartYAxis, 
    currentFaceXAxis, currentFaceYAxis,
    currentPlotXAxis, currentPlotYAxis,
    currentPDiagXAxis, currentPDiagYAxis,

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
        '#plot6'
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
    getRequest
        (i)
        ('face')
        (
            jsonData => {
                currentFaceData = jsonData

                if(isNull(jsonData[i]))
                    $(`#face${i+1}`).empty()
                else
                    update_faceData         
                        ( 
                            jsonData[i], 
                            `#face${i+1}`,
                            dotColors[i]
                        )
                
                update_chart('#chart')
            }
        )

    getRequest
        (i)
        ('persistence')
        (
            (err,jsonData) => {
                if(err) console.log('error fetching data')
                
                if(isNull(jsonData[i]))
                    $(`#pdiag${i+1}`).empty()
                else
                    {
                        update_persistenceDiagram         
                            ( 
                                jsonData[i],
                                `#pdiag${i+1}`,
                                dotColors[i]
                            )
                        
                        /*update_persistenceBarcode        
                            ( 
                                jsonData[i],
                                `#bar${i+1}`,
                                dotColors[i]
                            )*/
                    }
                    
            }
        )
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
        update_boxplot(false)
    }

// updates axes based on confidence interval
const confidence_interval = 
() =>
    {
        let confText = `${getConfidenceInterval()}% of data`

        $('#percentage').text(confText)

        let min, max

        let toRemove = (1.0 - (getConfidenceInterval()/100))/2

        let minExtent = 0, maxExtent = 0

        let data = []

        for(a of currentData)
            {
                if(a != null)
                    {
                        data = data.concat(a)
                    }
            } 
        
        if(getConfidenceInterval() == 100)
        {
            min = 0,
            max = data.length-1
        }
        else
        {
            min = Math.ceil(data.length * toRemove),
            max = data.length-min
        }

        if(data != null)
            {
                let sortedData = 
                    R.sort
                        (
                            (a,b) => a.y-b.y,
                            data
                        )
                
                changeChartAxes([sortedData[min].y, sortedData[max].y])
                
            }

        
    }
    

/**
 * Reloads the graph and each of the faces
 */
const reload = 
() => 
{

    checks(emotions)
    checks(subsections)

    toggleSVG()

    getRequest
        (null)
        ('embedding')
        (
            jsonData => {
                currentData = jsonData
                update_boxplot()
                update_chart('#chart')

                R.forEach
                    (
                        slide,
                        R.range(0,6)
                    )
            }
        )
    
}

const clear_cache = 
() => 
{
    d3.json('clear_cache', d=>{alert(d)})
}

window.onload = function(){
    $('#embeddingType').val('tsne')
    reload()
}