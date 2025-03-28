import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Input } from "./components/Input";
import { Button } from "./components/Button";
import { Card, CardContent } from "./components/Card";
import "./Generator.css";

export default function ShortLinkGenerator() {
  const [url, setUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [error, setError] = useState("");
  const [copySuccess, setCopySuccess] = useState(false);
  const navigate = useNavigate();

  const generateShortLink = async () => {
    setShortUrl("");
    setError("");
    setCopySuccess(false);

    if (!url) {
      setError("Введите ссылку!");
      return;
    }

    try {
      const response = await fetch("/api/link", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ link: url }),
      });

      if (!response.ok) {
        throw new Error("Не удалось создать короткую ссылку.");
      }

      const data = await response.json();
      setShortUrl(data.link);
    } catch (error) {
      setError(error.message);
    }
  };

  const copyToClipboard = () => {
    if (shortUrl) {
      navigator.clipboard.writeText(shortUrl)
        .then(() => setCopySuccess(true))
        .catch(() => setError("Не удалось скопировать ссылку"));
      
      setTimeout(() => setCopySuccess(false), 2000);
    }
  };

  return (
    <div className="container">
      <div className="content">
        <h1 className="title">Генератор коротких ссылок</h1>
        <Card className="card">
          <CardContent className="card-content">
            <div className="input-container">
              <Input
                type="url"
                placeholder="Введите ссылку"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <Button onClick={generateShortLink}>Сократить</Button>
            </div>
            {error && <p className="error-message">{error}</p>}
            {shortUrl && (
              <div className="short-url-container">
                <span className="short-url-label">Короткая ссылка:</span>
                <div className="short-url-box">
                  <a
                    href={shortUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="short-url-link"
                  >
                    {shortUrl}
                  </a>
                  <button onClick={copyToClipboard} className="copy-button">
                    Скопировать
                  </button>
                </div>
                {copySuccess && <p className="copy-success">Ссылка скопирована!</p>}
              </div>
            )}
          </CardContent>
        </Card>
        <Button onClick={() => navigate("/statistics")} className="stats-button">
          Перейти к статистике
        </Button>
        <Button onClick={() => navigate("/all-links")} className="all-links-button">
          Все ссылки
        </Button>
      </div>
    </div>
  );
}
