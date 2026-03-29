const music_options = ["Pop", "Indie", "Rock", "Classical", "RnB", "Hip-Hop", "EDM"];
const music_container = document.getElementById("music-button-container");
music_options.forEach(label => {
    const music_btn = document.createElement("button");
    music_btn.classList.add("option-btn");
    music_btn.textContent = label;
    music_btn.addEventListener("click", () => { music_btn.classList.toggle("selected"); });
    music_container.appendChild(music_btn);
});

const book_options = ["Action", "Comedy", "Crime", "Fantasy", "Horror", "Romance", "Sci-Fi"];
const book_container = document.getElementById("book-button-container");
book_options.forEach(label => {
    const book_btn = document.createElement("button");
    book_btn.classList.add("option-btn");
    book_btn.textContent = label;
    book_btn.addEventListener("click", () => { book_btn.classList.toggle("selected"); });
    book_container.appendChild(book_btn);
});

const movie_options = ["Action", "Comedy", "Crime", "Fantasy", "Horror", "Romance", "Sci-Fi"];
const movie_container = document.getElementById("movie-button-container");
movie_options.forEach(label => {
    const movie_btn = document.createElement("button");
    movie_btn.classList.add("option-btn");
    movie_btn.textContent = label;
    movie_btn.addEventListener("click", () => { movie_btn.classList.toggle("selected"); });
    movie_container.appendChild(movie_btn);
});

const cuisine_options = ["Indian", "Italian", "Chinese", "Japanese", "Mexican", "Thai", "Greek"];
const cuisine_container = document.getElementById("cuisine-button-container");
cuisine_options.forEach(label => {
    const cuisine_btn = document.createElement("button");
    cuisine_btn.classList.add("option-btn");
    cuisine_btn.textContent = label;
    cuisine_btn.addEventListener("click", () => { cuisine_btn.classList.toggle("selected"); });
    cuisine_container.appendChild(cuisine_btn);
});

const dietry_options = ["Vegetarian", "Vegan", "Gluten-free", "Non-vegetarian"];
const dietry_container = document.getElementById("dietry-button-container");
dietry_options.forEach(label => {
    const dietry_btn = document.createElement("button");
    dietry_btn.classList.add("option-btn");
    dietry_btn.textContent = label;
    dietry_btn.addEventListener("click", () => { dietry_btn.classList.toggle("selected"); });
    dietry_container.appendChild(dietry_btn);
});

const hobby_options = ["Sports", "Hiking", "Arts and Crafts", "Video-games", "Puzzles"];
const hobby_container = document.getElementById("hobby-button-container");
hobby_options.forEach(label => {
    const hobby_btn = document.createElement("button");
    hobby_btn.classList.add("option-btn");
    hobby_btn.textContent = label;
    hobby_btn.addEventListener("click", () => { hobby_btn.classList.toggle("selected"); });
    hobby_container.appendChild(hobby_btn);
});

document.querySelector(".save-button").addEventListener("click", async () => {
    const saveBtn = document.querySelector(".save-button");
    saveBtn.disabled = true;
    saveBtn.textContent = "Loading...";

    const selected_music = [...document.querySelectorAll("#music-button-container .option-btn.selected")]
        .map(btn => btn.textContent);
    const selected_books = [...document.querySelectorAll("#book-button-container .option-btn.selected")]
        .map(btn => btn.textContent);
    const selected_movies = [...document.querySelectorAll("#movie-button-container .option-btn.selected")]
        .map(btn => btn.textContent);
    const selected_cuisines = [...document.querySelectorAll("#cuisine-button-container .option-btn.selected")]
        .map(btn => btn.textContent);
    const selected_dietary = [...document.querySelectorAll("#dietry-button-container .option-btn.selected")]
        .map(btn => btn.textContent);
    const selected_hobbies = [...document.querySelectorAll("#hobby-button-container .option-btn.selected")]
        .map(btn => btn.textContent);

    try {
        const response = await fetch("/save-preferences", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                music:    selected_music,
                books:    selected_books,
                movies:   selected_movies,
                cuisines: selected_cuisines,
                dietary:  selected_dietary,
                hobbies:  selected_hobbies
            })
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();
        sessionStorage.setItem("recommendations", JSON.stringify(data.recommendations));
        window.location.href = "/dashboard";

    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong, please try again in a moment.");
        saveBtn.disabled = false;
        saveBtn.textContent = "Confirm Choices";
    }
});