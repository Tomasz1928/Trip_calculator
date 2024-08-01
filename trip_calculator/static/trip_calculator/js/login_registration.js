document.addEventListener("DOMContentLoaded", () => {

document.getElementById('recovery-account-button').addEventListener('click', validateRecoveryForm);

    function validateForm() {
        if (document.getElementById('login-form')) {validateLoginForm()}
        else {validateRegistrationForm()}
    }

    function validateRegistrationForm() {
        const registrationButton = document.getElementById('registration-button');
        const inputs = document.querySelectorAll('#firstname-input, #lastname-input, #email-input');
        disableButton(registrationButton, inputs)
    }

    function validateRecoveryForm() {
        const recoveryButton = document.getElementById('recovery-submit-button');
        const inputs = document.querySelectorAll('#recovery-email-input');
        console.log(inputs)
        disableButton(recoveryButton, inputs)
    }

    function validateLoginForm() {
        const loginButton = document.getElementById('login-button');
        const inputs = document.querySelectorAll('#username-input, #password-input');
        disableButton(loginButton, inputs)
    }

    function disableButton(button, inputs) {
        inputs.forEach(input => input.addEventListener('input', () => {
            const allFilled = [...inputs].every(input => input.value.trim() !== "");
            console.log(allFilled)
            button.disabled = !allFilled;
        }))
    }

    validateForm();
});
