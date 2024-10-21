import { Table, TableHeader, TableBody, TableRow, TableColumn, TableCell } from '@nextui-org/table';

const StopsTable = ({ stops }) => (
  <Table aria-label="Itinerary Stops" bordered shadow={false} css={{ height: 'auto', minWidth: '100%' }}>
    <TableHeader>
      <TableColumn>Place</TableColumn>
      <TableColumn>Activities</TableColumn>
    </TableHeader>
    <TableBody>
      {stops.map((stop, index) => (
        <TableRow key={index}>
          <TableCell>{stop.place}</TableCell>
          <TableCell>{stop.description}</TableCell>
        </TableRow>
      ))}
      ))}
    </TableBody>
  </Table>
)

export default StopsTable;