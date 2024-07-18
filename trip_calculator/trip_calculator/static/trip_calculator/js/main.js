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

});
