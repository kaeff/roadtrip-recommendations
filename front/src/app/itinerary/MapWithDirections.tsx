// MapWithDirections.js

import React, { useEffect, useState } from 'react';
import { GoogleMap, Marker, DirectionsRenderer, LoadScript } from '@react-google-maps/api';

const mapContainerStyle = {
  height: "400px",
  width: "100%"
};

export default const MapWithDirections = ({ stops }) => {
  const [directions, setDirections] = useState(null);
  const defaultCenter = stops.length > 0 ? { lat: stops[0].lat, lng: stops[0].lng } : { lat: 37.7749, lng: -122.4194 }; // Default center

  useEffect(() => {
    if (stops.length > 0) {
      calculateRoute();
    }
  }, [stops]);

  const calculateRoute = async () => {
    const directionsService = new window.google.maps.DirectionsService();

    const waypoints = stops.map(stop => ({
      location: { lat: stop.lat, lng: stop.lng },
      stopover: true
    }));

    const request = {
      origin: waypoints[0].location,
      destination: waypoints[waypoints.length - 1].location,
      waypoints: waypoints.slice(1, -1),
      travelMode: window.google.maps.TravelMode.DRIVING
    };

    directionsService.route(request, (result, status) => {
      if (status === window.google.maps.DirectionsStatus.OK) {
        setDirections(result);
      } else {
        console.error('Error fetching directions:', result);
      }
    });
  };

  return (
    <LoadScript googleMapsApiKey="YOUR_GOOGLE_MAPS_API_KEY">
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={defaultCenter}
        zoom={7}
      >
        {stops.map((stop, index) => (
          <Marker key={index} position={{ lat: stop.lat, lng: stop.lng }} />
        ))}
        {directions && <DirectionsRenderer directions={directions} />}
      </GoogleMap>
    </LoadScript>
  );
};
