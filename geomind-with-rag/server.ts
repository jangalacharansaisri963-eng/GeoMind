import "dotenv/config";
import express from "express";
import path from "path";
import { execFile } from "child_process";
import { createServer as createViteServer } from "vite";

const app = express();
const PORT = 3000;

app.use(express.json());

const SCRIPT_PATH = path.join(process.cwd(), "geomind", "server_api.py");

function runPython(args: string[]): Promise<any> {
  return new Promise((resolve, reject) => {
    execFile("python3", [SCRIPT_PATH, ...args], { maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
      if (error) {
        console.error("Python exec error:", stderr || error.message);
        return reject(new Error(stderr || error.message));
      }
      try {
        const data = JSON.parse(stdout.trim());
        resolve(data);
      } catch (err) {
        console.error("JSON parse error on python output:", stdout);
        reject(new Error("Invalid JSON response from GeoMind engine"));
      }
    });
  });
}

// ================= API ENDPOINTS =================

app.get("/api/health", (req, res) => {
  res.json({ status: "ok", model: "GeoMind-1" });
});

app.get("/api/model/info", async (req, res) => {
  try {
    const data = await runPython(["info"]);
    res.json(data);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

app.get("/api/datasets", async (req, res) => {
  try {
    const data = await runPython(["datasets"]);
    res.json(data);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/api/chat", async (req, res) => {
  try {
    const { message } = req.body;
    if (!message || typeof message !== "string") {
      return res.status(400).json({ error: "Message string is required" });
    }
    const data = await runPython(["ask", message]);
    res.json(data);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/api/train", async (req, res) => {
  try {
    const epochs = req.body.epochs ? parseInt(req.body.epochs, 10) : 3;
    const lr = req.body.lr ? parseFloat(req.body.lr) : 0.02;
    const data = await runPython(["train", epochs.toString(), lr.toString()]);
    res.json(data);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// ================= VITE MIDDLEWARE & STATIC =================

async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`GeoMind Full-Stack Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer().catch((err) => {
  console.error("Failed to start server:", err);
});
