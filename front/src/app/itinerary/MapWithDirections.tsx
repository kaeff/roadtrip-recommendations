import { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const MapWithDirections = ({ stops }) => {
  useEffect(() => {
    if (stops.length === 0) return;

    // Initialize the map
    const map = L.map('map')
    //.setView(stopToLatLngArray(stops[0]), 7);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    const markers = stops.map((stop, i) => {
      L.marker(stopToLatLngArray(stop)).addTo(map).bindPopup(`(${i+1}) ${stop.destination}`);
    });

    // Draw route between the stops (if there are at least 2 stops)
    if (stops.length > 1) {
      const routeCoordinates = stops.map(stopToLatLngArray);

      // // Create a polyline connecting the stops
      // L.polyline(routeCoordinates, { color: 'blue' }).addTo(map);

      // Fit map bounds to show all stops
      const bounds = L.latLngBounds(routeCoordinates);
      map.fitBounds(bounds);
    }

    // Cleanup function to remove the map instance when the component is unmounted
    return () => {
      map.remove();
    };
  }, [stops]);

  return <div id="map" style={{ height: '400px', width: '100%' }}></div>;
};

export default MapWithDirections;

function stopToLatLngArray(stop: any): L.LatLngExpression {
  return [
    stop.coordinates.latitude,
    stop.coordinates.longitude
  ];
}

