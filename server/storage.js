import { randomUUID } from "crypto";
import * as fs from "fs";
import * as path from "path";

const DB_DIR = path.join(process.cwd(), "db");
const USERS_FILE = path.join(DB_DIR, "users.json");
const POSTS_FILE = path.join(DB_DIR, "posts.json");

function ensureDbExists() {
  if (!fs.existsSync(DB_DIR)) {
    fs.mkdirSync(DB_DIR, { recursive: true });
  }
  if (!fs.existsSync(USERS_FILE)) {
    fs.writeFileSync(USERS_FILE, "[]", "utf-8");
  }
  if (!fs.existsSync(POSTS_FILE)) {
    fs.writeFileSync(POSTS_FILE, "[]", "utf-8");
  }
}

function readUsers() {
  ensureDbExists();
  const data = fs.readFileSync(USERS_FILE, "utf-8");
  return JSON.parse(data);
}

function writeUsers(users) {
  ensureDbExists();
  fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), "utf-8");
}

function readPosts() {
  ensureDbExists();
  const data = fs.readFileSync(POSTS_FILE, "utf-8");
  return JSON.parse(data);
}

function writePosts(posts) {
  ensureDbExists();
  fs.writeFileSync(POSTS_FILE, JSON.stringify(posts, null, 2), "utf-8");
}

export class JsonStorage {
  async getUser(id) {
    const users = readUsers();
    return users.find((u) => u.id === id);
  }

  async getUserByUsername(username) {
    const users = readUsers();
    return users.find((u) => u.username.toLowerCase() === username.toLowerCase());
  }

  async createUser(insertUser) {
    const users = readUsers();
    const id = randomUUID();
    const user = { ...insertUser, id };
    users.push(user);
    writeUsers(users);
    return user;
  }

  async getPosts(limit) {
    const posts = readPosts();
    const sorted = posts.sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
    return limit ? sorted.slice(0, limit) : sorted;
  }

  async getPost(id) {
    const posts = readPosts();
    return posts.find((p) => p.id === id);
  }

  async searchPosts(query) {
    const posts = readPosts();
    const lowerQuery = query.toLowerCase();
    return posts.filter(
      (p) =>
        p.title.toLowerCase().includes(lowerQuery) ||
        p.content.toLowerCase().includes(lowerQuery) ||
        p.author.toLowerCase().includes(lowerQuery)
    );
  }

  async createPost(insertPost) {
    const posts = readPosts();
    const id = randomUUID();
    const post = {
      ...insertPost,
      id,
      createdAt: new Date().toISOString(),
    };
    posts.push(post);
    writePosts(posts);
    return post;
  }
}

export const storage = new JsonStorage();
