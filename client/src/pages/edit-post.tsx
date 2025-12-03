import { useLocation, useRoute } from "wouter";
import { useAuth } from "@/components/AuthContext";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { insertPostSchema, type InsertPost } from "@shared/schema";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";
import { useToast } from "@/hooks/use-toast";
import { ChevronLeft } from "lucide-react";
import type { Post } from "@/components/PostCard";

export default function EditPostPage() {
  const { isAuthenticated, user } = useAuth();
  const [, setLocation] = useLocation();
  const [match, params] = useRoute("/post/:id/edit");
  const { toast } = useToast();
  const queryClient = useQueryClient();

  if (!isAuthenticated) {
    setLocation("/login");
    return null;
  }

  const { data: post, isLoading } = useQuery<Post>({
    queryKey: ["/api/posts", params?.id],
    queryFn: async () => {
      const response = await fetch(`/api/posts/${params?.id}`, { credentials: "include" });
      if (!response.ok) throw new Error("Failed to fetch post");
      return response.json();
    },
    enabled: !!params?.id,
  });

  const form = useForm<Partial<InsertPost>>({
    resolver: zodResolver(insertPostSchema.partial()),
    defaultValues: {
      title: post?.title || "",
      content: post?.content || "",
      category: post?.category || "",
    },
    values: post ? {
      title: post.title,
      content: post.content,
      category: post.category || "",
    } : undefined,
  });

  const updateMutation = useMutation({
    mutationFn: async (data: Partial<InsertPost>) => {
      const response = await fetch(`/api/posts/${params?.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        credentials: "include",
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Failed to update post");
      }
      return response.json();
    },
    onSuccess: (updated) => {
      queryClient.invalidateQueries({ queryKey: ["/api/posts"] });
      toast({
        title: "Success",
        description: "Post updated successfully",
      });
      setLocation(`/post/${updated.id}`);
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to update post",
        variant: "destructive",
      });
    },
  });

  const onSubmit = (data: Partial<InsertPost>) => {
    updateMutation.mutate(data);
  };

  if (!match || !params?.id) return null;

  if (isLoading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Skeleton className="mb-6 h-10 w-32" />
        <Card>
          <CardContent className="space-y-6 p-6">
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-48 w-full" />
            <Skeleton className="h-10 w-32" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!post || post.author !== user?.username) {
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
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground">You don't have permission to edit this post</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <Button
        variant="ghost"
        className="mb-6 gap-2"
        onClick={() => setLocation(`/post/${params?.id}`)}
        data-testid="button-back-post"
      >
        <ChevronLeft className="h-4 w-4" />
        Back
      </Button>

      <Card>
        <CardHeader>
          <CardTitle>Edit Post</CardTitle>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Title</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Post title"
                        data-testid="input-post-title"
                        defaultValue={post?.title}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="content"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Content</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Write your post content here..."
                        className="min-h-64"
                        data-testid="textarea-post-content"
                        defaultValue={post?.content}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="category"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Category (Optional)</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., React, JavaScript"
                        data-testid="input-post-category"
                        defaultValue={post?.category || ""}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="flex gap-2">
                <Button
                  type="submit"
                  disabled={updateMutation.isPending}
                  data-testid="button-update-post"
                >
                  {updateMutation.isPending ? "Updating..." : "Update Post"}
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
