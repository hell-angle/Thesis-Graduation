import psycopg2
from tabulate import tabulate

def connect_to_db():
    conn_string = "postgres://XXX:YYY@pg-2e0b495c-congtrinh-1dc8.h.aivencloud.com:10389/defaultdb?sslmode=require"
    return psycopg2.connect(conn_string)

def execute_query(cursor, query, description):
    print(f"\n--- {description} ---")
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(results, headers=headers, tablefmt='grid'))
    return results

def run_analysis():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Query 1: Get all relationships for BEEKEEPERS
        beekeeper_relations = """
        SELECT 
            n1.id as source_entity,
            n1.entity_type as source_type,
            e.weight as relationship_strength,
            n2.id as target_entity,
            n2.entity_type as target_type,
            e.description as relationship_description
        FROM nodes n1
        JOIN edges e ON n1.id = e.source
        JOIN nodes n2 ON e.target = n2.id
        WHERE n1.id = 'BEEKEEPERS'
        ORDER BY e.weight DESC;
        """
        execute_query(cursor, beekeeper_relations, "Relationships involving BEEKEEPERS")

        # Query 2: Find the strongest relationships (highest weights)
        strongest_relations = """
        SELECT 
            n1.id as source,
            n2.id as target,
            e.weight as strength,
            e.description
        FROM edges e
        JOIN nodes n1 ON e.source = n1.id
        JOIN nodes n2 ON e.target = n2.id
        ORDER BY e.weight DESC
        LIMIT 5;
        """
        execute_query(cursor, strongest_relations, "Top 5 Strongest Relationships")

        # Query 3: Get all activities/events in the system
        activities = """
        SELECT 
            n.id,
            n.description,
            COUNT(e.*) as total_connections
        FROM nodes n
        LEFT JOIN edges e ON n.id = e.source OR n.id = e.target
        WHERE n.entity_type IN ('EVENT', 'TECHNOLOGY')
        GROUP BY n.id, n.description
        ORDER BY total_connections DESC;
        """
        execute_query(cursor, activities, "Activities and Events Analysis")

        # Query 4: Analyze relationships for THE BEEKEEPER
        beekeeper_activities = """
        SELECT 
            n2.id as related_entity,
            n2.entity_type,
            e.weight as relationship_strength,
            e.description,
            e.keywords
        FROM nodes n1
        JOIN edges e ON n1.id = e.source
        JOIN nodes n2 ON e.target = n2.id
        WHERE n1.id = 'THE BEEKEEPER'
        ORDER BY e.weight DESC;
        """
        execute_query(cursor, beekeeper_activities, "THE BEEKEEPER's Activities and Relationships")

        # Query 5: Find isolated nodes (nodes with no relationships)
        isolated_nodes = """
        SELECT n.id, n.entity_type, n.description
        FROM nodes n
        LEFT JOIN edges e ON n.id = e.source OR n.id = e.target
        WHERE e.source IS NULL AND e.target IS NULL;
        """
        execute_query(cursor, isolated_nodes, "Isolated Nodes (if any)")

        # Query 6: Analyze entity types distribution
        entity_distribution = """
        SELECT 
            entity_type,
            COUNT(*) as count,
            ROUND(AVG(
                (SELECT COUNT(*)
                FROM edges e
                WHERE n.id = e.source OR n.id = e.target)
            )::numeric, 2) as avg_connections
        FROM nodes n
        GROUP BY entity_type
        ORDER BY count DESC;
        """
        execute_query(cursor, entity_distribution, "Entity Type Distribution and Connectivity")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_analysis()