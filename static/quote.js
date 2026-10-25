document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-quote")
    const message = document.getElementById("message")
    const submitBtn = form.querySelector("button[type='submit']")
    const resultDiv = document.getElementById("quote-result")
    const resultName = document.getElementById("quote-name")
    const resultSymbol = document.getElementById("quote-symbol")
    const resultPrice = document.getElementById("quote-price")

    form.addEventListener('submit', async(e) => {
        e.preventDefault()
        clearMessage ()

        const symbol = {
            symbol: form.symbol.value.trim()
        }

        submitBtn.disabled = true
        submitBtn.textContent = "Submitting..."

        try {
            const response = await fetch("/quote", {
                "method": "post",
                "headers": { "Content-Type": "application/json"},
                "body": JSON.stringify(symbol)
            })

            const result = await response.json()

            if (!response.ok) {
                showMessage(result.message, "danger")
                return
            }

            resultName.textContent = result.name
            resultSymbol.textContent = result.symbol
            resultPrice.textContent = result.price
            resultDiv.style.display = "block"

        } catch(error) {
            showMessage("Network error", "danger")
        } finally {
            submitBtn.disabled = false
            submitBtn.textContent = "Submit"
        }
    })
    function showMessage(text, type) {
        message.textContent = text
        message.className = `text-${type} text-center mt-3`
    }
    function clearMessage() {
        message.textContent = ""
        message.className = "text-center mt-3"
    }
})