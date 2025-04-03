import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent } from "./components/Card";
import { Button } from "./components/Button";
import "./AllLinks.css";

export default function AllLinksPage() {
  const [links, setLinks] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchLinks() {
      try {
        const response = await fetch("/api/link/list");
        if (!response.ok) {
          throw new Error("Не удалось загрузить ссылки");
        }
        const data = await response.json();

        if (!Array.isArray(data)) {
          throw new Error("Неверный формат данных");
        }
        
        setLinks(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchLinks();
  }, []);

  return (
    <div className="container">
      <div className="header">
        <Button onClick={() => navigate(-1)} className="back-button">
            Вернуться назад
        </Button>
        <h2>Все ссылки</h2>
      </div>
      <div className="content">
        <Card className="card">
          <CardContent className="card-content">
            {loading && <p>Загрузка...</p>}
            {error && <p className="error-message">{error}</p>}
            {!loading && !error && links.length > 0 ? (
              <table className="links-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Дата создания</th>
                    <th>Короткая ссылка</th>
                    <th>Длинная ссылка</th>
                  </tr>
                </thead>
                <tbody>
                  {links.map((link) => (
                    <tr key={link.id}>
                      <td>{link.id}</td>
                      <td>{new Date(link.created_at).toLocaleString()}</td>
                      <td>
                        <a href={`http://short-linker.ru/api/short/${link.short_link}`} target="_blank" rel="noopener noreferrer">
                          {`http://short-linker.ru/api/short/${link.short_link}`}
                        </a>
                      </td>
                      <td>{link.long_link}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              !loading && <p>Нет данных для отображения.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
