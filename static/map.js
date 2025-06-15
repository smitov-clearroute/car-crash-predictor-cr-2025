const canvas = document.getElementById("lemansMap");
const ctx = canvas.getContext("2d");
const trackImg = new Image();
trackImg.src = "/static/Circuit_de_la_Sarthe_map.webp";

// Generate 30 cars with rainbow colours and staggered progress
// const cars = Array.from({ length: 30 }, (_, i) => ({
//   id: `car${i + 1}`,
//   progress: i / 30,
//   color: `hsl(${(i * 360) / 30}, 100%, 50%)`
// }));

// Random colours for each car
const cars = Array.from({ length: 30 }, (_, i) => ({
  id: `car${i + 1}`,
  progress: i / 30,
  color: `rgb(${Math.floor(Math.random()*256)}, ${Math.floor(Math.random()*256)}, ${Math.floor(Math.random()*256)})`
}));

const trackPoints = [
  [214.34, 636.07], [187.19, 590.5], [147.41, 534.62], [127.92, 507.47],
  [138.64, 476.88], [131.07, 445.21], [112.22, 424.06], [125.11, 399.34],
  [110.12, 346.64], [111.02, 346.64], [111.91, 346.64], [92.13, 302.02],
  [90.8, 302.02], [89.47, 302.02], [70.25, 276.74], [70.25, 275.47],
  [70.25, 274.2], [61.05, 201.88], [64.15, 171.06], [78.21, 147.65],
  [89.93, 125.42], [121.25, 100.2], [146.04, 79.4], [169.95, 53.0],
  [206.64, 57.92], [250.44, 109.72], [274.97, 151.79], [296.07, 192.57],
  [325.64, 238.42], [338.83, 288.56], [367.98, 330.05], [402.75, 390.76],
  [428.31, 435.45], [455.18, 495.37], [478.44, 528.11], [497.22, 564.21],
  [513.08, 646.84], [527.14, 701.17], [526.27, 744.19], [466.23, 737.86],
  [402.7, 727.29], [339.92, 698.72], [291.42, 679.29], [262.43, 652.91],
  [226.03, 670.39], [214.34, 636.07]
];



function interpolateTrack(progress) {
  const total = trackPoints.length;
  const index = Math.floor(progress * (total - 1));
  const nextIndex = (index + 1) % total;
  const localProgress = (progress * (total - 1)) % 1;

  const x = trackPoints[index][0] + localProgress * (trackPoints[nextIndex][0] - trackPoints[index][0]);
  const y = trackPoints[index][1] + localProgress * (trackPoints[nextIndex][1] - trackPoints[index][1]);
  return [x, y];
}

function drawMap() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(trackImg, 0, 0);

  cars.forEach(car => {
    const [x, y] = interpolateTrack(car.progress);
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, Math.PI * 2);
    ctx.fillStyle = car.color;
    ctx.fill();
    ctx.strokeStyle = "#fff";
    ctx.stroke();
  });
}

function animate() {
  cars.forEach(car => {
    car.progress += 0.0002;
    if (car.progress > 1) car.progress = 0;
  });
  drawMap();
  requestAnimationFrame(animate);
}

trackImg.onload = () => {
  drawMap();
  animate();
};
