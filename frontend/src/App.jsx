
import './App.css'

import Navbar from './components/Navbar'
import Hero from './components/Hero'
import OutfitSection from './components/OutfitSection'
import Studio from './components/Studio'
import Footer from './components/Footer'

function App() {
  return (
    <div className="app">
      <Navbar />

      <main>
        <Hero />

        <section className="intro" id="about">
          <p className="section-label">
            CÂU CHUYỆN CỦA CHÚNG TÔI
          </p>

          <h2>Mặc lên niềm tự hào Việt.</h2>

          <p>
            Việt phục Remix đưa văn hóa trang phục Việt
            đến gần hơn với thế hệ mới thông qua trải nghiệm
            khám phá và phối đồ.
          </p>
        </section>

        <OutfitSection />

        <Studio />
      </main>

      <Footer />
    </div>
  )
}

export default App
