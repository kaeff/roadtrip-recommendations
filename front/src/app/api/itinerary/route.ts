import { address } from "framer-motion/client";
import { RemoteRunnable } from "langchain/runnables/remote";

const chain = new RemoteRunnable({ url: `http://localhost:8000/chain/` });

interface ItineraryResponse {
  stops: Stop[]
}
interface Stop {
  place: string,
  description: string
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const destination = searchParams.get('destination');
  const traveller_info = "Mid 30s couple travelling in a camper van."

  const result = await chain.invoke({
    destination,
    traveller_info
  }) as ItineraryResponse;

  const stopsGeocoded = await geocodeBatch(result.stops.map((s) => s.place));
  const stops = result.stops.map((stopFromChain, i) => {
    return { ...stopFromChain, geoProperties: stopsGeocoded[i] };
  });

  const itinerary = {
    destination,
    stops
  };

  console.log('itinerary', JSON.stringify(itinerary, null, 4));

  return new Response(JSON.stringify(itinerary), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}

const MAPBOX_GEOCODE_BATCH_URL = 'https://api.mapbox.com/search/geocode/v6/batch?' +
  `access_token=${process.env.MAPBOX_ACCESS_TOKEN}`

async function geocodeBatch(places: string[]) {
  const requestBody = places.map((place) => {
    return { "q": place, "limit": 1 }
  });
  
  const response = await fetch(MAPBOX_GEOCODE_BATCH_URL, { 
    method: 'POST',
    body: JSON.stringify(requestBody) 
  });
  
  if (response.status !== 200) {
    throw new Error(`Error calling mapbox geocode batch: ${response.status} ${response.statusText} ${await response.text()}`);
  }
  const responseBody = await response.json() as MapboxGeocodeBatchResponse;

  return responseBody.batch.map((b) => b.features[0].properties);
};

export interface MapboxGeocodeBatchResponse {
  batch: Batch[];
}

export interface Batch {
  type: string;
  features: Feature[];
  attribution: string;
}

export interface Feature {
  type: string;
  id: string;
  geometry: Geometry;
  properties: Properties;
}

export interface Geometry {
  type: string;
  coordinates: number[];
}

export interface Properties {
  mapbox_id: string;
  feature_type: string;
  full_address: string;
  name: string;
  name_preferred: string;
  coordinates: Coordinates;
  place_formatted: string;
  bbox: number[];
  context: Context;
}

export interface Context {
  district: District;
  region: Region;
  country: Country;
  place: District;
}

export interface Country {
  mapbox_id: string;
  name: string;
  wikidata_id: string;
  country_code: string;
  country_code_alpha_3: string;
}

export interface District {
  mapbox_id: string;
  name: string;
  wikidata_id?: string;
}

export interface Region {
  mapbox_id: string;
  name: string;
  wikidata_id: string;
  region_code: string;
  region_code_full: string;
}

export interface Coordinates {
  longitude: number;
  latitude: number;
}

