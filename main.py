#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status, HTTPException
from fastapi import Body, Query, Path, Form, Cookie, Header, UploadFile, File
#prueba
app = FastAPI()

#Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_lenght=0,
        max_length=60,
        example="San Francisco"
    )
    state: str = Field(
         ...,
        min_lenght=0,
        max_length=60,
        example="California"
    )
    country: str = Field(
         ...,
        min_lenght=0,
        max_length=60,
        example="USA"
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="Pedro"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example="Monroy"
    )
    age: int = Field(
        ...,
        gt=0, 
        lt=130,
        example=14
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example="brown"
    )
    is_married: Optional[bool] = Field(
        default=None,
        example=False
    )
    password: str = Field(
        ...,
        min_length=8,
        example="1234Abcd/"
    )

class User_info(Location, Person):
    pass

class ExpertPlusPerson(Person):
    english_academy_access = True

#Path Operations

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home and Hello World"
    )
def home():
    """
    Home

    This path operation returns a JSON with a Hello World

    Returns:
        {"Hello": "World"}
    """
    return {"Hello": "World"}

@app.post(
    path="/person/new",
    response_model=Person, 
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["People"],
    summary="Create a person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters: 
    - Request body parameter: 
        - **person: Person** -> A person model with first name, last name, age, hair color and marital stauts.

    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

@app.get(
    path="/person/details",
    status_code=status.HTTP_200_OK,
    tags=["People"],
    summary="Get person details"
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        title="User's name",
        min_length=1, 
        max_length=50,
        example="Mario"),
    last_name: Optional[str] = Query(
        None, 
        title="User's last name",
        min_length=1, 
        max_length=50,
        example="Gomez"),
    age: Optional[int] = Query(
        None, 
        title="User's age",
        ge=1, 
        le=130,
        example="56"),
):
    """
    Person details

    This path operation uses query parameters to return a JSON with the name, last name and age.

    Parameters: 
    - Query Parameters:
        - **name: Optional[str]** -> A query parameter with the name.
        - **last_name Optional[str]** -> A query parameter with the last name.
        - **age Optional[str]** -> A query parameter with the age of the person.

    Returns the name, last name and age.
    """    
    return {name + " " + last_name: age}

people = [1, 2, 3, 4, 5]

@app.get(
    path="/person/details/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["People"], 
    summary="Get person details"
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person's id")
):
    """
    Get person details

    This path operation returns if there is a person with that id.

    Parameters: 
    - Path Parameter:
        - **person_id: int** -> A query parameter with the user id.

    Returns a JSON with the ID and if that exists.
    """
    if person_id not in people: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="¡This person doesn't exist!" ) 
    return {person_id: "It exists!"}

@app.put(
    path="/person/{person_id}",
    response_model=User_info,
    response_model_exclude={"password", "description"},
    status_code=status.HTTP_202_ACCEPTED,
    tags=["People"],
    summary="Update person data"
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    """
    Update person data 

    The path operation updates the data of the user, including the location and the personal info.

    Parameters: 
    - Path Parameter:
        - **person_id: int** -> a path parameter with the user id.
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital.
        - **location: Location** -> A location model with the city state and country.

    Returns a combination of the models person and location without the password.
    """
    results = person.dict()
    results.update(location.dict())
    return results 
    
@app.post(
    path="/login",
    status_code=status.HTTP_201_CREATED,
    tags=["People"], 
    summary="Log into the app"
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Log into the app

    The form log the user into the app.

    Parameters:
    - Form Parameter:
        - **username: str** -> A form entry with the username.
        - **password: str** -> A form entry with the password.

    Returns a JSON with the username.
    """
    return {"username": username}

@app.post(
    path="/contact",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Contact"],
    summary="Contact form"
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
     last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    """
    Contact form

    This form be useful to contact the API's owner.

    Parameters: 
    - Form Parameter:
        - **first_name: str** -> A form entry with the first name.
        - **last_name: str** -> A form entry with the last name.
        - **email: EmailStr** -> A form entry with the email.
        - **message: str** -> A form entry with the message to send.
    - Header Parameter:
        - **user_agent: Optional[str]** -> A header parameter with the information of the user's device.
    - Cookies:
        - **ads: Optional[str]** -> A cookie parameter.

    Returns the user's device information.
    """
    return user_agent

@app.post(
    path="/post-image",
    status_code=status.HTTP_201_CREATED,
    tags=["Post"],
    summary="Upload image"
)
def post_image(
    image: UploadFile = File(...),
): 
    """
    Upload images

    This path operation upload images.

    Parameters: 
    - Request File:
        - **image: UploadFile** -> A request file for uploading images.

    Returns information of the image, the name, the type and the size in KB.

    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }