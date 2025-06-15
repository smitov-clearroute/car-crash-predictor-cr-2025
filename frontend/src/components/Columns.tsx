import { columns } from "../util/columns";

export default function Columns() {
  return (
    <thead className="bg-gray-900 sticky top-0 z-10 text-white font-bold">
    <tr>
      {columns.map((col, idx) => (
        <th
          key={idx}
          className="px-4 py-2 text-center"
          style={{ minWidth: col.width }}
        >
          {col.label}
        </th>
      ))}
    </tr>
  </thead>
  );
}
