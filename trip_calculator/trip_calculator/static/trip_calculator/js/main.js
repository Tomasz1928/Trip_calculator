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
            const p = document.getElementById('account-update-modal-p')
            const input = document.getElementById('account-update-modal-input')
            const label = document.getElementById('account-update-modal-label')
            const clickedButton = event.currentTarget.getAttribute('data-value')

            switch (clickedButton) {
                case 'firstname':
                    p.textContent = 'Provide your new firstname'
                    input.setAttribute('name','firstname')
                    input.setAttribute('type', 'text')
                    label.textContent= 'Firstname'
                    break;

                case 'lastname':
                    p.textContent = 'Provide your new lastname'
                    input.setAttribute('name','lastname')
                    input.setAttribute('type', 'text')
                    label.textContent= 'Lastname'
                    break;

                case 'email':
                    p.textContent = 'Provide your new email'
                    input.setAttribute('name','email')
                    input.setAttribute('type', 'email')
                    label.textContent= 'Email'
                    break;

                case 'password':
                    p.textContent = 'Provide your new password'
                    input.setAttribute('name','password')
                    input.setAttribute('type', 'password')
                    label.textContent= 'Password'
                    break;
            }
        })
    })
});
