# scripts/run_worker_guardian.sh
python -c "from workers.guardian_worker import GuardianWorker; import asyncio; asyncio.run(GuardianWorker().run())"