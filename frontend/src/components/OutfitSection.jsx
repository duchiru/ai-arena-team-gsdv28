
import OutfitCard from './OutfitCard'

const outfits = [
  {
    id: 1,
    name: 'Áo dài truyền thống',
    category: 'THANH LỊCH',
    description:
      'Nét duyên dáng vượt thời gian, dành cho những dịp đặc biệt.',
  },
  {
    id: 2,
    name: 'Áo ngũ thân',
    category: 'DI SẢN',
    description:
      'Khám phá vẻ đẹp của trang phục truyền thống Việt Nam.',
  },
  {
    id: 3,
    name: 'Việt phục đương đại',
    category: 'SÁNG TẠO',
    description:
      'Cảm hứng truyền thống trong ngôn ngữ thời trang mới.',
  },
]

function OutfitSection() {
  return (
    <section className="outfits" id="outfits">
      <div className="outfits-heading">
        <p className="section-label">THE COLLECTION</p>

        <h2>Khám phá phong cách Việt.</h2>

        <p>
          Mỗi trang phục là một câu chuyện về văn hóa và bản sắc.
        </p>
      </div>

      <div className="outfit-grid">
        {outfits.map((outfit, index) => (
          <OutfitCard
            key={outfit.id}
            name={outfit.name}
            category={outfit.category}
            description={outfit.description}
            number={String(index + 1).padStart(2, '0')}
          />
        ))}
      </div>
    </section>
  )
}

export default OutfitSection
