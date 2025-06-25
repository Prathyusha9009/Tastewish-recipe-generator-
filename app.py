from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Sample dataset with 10 recipes per cuisine
recipes_db = {
    "Indian": [
        {
            "title": "Chole Bhature",
            "ingredients": ["chickpeas", "onion", "tomato", "spices", "flour"],
            "instructions": [
                "Soak chickpeas overnight and cook until soft.",
                "Prepare masala with onion, tomato, and spices.",
                "Mix cooked chickpeas in masala and simmer.",
                "Make dough with flour and roll into bhature.",
                "Deep fry and serve hot with chole."
            ],
            "time": 45,
            "difficulty": "Medium"
        },
        {
            "title": "Paneer Butter Masala",
            "ingredients": ["paneer", "butter", "tomato", "cream", "spices"],
            "instructions": [
                "Prepare rich gravy using tomato, cream and spices.",
                "Add fried paneer cubes and simmer.",
                "Garnish with coriander and serve with naan."
            ],
            "time": 30,
            "difficulty": "Easy"
        },
        {
            "title": "Aloo Paratha",
            "ingredients": ["potatoes", "flour", "spices", "onion", "ghee"],
            "instructions": [
                "Boil and mash potatoes with spices and onion.",
                "Stuff mixture in rolled dough and seal edges.",
                "Cook on tawa with ghee until golden brown."
            ],
            "time": 25,
            "difficulty": "Easy"
        },
        {
            "title": "Rajma Chawal",
            "ingredients": ["kidney beans", "onion", "tomato", "spices", "rice"],
            "instructions": [
                "Soak and boil kidney beans.",
                "Prepare onion-tomato masala.",
                "Mix beans in masala and simmer.",
                "Serve hot with rice."
            ],
            "time": 40,
            "difficulty": "Medium"
        },
        {
            "title": "Masala Dosa",
            "ingredients": ["rice", "urad dal", "potatoes", "mustard seeds", "spices"],
            "instructions": [
                "Prepare dosa batter by fermenting rice and dal.",
                "Make potato filling with spices.",
                "Spread batter on tawa, add filling and fold dosa."
            ],
            "time": 35,
            "difficulty": "Medium"
        },
        {
            "title": "Sambar",
            "ingredients": ["toor dal", "vegetables", "tamarind", "sambar powder"],
            "instructions": [
                "Boil dal and cook vegetables.",
                "Add tamarind and sambar powder.",
                "Simmer and temper with mustard and curry leaves."
            ],
            "time": 30,
            "difficulty": "Easy"
        },
        {
            "title": "Butter Naan",
            "ingredients": ["flour", "yogurt", "baking powder", "butter"],
            "instructions": [
                "Make dough and let it rest.",
                "Roll and cook on tawa or tandoor.",
                "Brush with butter before serving."
            ],
            "time": 20,
            "difficulty": "Easy"
        },
        {
            "title": "Tandoori Chicken",
            "ingredients": ["chicken", "yogurt", "spices", "lemon"],
            "instructions": [
                "Marinate chicken with spices and yogurt.",
                "Grill or bake until cooked.",
                "Serve with lemon wedges."
            ],
            "time": 45,
            "difficulty": "Medium"
        },
        {
            "title": "Palak Paneer",
            "ingredients": ["spinach", "paneer", "garlic", "spices", "onion"],
            "instructions": [
                "Blanch spinach and blend.",
                "Prepare garlic-onion masala.",
                "Add spinach puree and paneer, cook for 10 min."
            ],
            "time": 30,
            "difficulty": "Easy"
        },
        {
            "title": "Biryani",
            "ingredients": ["basmati rice", "chicken", "yogurt", "spices", "onion"],
            "instructions": [
                "Marinate chicken and cook with spices.",
                "Layer with rice and cook on dum.",
                "Serve with raita."
            ],
            "time": 60,
            "difficulty": "Hard"
        }
    ],
    "Italian": [
        {
            "title": "Margherita Pizza",
            "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil"],
            "instructions": [
                "Spread tomato sauce on rolled pizza dough.",
                "Add mozzarella and fresh basil.",
                "Bake at high heat until crust is golden."
            ],
            "time": 25,
            "difficulty": "Easy"
        },
        {
            "title": "Pasta Carbonara",
            "ingredients": ["spaghetti", "eggs", "cheese", "pepper", "bacon"],
            "instructions": [
                "Cook pasta and save some starchy water.",
                "Fry bacon until crisp.",
                "Mix eggs and cheese, then combine with pasta and bacon.",
                "Add water for creamy texture."
            ],
            "time": 20,
            "difficulty": "Medium"
        },
        {
            "title": "Lasagna",
            "ingredients": ["lasagna sheets", "minced meat", "cheese", "tomato sauce"],
            "instructions": [
                "Prepare meat sauce.",
                "Layer sheets, sauce and cheese.",
                "Bake until golden and bubbling."
            ],
            "time": 50,
            "difficulty": "Hard"
        },
        {
            "title": "Bruschetta",
            "ingredients": ["bread", "tomato", "basil", "garlic", "olive oil"],
            "instructions": [
                "Toast bread.",
                "Top with tomato, basil, and garlic mix.",
                "Drizzle with olive oil."
            ],
            "time": 15,
            "difficulty": "Easy"
        },
        {
            "title": "Risotto",
            "ingredients": ["arborio rice", "onion", "white wine", "cheese"],
            "instructions": [
                "Sauté onion, add rice and wine.",
                "Gradually add broth and stir until creamy.",
                "Add cheese before serving."
            ],
            "time": 35,
            "difficulty": "Medium"
        },
        {
            "title": "Gnocchi",
            "ingredients": ["potatoes", "flour", "egg", "butter", "cheese"],
            "instructions": [
                "Boil and mash potatoes.",
                "Mix with flour and egg to form dough.",
                "Cut and boil gnocchi, then sauté in butter."
            ],
            "time": 40,
            "difficulty": "Medium"
        },
        {
            "title": "Tiramisu",
            "ingredients": ["ladyfingers", "coffee", "mascarpone", "cocoa powder"],
            "instructions": [
                "Dip ladyfingers in coffee.",
                "Layer with mascarpone cream.",
                "Dust with cocoa and chill."
            ],
            "time": 30,
            "difficulty": "Easy"
        },
        {
            "title": "Caprese Salad",
            "ingredients": ["tomato", "mozzarella", "basil", "olive oil"],
            "instructions": [
                "Slice tomatoes and mozzarella.",
                "Arrange with basil.",
                "Drizzle with olive oil."
            ],
            "time": 10,
            "difficulty": "Easy"
        },
        {
            "title": "Stuffed Shells",
            "ingredients": ["pasta shells", "ricotta", "spinach", "tomato sauce", "cheese"],
            "instructions": [
                "Stuff shells with ricotta and spinach mix.",
                "Place in baking dish with sauce and cheese.",
                "Bake until bubbly."
            ],
            "time": 40,
            "difficulty": "Medium"
        },
        {
            "title": "Pesto Pasta",
            "ingredients": ["pasta", "basil", "garlic", "pine nuts", "cheese"],
            "instructions": [
                "Blend basil, garlic, pine nuts and cheese with oil.",
                "Toss with cooked pasta."
            ],
            "time": 20,
            "difficulty": "Easy"
        }
    ],
    "Chinese": [
        {
            "title": "Vegetable Fried Rice",
            "ingredients": ["rice", "soy sauce", "vegetables", "garlic", "egg"],
            "instructions": [
                "Scramble eggs and stir fry vegetables.",
                "Add cooked rice and soy sauce.",
                "Mix well and cook on high heat."
            ],
            "time": 15,
            "difficulty": "Easy"
        },
        {
            "title": "Chilli Paneer",
            "ingredients": ["paneer", "bell pepper", "soy sauce", "onion", "cornflour"],
            "instructions": [
                "Fry paneer cubes until golden.",
                "Stir fry vegetables with sauces.",
                "Add paneer and coat with thickened sauce."
            ],
            "time": 25,
            "difficulty": "Medium"
        },
        {
            "title": "Spring Rolls",
            "ingredients": ["spring roll sheets", "vegetables", "soy sauce", "oil"],
            "instructions": [
                "Stir fry vegetables with sauce.",
                "Roll in sheets and seal.",
                "Deep fry until golden."
            ],
            "time": 30,
            "difficulty": "Medium"
        },
        {
            "title": "Hakka Noodles",
            "ingredients": ["noodles", "vegetables", "soy sauce", "vinegar", "pepper"],
            "instructions": [
                "Boil noodles and drain.",
                "Stir fry vegetables and mix with sauces.",
                "Add noodles and toss well."
            ],
            "time": 20,
            "difficulty": "Easy"
        },
        {
            "title": "Manchurian",
            "ingredients": ["vegetable balls", "soy sauce", "cornflour", "garlic"],
            "instructions": [
                "Fry vegetable balls.",
                "Make thick sauce and add balls.",
                "Simmer and serve."
            ],
            "time": 35,
            "difficulty": "Medium"
        },
        {
            "title": "Sweet and Sour Tofu",
            "ingredients": ["tofu", "pineapple", "soy sauce", "sugar", "vinegar"],
            "instructions": [
                "Fry tofu and set aside.",
                "Make sweet sour sauce with pineapple.",
                "Add tofu and simmer."
            ],
            "time": 30,
            "difficulty": "Medium"
        },
        {
            "title": "Hot and Sour Soup",
            "ingredients": ["mushroom", "carrot", "soy sauce", "pepper", "cornflour"],
            "instructions": [
                "Boil vegetables.",
                "Add sauces and thicken with cornflour."
            ],
            "time": 20,
            "difficulty": "Easy"
        },
        {
            "title": "Dim Sum",
            "ingredients": ["dumpling wrappers", "vegetables", "soy sauce", "ginger"],
            "instructions": [
                "Stuff wrappers and seal edges.",
                "Steam until translucent."
            ],
            "time": 30,
            "difficulty": "Medium"
        },
        {
            "title": "Kung Pao Chicken",
            "ingredients": ["chicken", "peanuts", "chilli", "soy sauce"],
            "instructions": [
                "Marinate and stir fry chicken.",
                "Add peanuts and sauce.",
                "Cook until thick."
            ],
            "time": 25,
            "difficulty": "Medium"
        },
        {
            "title": "Sesame Noodles",
            "ingredients": ["noodles", "soy sauce", "sesame oil", "garlic", "vinegar"],
            "instructions": [
                "Cook noodles.",
                "Toss with sauce and garlic."
            ],
            "time": 15,
            "difficulty": "Easy"
        }
    ]
}

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    ingredients = data.get('ingredients', '').lower()
    cuisine = data.get('cuisine', 'Any')

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    cuisine_recipes = recipes_db.get(cuisine, [])

    matching_recipes = []
    input_ings = [i.strip().lower() for i in ingredients.split(",")]

    for recipe in cuisine_recipes:
        match_count = sum(1 for ing in recipe['ingredients'] if ing.lower() in input_ings)
        if match_count >= 2:  # You can adjust this threshold
            matching_recipes.append(recipe)

    if not matching_recipes:
        return jsonify({"error": "No matching recipe found."})

    selected = random.choice(matching_recipes)

    result = f"🍽️ <b>{selected['title']}</b>\n\n"
    result += f"<b>Ingredients:</b> {', '.join(selected['ingredients'])}\n"
    result += f"<b>Cooking Time:</b> {selected['time']} minutes\n"
    result += f"<b>Difficulty:</b> {selected['difficulty']}\n\n"
    result += "<b>Instructions:</b>\n" + "\n".join(
        [f"{i+1}. {step}" for i, step in enumerate(selected['instructions'])])

    return jsonify({"recipe": result})

if __name__ == '__main__':
    app.run(debug=True)

