
function OutfitCard({ name, description, category, number }) {
  return (
    <article className="outfit-card">
      <div className="outfit-card-visual">
        <span className="outfit-number">{number}</span>
        <span className="outfit-category">{category}</span>
        <span className="outfit-symbol">✳</span>
      </div>

      <div className="outfit-card-content">
        <p className="outfit-label">KHÁM PHÁ VIỆT PHỤC</p>

        <h3>{name}</h3>

        <p className="outfit-description">
          {description}
        </p>

        <a className="outfit-link" href="#studio">
          Khám phá thêm ↗
        </a>
      </div>
    </article>
  )
}

export default OutfitCard
