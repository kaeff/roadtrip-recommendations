'use client'; // Mark this component as a client component

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import StopsTable from './StopsTable';

export default function ItineraryPage() {
  const searchParams = useSearchParams();
  const destination = searchParams.get('destination');
  const [stops, setStops] = useState([]);

  useEffect(() => {
    const fetchItinerary = async () => {
      if (!destination) return;

      try {
        const response = await fetch(`/api/itinerary?destination=${destination}`);
        const data = await response.json();
        setStops(data.stops || []);
      } catch (error) {
        console.error('Error fetching itinerary:', error);
      }
    };

    fetchItinerary();
  }, [destination]);

  return (
    <div className="p-5">
      <p className="text-2xl font-bold">Itinerary for {destination}</p>

      {stops.length > 0 ? (
        <StopsTable stops={stops} />
      ) : (
        <p>No itinerary available for this destination</p>
      )}
    </div>
  );
}
