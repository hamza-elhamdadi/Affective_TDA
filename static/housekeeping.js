/** housekeeping functions **/

//makes the program sleep for ms milliseconds
const sleep = 
(ms) => 
    new Promise
        (
            resolve => 
                setTimeout(resolve, ms)
        )

const full =
() =>
{
    let selections = document.getElementsByName('selection')
    if(selections[0].checked == true || selections[4].checked == true) return true
    else return false
    /*let setup = true
    for(sec of subsections){
        if(document.getElementById(sec).checked == false) setup = false
    }
    return setup*/
}

/**
 * makes a GET request and handles the response 
 * takes in the route to GET from
 * the function func to handle the response
 */
const getRequest =
twoD =>
route => 
    func => {
        let slidevalues = $('#sliders').serialize()
        let settings = $('#settings').find(":input:not(:hidden)").serialize()

        let specs, selection

        for(e of document.getElementsByName('selection'))
        {
            if(e.checked) selection = e.value
        }

        if(classes == 'reld') specs = `embeddingType=${selection}`
        else specs = `${classes}=${selection}`

        let binary_selected = selected.map(d => {if(d) return 1; else return 0;})

        let emotionvalues = `Angry=${binary_selected[0]}&Disgust=${binary_selected[1]}&Fear=${binary_selected[2]}&Happy=${binary_selected[3]}&Sad=${binary_selected[4]}&Surprise=${binary_selected[5]}` //

        let request = `${route}?${settings}&${specs}&focalEmotion=${$('#focalEmotion').val()}&${subsectionvalues}&${emotionvalues}&perplexity=30&${slidevalues}&twoD=${twoD}`
        //console.log(request)

        return d3.json(request, func)
    }
        

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

//gets the percent confidence interval 
const getConfidenceInterval = 
() =>
    $('#confInterval')
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

const toggleSVG = 
() =>
    {
        for(let i = 0; i < emotions.length; i++)
            {
                if(isChecked(emotions[i]))
                {
                    for(let j = 0; j < 3; j++){
                    //document.getElementById(`plot${i+1+(6*j)}`)
                    //        .setAttribute('display', 'inline') 
                    document.getElementById(`face${i+1+(6*j)}`)
                            .setAttribute('display', 'inline')
                    document.getElementById(`pdiag${i+1+(6*j)}`)
                            .setAttribute('display', 'inline')
                    }
                }
                else
                {
                    for(let j = 0; j < 3; j++){
                    //document.getElementById(`plot${i+1+(6*j)}`)
                    //        .setAttribute('display', 'none') 
                    document.getElementById(`face${i+1+(6*j)}`)
                            .setAttribute('display', 'none')
                    document.getElementById(`pdiag${i+1+(6*j)}`)
                            .setAttribute('display', 'none')
                    }
                }
            }
    }
    

/**
 * empties the svg for the chart 
 * with chartname stored in "chart"
 */
const emptyChart = 
chart =>
    $(chart).empty()

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