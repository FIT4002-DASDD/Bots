import { Bot } from "~/models";

export class BotController {
  async getAll(): Promise<Bot[]> {
    return await Bot.find();
  }
}
