
function OutfitCard({
  name,
  description,
  category,
  number,
  image,
  isSelected,
  onSelect,
}) {
  const visualStyle = image
    ? { backgroundImage: `url(${image})`, backgroundSize: 'cover', backgroundPosition: 'center' }
    : {}

  return (
    <article className="outfit-card">
      <div className={`outfit-card-visual${image ? ' outfit-card-visual--has-image' : ''}`} style={visualStyle}>
        {image && <div className="outfit-card-overlay" />}
        <span className="outfit-number">{number}</span>
        <span className="outfit-category">{category}</span>
      </div>

      <div className="outfit-card-content">
        <p className="outfit-label">KHÁM PHÁ VIỆT PHỤC</p>

        <h3>{name}</h3>

        <p className="outfit-description">
          {description}
        </p>

        <button
          className={`outfit-link outfit-link-button${
            isSelected ? ' outfit-link-button--active' : ''
          }`}
          type="button"
          aria-expanded={isSelected}
          onClick={onSelect}
        >
          {isSelected ? 'Ẩn phong cách' : 'Xem phong cách ↗'}
        </button>
      </div>
    </article>
  )
}

export default OutfitCard
