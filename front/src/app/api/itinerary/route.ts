import { RemoteRunnable } from "langchain/runnables/remote";

const chain = new RemoteRunnable({ url: `http://localhost:8000/chain/` });

export async function GET(req) {
  const { searchParams } = new URL(req.url);
  const destination = searchParams.get('destination');
  const traveller_info = "Mid 30s couple travelling in a camper van."

  const result = await chain.invoke({
    destination,
    traveller_info
  });

  console.log('chain result', result);

  const itinerary = {
      destination,
      stops: result.stops
  };

  return new Response(JSON.stringify(itinerary), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}


