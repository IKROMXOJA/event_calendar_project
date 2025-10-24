document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const token = localStorage.getItem('access'); // JWT token

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        editable: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },

        events: {
            url: '/api/events/',
            method: 'GET',
            extraParams: {},
            failure: () => alert('Eventlarni yuklashda xato'),
            headers: { Authorization: `Bearer ${token}` }
        },

        dateClick: function(info) {
            const startInput = document.getElementById('eventStart');
            startInput.value = info.dateStr + 'T09:00';
            const endInput = document.getElementById('eventEnd');
            endInput.value = info.dateStr + 'T10:00';
            new bootstrap.Modal(document.getElementById('addEventModal')).show();
        },

        eventClick: function(info) {
            const event = info.event;
            document.getElementById('editEventId').value = event.id;
            document.getElementById('editEventTitle').value = event.title;
            document.getElementById('editEventDescription').value = event.extendedProps.description;
            document.getElementById('editEventStart').value = event.start.toISOString().slice(0,16);
            document.getElementById('editEventEnd').value = event.end.toISOString().slice(0,16);
            new bootstrap.Modal(document.getElementById('editEventModal')).show();
        },

        eventDrop: function(info) {
            fetch(`/api/events/${info.event.id}/drag-update/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    start_date: info.event.start.toISOString(),
                    end_date: info.event.end.toISOString()
                })
            });
        }
    });

    calendar.render();
});
