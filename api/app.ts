import express from "express";
import cors from "cors";
import { exec } from "child_process";

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.get("/", (_, res) => {
  res.status(200).send();
});

app.get("/start-all-bots", (_, res) => {
  exec(
    "./test.sh",
    { cwd: "C:/Users/nerv/Documents/Projects/Bots/scripts" },
    (error, stdout, stderr) => {
      if (error) {
        console.log(`error: ${error.message}`);
        return;
      }
      if (stderr) {
        console.log(`stderr: ${stderr}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
    }
  );
  res.status(200).send();
});

app.listen(port, () => console.log(`Running on port ${port}`));
