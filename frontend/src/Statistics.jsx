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

  if (!shortLink) {
    setError("Введите короткую ссылку!");
    setLoading(false);
    return;
  }

  try {
    const response = await fetch(`/api/link/${shortLink}/statistics`);
    if (!response.ok) {
      throw new Error("Не удалось загрузить статистику");
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
      throw new Error("Некорректный формат данных от сервера");
    }

    setStats(data);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
}

  return (
    <div className="container">
      <div className="content">
        <h1 className="title">Статистика короткой ссылки</h1>
        <Card className="card">
          <CardContent className="card-content">
            <div className="input-container">
              <Input
                type="text"
                placeholder="Введите короткую ссылку"
                value={shortLink}
                onChange={(e) => setShortLink(e.target.value)}
              />
              <Button onClick={fetchStatistics}>Получить статистику</Button>
            </div>
            {loading && <p>Загрузка...</p>}
            {error && <p className="error-message">{error}</p>}
            {!loading && !error && stats.length > 0 ? (
              <table className="stats-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Дата создания</th>
                    <th>Дата обновления</th>
                    <th>IP пользователя</th>
                    <th>User Agent</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.map((stat) => (
                    <tr key={stat.id}>
                      <td>{stat.id}</td>
                      <td>{new Date(stat.created_at).toLocaleString()}</td>
                      <td>{new Date(stat.updated_at).toLocaleString()}</td>
                      <td>{stat.user_ip}</td>
                      <td>{stat.user_agent}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              !loading && <p>Нет данных для отображения.</p>
            )}
          </CardContent>
        </Card>
        <Button onClick={() => navigate("/")} className="back-button">
          Вернуться на главную
        </Button>
      </div>
    </div>
  );
}
