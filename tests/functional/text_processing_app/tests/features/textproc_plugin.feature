@outline

Feature: CLI input

Scenario Outline: CLI input is empty or only whitespaces
  Given the file input is "<raw_text>"
  When encoded with the RS plugin
  And decoded with the RS plugin
  Then the file output contains the same "<raw_text>" as the input

  Examples:
  | raw_text |
  | ""       |
  | "  "     |
  | "\n "    |
  | " \t"    |
