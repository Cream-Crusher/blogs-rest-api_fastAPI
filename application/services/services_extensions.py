

async def load_associated_property(property_name: object, session: object, model: object, column_db: str, add_model: object) -> object:
    if property_name:
        for obj_id in property_name:
            obj_db = await session.get(add_model, obj_id)
            if obj_db:
                getattr(model, column_db).append(obj_db)
