from prometheus_client import Counter, Histogram, start_http_server

REQUESTS_TOTAL = Counter(
  'bot_requests_total',
  'Total number of requests received by the bot',
  ['type']
)


GEMINI_REQUESTS = Counter(
  'bot_gemini_requests_total',
  'Total requests to Gemini API',
  ['status']
)


GEMINI_LATENCY = Histogram(
  'bot_gemini_latency_seconds',
  'Latency of Gemini API requests'
)


TASK_GENERATED = Counter("webapp_tasks_generated_total", "Количество созданных задач")
REQUEST_ERRORS = Counter("webapp_errors_total", "Количество ошибок в WebApp", ["endpoint"])

DB_QUERY_TIME = Histogram("webapp_db_query_seconds", "Время выполнения запроса к БД")

def start_metrics_server(port=8000):
  start_http_server(port)
  print(f"Metrics server started on port {port}")
