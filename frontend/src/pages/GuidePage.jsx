const BINS = [
  ["📄", "Paper & cardboard", "Dry newspapers, office paper, flattened boxes.", "Not: greasy, wet or waxed paper, used tissues."],
  ["🧴", "Plastic", "Rinsed bottles and containers.", "Not: dirty food packaging, plastic bags (unless drop-off exists)."],
  ["🍾", "Glass", "Empty bottles and jars.", "Not: mirrors, window glass, ceramics, light bulbs."],
  ["🥫", "Metal", "Rinsed cans and tins, clean foil.", "Not: batteries, pressurised cans, paint tins with paint."],
  ["🍌", "Organic / compost", "Fruit and vegetable scraps, garden waste.", "Not: plastic, meat/dairy where your compost does not accept it."],
  ["🔋", "Hazardous & e-waste", "Batteries, electronics, chemicals, bulbs.", "Take to a collection point - never the household bin."],
];

const TIPS = [
  "Rinse containers: food residue can ruin a whole batch of recycling.",
  "Flatten boxes to save space.",
  "When in doubt, leave it out of the recycling bin.",
  "Reduce and reuse before you recycle.",
  "Wrap broken glass safely before disposal.",
];

export default function GuidePage() {
  return (
    <div className="container stack page">
      <h1>Waste segregation guide</h1>
      <p>General guidance only. Local rules differ, so check your municipality.</p>
      <div className="grid">
        {BINS.map(([icon, title, yes, no]) => (
          <div className="card" key={title}>
            <p className="result-icon">{icon}</p>
            <h3>{title}</h3>
            <p>✅ {yes}</p>
            <p>🚫 {no}</p>
          </div>
        ))}
      </div>
      <div className="card">
        <h2>Recycling tips</h2>
        <ul>{TIPS.map((t) => <li key={t}>{t}</li>)}</ul>
      </div>
      <p className="small">
        Note: the AI model used here only recognises cardboard, glass, metal, paper, plastic and general trash.
        It cannot detect batteries, food waste, clothing or electronics.
      </p>
    </div>
  );
}
