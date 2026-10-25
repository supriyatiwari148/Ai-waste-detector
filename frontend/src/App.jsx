import { useState } from "react";
import Navbar from "./components/Navbar.jsx";
import Footer from "./components/Footer.jsx";
import Home from "./pages/Home.jsx";
import GuidePage from "./pages/GuidePage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";

// Simple page switching with state (no router library needed for 3 pages).
export default function App() {
  const [page, setPage] = useState("home");
  return (
    <>
      <Navbar page={page} onNavigate={setPage} />
      <main>
        {page === "home" && <Home />}
        {page === "guide" && <GuidePage />}
        {page === "history" && <HistoryPage />}
      </main>
      <Footer />
    </>
  );
}
