from neo4j import GraphDatabase

USERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
TAGS = ['Hi', 'Hello', 'Bye', 'Hey', 'Goodbye']


class GraphDB:

    def __init__(self):
        self.driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "1"))
        with self.driver.session() as session:
            for user in USERS:
                session.write_transaction(self._create_users, user)

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def update_message(self, status, redis_id):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._update_status, status, redis_id)

    def find_by_tag(self):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            for tag in TAGS:
                result = (session.write_transaction(self._find_by_tag, tag))
                for record in result:
                    print('User {name1} sent tag "{tag}" to user {name2}'.format(name1=record["name1"],
                                                                                 tag=record["tag"],
                                                                                 name2=record["name2"]))

    def find_by_spam(self):
        with self.driver.session() as session:
            result = (session.write_transaction(self._find_by_spam))
            for record in result:
                print('User {name1} sent spam to user {name2}'.format(name1=record["name1"],
                                                                      name2=record["name2"]))

    def blocked_tag_messages(self):
        with self.driver.session() as session:
            for tag in TAGS:
                result = (session.write_transaction(self._spam_tags, tag))
                for record in result:
                    print('User {name1} tried to send tag "{tag}" to user {name2}, but it does not happen'.format(
                        name1=record["name1"],
                        tag=record["tag"],
                        name2=record["name2"]))

    def send_message(self, sender, adresee, msgtext, status, redis_id):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._send_message, sender, adresee, msgtext, status, redis_id)

    def nodes_in_radius(self, radius):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = (session.write_transaction(self._nodes_in_radius, radius))
            print('All pairs at distance = {radius}'.format(radius=radius))
            for record in result:
                print(
                    '{name1} and {name2}'.format(name1=record["name1"], name2=record["name2"]))

    def find_shortest_way(self, name1, name2):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = (session.write_transaction(self._find_shortest_way, name1, name2))
            for record in result:
                print(
                    'Distance between {name1} and {name2} is {length}'.format(name1=name1, length=record, name2=name2))

    @staticmethod
    def _send_message(tx, sender, adresee, msgtext, status, redis_id):
        query = ("Match (a:Person {name: $sender}) "
                 "Match (b:Person {name: $adresee}) "
                 "MERGE (a)-[:SENDS {text: $msgtext, status: $status, redis_id: $redis_id} ]->(b)")
        tx.run(query, sender=sender, msgtext=msgtext, status=status, adresee=adresee, redis_id=redis_id)

    @staticmethod
    def _find_by_tag(tx, tag):
        query = ("MATCH (p1:Person) - [a:SENDS {text: $tag}]-> (p2:Person) "
                 "return a.text as text, p1.name as name1, p2.name as name2 ")
        result = tx.run(query, tag=tag)
        return [{"name1": record["name1"], "name2": record["name2"], "tag": record["text"]}
                for record in result]

    @staticmethod
    def _spam_tags(tx, tag):
        query = ('MATCH (p1:Person) - [a:SENDS {text: $tag, status:"spam"}]-> (p2:Person) '
                 'return a.text as text, p1.name as name1, p2.name as name2 ')
        result = tx.run(query, tag=tag)
        return [{"name1": record["name1"], "name2": record["name2"], "tag": record["text"]}
                for record in result]

    @staticmethod
    def _find_shortest_way(tx, name1, name2):
        query = ("MATCH (p1:Person {name: $name1} ),"
                 "(p2:Person {name: $name2}),"
                 "p = shortestPath((p1)-[*]-(p2))"
                 "RETURN length(p) as length")
        result = tx.run(query, name1=name1, name2=name2)
        return [record["length"] for record in result]

    @staticmethod
    def _update_status(tx, status, redis_id):
        query = "MATCH() - [a: SENDS {redis_id: $redis_id}]->() SET a.status = $status"
        tx.run(query, status=status, redis_id=redis_id)

    @staticmethod
    def _create_users(tx, user):
        query = "MERGE (a:Person {name: $user}) "
        tx.run(query, user=user)

    @staticmethod
    def _find_by_spam(tx):
        query = 'MATCH (p1:Person) - [a:SENDS {status:"spam"}]-> (p2:Person) return p1.name as name1, p2.name as name2'
        result = tx.run(query)
        return [{"name1": record["name1"], "name2": record["name2"]}
                for record in result]

    @staticmethod
    def _nodes_in_radius(tx, radius):
        query = 'MATCH (p1:Person) - [*2]-> (p2:Person) return p1.name as name1, p2.name as name2'
        result = tx.run(query, radius=radius)
        return [{"name1": record["name1"], "name2": record["name2"]}
                for record in result]
