import psycopg
#AsyncConnection.connect() creates an asyncio connection instead
with psycopg.connect("dbname=zhaojichang") as conn:
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM test;")
		
		#cur.fetchone()
		records=cur.fetchmany(size=5)
		#records=cur.fetchall()
		for record in records:
			print(record)
		