document.addEventListener("DOMContentLoaded", () => {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


    const tripButton = document.getElementById("main_trip");
    const friendButton = document.getElementById("main_friend");
    const costButtons = document.querySelectorAll('[id^="main-cost-button-"]');
    const accountButton = document.getElementById("main_account");

    const tripDetail = document.getElementById("main-trip-table");
    const friendDetail = document.getElementById("main-friend-table");
    const costDetails = document.querySelectorAll('[id^="main-cost-tabel-"]');
    const accountDetail = document.getElementById("main-account-table");

    const actions = {
        'friend': () => showTabel(friendDetail, flatten([tripDetail, ...costDetails, accountDetail])),
        'trip': () => showTabel(tripDetail, flatten([friendDetail, ...costDetails, accountDetail])),
        'account': () => showTabel(accountDetail, flatten([tripDetail, friendDetail, ...costDetails])),
        'hideAll': () => hideAll(flatten([tripDetail, friendDetail, ...costDetails, accountDetail])),
        'cost': (id = getCookie('trip_id')) => {
            actions.hideAll()
            const show = document.getElementById(`main-cost-tabel-${id}`);
            show.style.display = 'block';
        }
    }

    tripButton.addEventListener('click', () => actions.trip());
    friendButton.addEventListener('click', () => actions.friend());
    accountButton.addEventListener('click', () => actions.account());
    costButtons.forEach(element => {
        element.addEventListener('click', () => {
            const id = element.dataset.id;
            actions.cost(id);
        });
    })



    function showTabel(toShow, toHide) {
        toShow.style.display = 'block';
        toHide.forEach(element => element.style.display = 'none');
    }

    function hideAll(toHide) {
        toHide.forEach(element => element.style.display = 'none');
    }

    function flatten(arr) {
        return arr.reduce((acc, val) => acc.concat(val), []);
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }


    function openUpdatedTab() {
        const cookieValue = getCookie('home_page');
        if (cookieValue && actions[cookieValue]) {
            actions[cookieValue]();
        }
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
                'firstname': { pText: 'Provide your new firstname', inputName: 'firstname', inputType: 'text', placeholder: 'Firstname' },
                'lastname': { pText: 'Provide your new lastname', inputName: 'lastname', inputType: 'text', placeholder: 'Lastname' },
                'email': { pText: 'Provide your new email', inputName: 'email', inputType: 'email', placeholder: 'Email' },
                'password': { pText: 'Provide your new password', inputName: 'password', inputType: 'password', placeholder: 'Password' }
            }

            const setting = settings[clickedButton];

            if (setting) {
                p.textContent = setting.pText;
                submitButton.disabled = true
                input.setAttribute('name', setting.inputName);
                input.value = '';
                input.setAttribute('type', setting.inputType);
                input.setAttribute('placeholder', setting.placeholder);
            }
            input.addEventListener('input', () => {
                if (input.value !== '') {
                    submitButton.disabled = false
                }
            })
        });
    });

    document.querySelectorAll("[id^='edit-cost-split-button-']").forEach(button => {
        button.addEventListener('click', (event) => {
            const inputCostId = document.getElementById('cost-status-modal-input-cost-id');
            const inputUserId = document.getElementById('cost-status-modal-input-user_id');
            const inputTripId = document.getElementById('cost-status-modal-input-trip-id');
            const textArea = document.getElementById('cost-status-modal-text');
            const costId = event.currentTarget.getAttribute('data-value-cost-id');
            const friendId = event.currentTarget.getAttribute('data-value-friend-id');
            const tripId = event.currentTarget.getAttribute('data-value-trip-id');
            const friendName = event.currentTarget.getAttribute('data-value-friend-name');


            const text = `Did friend ${friendName} return your money?`
            textArea.textContent = text
            inputCostId.setAttribute('value', costId)
            inputUserId.setAttribute('value', friendId)
            inputTripId.setAttribute('value', tripId)
        });
    })

    document.querySelectorAll("[id^='edit-cost-remove-button-']").forEach(button => {
        button.addEventListener('click', (event) => {
            const inputCostId = document.getElementById('cost-remove-modal-input-cost-id');
            const inputTripId = document.getElementById('cost-remove-modal-input-trip-id');
            const textArea = document.getElementById('cost-remove-modal-text');
            const costId = event.currentTarget.getAttribute('data-value-cost-id');
            const costName = event.currentTarget.getAttribute('data-value-cost-name');
            const tripId = event.currentTarget.getAttribute('data-value-trip-id');


            const text = `You want remove Cost: ${costName} ?`
            textArea.textContent = text
            inputCostId.setAttribute('value', costId)
            inputTripId.setAttribute('value', tripId)
        });
    })

    document.querySelectorAll("[id^='edit-cost-value-button-']").forEach(button => {
        button.addEventListener('click', (event) => {
            const inputCostId = document.getElementById('cost-update-modal-input-cost-id');
            const inputValue = document.getElementById('cost-update-modal-input-value');
            const inputTripId = document.getElementById('cost-update-modal-input-trip-id');
            const textArea = document.getElementById('cost-update-modal-text');
            const costId = event.currentTarget.getAttribute('data-value-cost-id');
            const tripId = event.currentTarget.getAttribute('data-value-trip-id');
            const costName = event.currentTarget.getAttribute('data-value-cost-name');
            const costValue = event.currentTarget.getAttribute('data-value-cost-value');

            const text = `Input new cost value for: ${costName}`
            textArea.textContent = text
            inputCostId.setAttribute('value', costId)
            inputValue.value = null
            inputValue.setAttribute('placeholder', costValue)
            inputTripId.setAttribute('value', tripId)
        });
    })


    document.querySelectorAll("[id^='edit-cost-title-button-']").forEach(button => {
        button.addEventListener('click', (event) => {
            const inputCostId = document.getElementById('cost-title-modal-input-cost-id');
            const inputTitle = document.getElementById('cost-title-modal-input-value');
            const inputTripId = document.getElementById('cost-title-modal-input-trip-id');
            const textArea = document.getElementById('cost-title-modal-text');
            const costId = event.currentTarget.getAttribute('data-value-cost-id');
            const tripId = event.currentTarget.getAttribute('data-value-trip-id');
            const costTitle = event.currentTarget.getAttribute('data-value-cost-title');

            const text = `Input new cost title`
            textArea.textContent = text
            inputCostId.setAttribute('value', costId)
            inputTitle.value = null
            inputTitle.setAttribute('placeholder', costTitle)
            inputTripId.setAttribute('value', tripId)
        });
    })



    openUpdatedTab()
});
