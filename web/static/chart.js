export function renderLineChart(canvas, data, labels = []) {
  if (!canvas) {
    return;
  }

  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return;
  }

  const width = canvas.width;
  const height = canvas.height;
  ctx.clearRect(0, 0, width, height);

  const padding = 40;
  if (!data.length) {
    ctx.fillStyle = "#6b7280";
    ctx.font = "14px sans-serif";
    ctx.fillText("No data", padding, height / 2);
    return;
  }

  const minValue = Math.min(...data);
  const maxValue = Math.max(...data);
  const range = maxValue - minValue || 1;

  ctx.strokeStyle = "#cbd5f5";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, height - padding);
  ctx.lineTo(width - padding, height - padding);
  ctx.stroke();

  ctx.strokeStyle = "#4a59ff";
  ctx.lineWidth = 2;
  ctx.beginPath();

  data.forEach((value, index) => {
    const x = padding + (index / (data.length - 1 || 1)) * (width - padding * 2);
    const y = height - padding - ((value - minValue) / range) * (height - padding * 2);
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });

  ctx.stroke();

  ctx.fillStyle = "#4b5563";
  ctx.font = "12px sans-serif";
  ctx.fillText(maxValue.toFixed(2), padding, padding - 8);
  ctx.fillText(minValue.toFixed(2), padding, height - padding + 18);

  if (labels.length) {
    const lastLabel = labels[labels.length - 1];
    ctx.fillText(lastLabel, width - padding - 20, height - padding + 18);
  }
}
