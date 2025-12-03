import { useState } from "react";
import { useLocation } from "wouter";
import { useAuth } from "@/components/AuthContext";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { ChevronLeft } from "lucide-react";

export default function CreatePostPage() {
  const { isAuthenticated } = useAuth();
  const [, setLocation] = useLocation();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [category, setCategory] = useState("");

  if (!isAuthenticated) {
    setLocation("/login");
    return null;
  }

  const createMutation = useMutation({
    mutationFn: async () => {
      if (!title.trim() || !content.trim()) {
        throw new Error("Title and content are required");
      }

      const response = await fetch("/api/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: title.trim(),
          content: content.trim(),
          category: category.trim() || undefined,
        }),
        credentials: "include",
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Failed to create post");
      }
      return response.json();
    },
    onSuccess: (post) => {
      queryClient.invalidateQueries({ queryKey: ["/api/posts"] });
      toast({
        title: "Success",
        description: "Post created successfully",
      });
      setLocation(`/post/${post.id}`);
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to create post",
        variant: "destructive",
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate();
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <Button
        variant="ghost"
        className="mb-6 gap-2"
        onClick={() => setLocation("/")}
        data-testid="button-back-home"
      >
        <ChevronLeft className="h-4 w-4" />
        Back
      </Button>

      <Card>
        <CardHeader>
          <CardTitle>Create New Post</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Title</label>
              <Input
                placeholder="Post title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                data-testid="input-post-title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Content</label>
              <Textarea
                placeholder="Write your post content here..."
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="min-h-64"
                data-testid="textarea-post-content"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Category (Optional)
              </label>
              <Input
                placeholder="e.g., React, JavaScript"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                data-testid="input-post-category"
              />
            </div>

            <div className="flex gap-2">
              <Button
                type="submit"
                disabled={createMutation.isPending}
                data-testid="button-create-post"
              >
                {createMutation.isPending ? "Creating..." : "Create Post"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
