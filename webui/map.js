
function initLiveMap(mapElementId, driverCount) {
    // Initialize map
    const map = L.map(mapElementId).setView([34.73, -112.0], 13);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Driver markers and routes
    const drivers = {};
    const colors = ['blue', 'green', 'red', 'purple'];

    // Initialize WebSocket connections
    for (let i = 1; i <= driverCount; i++) {
        const ws = new WebSocket(`ws://${window.location.host}/api/itinerary/ws/driver/${i}`);

        // Create driver marker
        const icon = L.divIcon({
            className: 'driver-marker',
            html: `<div class="driver-icon" style="background-color: ${colors[i-1]};">${i}</div>`,
            iconSize: [24, 24]
        });

        drivers[i] = {
            marker: L.marker([0, 0], {icon}).addTo(map),
            route: null,
            ws: ws
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'location_update') {
                // Update marker position
                drivers[i].marker.setLatLng([data.lat, data.lng]);

                // Update route line (if applicable)
                // ...
            }
        };
    }

    return map;
}
