import express, { Request, Response } from "express";
import { BotController } from "~/controllers/botController";

const router = express.Router();

router.get("/", async (req: Request, res: Response) => {
  const controller = new BotController();
  res.send(await controller.getAll());
});

export default router;
