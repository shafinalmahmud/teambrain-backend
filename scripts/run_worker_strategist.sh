# scripts/run_worker_strategist.sh
python -c "from workers.strategist_worker import StrategistWorker; import asyncio; asyncio.run(StrategistWorker().run())"