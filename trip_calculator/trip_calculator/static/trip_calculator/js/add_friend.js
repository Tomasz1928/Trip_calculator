document.addEventListener("DOMContentLoaded", () => {
    const addFriendButton = document.getElementById("add-friend-button");
    const sendButton = document.getElementById("send-button");
    const inputs = document.querySelectorAll('#firstname-input, #lastname-input, #email-input');
    const tableBody = document.getElementById("table-body");

    if (!tableBody) {
        console.error('Element with id "table-body" not found.');
        return;
    }

    inputs.forEach(input => input.addEventListener('input', checkInputs));

    addFriendButton.addEventListener("click", addElement);

    function checkInputs() {
        const allFilled = [...inputs].every(input => input.value.trim() !== "");
        addFriendButton.disabled = !allFilled;
    }

    function checkTableData() {
        if (!tableBody) {
            console.error('Element with id "table-body" not found.');
            return;
        }
        // Sprawdź, czy tableBody ma dzieci (wiersze tabeli)
        const tableHasData = Array.from(tableBody.children).some(row => row.querySelectorAll('td').length > 0);
        sendButton.style.display = tableHasData ? "block" : "none";
        sendButton.disabled = !tableHasData;
    }

    function collectData() {
        const data = {};
        inputs.forEach(input => {
            data[input.id.split('-')[0]] = input.value.trim();
            input.value = '';
        });
        return data;
    }

    function createTableCell(content, attributeName) {
        const cell = document.createElement('td');
        cell.setAttribute('data-' + attributeName, content);
        cell.textContent = content;
        return cell;
    }

    function addElement() {
        const data = collectData();

        const newTableRow = document.createElement('tr');

        newTableRow.append(
            createTableCell(data.firstname, 'firstname'),
            createTableCell(data.lastname, 'lastname'),
            createTableCell(data.email, 'email')
        );

        const colButton = document.createElement('td');
        const button = document.createElement('button');
        button.className = 'btn-close';
        button.addEventListener("click", () => { tableBody.removeChild(newTableRow); checkTableData() });
        colButton.appendChild(button);

        newTableRow.appendChild(colButton);
        tableBody.appendChild(newTableRow);
        checkInputs();
        checkTableData();
    }

    sendButton.addEventListener("click", () => {
        const data = []
        tableBody.querySelectorAll('tr').forEach(row => {
            const firstname = row.querySelector('[data-firstname]').textContent;
            const lastname = row.querySelector('[data-lastname]').textContent;
            const email = row.querySelector('[data-email]').textContent;

            data.push({
                firstname: firstname,
                lastname: lastname,
                email: email
            });
        });
        console.log(data)
    });

    checkInputs();
    checkTableData();
});
