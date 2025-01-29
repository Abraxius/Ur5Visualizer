const objectList = document.getElementById('object-list');
const addObjectForm = document.getElementById('add-object-form');

// Neues Objekt hinzufügen
addObjectForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const shape = document.getElementById('shape').value;
    const color = document.getElementById('color').value;
    const x = parseInt(document.getElementById('x').value);
    const y = parseInt(document.getElementById('y').value);

    const response = await fetch('/add_object', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ shape, color, x, y }),
    });

    if (response.ok) {
        alert('Object added successfully!');
        loadObjects(); // Aktualisiere die Liste
    } else {
        alert('Failed to add object.');
    }
});

// Liste der Objekte laden und anzeigen
async function loadObjects() {
    const response = await fetch('/get_objects');
    const data = await response.json();
    objectList.innerHTML = ''; // Liste leeren

    data.objects.forEach((obj) => {
        const li = document.createElement('li');
        li.textContent = `ID: ${obj.id}, Shape: ${obj.shape}, Color: ${obj.color}, Position: (${obj.x}, ${obj.y})`;

        // Button zum Aktualisieren der Position
        const updateBtn = document.createElement('button');
        updateBtn.textContent = 'Update Position';
        updateBtn.onclick = async () => {
            const newX = parseInt(prompt('New X Position:', obj.x));
            const newY = parseInt(prompt('New Y Position:', obj.y));

            const updateResponse = await fetch(`/update_object/${obj.id}?x=${newX}&y=${newY}`, {
                method: 'PUT',
            });

            if (updateResponse.ok) {
                alert('Object updated successfully!');
                loadObjects(); // Aktualisiere die Liste
            } else {
                alert('Failed to update object.');
            }
        };

        li.appendChild(updateBtn);
        objectList.appendChild(li);
    });
}

// Initiales Laden der Objekte
loadObjects();
