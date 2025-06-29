from fastapi import FastAPI
from typing import List, Dict

app = FastAPI()

# Sample data for testimonials
testimonials = [
    {
        "img": "assets/images/gallery/1.jpg",
        "couple": "Ramesh & Priya",
        "testimonial": "We are extremely happy with the match we found.",
        "link": "#"
    }
]

@app.get("/testimonials", response_model=List[Dict])
async def get_testimonials():
    return testimonials