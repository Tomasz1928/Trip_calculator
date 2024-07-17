document.addEventListener("DOMContentLoaded", () => {
    const addCost = document.getElementById("add-cost-table");
    const sendButton = document.getElementById("send-button");
    const inputs = document.querySelectorAll('#cost-amount-input, #cost-title-input');
    const inputCheckbox =  document.querySelectorAll('#split-cost-checkbox input[type="checkbox"]')

    const tableBody = document.getElementById("table-body");
    const formDiv = document.getElementById('form_content')
    const crfsToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    inputCheckbox.forEach(input => input.addEventListener('change', checkInputs));
    inputs.forEach(input => input.addEventListener('input', checkInputs));
    addCost.addEventListener("click", addElement);

    document.querySelectorAll('.dropdown-menu').forEach(function (dropdown) {
        dropdown.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    });

    function checkInputs() {
        const allFilled = [...inputs].every(input => input.value.trim() !== "" &&
         document.querySelectorAll('#split-cost-checkbox input[type="checkbox"]:checked').length > 0);
        addCost.disabled = !allFilled;
    }

    function checkTableData() {
        const tableHasData = Array.from(tableBody.children).some(row => row.querySelectorAll('td').length > 0);
        sendButton.style.display = tableHasData ? "block" : "none";
        sendButton.disabled = !tableHasData;
    }

    function collectData() {
        const data = {}
        const inputsCheckBox = document.querySelectorAll('#split-cost-checkbox input[type="checkbox"]:checked');
        inputs.forEach(input => {
            data[input.id.split('-')[1]] = input.value.trim();
            input.value = '';
        });

        const splitList = []

        inputsCheckBox.forEach(input => {
            splitList.push(input.value.trim())
            input.checked = false
        })

        data['split'] = splitList
        return data;
    }

    function createTableCell(content, attributeName) {
        const cell = document.createElement('td');
        cell.setAttribute('data-' + attributeName, content);
        if (typeof content === "string") {
            cell.textContent = content;
        } else { cell.appendChild(content) }
        return cell;
    }

    function createDropdown(items) {
        const dropdownDiv = document.createElement('div');
        dropdownDiv.className = 'dropdown';

        const button = document.createElement('button');
        button.className = 'btn btn-primary dropdown-toggle table-button';
        button.type = 'button';
        button.id = 'dropdownMenuButton';
        button.setAttribute('data-bs-toggle', 'dropdown');
        button.setAttribute('aria-expanded', 'false');
        button.textContent = 'Split';

        const ul = document.createElement('ul');
        ul.className = 'dropdown-menu background-dropdown-color dropdown-list';
        ul.id = 'split-cost-checkbox';
        ul.setAttribute('aria-labelledby', 'dropdownMenuButton');
        ul.style.maxWidth = '250px';
        ul.style.maxHeight = '250px';
        ul.style.whiteSpace = 'nowrap';
        ul.style.overflowY = 'auto';


        items.forEach(item => {
            const li = document.createElement('li');
            li.className = 'ps-2 pe-2';
            li.textContent = item;
            ul.appendChild(li);
        });

        dropdownDiv.appendChild(button);
        dropdownDiv.appendChild(ul);

        return dropdownDiv
    }

    function addElement() {
        const data = collectData();

        const newTableRow = document.createElement('tr');

        newTableRow.append(
            createTableCell(data.title, 'title'),
            createTableCell(data.amount, 'amount'),
            createTableCell(createDropdown(data.split), 'split')
        );

        const colButton = document.createElement('td');
        const button = document.createElement('button');
        button.className = 'btn-close';
        button.addEventListener("click", () => { tableBody.removeChild(newTableRow); checkTableData() });
        colButton.appendChild(button);

        newTableRow.appendChild(colButton);
        tableBody.appendChild(newTableRow);
        checkTableData()
        checkInputs()
    }

        sendButton.addEventListener("click", () => {
        const data = []
        tableBody.querySelectorAll('tr').forEach(row => {
            const title = row.querySelector('[data-title]').textContent;
            const amount = row.querySelector('[data-amount]').textContent;
            const split= []
            row.querySelectorAll('[data-split] li').forEach(li => {split.push(li.textContent)})

            data.push({ title: title, amount: amount, split: split })
        });

        const inputs = [
            { name: 'cost', value: JSON.stringify(data) },
            { name: 'csrfmiddlewaretoken', value: crfsToken }
        ]

            formDiv.innerHTML = ''
            const form = document.createElement('form')
            form.setAttribute("method", "post")

            inputs.forEach(inputData => {
                const input = document.createElement('input');
                input.setAttribute("type", "hidden");
                input.setAttribute("name", inputData.name);
                input.setAttribute("value", inputData.value);
                form.appendChild(input);
            });
            formDiv.append(form)
            form.submit()
            formDiv.innerHTML = ''


        });

    checkTableData();
    checkInputs()
});
