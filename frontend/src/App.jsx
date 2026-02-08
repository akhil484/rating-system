import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import './App.css'
import AllProducts from "./components/AllProducts"
import ProductReviews from "./components/Reviews/ProductReviews.jsx"
import PostReview from "./components/ReviewForm/PostReview"

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
        </header>

        <main>
          <Routes>
            <Route path={"/products"} element={<AllProducts />}/>
            <Route path={"/product/:uid"} element={<ProductReviews />}/>
            <Route path={"/product-review/:uid"} element={<PostReview />}/>
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
