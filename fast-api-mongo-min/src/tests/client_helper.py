from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_test_client(app, get_db, Base):

    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    return TestClient(app)
