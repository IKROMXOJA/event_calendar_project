const token = localStorage.getItem('access');

// ADD EVENT
document.getElementById('addEventForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        title: document.getElementById('eventTitle').value,
        description: document.getElementById('eventDescription').value,
        start_date: document.getElementById('eventStart').value,
        end_date: document.getElementById('eventEnd').value
    };
    await fetch('/api/events/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(data)
    });
    location.reload();
});

// EDIT EVENT
document.getElementById('editEventForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('editEventId').value;
    const data = {
        title: document.getElementById('editEventTitle').value,
        description: document.getElementById('editEventDescription').value,
        start_date: document.getElementById('editEventStart').value,
        end_date: document.getElementById('editEventEnd').value
    };
    await fetch(`/api/events/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(data)
    });
    location.reload();
});

// DELETE EVENT
document.getElementById('deleteEventBtn').addEventListener('click', async () => {
    const id = document.getElementById('editEventId').value;
    await fetch(`/api/events/${id}/`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
    });
    location.reload();
});
