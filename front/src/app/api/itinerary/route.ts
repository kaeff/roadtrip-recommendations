import { address } from "framer-motion/client";
import { RemoteRunnable } from "langchain/runnables/remote";

const chain = new RemoteRunnable({ url: `http://localhost:8000/chain/` });

interface ItineraryResponse {
  stops: Stop[]
}
interface Stop {
  destination: string,
  activities: string
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const destination = searchParams.get('destination');
  const traveller_info = "Mid 30s couple travelling in a camper van."

  const result = await chain.invoke({
    destination,
    traveller_info
  }) as ItineraryResponse;

  console.log('ItineraryResponse', JSON.stringify(result, null, 4));

  // const stopsGeocoded = await geocodeBatch(result.stops.map((s) => s.place));
  // const stops = result.stops.map((stopFromChain, i) => {
  //   return { ...stopFromChain, geoProperties: stopsGeocoded[i] };
  // });
  const stops = result.stops;

  const itinerary = {
    destination,
    stops
  };

  return new Response(JSON.stringify(itinerary), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}
