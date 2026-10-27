const express = require("express");

const fetch = (...args) =>
    import("node-fetch").then(({ default: fetch }) => fetch(...args));

const app = express();
const port = Number(process.env.PORT) || 3000;
const backendUrl = (process.env.BACKEND_URL || "http://localhost:5000")
    .replace(/\/+$/, "");

// Allow Express to read HTML form data
app.use(express.urlencoded({ extended: true }));
app.use(express.json());


// Home page
app.get("/", (req, res) => {
    res.sendFile("index.html", { root: __dirname });
});


// Handle form submission
app.post("/submit", async (req, res) => {
    const { name, email, message } = req.body || {};
    const fields = { name, email, message };
    const invalidField = Object.entries(fields).find(
        ([, value]) => typeof value !== "string" || value.trim() === ""
    );

    if (invalidField) {
        return res.status(400).send(`A valid ${invalidField[0]} is required.`);
    }

    try {
        const response = await fetch(`${backendUrl}/submit`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name.trim(),
                email: email.trim(),
                message: message.trim()
            })
        });

        const result = await response.json().catch(() => null);

        if (!response.ok) {
            console.error(`Flask returned HTTP ${response.status}:`, result);
            return res.status(502).send("The Flask backend could not process the submission.");
        }

        if (!result || typeof result.message !== "string") {
            console.error("Flask returned an invalid response.");
            return res.status(502).send("The Flask backend returned an invalid response.");
        }

        return res.send(result.message);
    } catch (error) {
        console.error(`Error connecting to Flask at ${backendUrl}:`, error);
        return res.status(502).send("Could not connect to Flask.");
    }
});


// Start Node.js server
app.listen(port, "0.0.0.0", () => {
    console.log(`Frontend is running on port ${port}`);
});