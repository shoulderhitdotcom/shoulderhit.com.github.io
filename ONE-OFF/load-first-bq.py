bq load \
    --source_format=PARQUET \
    shoulderhit.daily_news \
    ./todays-news.parquet
