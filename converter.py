import json
import psycopg2
from psycopg2.extras import execute_batch

def create_tables(cursor):
    # Create nodes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nodes (
        id VARCHAR(255) PRIMARY KEY,
        entity_type VARCHAR(255),
        description TEXT,
        source_id VARCHAR(255)
    );
    """)
    
    # Create edges table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS edges (
        id SERIAL PRIMARY KEY,
        source VARCHAR(255),
        target VARCHAR(255),
        weight FLOAT,
        description TEXT,
        keywords TEXT,
        source_id VARCHAR(255),
        FOREIGN KEY (source) REFERENCES nodes(id),
        FOREIGN KEY (target) REFERENCES nodes(id)
    );
    """)

def insert_data(cursor, data):
    # Insert nodes
    node_query = """
    INSERT INTO nodes (id, entity_type, description, source_id)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET
        entity_type = EXCLUDED.entity_type,
        description = EXCLUDED.description,
        source_id = EXCLUDED.source_id;
    """
    
    node_data = [(
        node['id'],
        node['entity_type'],
        node['description'],
        node['source_id']
    ) for node in data['nodes']]
    
    execute_batch(cursor, node_query, node_data)
    
    # Insert edges
    edge_query = """
    INSERT INTO edges (source, target, weight, description, keywords, source_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    edge_data = [(
        edge['source'],
        edge['target'],
        edge['weight'],
        edge['description'],
        edge['keywords'],
        edge['source_id']
    ) for edge in data['edges']]
    
    execute_batch(cursor, edge_query, edge_data)

def main():
    # Replace with your actual connection string
    conn_string = "postgres://XXX:YYY@pg-2e0b495c-congtrinh-1dc8.h.aivencloud.com:10389/defaultdb?sslmode=require"
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        # Read JSON data
        with open('graph_data.json', 'r') as file:
            data = json.load(file)
        
        # Create tables
        create_tables(cursor)
        
        # Insert data
        insert_data(cursor, data)
        
        # Commit the transaction
        conn.commit()
        print("Data successfully migrated to PostgreSQL!")
        
        # Verify the data
        cursor.execute("SELECT COUNT(*) FROM nodes")
        node_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM edges")
        edge_count = cursor.fetchone()[0]
        print(f"Inserted {node_count} nodes and {edge_count} edges")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()