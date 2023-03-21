bq load \
--source_format=PARQUET \
--noreplace \
testing-of-bigquery:shoulderhit.daily_news \
todays-news.parquet