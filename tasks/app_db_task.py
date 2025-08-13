import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
import psycopg2
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

def fetch_and_store_posts(ts_nodash: str,
                          dsn: str = "postgresql://postgres:0000@127.0.0.1:5432/sajib") -> int:
    try:
        created_at = datetime.strptime(ts_nodash, "%Y%m%dT%H%M%S")
        
        # Fetch API data with curl
        result = subprocess.run([
            'curl', '--connect-timeout', '5', '--max-time', '15',
            'https://jsonplaceholder.typicode.com/posts'
        ], capture_output=True, text=True, timeout=20)
        
        if result.returncode != 0:
            raise AirflowFailException(f"API call failed: {result.stderr}")
        
        data = json.loads(result.stdout)
        rows = [(item["userId"], item["id"], item["title"], item["body"], created_at) 
                for item in data]
        
        # Store in PostgreSQL
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS public.posts (
                        user_id INTEGER, post_id INTEGER PRIMARY KEY,
                        title TEXT, body TEXT, created_at TIMESTAMP
                    );
                """)
                cur.executemany("""
                    INSERT INTO public.posts (user_id, post_id, title, body, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (post_id) DO UPDATE SET
                        user_id = EXCLUDED.user_id, title = EXCLUDED.title,
                        body = EXCLUDED.body, created_at = EXCLUDED.created_at;
                """, rows)
        
        log.info("Stored %d posts in database", len(rows))
        return len(rows)
        
    except (subprocess.TimeoutExpired, json.JSONDecodeError, psycopg2.Error) as e:
        raise AirflowFailException(str(e))
    except Exception as e:
        log.exception("fetch_and_store_posts failed")
        raise AirflowFailException(str(e))