import { Table, TableHeader, TableBody, TableRow, TableColumn, TableCell } from '@nextui-org/table';

const StopsTable = ({ stops }) => (
  <Table aria-label="Itinerary Stops" bordered shadow={false} css={{ height: 'auto', minWidth: '100%' }}>
    <TableHeader>
      <TableColumn>Day</TableColumn>
      <TableColumn>Destination</TableColumn>
      <TableColumn>Activities</TableColumn>
    </TableHeader>
    <TableBody>
      {stops.map((stop, index) => (
        <TableRow key={index}>
          <TableCell>{index + 1}</TableCell>
          <TableCell>{stop.destination}</TableCell>
          <TableCell>{stop.activities}</TableCell>
        </TableRow>
      ))}
      ))}
    </TableBody>
  </Table>
)

export default StopsTable;