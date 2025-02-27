// Database operations cli

const resetMongo = require("./mongo/reset");
const resetSelectMongo = require("./mongo/reset_select");
const privateResetMongo = require("./mongo/private_reset");
const exportSelections = require("./mongo/export");
const admin = require("./mongo/admin");
const clean = require("./mongo/clean");

// ========================================

require("yargs") // eslint-disable-line
  .usage("Usage: node $0 <command>")
  .command(
    "reset",
    "Reset all data in database.",
    () => {},
    (argv) => {
      resetMongo();
    }
  )
  .command(
    "reset-select",
    "Reset selection and result data in database.",
    () => {},
    (argv) => {
      resetSelectMongo();
    }
  )
  .command(
    "private-reset",
    "Reset all data in database.",
    () => {},
    (argv) => {
      privateResetMongo();
    }
  )
  .command(
    "export",
    "Export student selections to server/database/private-data/ folder.",
    () => {},
    (argv) => {
      exportSelections(argv.f);
    }
  )
  .command(
    "admin <password>",
    "Modify admin password",
    (yargs) => {
      yargs.positional("password", {
        demandOption: true,
        describe: "Modify default vlaue to change new Password",
        type: "string",
      });
    },
    (argv) => {
      admin(argv.password);
    }
  )
  .command(
    "clean",
    "Clean selections db",
    () => {},
    (argv) => {
      clean();
    }
  )
  // .command(
  //   "update-opentime",
  //   "Update openTime.",
  //   (yargs) => {
  //     yargs.positional("resource", {
  //       describe: "Resource to be update",
  //       choices: ["opentime"],
  //     });
  //   },
  //   (argv) => {
  //     updateOpentime();
  //   }
  // )
  .epilog("Type 'node database.js <command> --help' for help of each command.")
  .alias("h", "help")
  .version(false)
  .strictCommands(true)
  .demandCommand(1, "No command specified.").argv;
