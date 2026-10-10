
import { useState } from 'react'
import studioBg1 from '../assets/studio-bg-1.png'
import studioBg2 from '../assets/studio-bg-2.png'
import studioBg3 from '../assets/studio-bg-3.png'

function Studio() {
  const [studioOpen, setStudioOpen] = useState(false)

  return (
    <section className="studio" id="studio">
      <div className="studio-bg-wrapper">
        <div className="studio-bg-images">
          <img src={studioBg1} alt="Cổng đền cổ kính Việt Nam" className="studio-bg-img" />
          <img src={studioBg2} alt="Rồng trên mái ngói truyền thống" className="studio-bg-img" />
          <img src={studioBg3} alt="Kiến trúc chùa Việt Nam" className="studio-bg-img" />
        </div>
        <div className="studio-bg-overlay" />
      </div>

      <div className="studio-content">
        <p className="section-label">
          YOUR STYLE, YOUR STORY
        </p>

        <h2>Sẵn sàng tạo phong cách riêng?</h2>

        <p>
          Khám phá từng thành phần trang phục và ý nghĩa của chúng.
        </p>

        <button
          className="secondary-button"
          onClick={() => setStudioOpen(!studioOpen)}
        >
          {studioOpen ? 'Đóng Studio' : 'Khám phá Studio'}
        </button>

        {studioOpen && (
          <div className="studio-message">
            <h3>Chào mừng đến với Studio!</h3>
            <p>
              Tại đây, bạn sẽ khám phá trang phục Việt Nam
              và tìm hiểu cách phối đồ phù hợp với từng hoàn cảnh.
            </p>
          </div>
        )}
      </div>
    </section>
  )
}

export default Studio
