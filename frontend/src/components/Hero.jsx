
import heroBg from '../assets/hero-bg.png'

function Hero() {
  return (
    <section
      className="hero"
      id="home"
      style={{ backgroundImage: `url(${heroBg})` }}
    >
      <div className="hero-overlay" />
      <p className="eyebrow">
        DI SẢN TRONG PHONG CÁCH MỚI
      </p>

      <h1>
        Việt phục,
        <br />
        theo cách của bạn.
      </h1>

      <p className="hero-description">
        Khám phá vẻ đẹp trang phục Việt Nam,
        kết hợp truyền thống với phong cách hiện đại.
      </p>

      <a className="primary-button" href="#studio">
        Bắt đầu khám phá ↗
      </a>

      <p className="hero-note">
        TÔN VINH BẢN SẮC · KHƠI NGUỒN SÁNG TẠO
      </p>
    </section>
  )
}

export default Hero
