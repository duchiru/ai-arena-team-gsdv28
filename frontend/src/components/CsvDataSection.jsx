
import { useEffect, useMemo, useState } from 'react'
import {
  loadDescriptions,
  loadNotRecommended,
} from '../data/csvService.js'

const dataTypeLabels = {
  all: 'Tất cả dữ liệu',
  description: 'Thành phần trang phục',
  rule: 'Lưu ý phối đồ',
}

function normalizeText(value) {
  return value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
}

function getPreview(text) {
  if (text.length <= 150) return text

  return `${text.slice(0, 150).trim()}...`
}

function CsvDataSection() {
  const [descriptions, setDescriptions] = useState([])
  const [rules, setRules] = useState([])
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [dataType, setDataType] = useState('all')
  const [topic, setTopic] = useState('all')
  const [openCardId, setOpenCardId] = useState(null)

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

  const knowledgeCards = useMemo(() => {
    const descriptionCards = descriptions.map((item, index) => ({
      id: `description-${item.component}-${index}`,
      type: 'description',
      badge: 'Thành phần',
      title: item.component,
      body: item.description,
      topics: [item.component],
    }))

    const ruleCards = rules.map((item, index) => ({
      id: `rule-${item.dresscode}-${index}`,
      type: 'rule',
      badge: 'Lưu ý',
      title: item.dresscode,
      body: item.reason,
      topics: item.dresscode
        .split('/')
        .map((value) => value.trim())
        .filter(Boolean),
    }))

    return [...descriptionCards, ...ruleCards]
  }, [descriptions, rules])

  const topicOptions = useMemo(() => {
    const values = knowledgeCards.flatMap((card) => card.topics)

    return Array.from(new Set(values)).sort((a, b) =>
      a.localeCompare(b, 'vi')
    )
  }, [knowledgeCards])

  const filteredCards = useMemo(() => {
    const keyword = normalizeText(searchTerm.trim())

    return knowledgeCards.filter((card) => {
      const matchesType = dataType === 'all' || card.type === dataType
      const matchesTopic = topic === 'all' || card.topics.includes(topic)
      const searchableText = normalizeText(
        `${card.title} ${card.body} ${card.topics.join(' ')}`
      )

      return (
        matchesType &&
        matchesTopic &&
        (keyword === '' || searchableText.includes(keyword))
      )
    })
  }, [dataType, knowledgeCards, searchTerm, topic])

  function resetFilters() {
    setSearchTerm('')
    setDataType('all')
    setTopic('all')
    setOpenCardId(null)
  }

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
        <p>
          Tìm nhanh thành phần, bối cảnh và lưu ý phối đồ để chọn áo dài phù
          hợp hơn với từng điều kiện.
        </p>
      </div>

      {errors.length > 0 && (
        <div className="csv-error" role="alert">
          <h3>Có dữ liệu chưa tải được</h3>
          {errors.map((error) => (
            <p key={error}>{error}</p>
          ))}
        </div>
      )}

      {knowledgeCards.length === 0 ? (
        <p className="csv-empty">Chưa có dữ liệu để hiển thị.</p>
      ) : (
        <>
          <div className="csv-controls" aria-label="Bộ lọc kiến thức Việt phục">
            <label className="csv-field">
              <span>Tìm kiếm</span>
              <input
                type="search"
                value={searchTerm}
                onChange={(event) => {
                  setSearchTerm(event.target.value)
                  setOpenCardId(null)
                }}
                placeholder="Nhập áo dài, công sở, lễ nghi..."
              />
            </label>

            <label className="csv-field">
              <span>Nhóm dữ liệu</span>
              <select
                value={dataType}
                onChange={(event) => {
                  setDataType(event.target.value)
                  setOpenCardId(null)
                }}
              >
                {Object.entries(dataTypeLabels).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>

            <label className="csv-field">
              <span>Trang phục / bối cảnh</span>
              <select
                value={topic}
                onChange={(event) => {
                  setTopic(event.target.value)
                  setOpenCardId(null)
                }}
              >
                <option value="all">Tất cả chủ đề</option>
                {topicOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="csv-result-meta">
            <span>{filteredCards.length} mục phù hợp</span>

            {(searchTerm || dataType !== 'all' || topic !== 'all') && (
              <button
                className="csv-reset"
                type="button"
                onClick={resetFilters}
              >
                Xóa lọc
              </button>
            )}
          </div>

          {filteredCards.length === 0 ? (
            <p className="csv-empty">
              Không tìm thấy dữ liệu phù hợp. Hãy thử từ khóa hoặc bộ lọc khác.
            </p>
          ) : (
            <div className="csv-grid csv-grid--compact">
              {filteredCards.map((card) => {
                const isOpen = openCardId === card.id
                const isTitleOnly = card.type === 'description' && !isOpen

                return (
                  <article
                    className={`csv-card csv-knowledge-card${
                      card.type === 'rule' ? ' csv-card-warning' : ''
                    }${isTitleOnly ? ' csv-knowledge-card--title-only' : ''
                    }`}
                    key={card.id}
                  >
                    <div className="csv-card-topline">
                      <span className={`csv-chip csv-chip--${card.type}`}>
                        {card.badge}
                      </span>
                    </div>

                    <h4>{card.title}</h4>

                    {!isTitleOnly && (
                      <p
                        className={`csv-card-body${
                          isOpen ? '' : ' csv-card-body--collapsed'
                        }`}
                      >
                        {isOpen ? card.body : getPreview(card.body)}
                      </p>
                    )}

                    <button
                      className="csv-detail-button"
                      type="button"
                      aria-expanded={isOpen}
                      onClick={() => setOpenCardId(isOpen ? null : card.id)}
                    >
                      {isOpen ? 'Thu gọn' : 'Chi tiết'}
                    </button>
                  </article>
                )
              })}
            </div>
          )}
        </>
      )}
    </section>
  )
}

export default CsvDataSection
