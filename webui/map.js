function initLiveMap(mapElementId, driverCount) {
    const map = L.map(mapElementId).setView([34.73, -112.0], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const drivers = {};
    const colors = ['blue', 'green', 'red', 'purple'];
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

    for (let i = 1; i <= driverCount; i++) {
        const ws = new WebSocket(`${wsProtocol}//${window.location.host}/api/itinerary/ws/driver/${i}`);

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
                drivers[i].marker.setLatLng([data.lat, data.lng]);
            }
        };
    }

    return map;
}
