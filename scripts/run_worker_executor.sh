# scripts/run_worker_executor.sh
python -c "from workers.executor_worker import ExecutorWorker; import asyncio; asyncio.run(ExecutorWorker().run())"