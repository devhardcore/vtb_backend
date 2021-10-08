from fastapi import FastAPI
# import sqlalchemy

app = FastAPI()

themes = {1, 2, 3}


@app.get("/themes")
def get_list_of_themes():
    return {"themes": themes}


@app.get("/theme/{theme_id}")
def get_theme(theme_id: int):
    return{
        "theme_id": theme_id,
        "name": "...",
        "theory": "...",
        "links": "...",
        "quiz": [{
            "question": "...",
            "image_url": "...",
            "wrong_answers": "...",
            "answer": "...",
            "points": "..."
        }],
    }
