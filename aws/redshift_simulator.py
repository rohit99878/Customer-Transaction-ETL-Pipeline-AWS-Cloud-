# aws/redshift_simulator.py
class RedshiftSimulator:
    def __init__(self):
        pass

    def execute_sql(self, query):
        print(f"\n[Redshift SQL] Executed:\n{query}\n")

    def copy_from_s3(self, table, s3_path):
        sql = f"""
COPY {table}
FROM '{s3_path}'
FORMAT AS CSV
IGNOREHEADER 1;
"""
        print("[Redshift Simulator] COPY command (simulated):")
        print(sql)

    def run_analytics_queries(self):
        queries = [
            "SELECT COUNT(*) AS total_rows FROM customer_transactions;",
            "SELECT AVG(total_amount) AS avg_total FROM customer_transactions;",
            "SELECT product, SUM(amount) AS total_sales FROM customer_transactions GROUP BY product ORDER BY total_sales DESC LIMIT 10;"
        ]
        print("[Redshift Simulator] Running sample analytics queries:")
        for q in queries:
            self.execute_sql(q)
