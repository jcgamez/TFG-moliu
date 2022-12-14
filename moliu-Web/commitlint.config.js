/*
* Commitlint configuration file:
*
* The commit message must satisfy these rules to complete the commit process
* The rules have been specified according to conventional commits standard
*/

module.exports = {
    extends: ["@commitlint/config-conventional"],
    rules: {
      "type-enum": [
        2,
        "always",
        [
          "assets",
          "build",
          "chore",
          "ci",
          "config",
          "docs",
          "feat",
          "fix",
          "initial",
          "perf",
          "refactor",
          "remove",
          "rename",
          "revert",
          "style",
          "test",
        ],
      ],
      "scope-enum": [
        2,
        "always",
        [
          "activity",
          "design",
          "patient",
          "security",
          "specialist",
          "game",
          "ia",
        ]
    ],
    },
  };