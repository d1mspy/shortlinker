import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card, CardContent } from "./components/Card";
import { useNavigate } from "react-router-dom";
import { Button } from "./components/Button";
import { Input } from "./components/Input";
import "./Statistics.css";

export default function StatisticsPage() {
  const { shortLink: paramShortLink } = useParams();
  const [shortLink, setShortLink] = useState(paramShortLink || "");
  const [stats, setStats] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchStatistics = async () => {
    setLoading(true);
    setError("");
    setStats([]);

    let processedLink = shortLink.trim();
    if (processedLink.length > 10) {
      processedLink = processedLink.slice(-10);
    }

    if (!processedLink) {
      setError("Введите короткую ссылку!");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`/api/link/${processedLink}/statistics`);
      if (!response.ok) {
        throw new Error("Не удалось загрузить статистику");
      }

      const data = await response.json();

      if (!Array.isArray(data)) {
        throw new Error("У этой ссылки еще нет статистики");
      }

      setStats(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="statistics-page container">
      <div className="content">
        <h1 className="stats-title">Статистика короткой ссылки</h1>
        <Card className="card">
          <CardContent className="card-content">
            <div className="stats-input-container">
              <Input
                type="text"
                placeholder="Введите короткую ссылку"
                value={shortLink}
                onChange={(e) => setShortLink(e.target.value)}
              />
              <Button onClick={fetchStatistics}>Получить статистику</Button>
            </div>
  
            {error && <p className="stats-error-message">{error}</p>}
  
            <div className="stats-table-container">
              <table className="stats-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Дата создания</th>
                    <th>IP пользователя</th>
                    <th>User Agent</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.length > 0 ? (
                    stats.map((stat) => (
                      <tr key={stat.id}>
                        <td>{stat.id}</td>
                        <td>{new Date(stat.created_at).toLocaleString()}</td>
                        <td>Не покажем (но фиксируем...)</td>
                        <td>{stat.user_agent}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="4" className="empty-message">Нет данных</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
        <div className="back-button-container">
          <Button onClick={() => navigate("/")} className="back-button">
            Вернуться назад
          </Button>
        </div>
      </div>
    </div>
  );
}
