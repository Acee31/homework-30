from contextlib import asynccontextmanager
from typing import AsyncGenerator, List

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas
from app.database import async_session, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeOut],
    summary="Эндпоинт для получения списка рецептов",
    description="Возвращает список всех рецептов из базы данных. "
    "Сортировка идет по кол-ву просмотров (по убыванию), "
    "а затем по времени приготовления (по возрастанию)",
)
async def recipes(session: AsyncSession = Depends(get_session)):
    res = await session.execute(
        select(models.Recipe).order_by(
            models.Recipe.views.desc(), models.Recipe.cooking_time
        )
    )
    return res.scalars().all()


@app.get(
    "/recipes/{id}",
    response_model=schemas.RecipeOut,
    summary="Получение рецепта по ID",
    description="Возвращает подробную информацию о рецепте. "
    "При каждом запросе увеличивает счетчик просмотров.",
)
async def recipe_with_id(
    id: int = Path(..., title="ID рецепта", description="ID рецепта", gt=0),
    session: AsyncSession = Depends(get_session),
):
    res = await session.get(models.Recipe, id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Рецепт с id - {id} не найден")

    res.views = res.views + 1 # type: ignore
    await session.commit()
    return res


@app.post(
    "/recipes",
    response_model=schemas.RecipeOut,
    summary="Создание нового рецепта",
    description="Создает новый рецепт в базе данных. "
    "Принимает название блюда, описание, время приготовления. "
    "Число просмотров устанавливается в 0",
)
async def post_recipe(
    recipe: schemas.RecipeIn, session: AsyncSession = Depends(get_session)
):
    new_recipe = models.Recipe(**recipe.dict())
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)

    return new_recipe
