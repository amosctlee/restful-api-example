

# Dependency
def get_db():
    # 會 return generator，因此直接呼叫回傳的不是 db
    # 最好透過 Depends 來使用
    from db import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
