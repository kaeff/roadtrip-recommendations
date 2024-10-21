'use client';

import { useState } from 'react';
import { Input, Button, Spacer } from '@nextui-org/react';
import { useRouter } from 'next/navigation'; // Use the Next.js App Router's useRouter hook

export default function PlanPage() {
  const [destination, setDestination] = useState('');
  const router = useRouter();

  const handleSubmit = () => {
    // Navigate to the itinerary page with the destination as a query parameter
    router.push(`/itinerary?destination=${destination}`);
  };

  return (
    <div className="p-5">
      <p className="text-2xl font-bold">Where do you want to go?</p>
      <Spacer y={1} />
      <Input
        clearable
        underlined
        labelPlaceholder="Destination"
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
      />
      <Spacer y={1.5} />
      <Button color="primary" onPress={handleSubmit}>Suggest an itinerary</Button>
    </div>
  );
}
