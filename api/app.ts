import express from "express";
import cors from "cors";
import { spawn } from "child_process";

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.get("/", (_, res) => {
  res.status(200).send("server running");
});

app.get("/start-all-bots", (_, res) => {
  console.log("starting bots");
  let script = spawn("sh", ["./scripts/start_server.sh"], {
    cwd: "/root/Bots",
  });

  script.stdout.setEncoding("utf8");
  script.stdout.on("data", function (data: String) {
    console.log("stdout: " + data);
  });

  script.stderr.setEncoding("utf8");
  script.stderr.on("data", function (data: String) {
    console.log("stderr: " + data);
  });

  script.on("close", function (code: String) {
    console.log("closing code: " + code);
  });

  console.log("bots running in background");
  res.status(200).send();
});

app.listen(port, () => console.log(`Running on port ${port}`));
