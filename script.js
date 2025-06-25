document.getElementById("recipe-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const ingredients = document.getElementById("ingredients").value.trim();
    const cuisine = document.getElementById("cuisine").value;

    if (!ingredients) {
        alert("Please enter ingredients.");
        return;
    }

    const responseBox = document.getElementById("response");
    responseBox.innerHTML = "⏳ Generating your recipe...";

    try {
        const res = await fetch("http://127.0.0.1:5000/generate-recipe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ ingredients, cuisine })
        });

        const data = await res.json();

        if (data.recipe) {
            responseBox.innerHTML = `<pre>${data.recipe}</pre>`;
        } else {
            responseBox.innerHTML = `<p style="color: red;">❌ ${data.error}</p>`;
        }
    } catch (err) {
        responseBox.innerHTML = `<p style="color: red;">🚨 Failed to fetch recipe. Make sure Flask server is running.</p>`;
        console.error(err);
    }
});

