import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ShortLinkGenerator from "./Generator";
import StatisticsPage from "./Statistics";
import AllLinksPage from "./AllLinks";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ShortLinkGenerator />} />
      <Route path="/statistics" element={<StatisticsPage />} />
      <Route path="/all-links" element={<AllLinksPage />} />
    </Routes>
  );
}
