import { type User, type InsertUser, type Post, type InsertPost } from "@shared/schema";
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

function readUsers(): User[] {
  ensureDbExists();
  const data = fs.readFileSync(USERS_FILE, "utf-8");
  return JSON.parse(data);
}

function writeUsers(users: User[]): void {
  ensureDbExists();
  fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), "utf-8");
}

function readPosts(): Post[] {
  ensureDbExists();
  const data = fs.readFileSync(POSTS_FILE, "utf-8");
  return JSON.parse(data);
}

function writePosts(posts: Post[]): void {
  ensureDbExists();
  fs.writeFileSync(POSTS_FILE, JSON.stringify(posts, null, 2), "utf-8");
}

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  getPosts(limit?: number): Promise<Post[]>;
  getPost(id: string): Promise<Post | undefined>;
  searchPosts(query: string): Promise<Post[]>;
  createPost(post: InsertPost): Promise<Post>;
}

export class JsonStorage implements IStorage {
  async getUser(id: string): Promise<User | undefined> {
    const users = readUsers();
    return users.find((u) => u.id === id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    const users = readUsers();
    return users.find((u) => u.username.toLowerCase() === username.toLowerCase());
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const users = readUsers();
    const id = randomUUID();
    const user: User = { ...insertUser, id };
    users.push(user);
    writeUsers(users);
    return user;
  }

  async getPosts(limit?: number): Promise<Post[]> {
    const posts = readPosts();
    const sorted = posts.sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
    return limit ? sorted.slice(0, limit) : sorted;
  }

  async getPost(id: string): Promise<Post | undefined> {
    const posts = readPosts();
    return posts.find((p) => p.id === id);
  }

  async searchPosts(query: string): Promise<Post[]> {
    const posts = readPosts();
    const lowerQuery = query.toLowerCase();
    return posts.filter(
      (p) =>
        p.title.toLowerCase().includes(lowerQuery) ||
        p.content.toLowerCase().includes(lowerQuery) ||
        p.author.toLowerCase().includes(lowerQuery)
    );
  }

  async createPost(insertPost: InsertPost): Promise<Post> {
    const posts = readPosts();
    const id = randomUUID();
    const post: Post = {
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
