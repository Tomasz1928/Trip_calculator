document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('create_trip_modal').addEventListener('click', updateModalInfo)
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('create_trip_submit').addEventListener('click', createAndSendForm)
});

async function collectAllData() {
    return {
        title: document.getElementById('Trip_name').value,
        description: document.getElementById('Trip_description').value,
        startDate: document.getElementById('Trip_start_date').value,
        endDate: document.getElementById('Trip_end_date').value,
        csrfmiddlewaretoken: document.querySelector('[name="csrfmiddlewaretoken"]').value,
        names: Array.from(document.querySelectorAll('#checkboxGroup input[type="checkbox"]:checked')).map(checkbox => checkbox.value)
    }
}

async function updateModalInfo() {
    data = await collectAllData()
    console.log(data)

    const summaryText = `
                Trip Name: ${data.title}<br>
                Trip start: ${data.startDate}<br>
                Trip end: ${data.endDate}<br>
                Description: ${data.description}<br>
                Squad: ${data.names.join(', ')}`;

    const summaryElement = document.createElement('p');
    summaryElement.innerHTML = summaryText;

    const modalBody = document.getElementById('modal_summary_trip_create');
    modalBody.innerHTML = '';
    modalBody.appendChild(summaryElement);
}

async function createAndSendForm(){
const data = await collectAllData()
const form = document.createElement('form');
form.setAttribute('method', 'POST');
form.setAttribute('action', 'http://127.0.0.1:8000/trip/create_trip/');
console.log(data)

for (const key in data) {

    if (data.hasOwnProperty(key)) {
        const input = document.createElement('input');
        input.setAttribute('type', 'hidden');
        input.setAttribute('name', key);
        input.setAttribute('value', data[key])
        form.appendChild(input);
    }
}
const modalBody = document.getElementById('modal_summary_trip_create');
modalBody.appendChild(form);
form.submit();
}