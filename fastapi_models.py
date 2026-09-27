from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, JSON, Numeric, String, TIMESTAMP, event, func, inspect
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

from postgres_database import Base, SessionLocal


class Test(Base):
    __tablename__ = "Test"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    Fname = Column(String(100), nullable=True)
    salary = Column(Numeric(10, 2), nullable=True)
    createdby = Column(String(50), nullable=False, default="System")
    createdat = Column(DateTime, default=datetime.now, nullable=False)
    modifiedby = Column(String(50), nullable=True)
    modifiedat = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    def __repr__(self):
        return f"<Test(Id={self.Id}, name='{self.name}', salary={self.salary})>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    createdby = Column(String(50), nullable=False, default="System", server_default="System")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    modifiedby = Column(String(50), nullable=True)
    modified_Dt = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


class UserAudit(Base):
    __tablename__ = "user_audits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True, index=True)
    action = Column(String(10), nullable=False)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    changed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


_AUDITED_USER_FIELDS = ("email", "createdby", "created_at", "modifiedby", "modified_Dt")
_PENDING_USER_AUDITS = "pending_user_audits"


def _audit_value(value):
    # Convert timestamps to values that can be stored in JSON columns.
    return value.isoformat() if isinstance(value, datetime) else value


def _user_snapshot(user):
    # Keep a snapshot of non-sensitive user fields; passwords are deliberately excluded.
    return {field: _audit_value(getattr(user, field)) for field in _AUDITED_USER_FIELDS}


def _capture_user_changes(session: Session, flush_context, instances):
    # Keep pending audit details on the session until the user rows have been flushed.
    pending = session.info.setdefault(_PENDING_USER_AUDITS, [])

    # Capture inserts before flush; generated primary keys are available afterward.
    for user in session.new:
        if isinstance(user, User):
            pending.append({"user": user, "action": "CREATE", "old_values": None})

    # Capture only fields whose SQLAlchemy history actually changed.
    for user in session.dirty:
        if not isinstance(user, User) or user in session.deleted:
            continue
        state = inspect(user)
        changed_fields = [field for field in _AUDITED_USER_FIELDS if state.attrs[field].history.has_changes()]
        if changed_fields:
            pending.append({
                "user": user,
                "action": "UPDATE",
                "old_values": {
                    field: _audit_value(state.attrs[field].history.deleted[0])
                    if state.attrs[field].history.deleted
                    else None
                    for field in changed_fields
                },
                "changed_fields": changed_fields,
            })

    # Preserve deleted values before the database removes the user row.
    for user in session.deleted:
        if isinstance(user, User):
            pending.append({"user": user, "action": "DELETE", "old_values": _user_snapshot(user)})


def _write_user_audits(session: Session, flush_context):
    # Consume this flush's snapshots so the audit insert does not audit itself.
    pending = session.info.pop(_PENDING_USER_AUDITS, [])
    for change in pending:
        user = change["user"]
        action = change["action"]

        # Read inserted or updated values after SQLAlchemy has applied defaults and generated IDs.
        if action == "CREATE":
            new_values = _user_snapshot(user)
        elif action == "UPDATE":
            new_values = {
                field: _audit_value(getattr(user, field))
                for field in change["changed_fields"]
            }
        else:
            new_values = None

        # Add the audit row to the same session transaction as the user change.
        session.add(UserAudit(
            user_id=user.id,
            action=action,
            old_values=change["old_values"],
            new_values=new_values,
        ))


def _clear_pending_user_audits(session: Session, previous_transaction):
    # Discard snapshots if the transaction rolls back before audit rows are written.
    session.info.pop(_PENDING_USER_AUDITS, None)


event.listen(SessionLocal, "before_flush", _capture_user_changes)
event.listen(SessionLocal, "after_flush_postexec", _write_user_audits)
event.listen(SessionLocal, "after_soft_rollback", _clear_pending_user_audits)