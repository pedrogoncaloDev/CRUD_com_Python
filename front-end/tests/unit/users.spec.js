import { API_URL } from "../../src/utils.js";
import axios from "axios";

/* eslint-env jest */
describe("CRUD for users", () => {
    it("Select all users", async () => {
        const response = await axios.get(API_URL);

        expect(response.status).toBe(200);
        expect(Array.isArray(response.data)).toBe(true);
    });

    // it("Create a new user", async () => {
    //     const newUser = { name: "Test User", email: "test@example.com" };
    //     const response = await axios.post(API_URL, newUser);
    //     expect(response.status).toBe(201);
    //     expect(response.data).toHaveProperty("id");
    //     expect(response.data.name).toBe(newUser.name);
    // });

    // it("Update a user", async () => {
    //     // First, create a user to update
    //     const user = { name: "Update Me", email: "update@example.com" };
    //     const createRes = await axios.post(API_URL, user);
    //     const userId = createRes.data.id;

    //     // Update the user
    //     const updatedData = { name: "Updated Name" };
    //     const updateRes = await axios.put(`${API_URL}/${userId}`, updatedData);
    //     expect(updateRes.status).toBe(200);
    //     expect(updateRes.data.name).toBe(updatedData.name);
    // });

    // it("Delete a user", async () => {
    //     // First, create a user to delete
    //     const user = { name: "Delete Me", email: "delete@example.com" };
    //     const createRes = await axios.post(API_URL, user);
    //     const userId = createRes.data.id;

    //     // Delete the user
    //     const deleteRes = await axios.delete(`${API_URL}/${userId}`);
    //     expect(deleteRes.status).toBe(204);
    // });
});