import logging
import subprocess
from pathlib import Path
from airflow.exceptions import AirflowFailException

log = logging.getLogger(__name__)

DATA_ROOT = Path("/Users/ashiqurrahman/DE_Projects/airflow29_home/data")
TMP = DATA_ROOT / "tmp"


def fetch_api_data(ts_nodash):

    TMP.mkdir(parents=True, exist_ok=True)
    file_path = TMP / f"api_{ts_nodash}.txt"

    # Use the same curl command that works in BashOperator
    curl_cmd = [
        'curl',
        '--connect-timeout', '5',
        '--max-time', '15',
        'https://jsonplaceholder.typicode.com/posts'
    ]

    try:
        # Run curl command with timeout
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=20  # Slightly longer than curl's own timeout
        )

        if result.returncode == 0:
            # Write successful data
            file_path.write_text(result.stdout)
            log.info("API data saved to %s (%d bytes)", file_path, len(result.stdout))
        else:
            # Write error info
            error_msg = f"curl failed with return code {result.returncode}: {result.stderr}"
            file_path.write_text(error_msg)
            log.error(error_msg)

    except subprocess.TimeoutExpired:
        error_msg = "curl command timed out"
        file_path.write_text(error_msg)
        log.error(error_msg)
    except Exception as e:
        error_msg = f"Subprocess error: {str(e)}"
        file_path.write_text(error_msg)
        log.error(error_msg)

    return str(file_path)