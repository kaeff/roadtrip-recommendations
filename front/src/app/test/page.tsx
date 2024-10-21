"use client";

import {Table, TableHeader, TableColumn, TableBody, TableRow, TableCell} from "@nextui-org/react";

export default function App() {
  return (
        <Table aria-label="Itinerary Stops" bordered shadow={false} css={{ height: 'auto', minWidth: '100%' }}>
          <TableHeader>
            <TableColumn>Destination</TableColumn>
            <TableColumn>Activities</TableColumn>
          </TableHeader>
          <TableBody>
            <TableRow key="1">
              <TableCell>Biarritz, France</TableCell>
              <TableCell>Surf on grand plage</TableCell>
            </TableRow>
            ))}
          </TableBody>
        </Table>
  );
}
