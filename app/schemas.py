from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    """
    Базовая схема рецепта
    """

    title: str = Field(..., title="Название блюда", description="Название блюда")
    description: str = Field(
        ..., title="Описание рецепта", description="Описание рецепта"
    )
    cooking_time: int = Field(
        ...,
        title="Время приготовления блюда (в минутах)",
        ge=1,
        description="Время приготовления (в минутах)",
    )


class RecipeIn(BaseRecipe):
    """
    Схема для создания нового рецепта
    """

    ...


class RecipeOut(BaseRecipe):
    """
    Схема для вывода рецепта с ID и количеством просмотров
    """

    id: int = Field(..., title="ID рецепта", description="ID рецепта")
    views: int = Field(
        0, title="Количество просмотров", description="Количество просмотров"
    )

    class Config:
        orm_model = True
