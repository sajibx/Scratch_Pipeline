## Project Overview

This is an Apache Airflow project containing DAGs and tasks for data pipeline development and experimentation. The project is structured as a scratch workspace for Airflow development within the `airflow_home/dags/scratch_pro` directory.

## Directory Structure

- `dags/` - Airflow DAG definitions
  - `full_pipeline.py` - Complete pipeline with file creation and movement
  - `modular_pipeline.py` - Modular DAG referencing external tasks
  - `cds.py` - CoinDesk data fetching pipeline
  - `zzz_smoke.py` - Simple smoke test DAG
- `tasks/` - Reusable task modules
  - `coindesk.py` - Data fetching functions for external APIs
- `plugins/` - Airflow plugin definitions
- `tests/` - Test files and scripts
- `data/` - Data directories (raw, staging, warehouse)
- `scripts/` - Utility scripts
- `tmp/` - Temporary files and processing

## Architecture

The project follows a modular Airflow architecture pattern:

1. **DAG Layer**: DAG definitions in `dags/` directory that orchestrate workflows
2. **Task Layer**: Reusable Python functions in `tasks/` module for data processing logic
3. **Plugin Layer**: Custom Airflow plugins for extended functionality

Key patterns:
- DAGs import task functions from the `tasks/` module using sys.path manipulation
- Tasks are designed to be stateless and accept parameters via `op_kwargs`
- External API calls use requests library with proper timeout handling
- File operations use environment variables for path configuration (`AIRFLOW_HOME`)

## Development Commands

### Running Tests
```bash
python tests/test.py
python tests/test2.py
```

### Testing Individual Tasks
Tasks in the `tasks/` module can be imported and tested independently:
```python
from tasks.coindesk import fetch_data
```

## Configuration Notes

- Default DAG owner is "sajib"
- DAGs use `catchup=False` to prevent backfilling
- Execution timeouts are configured (typically 45 seconds to 1 minute)
- File paths use absolute paths referencing `AIRFLOW_HOME` environment variable
- API calls include proper timeout configurations (5s connect, 10s read)

## Common Patterns

- DAGs follow the pattern: define default_args, create DAG context, define tasks, set dependencies
- Task functions accept `**context` parameter for Airflow context access
- External data is typically saved to `$AIRFLOW_HOME/data/tmp/` directory
- sys.path manipulation is used to import from sibling directories within the DAG structure
