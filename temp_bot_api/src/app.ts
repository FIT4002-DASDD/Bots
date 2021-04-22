import cors from "cors";
import express, { NextFunction, Request, Response } from "express";
import { getConnection } from "typeorm";
import { config } from "~/configs/config";
import { TryDBConnect } from "~/helpers/dbConnection";
import botRoute from "./routes/botRoute";

const initServer = async () => {
  const app: express.Application = express();

  app.use(express.json());
  app.use(express.urlencoded({ extended: false }));

  app.use(async (req: Request, res: Response, next) => {
    await TryDBConnect(() => {
      res.json({
        error: "Database connection error, please try again later",
      });
    }, next);
  });

  // Health check route for AWS
  app.get("/health", (req, res) => {
    res.status(200).send("Server is running");
  });

  // Setting up routes
  app.use("/bots", botRoute);

  // Just checking if given PORT variable is an integer or not
  let port = parseInt(config.PORT || "");
  if (isNaN(port) || port === 0) {
    port = 8888;
  }

  app.listen(port, () => {
    console.log(`Server Started at: http://localhost:${port}`);
  });
};

initServer();
