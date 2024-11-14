interface ItineraryResponse {
  stops: Stop[];
}
interface Stop {
  destination: string;
  activities: string;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const destination = searchParams.get('destination');
  const traveller_info = "Mid 30s couple travelling in a camper van.";

  try {
    // Replace RemoteRunnable with a direct POST request
    const response = await fetch('http://localhost:8000/itinerary', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ destination, traveller_info }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    // Parse response as ItineraryResponse
    const result: ItineraryResponse = await response.json();

    console.log('ItineraryResponse', JSON.stringify(result, null, 4));

    const stops = result.stops;

    const itinerary = {
      destination,
      stops,
    };

    return new Response(JSON.stringify(itinerary), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Failed to fetch itinerary:', error);
    return new Response(JSON.stringify(error), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
