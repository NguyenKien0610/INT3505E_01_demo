// server.js
const express = require("express");
const jwt = require("jsonwebtoken");
const dotenv = require("dotenv");
const path = require("path");
const swaggerUi = require("swagger-ui-express");
const YAML = require("yamljs");

dotenv.config();
const app = express();
app.use(express.json());

const ACCESS_SECRET = process.env.ACCESS_SECRET || "access_secret_123";
const REFRESH_SECRET = process.env.REFRESH_SECRET || "refresh_secret_123";

// ===== Mock "DB" =====
const users = {
  user1: { password: "123", role: "user",  scopes: ["read:books"] },
  admin: { password: "123", role: "admin", scopes: ["read:books", "write:books", "delete:books"] },
};

// Token bị thu hồi (demo revoke / leakage)
const revokedTokens = new Set();

// ===== Helpers =====
function signAccess(username, extra = {}) {
  // access token sống ngắn để dễ demo refresh
  return jwt.sign(
    { sub: username, ...extra },
    ACCESS_SECRET,
    { expiresIn: "1m" }
  );
}

function signRefresh(username) {
  return jwt.sign({ sub: username }, REFRESH_SECRET, { expiresIn: "5m" });
}

// Middleware xác thực Bearer token
function authenticate(req, res, next) {
  const auth = req.headers.authorization || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : null;
  if (!token) return res.status(401).json({ message: "Thiếu token" });

  if (revokedTokens.has(token)) {
    return res.status(403).json({ message: "Token đã bị thu hồi" });
  }
  jwt.verify(token, ACCESS_SECRET, (err, payload) => {
    if (err) return res.status(403).json({ message: "Token không hợp lệ hoặc đã hết hạn" });
    const username = payload.sub;
    const user = users[username];
    if (!user) return res.status(401).json({ message: "User không tồn tại" });
    req.user = { username, role: user.role, scopes: user.scopes, token };
    next();
  });
}

// Middleware kiểm tra scope
function requireScope(required) {
  return (req, res, next) => {
    if (!req.user?.scopes?.includes(required)) {
      return res.status(403).json({ message: "Không có quyền truy cập" });
    }
    next();
  };
}

// ===== Routes =====
app.get("/", (_req, res) => {
  res.json({ message: "JWT Authentication Demo 🚀 (Node.js + Express)" });
});

// Login: trả access + refresh
app.post("/login", (req, res) => {
  const { username, password } = req.body || {};
  const user = users[username];
  if (!user || user.password !== password) {
    return res.status(401).json({ message: "Sai tên đăng nhập hoặc mật khẩu" });
  }
  const access_token = signAccess(username, { role: user.role, scopes: user.scopes });
  const refresh_token = signRefresh(username);
  res.json({ access_token, refresh_token, token_type: "bearer" });
});

// Refresh: đổi access token mới
app.post("/refresh", (req, res) => {
  const { refresh_token } = req.body || {};
  if (!refresh_token) return res.status(401).json({ message: "Thiếu refresh token" });

  jwt.verify(refresh_token, REFRESH_SECRET, (err, payload) => {
    if (err) return res.status(403).json({ message: "Refresh token không hợp lệ hoặc hết hạn" });
    const username = payload.sub;
    const user = users[username];
    if (!user) return res.status(401).json({ message: "User không tồn tại" });
    const new_access = signAccess(username, { role: user.role, scopes: user.scopes });
    res.json({ access_token: new_access });
  });
});

// Books: read (user & admin)
app.get("/books/:id", authenticate, requireScope("read:books"), (req, res) => {
  res.json({ book_id: req.params.id, title: "Clean Architecture", by: req.user.username });
});

// Books: create (admin only)
app.post("/books", authenticate, requireScope("write:books"), (req, res) => {
  res.json({ message: `Sách mới được thêm bởi ${req.user.username}` });
});

// Books: delete (admin only)
app.delete("/books/:id", authenticate, requireScope("delete:books"), (req, res) => {
  res.json({ message: `Sách ${req.params.id} đã bị xóa bởi admin ${req.user.username}` });
});

// Logout: revoke access token (demo leakage & revoke)
app.post("/logout", (req, res) => {
  const tokenFromBody = req.body?.token;
  const auth = req.headers.authorization || "";
  const tokenFromHeader = auth.startsWith("Bearer ") ? auth.slice(7) : null;
  const token = tokenFromBody || tokenFromHeader;

  if (!token) return res.status(400).json({ message: "Không có token để thu hồi" });
  revokedTokens.add(token);
  res.json({ message: "Token đã bị thu hồi thành công" });
});

// Secure action: mô phỏng phát hiện replay (gọi lại token đã revoke)
app.post("/secure-action", authenticate, (req, res) => {
  if (revokedTokens.has(req.user.token)) {
    return res.status(403).json({ message: "Replay attack bị phát hiện!" });
  }
  res.json({ message: "Hành động an toàn được thực hiện!" });
});

// ===== Swagger UI =====
const swaggerDocument = YAML.load(path.join(__dirname, "openapi.yaml"));
app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));
// (tùy chọn) serve file YAML thô để xem
app.get("/openapi.yaml", (_req, res) => {
  res.sendFile(path.join(__dirname, "openapi.yaml"));
});

// ===== Start =====
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
  console.log(`📖 Swagger UI at http://localhost:${PORT}/docs`);
});
