import typing

from ..core import EntityManager

T = typing.TypeVar('T')


class Communication(EntityManager, typing.Generic[T]):
    object_name = 'communication'

    async def list(
            self,
            related_class: typing.Optional[str] = None,
            related_id: typing.Optional[int] = None,
            page: int = 0,
            count: int = 100,
            *args,
            **kwargs
    ) -> typing.List[T]:
        raw_result = await self._list(
            page=page,
            count=count,
            params={
                'class': related_class,
                'related_id': related_id,
            },
            **kwargs,
        )

        return [self._entity_class(id_=item.pop('id'), **item) for item in raw_result['items']]

    async def get(
            self,
            id_: int,
            related_class: typing.Optional[str] = None,
            related_id: typing.Optional[int] = None,
            **kwargs,
    ) -> T:
        raw_result = await self._get(
            id_=id_,
            params={
                'class': related_class,
                'related_id': related_id,
            },
            **kwargs,
        )

        return self._entity_class(id_=raw_result.pop('id'), **raw_result)

    async def save(
            self,
            model: T,
            related_class: typing.Optional[str] = None,
            related_id: typing.Optional[int] = None,
    ) -> T:
        raw_result = await self._save(
            params={
                'class': related_class,
                'related_id': related_id,
            },
            **model.serialize(),
        )
        return self._entity_class(id_=raw_result.pop('id'), **raw_result)
