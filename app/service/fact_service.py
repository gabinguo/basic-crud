from sqlalchemy import asc
from typing import Dict, Any, List
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


def find_all_facts(limit: int = 100, offset: int = 0) -> List[Fact]:
    facts = Fact.query.order_by(asc(Fact.id)).limit(limit).offset(offset).all()
    return facts


def find_fact_by_id(fact_id: int) -> Fact:
    fact = Fact.query.filter_by(id=fact_id).first()
    if not fact:
        logger.error(f"Cannot find fact with id {fact_id}")
        return None
    return fact


def find_unique_source_names():
    row = db.session.query(Fact.source_name).distinct().all()
    source_names = [item[0] for item in row]
    return source_names


def find_unique_predicate_ids():
    row = db.session.query(Fact.predicate_id).distinct().all()
    predicate_ids = [item[0] for item in row]
    return predicate_ids
