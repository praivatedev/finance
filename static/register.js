document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("form-register")
    const message = document.getElementById("message")
    const submitBtn = form.querySelector("button[type='submit']")

    form.addEventListener('submit' , async function (e) {
        e.preventDefault()
        clearMessage()

        const data = {
            username: form.username.value.trim(),
            password: form.password.value,
            confirmation: form.confirmation.value
        }

        submitBtn.disabled = true
        submitBtn.textContent = "Registering..."

        try {
            const response = await fetch("/register", {
                "method": "POST",
                "headers": { "Content-Type": "application/json"},
                "body": JSON.stringify(data)
            })

            console.log(response)            

            const result = await response.json()
            console.log(result)

            if (!response.ok) {
                showMessage(result.message, "danger")
                return
            }

            window.location.href = "/login"
        } catch (error) {
            showMessage("Network error. Please try again.", "danger")
        } finally {
            submitBtn.disabled = false
            submitBtn.textContent = " Register"
        }
    }) 
    function showMessage(text, type) {
        message.textContent = text
        message.className = `text-${type} text-center mt-3`
    }
    function clearMessage () {
        message.textContent = ""
        message.className = "text-center mt-3"
    }
})

