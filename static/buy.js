document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-buy")
    const buy_btn = form.querySelector('button[type="submit"]')
    const message = document.getElementById("message")

    console.log("form found:", form)

    form.addEventListener("submit", async(e) => {
        e.preventDefault()
        clear_message()

        const body = {
            "symbol": form.symbol.value.trim()
        }

        buy_btn.disabled = true
        buy_btn.textContent = "Buying..."

        try {
            const response = await fetch("/buy", {
                "method": "post",
                "headers": { "Content-Type": "application/json" },
                "body": JSON.stringify(body)
            })

            const result = await response.json()

            if (!response.ok){
                show_message(result.message, "danger")
                return
            }
            show_message(`Bought ${result.symbol} at $${result.price}`, "success")

        } catch (error) {
            show_message(error.message, "danger")

        } finally {
            buy_btn.textContent = "Buy"
            buy_btn.disabled = false
        }
    })

    function show_message(text, type) {
        message.textContent = text
        message.className = `text-${type} text-center mt-3`
    }
    function clear_message() {
        message.textContent = ""
        message.className = 'text-center mt-3'
    }

})


