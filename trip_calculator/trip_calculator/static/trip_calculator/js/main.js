document.addEventListener("DOMContentLoaded", () => {

    const tripButton = document.getElementById("main_trip");
    const friendButton = document.getElementById("main_friend");
    const costButtons = document.querySelectorAll('[id^="main-cost-button-"]');
    const accountButton = document.getElementById("main_account");

    const tripDetail = document.getElementById("main-trip-table");
    const friendDetail = document.getElementById("main-friend-table");
    const costDetails = document.querySelectorAll('[id^="main-cost-tabel-"]');
    const accountDetail = document.getElementById("main-account-table");

    tripButton.addEventListener('click', () => {
        const list = flatten([friendDetail, ...costDetails, accountDetail]);
        showTabel(tripDetail, list);
    });

    friendButton.addEventListener('click', () => {
        const list = flatten([tripDetail, ...costDetails, accountDetail]);
        showTabel(friendDetail, list);
    });

    accountButton.addEventListener('click', () => {
        const list = flatten([tripDetail, friendDetail, ...costDetails]);
        showTabel(accountDetail, list);
    });

    costButtons.forEach(element => {
        element.addEventListener('click', () => {
            const id = element.dataset.id;
            const list = flatten([tripDetail, friendDetail, ...costDetails, accountDetail]);
            hideAll(list);
            const show = document.getElementById(`main-cost-tabel-${id}`);
            show.style.display = 'block';
        });
    });

    function showTabel(toShow, toHide) {
        console.log(toHide);
        toShow.style.display = 'block';
        toHide.forEach(element => element.style.display = 'none');
    }

    function hideAll(toHide) {
        toHide.forEach(element => element.style.display = 'none');
    }

    function flatten(arr) {
        return arr.reduce((acc, val) => acc.concat(val), []);
    }


    document.querySelectorAll("[id^='edit-friend-button-']").forEach(button => {
        button.addEventListener('click', (event) => {
            const inputUser_id = document.querySelector('[id = "friend-edit-modal"] input[name="user_id"]')
            const inputFriend_id = document.querySelector('[id = "friend-edit-modal"] input[name="friend_id"]')
            const clickedButton = event.currentTarget
            inputUser_id.setAttribute('value', clickedButton.getAttribute('data-value-user_id'))
            inputFriend_id.setAttribute('value', clickedButton.getAttribute('data-value-friend_id'))
        })
    })



    document.querySelectorAll("[id^='account-edit-button-']").forEach(button => {
        button.addEventListener('click', (event) => {
            const p = document.getElementById('account-update-modal-p');
            const input = document.getElementById('account-update-modal-input');
            const label = document.getElementById('account-update-modal-label');
            const clickedButton = event.currentTarget.getAttribute('data-value');
            const submitButton = document.getElementById('account-edit-modal-submit-button');

            const settings = {
                'firstname': { pText: 'Provide your new firstname', inputName: 'firstname', inputType: 'text', labelText: 'Firstname' },
                'lastname': { pText: 'Provide your new lastname', inputName: 'lastname', inputType: 'text', labelText: 'Lastname' },
                'email': { pText: 'Provide your new email', inputName: 'email', inputType: 'email', labelText: 'Email' },
                'password': { pText: 'Provide your new password', inputName: 'password', inputType: 'password', labelText: 'Password' }
            }

            const setting = settings[clickedButton];

            if (setting) {
                p.textContent = setting.pText;
                submitButton.disabled = true
                input.setAttribute('name', setting.inputName);
                input.value = '';
                input.setAttribute('type', setting.inputType);
                label.textContent = setting.labelText;
            }
            input.addEventListener('input', () => {
                if (input.value !== '') {
                    submitButton.disabled = false
                }
            })
        });
    });
});
