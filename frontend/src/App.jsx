import {
  useState,
} from "react";

import Sidebar from "./components/Sidebar";
import AnalyzePage from "./pages/AnalyzePage";
import DashboardPage from "./pages/DashboardPage";
import MemoryPage from "./pages/MemoryPage";

import "./styles/main.css";
import "./styles/status-actions.css";


function App() {
  const [activePage, setActivePage] =
    useState("dashboard");


  function renderPage() {
    if (activePage === "analyze") {
      return <AnalyzePage />;
    }

    if (activePage === "memory") {
      return <MemoryPage />;
    }

    return (
      <DashboardPage
        onAnalyzeClick={() =>
          setActivePage("analyze")
        }
      />
    );
  }


  return (
    <div className="app-shell">
      <Sidebar
        activePage={activePage}
        onPageChange={setActivePage}
      />

      <main className="main-area">
        {renderPage()}
      </main>
    </div>
  );
}


export default App;