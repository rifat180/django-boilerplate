const toastMessage = (message, color, time) => {
    let pElement = document.createElement("p")
    pElement.className = `toast-message p-3 mb-2 shadow ${color}`
    pElement.style.width = "22rem"
    pElement.innerText = message
    document.querySelector("#toast-message-container").appendChild(pElement)
    dismissToastMessage(pElement, time)
}

const dismissToastMessage = (element, time) => {
    setTimeout(() => {
        element.remove()
    }, time)
}

const dismissAllToastMessage = () => {
    let elements = document.querySelectorAll(".toast-message")
    elements.forEach(element => {
        dismissToastMessage(element, 1500)
    })
}

dismissAllToastMessage()
