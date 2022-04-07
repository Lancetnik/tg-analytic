from pydantic import BaseModel, validator


class Pagination(BaseModel):
    page: int = 1
    size: int = 10

    @validator('page')
    def page_gt_one(cls, v):
        if v < 1:
            raise ValueError('Page can not be less then 1')
        return v

    @validator('size')
    def size_gt_one(cls, v):
        if v < 1:
            raise ValueError('Size can not be less then 1')
        return v
