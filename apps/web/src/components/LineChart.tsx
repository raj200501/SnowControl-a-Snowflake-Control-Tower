import "./LineChart.css";

type LineChartProps = {
  points: { label: string; value: number }[];
  stroke?: string;
};

export function LineChart({ points, stroke = "#38bdf8" }: LineChartProps) {
  if (points.length === 0) {
    return <div className="chart-empty">No data</div>;
  }
  const values = points.map((point) => point.value);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const height = 120;
  const width = 360;

  const coords = points.map((point, idx) => {
    const x = (idx / Math.max(points.length - 1, 1)) * width;
    const range = max - min || 1;
    const y = height - ((point.value - min) / range) * height;
    return `${x},${y}`;
  });

  return (
    <svg className="line-chart" viewBox={`0 0 ${width} ${height}`}>
      <polyline points={coords.join(" ")} fill="none" stroke={stroke} strokeWidth="3" />
    </svg>
  );
}
