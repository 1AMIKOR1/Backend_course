from fastapi import FastAPI, Query, Body

import uvicorn

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Moscow', 'count_of_stars': 5},
    {'id': 2, 'title': 'Oskol', 'count_of_stars': 4}
]

@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Код отеля"),
        title: str | None = Query(None, description="Название отеля"),
        count_of_stars: int | None = Query(None, description="Количество звезд")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if count_of_stars and hotel["count_of_stars"] != count_of_stars:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels")
def create_hotels(
    title: str = Body(),
    count_of_stars: int = Body(),
):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "count_of_stars": count_of_stars
    })
    return {"status": "OK"}

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str = Body(),
    count_of_stars: int = Body(),
    ):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["count_of_stars"] = count_of_stars

    return {"status": "OK"}

@app.patch("/hotels/{hotel_id}")
def modify_hotel(
    hotel_id: int,
    title: str | None = Body(None),
    count_of_stars: int | None = Body(None)
    ):
    print(count_of_stars)
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if count_of_stars:
                hotel["count_of_stars"] = count_of_stars
            if title:
                hotel["title"] = title

    return {"status": "OK"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)