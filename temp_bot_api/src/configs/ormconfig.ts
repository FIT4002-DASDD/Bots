import path from "path";
import { ConnectionOptions } from "typeorm";
import { config } from "./config";
// const result = dotenv.config();

const isCompiled = path.extname(__filename).includes("js");
console.log([__dirname + "../models/**/*{.ts,.js}"]);
export = {
  type: "postgres",
  host: config.DB_HOST || "localhost",
  port: config.DB_PORT || 5432,
  username: config.DB_USERNAME || "postgres",
  password: config.DB_PASSWORD || "password",
  database: config.DB_NAME || "postgres",
  synchronize: config.DB_SYNC || false,
  logging: config.DB_LOGS || false,
  autoReconnect: true,
  reconnectTries: Number.MAX_VALUE,
  reconnectInterval: 2000,
  migrationsRun: false,
  entities: ["src/models/**/*{.ts,.js}"],
  migrations: ["src/migrations/**/*{.ts,.js}"],
  seeds: ["src/database/seeds/**/*{.ts,.js}"],
  factories: ["src/database/factories/**/*{.ts,.js}"],
  cli: {
    entitiesDir: "src/models",
    migrationsDir: "src/migrations",
  },
} as ConnectionOptions;
