import { useState } from "react";
import { apiService } from "../../services/api";
import "./Register.css";

function Register() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Валидация
    if (formData.password !== formData.confirmPassword) {
      setError("Пароли не совпадают");
      setLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setError("Пароль должен быть не менее 6 символов");
      setLoading(false);
      return;
    }

    const registerData = {
      full_name: formData.name.trim(),
      email: formData.email.trim(),
      password: formData.password.trim(),
      role: "user",
    };

    try {
      const response = await apiService.register(registerData);
      console.log("Ответ от регистрации:", response);

      if (response.id || response.email) {
        console.log(" Регистрация успешна!", response);
        alert(" Регистрация выполнена успешно! Теперь вы можете войти.");
        window.location.href = "/login";
      } else {
        setError("Неизвестный формат ответа от сервера");
      }
    } catch (err) {
      console.error("Ошибка регистрации:", err);

      let errorMessage = "Ошибка соединения с сервером";

      if (err instanceof Error) {
        const errorText = err.message.toLowerCase();

        if (
          errorText.includes("409") ||
          errorText.includes("email already exists")
        ) {
          errorMessage = "Пользователь с таким email уже существует";
        } else if (
          errorText.includes("400") ||
          errorText.includes("validation")
        ) {
          errorMessage = "Неверные данные для регистрации";
        } else if (errorText.includes("500")) {
          errorMessage = "Ошибка на сервере. Попробуйте позже";
        } else {
          errorMessage = err.message;
        }
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="sphere1"></div>
      <div className="sphere2"></div>

      <div className="register-content">
        <div className="logo-section">
          <img src="/vite.png" className="logo" alt="logo" />
          <h1>Support Dashboard</h1>
          <p className="subtitle">Создайте свой аккаунт</p>
        </div>

        <form className="register-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              required
              className="input"
              placeholder="Полное имя"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <input
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="input"
              placeholder="E-mail"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <input
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="input"
              placeholder="Пароль (мин. 6 символов)"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <input
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className="input"
              placeholder="Подтвердите пароль"
              disabled={loading}
            />
          </div>

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

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? "Регистрация..." : "Зарегистрироваться"}
          </button>
        </form>

        <div className="signup-section">
          <p className="signup-text">
            Уже есть аккаунт?{" "}
            <a href="/login" className="signup-link">
              Войти
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;
