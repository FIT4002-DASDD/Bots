# Getting started

- Install:
  - PostgreSQL
  - Node.js
  - Yarn
  - DataGrip (Optional)
- Create a database in Postgres using PGAdmin. Put the credentials inside `.dev.env` following the structure of `.example.env`
- Run `yarn` in this directory (`\backend`) to install the node_modules dependencies
- Run `yarn schema:sync` to create tables in the database using the models defined in `src\models`.
  - You will need to run this every time the models are changed or you can set the `DB_SYNC=true` in the `.dev.env` for automatic synchronisation. This is only recommended for development, not production, as sync may drop data.
- Import the csv files in `src/google-data` into the tables using PGAdmin or DataGrip
- Start the server: `yarn start`
