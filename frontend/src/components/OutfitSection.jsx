
import { useEffect, useRef, useState } from 'react'
import OutfitCard from './OutfitCard'
import cardBg1 from '../assets/card-bg-1.png'
import cardBg2 from '../assets/card-bg-2.png'
import cardBg3 from '../assets/card-bg-3.png'

const outfits = [
  {
    id: 1,
    detailId: 'ao-dai-truyen-thong',
    name: 'ÁO DÀI TRUYỀN THỐNG',
    category: 'THANH LỊCH',
    description:
      'Nét duyên dáng vượt thời gian, dành cho những dịp đặc biệt.',
    image: cardBg1,
    detail: {
      intro:
        'Áo dài truyền thống phù hợp khi người mặc cần sự trang trọng, nền nã và giữ trọn tinh thần thanh lịch của trang phục Việt.',
      useCases: ['Lễ nghi', 'Sự kiện', 'Công sở trang trọng', 'Chụp ảnh kỷ niệm'],
      styling:
        'Ưu tiên cổ cao, tà dài, chất liệu đứng vừa phải như lụa, gấm mỏng hoặc vải trơn có độ rũ. Màu trắng, đỏ sẫm, xanh ngọc, vàng kem và họa tiết nhẹ giúp tổng thể sang mà không quá phô.',
      avoid:
        'Tránh chất liệu quá xuyên thấu, xẻ tà quá cao hoặc phụ kiện lớn khi dùng trong học đường, công sở và các dịp nghi lễ.',
    },
  },
  {
    id: 2,
    detailId: 'ao-tu-than',
    name: 'ÁO TỨ THÂN',
    category: 'DI SẢN',
    description:
      'Khám phá vẻ đẹp của trang phục truyền thống Việt Nam.',
    image: cardBg2,
    detail: {
      intro:
        'Áo tứ thân gợi tinh thần Bắc Bộ, hợp với các hoạt động văn hóa, biểu diễn, lễ hội hoặc những buổi chụp ảnh mang chất dân gian.',
      useCases: ['Lễ hội', 'Biểu diễn văn hóa', 'Du lịch di sản', 'Chụp ảnh truyền thống'],
      styling:
        'Phối áo tứ thân với yếm, váy lĩnh hoặc váy đụp, khăn mỏ quạ và bảng màu nâu, đen, vàng đất, hồng sen. Nên giữ nhịp màu tiết chế để trang phục có chiều sâu cổ truyền.',
      avoid:
        'Không nên dùng quá nhiều chất liệu bóng, phụ kiện hiện đại hoặc phom dáng quá ôm vì dễ làm mất tinh thần mộc mạc của trang phục.',
    },
  },
  {
    id: 3,
    detailId: 'viet-phuc-duong-dai',
    name: 'VIỆT PHỤC ĐƯƠNG ĐẠI',
    category: 'SÁNG TẠO',
    description:
      'Cảm hứng truyền thống trong ngôn ngữ thời trang mới.',
    image: cardBg3,
    detail: {
      intro:
        'Việt phục đương đại dành cho người muốn giữ dấu ấn truyền thống nhưng cần sự linh hoạt trong đời sống hiện đại.',
      useCases: ['Dạo phố', 'Sự kiện sáng tạo', 'Du lịch', 'Gặp gỡ bán trang trọng'],
      styling:
        'Có thể chọn cổ áo, tà áo, họa tiết hoặc bảng màu lấy cảm hứng Việt, sau đó phối với quần ống suông, chân váy trơn hoặc phụ kiện nhỏ. Tinh thần chính là tiết chế và có điểm nhấn văn hóa rõ.',
      avoid:
        'Tránh trộn quá nhiều họa tiết, phụ kiện nghi lễ nặng hoặc chất liệu dày bí khi cần di chuyển nhiều.',
    },
  },
]

function OutfitSection() {
  const [selectedOutfitId, setSelectedOutfitId] = useState(null)
  const detailRef = useRef(null)
  const selectedOutfit = outfits.find((outfit) => outfit.id === selectedOutfitId)

  useEffect(() => {
    if (selectedOutfit && detailRef.current) {
      detailRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      })
    }
  }, [selectedOutfit])

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
            image={outfit.image}
            isSelected={selectedOutfitId === outfit.id}
            onSelect={() =>
              setSelectedOutfitId((currentId) =>
                currentId === outfit.id ? null : outfit.id
              )
            }
          />
        ))}
      </div>

      {selectedOutfit && (
        <div
          className="outfit-detail-grid"
          ref={detailRef}
          aria-label="Chi tiết phong cách Việt phục"
        >
          <article
            className="outfit-detail"
            id={selectedOutfit.detailId}
            key={selectedOutfit.detailId}
          >
            <p className="outfit-detail-number">
              {String(selectedOutfit.id).padStart(2, '0')} · {selectedOutfit.category}
            </p>

            <h3>{selectedOutfit.name}</h3>

            <p className="outfit-detail-intro">{selectedOutfit.detail.intro}</p>

            <div className="outfit-detail-tags">
              {selectedOutfit.detail.useCases.map((useCase) => (
                <span key={useCase}>{useCase}</span>
              ))}
            </div>

            <div className="outfit-detail-columns">
              <div>
                <h4>Gợi ý phối</h4>
                <p>{selectedOutfit.detail.styling}</p>
              </div>

              <div>
                <h4>Nên tránh</h4>
                <p>{selectedOutfit.detail.avoid}</p>
              </div>
            </div>
          </article>
        </div>
      )}
    </section>
  )
}

export default OutfitSection
