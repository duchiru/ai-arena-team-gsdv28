
import { useEffect, useState } from 'react'
import {
  loadDescriptions,
  loadNotRecommended,
} from '../data/csvService.js'

function CsvDataSection() {
  const [descriptions, setDescriptions] = useState([])
  const [rules, setRules] = useState([])
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState([])

  useEffect(() => {
    let cancelled = false

    async function loadData() {
      setLoading(true)
      setErrors([])

      const results = await Promise.allSettled([
        loadDescriptions(),
        loadNotRecommended(),
      ])

      if (cancelled) return

      const newErrors = []

      if (results[0].status === 'fulfilled') {
        setDescriptions(results[0].value)
      } else {
        setDescriptions([])
        newErrors.push(
          `Không tải được mô tả trang phục: ${results[0].reason.message}`
        )
      }

      if (results[1].status === 'fulfilled') {
        setRules(results[1].value)
      } else {
        setRules([])
        newErrors.push(
          `Không tải được quy tắc phối đồ: ${results[1].reason.message}`
        )
      }

      setErrors(newErrors)
      setLoading(false)
    }

    loadData()

    return () => {
      cancelled = true
    }
  }, [])

  if (loading) {
    return (
      <section className="csv-section">
        <p>Đang tải dữ liệu trang phục...</p>
      </section>
    )
  }

  return (
    <section className="csv-section" id="csv-data">
      <div className="csv-heading">
        <p className="section-label">DỮ LIỆU VĂN HÓA</p>
        <h2>Khám phá kiến thức Việt phục.</h2>
      </div>

      {errors.length > 0 && (
        <div className="csv-error" role="alert">
          <h3>Có dữ liệu chưa tải được</h3>
          {errors.map((error) => (
            <p key={error}>{error}</p>
          ))}
        </div>
      )}

      <div className="csv-group">
        <h3>Thành phần trang phục</h3>

        {descriptions.length === 0 ? (
          <p>Chưa có dữ liệu mô tả để hiển thị.</p>
        ) : (
          <div className="csv-grid">
            {descriptions.map((item, index) => (
              <article
                className="csv-card"
                key={`${item.component}-${index}`}
              >
                <h4>{item.component}</h4>
                <p>{item.description}</p>
              </article>
            ))}
          </div>
        )}
      </div>

      <div className="csv-group">
        <h3>Lưu ý khi phối đồ</h3>

        {rules.length === 0 ? (
          <p>Chưa có dữ liệu lưu ý để hiển thị.</p>
        ) : (
          <div className="csv-grid">
            {rules.map((item, index) => (
              <article
                className="csv-card csv-card-warning"
                key={`${item.dresscode}-${index}`}
              >
                <h4>{item.dresscode}</h4>
                <p>{item.reason}</p>
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

export default CsvDataSection
