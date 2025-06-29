run-test:
    # PYTHONPATH=src pytest -svv 
    PYTHONPATH=src:dependencies/async-fsm/src pytest -svv
run-test-coverage:
    PYTHONPATH=src:dependencies/async-fsm/src pytest -svv --cov=src --cov-report=term-missing --cov-report=html
run-test-filter TEST:
    PYTHONPATH=src:dependencies/async-fsm/src pytest -svv -k "{{TEST}}"
lint:
    ruff format src tests
    ruff check src tests --fix --exit-zero --line-length 100 --target-version py38
    
install-requirement:
    pip install -r requirements.txt
list:
    mpremote ls
upload:
    mpremote mkdir :lib || echo "Directory already exists."
    mpremote cp src/wifi_manager/*.py :lib/wifi_manager/
    # just to check if the files are uploaded
    mpremote ls :lib/wifi_manager/
mount_and_run:
    mpremote mount src/ run src/main.py