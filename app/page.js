const modelData = [
  { name: '3 Series', value: 26 },
  { name: '5 Series', value: 22 },
  { name: 'X5', value: 18 },
  { name: 'X3', value: 14 },
  { name: '1 Series', value: 10 },
  { name: 'Other', value: 10 },
];

const monthlyPerformance = [
  { month: 'Jan', avgPrice: 19800, avgMpg: 38 },
  { month: 'Feb', avgPrice: 21400, avgMpg: 39 },
  { month: 'Mar', avgPrice: 22600, avgMpg: 41 },
  { month: 'Apr', avgPrice: 23850, avgMpg: 40 },
  { month: 'May', avgPrice: 24900, avgMpg: 42 },
  { month: 'Jun', avgPrice: 26120, avgMpg: 43 },
];

const priceByModel = [
  { model: '3 Series', price: 24100 },
  { model: '5 Series', price: 28850 },
  { model: 'X3', price: 31900 },
  { model: 'X5', price: 38700 },
  { model: '1 Series', price: 19900 },
  { model: 'M Series', price: 46200 },
];

const insightCards = [
  { label: 'Listings', value: '10,781', tone: 'blue' },
  { label: 'Avg. Price', value: '£26.3k', tone: 'green' },
  { label: 'Fuel Economy', value: '41.4 mpg', tone: 'amber' },
  { label: 'Top Model', value: '3 Series', tone: 'purple' },
];

export default function HomePage() {
  return (
    <main className="page-shell">
      <div className="topbar">
        <div>
          <p className="eyebrow">BMW Intelligence</p>
          <h1>Market dashboard</h1>
        </div>
        <button className="primary-btn">Refresh data</button>
      </div>

      <section className="stats-grid">
        {insightCards.map((card) => (
          <article key={card.label} className={`stat-card ${card.tone}`}>
            <span>{card.label}</span>
            <strong>{card.value}</strong>
          </article>
        ))}
      </section>

      <section className="panel-grid">
        <article className="panel large-panel">
          <div className="panel-header">
            <h2>Average price trend</h2>
            <span>Last 6 months</span>
          </div>
          <div className="chart-wrap">
            <svg viewBox="0 0 600 260" preserveAspectRatio="none" className="mini-line">
              <defs>
                <linearGradient id="trendFill" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="#5eead4" stopOpacity="0.55" />
                  <stop offset="100%" stopColor="#5eead4" stopOpacity="0.05" />
                </linearGradient>
              </defs>
              <path d="M0 180 C 90 150, 120 95, 170 120 S 260 160, 330 110 S 440 55, 470 80 S 550 25, 600 40 L600 260 L0 260 Z" fill="url(#trendFill)" />
              <path d="M0 180 C 90 150, 120 95, 170 120 S 260 160, 330 110 S 440 55, 470 80 S 550 25, 600 40" fill="none" stroke="#5eead4" strokeWidth="4" strokeLinecap="round" />
            </svg>
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <h2>Model mix</h2>
            <span>Current inventory</span>
          </div>
          <div className="chart-wrap donut-wrap">
            <div className="donut-chart">
              <div className="donut-center">
                <strong>38%</strong>
                <span>Premium</span>
              </div>
            </div>
            <ul className="legend-list">
              {modelData.map((item) => (
                <li key={item.name}>
                  <span className="dot" style={{ background: item.name === '3 Series' ? '#60a5fa' : item.name === '5 Series' ? '#34d399' : item.name === 'X5' ? '#fbbf24' : item.name === 'X3' ? '#a78bfa' : '#f472b6' }} />
                  <span>{item.name}</span>
                  <b>{item.value}%</b>
                </li>
              ))}
            </ul>
          </div>
        </article>
      </section>

      <section className="panel-grid lower-grid">
        <article className="panel">
          <div className="panel-header">
            <h2>Revenue outlook</h2>
            <span>Price by model</span>
          </div>
          <div className="simple-bars">
            {priceByModel.map((row) => (
              <div key={row.model} className="bar-row">
                <span>{row.model}</span>
                <div className="bar-track">
                  <div className="bar-fill" style={{ width: `${(row.price / 50000) * 100}%` }} />
                </div>
                <strong>£{row.price.toLocaleString()}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <h2>Insights</h2>
            <span>AI summary</span>
          </div>
          <div className="insight-box">
            <p>
              The 3 Series remains the strongest value segment, while X5 pricing continues to lead the premium category.
              Average fuel efficiency improved 6.4% across the most recent listings compared with the previous quarter.
            </p>
          </div>
        </article>
      </section>
    </main>
  );
}
