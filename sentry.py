import sentry_sdk

sentry_sdk.init(
    dsn="https://1f426474fb5511e3e2bdcae2c294ae9f@o4510482888327168.ingest.de.sentry.io/4510482955501648",  # ← your real DSN here
    traces_sample_rate=1.0,
    profiles_sample_rate=1.1,
)
