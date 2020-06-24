/** housekeeping functions **/

//makes the program sleep for ms milliseconds
const sleep = 
(ms) => 
    new Promise
        (
            resolve => 
                setTimeout(resolve, ms)
        )

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