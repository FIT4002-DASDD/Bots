import dotenv from "dotenv";
import path from "path";
const env = process.env;
switch (env.NODE_ENV) {
  case "development":
  case "dev":
    dotenv.config({ path: path.resolve(__dirname, "../../.dev.env") });
    break;
  case "production":
  case "prod":
    dotenv.config({ path: path.resolve(__dirname, "../../.prod.env") });
    break;
  default:
    dotenv.config({ path: path.resolve(__dirname, "../../.dev.env") });
}

export type Config = {
  PORT: string;
  DB_HOST: string;
  DB_PORT: number;
  DB_NAME: string;
  DB_USERNAME: string;
  DB_PASSWORD: string;
  DB_SYNC: boolean;
  DB_LOGS: boolean;
};
export const config: Config = {
  PORT: env.PORT || "localhost",
  DB_HOST: env.DB_HOST || "localhost",
  DB_PORT: env.DB_PORT ? parseInt(env.DB_PORT) : 5432,
  DB_NAME: env.DB_NAME || "postgres",
  DB_USERNAME: env.DB_USERNAME || "postgres",
  DB_PASSWORD: env.DB_PASSWORD || "password",
  DB_SYNC: env.DB_SYNC === "true" ? true : false,
  DB_LOGS: env.DB_LOGS === "true" ? true : false,
};
console.log(process.env.NODE_ENV);
console.log(config);
