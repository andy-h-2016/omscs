#!/bin/sh

# Directory relative to pwd containing expected log files
LOG_DIR=Logs

# ANSI colors
GREEN='\e[1;92m'
RED='\e[1;91m'
OFF='\e[0m'

# Unless given as envvars, use python3/python, colordiff/diff
PYTHON=${PYTHON:-$(command -v python3 >/dev/null 2>&1 && echo python3 || echo python)}
DIFF=${DIFF:-$(command -v colordiff >/dev/null 2>&1 && echo colordiff || echo diff)}

for LOG_FILE_REF in "${LOG_DIR}"/*.log; do
  TOPO=$(basename "$LOG_FILE_REF" .log)
  TOPO_FILE="${TOPO}.py"
  LOG_FILE="${TOPO}.log"

  if [ ! -f "${TOPO_FILE}" ]; then
    continue
  fi

  printf '%-32s' "${TOPO}"

  if ! "${PYTHON}" run.py "${TOPO}"; then
    printf "${RED}%s${OFF}\n" "FAILURE"
    printf '  command failed: "%s" run.py "%s"\n' \
                              "${PYTHON}" "${TOPO}"
    break
  fi

  if ! cmp -s "${LOG_FILE}" "${LOG_FILE_REF}"; then
    printf "${RED}%s${OFF}\n" "FAILURE"
    "${DIFF}" -u "${LOG_FILE}" "${LOG_FILE_REF}"
    break
  fi

  # Delete or comment out this line to keep results of successful runs
  rm -f "${LOG_FILE}"

  printf "${GREEN}%s${OFF}\n" "SUCCESS"
done
