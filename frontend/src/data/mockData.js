export const DRIVERS_2026 = {
  VER: { name: "Max Verstappen", team: "Red Bull Racing", code: "VER" },
  PER: { name: "Sergio Perez", team: "Red Bull Racing", code: "PER" },
  NOR: { name: "Lando Norris", team: "McLaren", code: "NOR" },
  PIA: { name: "Oscar Piastri", team: "McLaren", code: "PIA" },
  LEC: { name: "Charles Leclerc", team: "Ferrari", code: "LEC" },
  HAM: { name: "Lewis Hamilton", team: "Ferrari", code: "HAM" },
  RUS: { name: "George Russell", team: "Mercedes", code: "RUS" },
  ANO: { name: "Kimi Antonelli", team: "Mercedes", code: "ANO" },
  ALO: { name: "Fernando Alonso", team: "Aston Martin", code: "ALO" },
  STR: { name: "Lance Stroll", team: "Aston Martin", code: "STR" },
  GAS: { name: "Pierre Gasly", team: "Alpine", code: "GAS" },
  DOO: { name: "Jack Doohan", team: "Alpine", code: "DOO" },
  TSU: { name: "Yuki Tsunoda", team: "Racing Bulls", code: "TSU" },
  LAW: { name: "Liam Lawson", team: "Racing Bulls", code: "LAW" },
  HUL: { name: "Nico Hulkenberg", team: "Kick Sauber", code: "HUL" },
  BOR: { name: "Gabriel Bortoleto", team: "Kick Sauber", code: "BOR" },
  SAI: { name: "Carlos Sainz", team: "Williams", code: "SAI" },
  ALB: { name: "Alexander Albon", team: "Williams", code: "ALB" },
  OCO: { name: "Esteban Ocon", team: "Haas", code: "OCO" },
  BEA: { name: "Oliver Bearman", team: "Haas", code: "BEA" },
};

export const TEAM_COLORS = {
  "Red Bull Racing": "#3671C6",
  McLaren: "#FF8000",
  Ferrari: "#E8002D",
  Mercedes: "#27F4D2",
  "Aston Martin": "#229971",
  Alpine: "#FF87BC",
  "Racing Bulls": "#6692FF",
  "Kick Sauber": "#52E252",
  Williams: "#64C4FF",
  Haas: "#B6BABD",
};

export const CALENDAR = {
  2024: [
    "Bahrain Grand Prix",
    "Saudi Arabian Grand Prix",
    "Australian Grand Prix",
    "Japanese Grand Prix",
    "Chinese Grand Prix",
    "Miami Grand Prix",
    "Emilia Romagna Grand Prix",
    "Monaco Grand Prix",
    "Canadian Grand Prix",
    "Spanish Grand Prix",
    "Austrian Grand Prix",
    "British Grand Prix",
    "Hungarian Grand Prix",
    "Belgian Grand Prix",
    "Dutch Grand Prix",
    "Italian Grand Prix",
    "Azerbaijan Grand Prix",
    "Singapore Grand Prix",
    "United States Grand Prix",
    "Mexico City Grand Prix",
    "São Paulo Grand Prix",
    "Las Vegas Grand Prix",
    "Qatar Grand Prix",
    "Abu Dhabi Grand Prix",
  ],
  2025: [
    "Australian Grand Prix",
    "Chinese Grand Prix",
    "Japanese Grand Prix",
    "Bahrain Grand Prix",
    "Saudi Arabian Grand Prix",
    "Miami Grand Prix",
    "Emilia Romagna Grand Prix",
    "Monaco Grand Prix",
    "Spanish Grand Prix",
    "Canadian Grand Prix",
    "Austrian Grand Prix",
    "British Grand Prix",
    "Hungarian Grand Prix",
    "Belgian Grand Prix",
    "Dutch Grand Prix",
    "Italian Grand Prix",
    "Azerbaijan Grand Prix",
    "Singapore Grand Prix",
    "United States Grand Prix",
    "Mexico City Grand Prix",
    "São Paulo Grand Prix",
    "Las Vegas Grand Prix",
    "Qatar Grand Prix",
    "Abu Dhabi Grand Prix",
  ],
  2026: [
    "Australian Grand Prix",
    "Chinese Grand Prix",
    "Japanese Grand Prix",
    "Bahrain Grand Prix",
    "Saudi Arabian Grand Prix",
    "Miami Grand Prix",
    "Emilia Romagna Grand Prix",
    "Monaco Grand Prix",
    "Spanish Grand Prix",
    "Canadian Grand Prix",
    "Austrian Grand Prix",
    "British Grand Prix",
    "Hungarian Grand Prix",
    "Belgian Grand Prix",
    "Dutch Grand Prix",
    "Italian Grand Prix",
    "Azerbaijan Grand Prix",
    "Singapore Grand Prix",
    "United States Grand Prix",
    "Mexico City Grand Prix",
    "São Paulo Grand Prix",
    "Las Vegas Grand Prix",
    "Qatar Grand Prix",
    "Abu Dhabi Grand Prix",
  ],
};

