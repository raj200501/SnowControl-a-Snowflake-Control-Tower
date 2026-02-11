import "./DataTable.css";

type Column<T> = {
  header: string;
  render: (row: T) => string | number;
};

type DataTableProps<T> = {
  columns: Column<T>[];
  data: T[];
};

export function DataTable<T>({ columns, data }: DataTableProps<T>) {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.header}>{column.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.header}>{column.render(row)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
