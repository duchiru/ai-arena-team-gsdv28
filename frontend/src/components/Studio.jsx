
import { useState } from 'react'

function Studio() {
  const [studioOpen, setStudioOpen] = useState(false)

  return (
    <section className="studio" id="studio">
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
    </section>
  )
}

export default Studio