export const RACE_STATUS = {
  past: ["Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix"],
  future: [
    "Japanese Grand Prix",
    "Chinese Grand Prix",
    "Miami Grand Prix",
    "Emilia Romagna Grand Prix",
    "Monaco Grand Prix",
    "Spanish Grand Prix",
    "Canadian Grand Prix",
    "Austrian Grand Prix",
    "British Grand Prix",
    "Hungarian Grand Prix",
    "Belgian Grand Prix",
    "Dutch Grand Prix",
    "Italian Grand Prix",
    "Azerbaijan Grand Prix",
    "Singapore Grand Prix",
    "United States Grand Prix",
    "Mexico City Grand Prix",
    "São Paulo Grand Prix",
    "Las Vegas Grand Prix",
    "Qatar Grand Prix",
    "Abu Dhabi Grand Prix",
  ],
};

function generatePredictions(year, gpName) {
  const isPast = year < 2026 || (year === 2026 && RACE_STATUS.past.includes(gpName));

  const basePositions = [
    { driver: "VER", base: 1.2, uncertainty: 0.4 },
    { driver: "NOR", base: 2.5, uncertainty: 0.6 },
    { driver: "LEC", base: 2.8, uncertainty: 0.7 },
    { driver: "HAM", base: 3.5, uncertainty: 0.8 },
    { driver: "RUS", base: 4.2, uncertainty: 0.9 },
    { driver: "PIA", base: 4.8, uncertainty: 0.8 },
    { driver: "ANO", base: 6.0, uncertainty: 1.2 },
    { driver: "SAI", base: 6.5, uncertainty: 1.0 },
    { driver: "ALO", base: 7.0, uncertainty: 1.1 },
    { driver: "PER", base: 7.8, uncertainty: 1.3 },
    { driver: "GAS", base: 9.0, uncertainty: 1.2 },
    { driver: "TSU", base: 10.0, uncertainty: 1.4 },
    { driver: "STR", base: 11.0, uncertainty: 1.5 },
    { driver: "ALB", base: 12.0, uncertainty: 1.3 },
    { driver: "OCO", base: 13.0, uncertainty: 1.6 },
    { driver: "HUL", base: 14.0, uncertainty: 1.5 },
    { driver: "DOO", base: 15.0, uncertainty: 1.8 },
    { driver: "LAW", base: 16.0, uncertainty: 1.7 },
    { driver: "BOR", base: 17.0, uncertainty: 2.0 },
    { driver: "BEA", base: 18.0, uncertainty: 1.9 },
  ];

  const predictions = basePositions.map((p, i) => {
    const noise = (Math.random() - 0.5) * 0.4;
    const predPos = p.base + noise;
    const confidence = Math.max(0.65, Math.min(0.98, 1 - p.uncertainty / 20));
    const driverInfo = DRIVERS_2026[p.driver];
    return {
      position: i + 1,
      driver: p.driver,
      driverName: driverInfo.name,
      team: driverInfo.team,
      predictedPosition: Number(predPos.toFixed(1)),
      uncertainty: Number(p.uncertainty.toFixed(1)),
      confidence: Number(confidence.toFixed(2)),
    };
  });

  let actualResults = null;
  let comparison = null;
  let accuracy = null;

  if (isPast) {
    const actualPositions = [...basePositions]
      .sort(() => Math.random() - 0.5)
      .map((p, i) => ({
        position: i + 1,
        driver: p.driver,
        driverName: DRIVERS_2026[p.driver].name,
        team: DRIVERS_2026[p.driver].team,
      }));

    actualResults = actualPositions;

    comparison = predictions.map((pred) => {
      const actual = actualPositions.find((a) => a.driver === pred.driver);
      const actualPos = actual ? actual.position : 15;
      return {
        driver: pred.driver,
        driverName: pred.driverName,
        team: pred.team,
        actual: actualPos,
        predicted: pred.predictedPosition,
        delta: Number((pred.predictedPosition - actualPos).toFixed(1)),
      };
    });

    const absErrors = comparison.map((c) => Math.abs(c.delta));
    const mae = Number((absErrors.reduce((a, b) => a + b, 0) / absErrors.length).toFixed(2));
    const closeMatches = absErrors.filter((e) => e <= 3).length;
    const exactMatches = absErrors.filter((e) => e === 0).length;

    const actualPodium = comparison.sort((a, b) => a.actual - b.actual).slice(0, 3);
    const predictedPodium = comparison.sort((a, b) => a.predicted - b.predicted).slice(0, 3);
    const podiumCorrect = actualPodium.filter((ap) =>
      predictedPodium.some((pp) => pp.driver === ap.driver)
    ).length;

    accuracy = {
      mae,
      closeMatches: `${closeMatches}/${absErrors.length}`,
      podiumAccuracy: `${podiumCorrect}/3`,
      exactMatches,
      totalDrivers: absErrors.length,
    };

    comparison.sort((a, b) => a.actual - b.actual);
  }

  return { predictions, actualResults, comparison, accuracy, isPast };
}

export function getPrediction(year, gpName) {
  return generatePredictions(year, gpName);
}

export function getDriverData(_driverCode) {
  const features = {
    avg_position: Math.random() * 10 + 1,
    position_std: Math.random() * 3 + 0.5,
    avg_points: Math.random() * 15 + 2,
    total_points: Math.random() * 200 + 20,
    podium_rate: Math.random() * 0.5 + 0.1,
    top10_rate: Math.random() * 0.4 + 0.5,
    position_volatility: Math.random() * 2 + 0.5,
    avg_grid: Math.random() * 10 + 1,
    grid_to_finish_delta: (Math.random() - 0.5) * 3,
    track_avg_position: Math.random() * 10 + 1,
    track_races_count: Math.floor(Math.random() * 10 + 1),
  };
  return features;
}
