import os
import json
import time
from tqdm import trange
from sqlalchemy import create_engine, MetaData, update, text, select, func
try:
    from SPARQLWrapper import SPARQLWrapper, JSON
except:
    print("SPARQLWrapper not installed")
    exit(1)


from configs import basedir

wikidata_endpoint = "https://query.wikidata.org/sparql"
sparql = SPARQLWrapper(wikidata_endpoint)
sparql.setReturnFormat(JSON)

label_mapping = json.load(open(os.path.join(basedir, "all_properties_label.json")))

engine = create_engine(f'sqlite:///{os.path.join(basedir, "crud_prod.db")}')
meta = MetaData(bind=engine)
MetaData.reflect(meta)
Fact = meta.tables["fact"]


def get_unique_values(column_name: str):
    sql = text(f"SELECT DISTINCT {column_name} FROM fact")
    return [item[0] for item in engine.execute(sql).fetchall()]


def update_predicate_labels():
    unique_predicates = get_unique_values("predicate_id")
    for predicate_id in unique_predicates:
        u = update(Fact)
        u = u.values({'predicate_label': label_mapping[predicate_id][0]})
        u = u.where(Fact.c.predicate_id == predicate_id)
        engine.execute(u)


def find_label_for_entity(qid):
    query = """
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wikibase: <http://wikiba.se/ontology#>
            select ?label
                where {{
                    wd:{entity} rdfs:label ?label.
                    filter(lang(?label)='en').
                }} limit 3000
                    """.format(entity=qid)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        return result["label"]["value"]
    return None


def update_entity_labels():
    count_query = select([func.count()]).select_from(Fact)
    total = engine.execute(count_query).scalar()
    for row_id in trange(1, total + 1):
        subject_id, subject_label = engine.execute(
            select([Fact.c.subject_id, Fact.c.subject_label]).where(Fact.c.id == row_id)).fetchone()
        if subject_label is not None:
            continue
        label = None
        try:
            label = find_label_for_entity(subject_id)
        except:
            time.sleep(5)

        if label is None:
            continue

        u = update(Fact)
        u = u.values({'subject_label': label})
        u = u.where(Fact.c.id == row_id)
        engine.execute(u)


# update_predicate_labels()
update_entity_labels()
