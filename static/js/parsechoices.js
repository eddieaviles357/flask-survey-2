let choiceElements = document.querySelectorAll('label')
let inputs = document.querySelectorAll('input')
choiceElements.forEach((ele,idx) => {
    let attrFor = attrID = attrVal = ele.innerHTML.split(' ').join('-')
    ele.setAttribute('for', attrFor)
    inputs[idx].setAttribute('id', attrID)
    inputs[idx].setAttribute('value', attrVal.split('-').join(' '))
})