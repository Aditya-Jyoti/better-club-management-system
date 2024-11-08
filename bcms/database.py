from prisma import Prisma

db = Prisma()


# dependency for prisma db connection
async def get_db():
    if not db.is_connected():
        await db.connect()
    try:
        yield db
    finally:
        pass
        
