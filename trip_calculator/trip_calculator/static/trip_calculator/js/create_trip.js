document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById('create-trip')
    const tripName = document.getElementById('trip_name')
    const tripStart = document.getElementById('trip_start_date')
    const tripEnd = document.getElementById('trip_end_date')
    const tripDescription = document.getElementById('trip_description')
    const checkboxes = document.querySelectorAll('#trip-squad-checkbox input[type="checkbox"]');
    const formDiv = document.getElementById('form_content')
    const crfsToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    ['#trip_name', '#trip_start_date', '#trip_end_date', '#trip_description'].forEach(selector => {
        const element = document.querySelector(selector);
        element.addEventListener('input', collectData)
    })

    checkboxes.forEach(checkbox => checkbox.addEventListener('change', collectData))

    const overview = {
        trip_name: document.getElementById('trip-overall-name'),
        trip_date: document.getElementById('trip-overall-start'),
        trip_description: document.getElementById('trip-overall-description'),
        trip_squad: document.getElementById('trip-overall-squad')
    }

    document.querySelectorAll('.dropdown-menu').forEach(function (dropdown) {
        dropdown.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    });


    function collectData() {
        const squad = document.querySelectorAll('#trip-squad-checkbox input[type="checkbox"]:checked');
        selectedNames = []
        selectedUserId = []
        squad.forEach(checkbox => {
            selectedUserId.push(parseInt(checkbox.value.trim()));
            const label = document.querySelector(`label[for="${checkbox.id}"]`)
            if (label) { selectedNames.push(label.getAttribute('data-value')) }

        });

        data = {
            tripName: tripName.value,
            tripStart: tripStart.value,
            tripEnd: tripEnd.value,
            tripDescription: tripDescription.value,
            tripSquad: selectedNames,
            tripSquadIds: selectedUserId
        }

        Overview(data)
        return data
    }

    function Overview(data) {
        overview.trip_name.textContent = 'Trip name: ' + data.tripName
        overview.trip_date.textContent = `Trip date: ${data.tripStart} - ${data.tripEnd}`
        overview.trip_description.textContent = 'Trip description: ' + data.tripDescription
        overview.trip_squad.textContent = 'Trip squad: ' + data.tripSquad.join(', ')
    }


    function validateCreateTrip() {
        const inputs = document.querySelectorAll('#trip_name, #trip_start_date, #trip_end_date');
        inputs.forEach(input => input.addEventListener('input', () => {
            const allFilled = [...inputs].every(input => input.value.trim() !== "");
            button.disabled = !allFilled;
        }))
    }

    button.addEventListener('click', () => {
        formDiv.innerHTML = ''
        const data = collectData()
        const form = document.createElement('form')
        form.setAttribute("method", "post")

        const inputs = [
            { name: 'name', value: data.tripName },
            { name: 'start', value: data.tripStart },
            { name: 'end', value: data.tripEnd },
            { name: 'description', value: data.tripDescription },
            { name: 'squad', value: JSON.stringify(data.tripSquadIds) },
            { name: 'csrfmiddlewaretoken', value: crfsToken }
        ];

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
    })


    validateCreateTrip();
});
