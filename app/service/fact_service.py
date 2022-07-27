from sqlalchemy import func
from typing import Dict, Any, List, Tuple
import logging

from app import db
from app.model.fact import Fact

logger = logging.getLogger(__name__)


def create_a_fact(data: Dict[str, Any]) -> bool:
    fact = Fact.query.filter_by(
        subject_url=data["subject_url"],
        object_url=data["object_url"],
        predicate_url=data["predicate_url"]
    ).first()
    if fact:
        logger.error(f"Already exists fact with subject_url: {data['subject_url']}")
        return False

    new_fact = Fact(**data)
    db.session.add(new_fact)
    db.session.commit()

    return True


def delete_a_fact(fact_id: int) -> bool:
    fact = Fact.query.filter_by(id=fact_id).first()
    if not fact:
        logger.error(f"Cannot find fact with id {fact_id}")
        return False
    db.session.delete(fact)
    db.session.commit()
    return True


def update_a_fact(fact_id: int, data: Dict[str, Any]) -> bool:
    fact = Fact.query.filter_by(id=fact_id).first()
    if not fact:
        logger.error(f"Cannot find fact with id {fact_id}")
        return False
    fact.feedback = data["feedback"]
    db.session.add(fact)
    db.session.commit()
    return True


def find_all_facts(page: int, per_page: int = 10, source_name: str = None, predicate_id: str = None) -> Tuple[List[Fact], int]:
    filters = {"source_name": source_name, "predicate_id": predicate_id}
    filters = {k: v for k, v in filters.items() if v is not None}
    if filters:
        fact_query = Fact.query.filter_by(**filters).paginate(page, per_page, False)
    else:
        fact_query = Fact.query.paginate(page=page, per_page=per_page, error_out=False)
    total = fact_query.total
    facts = fact_query.items
    return facts, total


def find_fact_by_id(fact_id: int) -> Fact:
    fact = Fact.query.filter_by(id=fact_id).first()
    if not fact:
        logger.error(f"Cannot find fact with id {fact_id}")
        return None
    return fact


def value_counts_source_name():
    row = db.session.query(Fact.source_name, func.count()).group_by(Fact.source_name).all()
    value_counts = {item[0]: item[1] for item in row}
    return [{
        'type': key,
        'count': value,
    } for key, value in value_counts.items()]


def value_counts_predicate_id():
    row = db.session.query(Fact.predicate_id, func.count()).group_by(Fact.predicate_id).all()
    value_counts = {item[0]: item[1] for item in row}
    return [{
        'type': key,
        'count': value,
    } for key, value in value_counts.items()]


def average_confidence():
    row = db.session.query(func.avg(Fact.confidence_reader)).first()
    return row[0]


def find_unique_source_names(predicate_id: str = None):
    if predicate_id:
        row = db.session.query(Fact.source_name, Fact.predicate_id).filter(Fact.predicate_id == predicate_id).distinct().all()
    else:
        row = db.session.query(Fact.source_name).distinct().all()
    source_names = [item[0] for item in row]
    return source_names


def find_unique_predicate_ids(source_name: str = None):
    if source_name:
        row = db.session.query(Fact.predicate_id, Fact.source_name).filter(Fact.source_name == source_name).distinct().all()
    else:
        row = db.session.query(Fact.predicate_id).distinct().all()
    predicate_ids = [item[0] for item in row]
    return predicate_ids

