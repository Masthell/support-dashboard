// src/pages/MonitoringPage.tsx
import { useEffect } from "react";

export default function MonitoringPage() {
  useEffect(() => {
    // Редирект на Grafana с небольшой задержкой для UX
    const timer = setTimeout(() => {
      window.location.href =
        "http://localhost:3000/goto/df6vrc68bypdse?orgId=1";
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        color: "white",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        padding: "20px",
      }}
    >
      <div
        style={{
          background: "rgba(255, 255, 255, 0.1)",
          padding: "40px",
          borderRadius: "20px",
          backdropFilter: "blur(10px)",
          maxWidth: "600px",
        }}
      >
        <h1 style={{ fontSize: "2.5rem", marginBottom: "20px" }}>
          🚀 Добро пожаловать в систему мониторинга!
        </h1>

        <div
          style={{
            width: "60px",
            height: "60px",
            border: "5px solid rgba(255,255,255,0.3)",
            borderTop: "5px solid white",
            borderRadius: "50%",
            margin: "30px auto",
            animation: "spin 1s linear infinite",
          }}
        ></div>

        <p style={{ fontSize: "1.2rem", marginBottom: "30px", opacity: 0.9 }}>
          Перенаправляем вас на панель мониторинга Grafana...
        </p>

        <div
          style={{
            background: "rgba(255, 255, 255, 0.2)",
            padding: "15px",
            borderRadius: "10px",
            marginTop: "20px",
          }}
        >
          <p style={{ fontSize: "0.9rem", marginBottom: "10px" }}>
            Если автоматический переход не сработал:
          </p>
          <a
            href="http://localhost:3000/goto/df6vrc68bypdse?orgId=1"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: "inline-block",
              padding: "12px 24px",
              background: "#4CAF50",
              color: "white",
              textDecoration: "none",
              borderRadius: "8px",
              fontWeight: "bold",
              transition: "transform 0.2s",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.transform = "scale(1.05)")
            }
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
          >
            📊 Нажмите здесь для открытия мониторинга
          </a>
        </div>
      </div>

      <style>{`
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `}</style>
    </div>
  );
}
