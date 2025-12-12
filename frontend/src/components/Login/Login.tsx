import { useState } from "react";
import { apiService } from "../../services/api";
import type { LoginData } from "../../services/types";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    const loginData: LoginData = {
      email: email.trim(),
      password: password.trim(),
    };

    try {
      const response = await apiService.login(loginData);

      if (response.access_token) {
        localStorage.setItem("access_token", response.access_token);
        localStorage.setItem("user_id", response.user_id?.toString() || "");
        localStorage.setItem("user_email", response.email || "");
        localStorage.setItem("user_role", response.role || "");

        console.log("Успешный вход!", response);
        setSuccess("Вход выполнен успешно! Перенаправляем на панель...");

        // Переход через 1.5 секунды
        setTimeout(() => {
          window.location.href = "/monitoring";
        }, 1500);
      } else {
        setError(response.detail || "Ошибка входа");
      }
    } catch (err) {
      console.error("Ошибка входа:", err);
      setError(
        err instanceof Error ? err.message : "Ошибка соединения с сервером"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="sphere1"></div>
      <div className="sphere2"></div>

      <div className="login-content">
        <div className="logo-section">
          <img src="/vite.png" className="logo" alt="logo" />
          <h1>Monitoring Control</h1>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="input"
              placeholder="E-mail"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="input"
              placeholder="Password"
              disabled={loading}
            />
          </div>

          {/* Ошибка */}
          {error && (
            <div
              style={{
                color: "#ff6b6b",
                backgroundColor: "rgba(255, 107, 107, 0.1)",
                padding: "0.75rem",
                borderRadius: "8px",
                marginBottom: "1rem",
                border: "1px solid rgba(255, 107, 107, 0.3)",
              }}
            >
              {error}
            </div>
          )}

          {/* Успех */}
          {success && (
            <div
              style={{
                color: "#33a728",
                backgroundColor: "rgba(51, 167, 40, 0.1)",
                padding: "0.75rem",
                borderRadius: "8px",
                marginBottom: "1rem",
                border: "1px solid rgba(51, 167, 40, 0.3)",
              }}
            >
              {success}
            </div>
          )}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? "Вход..." : "Войти"}
          </button>
        </form>

        <div className="signup-section">
          <p className="signup-text">
            Нет аккаунта?{" "}
            <a href="/register" className="signup-link">
              Зарегистрироваться
            </a>
          </p>
          <a href="#" className="forgot-link">
            Забыли пароль?
          </a>
        </div>
      </div>
    </div>
  );
}

export default Login;
